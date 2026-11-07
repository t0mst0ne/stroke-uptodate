from datetime import datetime, date, timedelta
from pathlib import Path
from collections import Counter, defaultdict
import json
import re
from . import db, config, webscraper, crossref_fetcher

REPORTS_DIR = Path(__file__).parent.parent / "reports"
DATA_DIR = Path(__file__).parent.parent / "data"
TRIAL_PATTERN = re.compile(r"\b(NCT\d{8}|[A-Z][A-Z0-9]+-\d+(?:-\d+)?|[A-Z]{2,}\s*\d{3,})\b")


def _match_group(text: str) -> list[str]:
    groups = config.drug_groups()
    return [
        grp for grp, kws in groups.items()
        if any(crossref_fetcher.term_matches(kw, text) for kw in kws)
    ]


def _extract_trials(text: str) -> list[str]:
    return TRIAL_PATTERN.findall(text)


def _load_cached_web() -> dict[str, list[webscraper.Article]]:
    cache_file = DATA_DIR / "webscrape_cache.json"
    if not cache_file.exists():
        return {}
    raw = json.loads(cache_file.read_text())
    return {
        src: [webscraper.Article(**a) for a in arts]
        for src, arts in raw.items()
    }


def _load_cached_journals() -> dict[str, list[crossref_fetcher.JournalArticle]]:
    cache_file = DATA_DIR / "journals_cache.json"
    if not cache_file.exists():
        return {}
    raw = json.loads(cache_file.read_text())
    return {
        j: [crossref_fetcher.JournalArticle(**a) for a in arts]
        for j, arts in raw.items()
    }


def build_report(days: int = 7) -> str:
    tweets = db.get_tweets_since(days)
    accounts = {a["handle"]: a for a in db.get_accounts()}
    today = date.today()
    start_date = today - timedelta(days=days)
    week = today.isocalendar()
    week_label = f"{week[0]}-W{week[1]:02d}"

    web_results = _load_cached_web()
    journal_results = _load_cached_journals()

    lines = []
    lines.append(f"# 腦中風與腦血管疾病趨勢週報 — {week_label}")
    lines.append(
        f"\n> 生成日期：{today.isoformat()}｜涵蓋期間：{start_date.isoformat()} 至 {today.isoformat()}（最近 {days} 天）\n"
    )

    if tweets:
        conf_kws = config.conference_keywords()
        group_tweets: dict[str, list[dict]] = defaultdict(list)
        trial_mentions: Counter = Counter()
        conference_tweets: list[dict] = []
        author_counts: Counter = Counter()

        for tw in tweets:
            for g in _match_group(tw["content"]):
                group_tweets[g].append(tw)
            trial_mentions.update(_extract_trials(tw["content"]))
            if any(kw.lower() in tw["content"].lower() for kw in conf_kws):
                conference_tweets.append(tw)
            author_counts[tw["author"]] += 1

        top_tweets = sorted(tweets, key=lambda t: t["likes"] + t["retweets"] * 2, reverse=True)
        active_groups = sorted(group_tweets.items(), key=lambda x: len(x[1]), reverse=True)

        lines.append("## 社群動態摘要 (X / Twitter)\n")
        lines.append(f"> 共收集 {len(tweets)} 則腦中風相關推文｜追蹤 {len(accounts)} 個帳號\n")
        lines.append("### 熱門治療與研究主題\n")
        lines.append("| 主題 | 推文數 | 最活躍帳號 |")
        lines.append("|------|--------|------------|")
        for grp, tws in active_groups[:8]:
            top_auth = Counter(t["author"] for t in tws).most_common(1)[0][0] if tws else "—"
            lines.append(f"| {grp} | {len(tws)} | @{top_auth} |")

        lines.append("")
        lines.append("### 本週最活躍 KOL\n")
        lines.append("| 帳號 | 推文數 |")
        lines.append("|------|--------|")
        for auth, cnt in author_counts.most_common(10):
            lines.append(f"| @{auth} | {cnt} |")

        if conference_tweets:
            lines.append("\n## 國際會議與摘要動態\n")
            lines.append(f"_{len(conference_tweets)} 則推文提及國際腦中風會議或摘要_\n")
            for tw in sorted(conference_tweets, key=lambda t: t["likes"], reverse=True)[:5]:
                lines.append(f"**@{tw['author']}** — {tw['created_at'][:10]}")
                lines.append(f"> {tw['content'][:280].strip()}")
                lines.append(f"👍 {tw['likes']} | 🔁 {tw['retweets']} | [link]({tw['url']})\n")

        lines.append("## 各領域推文焦點\n")
        for grp, tws in active_groups:
            if not tws:
                continue
            lines.append(f"### {grp} ({len(tws)} tweets)\n")
            top = sorted(tws, key=lambda t: t["likes"] + t["retweets"] * 2, reverse=True)[:4]
            for tw in top:
                lines.append(f"**@{tw['author']}** — {tw['created_at'][:10]}")
                lines.append(f"> {tw['content'][:300].strip()}")
                lines.append(f"👍 {tw['likes']} | 🔁 {tw['retweets']} | [link]({tw['url']})\n")

        if trial_mentions:
            lines.append("## 臨床試驗提及次數\n")
            lines.append("| 試驗 / 代號 | 提及次數 |")
            lines.append("|-------------|----------|")
            for trial, cnt in trial_mentions.most_common(15):
                lines.append(f"| {trial} | {cnt} |")
            lines.append("")

        lines.append("## 高互動推文排行\n")
        for tw in top_tweets[:10]:
            lines.append(f"**@{tw['author']}** — {tw['created_at'][:10]}")
            lines.append(f"> {tw['content'][:300].strip()}")
            lines.append(f"👍 {tw['likes']} | 🔁 {tw['retweets']} | [link]({tw['url']})\n")

    if web_results:
        lines.append(webscraper.format_articles_md(web_results))

    if journal_results:
        lines.append(crossref_fetcher.format_articles_md(journal_results))

    if not tweets and not web_results and not journal_results:
        lines.append(f"\n_最近 {days} 天內無資料，請先執行 `uv run python main.py scrape` 與 `uv run python main.py journals`。_\n")

    lines.append("\n---")
    lines.append(f"_報告涵蓋最近 {days} 天資料（{start_date.isoformat()} ~ {today.isoformat()}）。_")
    return "\n".join(lines)


def write_report(days: int = 7) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    week = date.today().isocalendar()
    fname = REPORTS_DIR / f"{week[0]}-W{week[1]:02d}.md"
    fname.write_text(build_report(days))
    return fname
