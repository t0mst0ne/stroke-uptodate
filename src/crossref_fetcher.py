"""Fetch recent journal articles from CrossRef API and pre-screen for stroke & cerebrovascular relevance."""

import asyncio
import re
import yaml
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

import httpx

from . import config

SOURCE_DIR = Path(__file__).parent.parent / "source"
JATS_TAG = re.compile(r"<[^>]+>")

# Trial names and scales that are also common English words when lowercase — require exact uppercase match
CASE_SENSITIVE_TRIALS = {
    "TENSION", "POINT", "EXTEND", "TRACE", "SWITCH", "CREST", "DISTAL", "ENRICH", "DAWN", "TESLA", "LASTE", "ASPECTS",
}

# Pre-screen: two-tier filter for general neurology/medical journals & news.
# Tier 1 — unambiguous stroke/cerebrovascular terms: pass immediately.
# Tier 2 — shared antithrombotic/cardiovascular terms: only pass when
#           a Tier-1 term is also present. This blocks pure cardiology/VTE
#           articles that mention DOACs or aspirin without stroke/cerebrovascular context.
STROKE_DIRECT = [
    "stroke", "cerebrovascular", "cerebral infarction", "brain ischemia",
    "ischemic stroke", "hemorrhagic stroke", "intracerebral hemorrhage", "ICH",
    "subarachnoid hemorrhage", "SAH", "transient ischemic attack", "TIA",
    "thrombectomy", "thrombolysis", "tenecteplase", "alteplase",
    "large vessel occlusion", "LVO", "medium vessel occlusion", "MeVO",
    "basilar artery occlusion", "carotid stenosis", "carotid endarterectomy",
    "carotid stenting", "intracranial atherosclerosis", "ICAD",
    "moyamoya", "CADASIL", "small vessel disease", "CSVD",
    "cerebral venous thrombosis", "cerebral amyloid angiopathy",
    "cerebral aneurysm", "arteriovenous malformation", "NIHSS", "ASPECTS",
    "penumbra", "infarct core", "hematoma expansion", "hemicraniectomy",
    "ANGEL-ASPECT", "SELECT2", "TENSION", "LASTE", "ESCAPE-MeVO",
    "DISTAL", "ENRICH", "ANNEXA-I", "INTERACT3", "INTERACT4",
    "OCEANIC-STROKE", "LIBREXIA-STROKE",
]


@dataclass
class JournalArticle:
    title: str
    doi: str
    journal: str
    authors: list[str]
    published: Optional[str]
    abstract: str
    abstract_digest: str
    tags: list[str] = field(default_factory=list)
    url: str = ""


def _load_journals() -> list[dict]:
    data = yaml.safe_load((SOURCE_DIR / "journals.yml").read_text())
    return data.get("journals", [])


def _crossref_email() -> str:
    data = yaml.safe_load((SOURCE_DIR / "journals.yml").read_text())
    return data.get("crossref_email", "")


def _clean_abstract(raw: str) -> str:
    return re.sub(r"\s+", " ", JATS_TAG.sub("", raw)).strip()


def _digest_abstract(abstract: str, max_chars: int = 400) -> str:
    if not abstract:
        return ""
    signal_words = [
        "significantly", "improved", "reduced", "increased", "demonstrated",
        "showed", "resulted", "HR ", "hazard ratio", "OR ", "odds ratio",
        "RR ", "risk ratio", "mRS", "NIHSS", "recanalization", "reperfusion",
        "mortality", "hemorrhage", "sICH", "p=", "p<", "p >", "95% CI",
        "median", "days", "months", "primary outcome", "primary endpoint",
        "statistically", "noninferior",
    ]
    sentences = re.split(r"(?<=[.!?])\s+", abstract)
    scored = sorted(
        ((sum(1 for w in signal_words if w.lower() in s.lower()), s) for s in sentences),
        key=lambda x: -x[0],
    )
    parts, total = [], 0
    for _, s in scored:
        if total + len(s) > max_chars:
            break
        parts.append(s)
        total += len(s)
    return " ".join(parts).strip() if parts else abstract[:max_chars]


def term_matches(term: str, text: str) -> bool:
    if term in CASE_SENSITIVE_TRIALS:
        return bool(re.search(rf"\b{re.escape(term)}\b", text))
    return bool(re.search(rf"\b{re.escape(term)}(?:s)?\b", text, re.I))


def extract_tags(text: str) -> list[str]:
    return list(dict.fromkeys(k for k in config.keywords() if term_matches(k, text)))


def passes_prescreen(text: str) -> bool:
    return any(term_matches(t, text) for t in STROKE_DIRECT)


def _pub_date(item: dict) -> Optional[str]:
    parts = (
        item.get("published-online", {}).get("date-parts")
        or item.get("published", {}).get("date-parts")
        or item.get("published-print", {}).get("date-parts")
        or item.get("created", {}).get("date-parts")
        or [[]]
    )
    dp = (parts or [[]])[0]
    if len(dp) >= 3:
        return f"{dp[0]:04d}-{dp[1]:02d}-{dp[2]:02d}"
    if len(dp) == 2:
        return f"{dp[0]:04d}-{dp[1]:02d}"
    if len(dp) == 1:
        return f"{dp[0]:04d}"
    return None


# ── CrossRef fetch ─────────────────────────────────────────────────────────────

async def _fetch_journal(
    client: httpx.AsyncClient,
    sem: asyncio.Semaphore,
    journal: dict,
    email: str,
) -> list[JournalArticle]:
    issn = journal["issn"]
    days_back = journal.get("days_back", 7)
    max_items = journal.get("max_items", 30)
    topic_filter = journal.get("topic_filter", journal.get("bc_filter", True))
    from_date = (date.today() - timedelta(days=days_back)).isoformat()

    params = {
        "filter": f"issn:{issn},from-created-date:{from_date}",
        "rows": max_items,
        "sort": "created",
        "order": "desc",
        "select": "DOI,title,author,abstract,created,published,published-print,published-online,URL,container-title",
    }
    headers = {"User-Agent": f"stroke-uptodate/1.0 (mailto:{email})"}

    r = None
    async with sem:
        for attempt in range(3):
            try:
                r = await client.get(
                    "https://api.crossref.org/works",
                    params=params,
                    headers=headers,
                    timeout=25,
                )
                if r.status_code == 429:
                    await asyncio.sleep(1.5 * (attempt + 1))
                    continue
                r.raise_for_status()
                break
            except Exception:
                if attempt == 2:
                    return []
                await asyncio.sleep(1.0)
        await asyncio.sleep(0.2)

    if r is None or r.status_code != 200:
        return []

    articles = []
    for item in r.json().get("message", {}).get("items", []):
        title = (item.get("title") or [""])[0]
        if not title or len(title) < 10:
            continue
        abstract = _clean_abstract(item.get("abstract", ""))
        combined = title + " " + abstract

        if topic_filter and not passes_prescreen(combined):
            continue

        authors_raw = item.get("author", [])
        authors = [
            f"{a.get('family', '')} {a.get('given', '')[:1]}".strip()
            for a in authors_raw[:4]
        ]
        if len(authors_raw) > 4:
            authors.append("et al.")

        doi = item.get("DOI", "")
        journal_name = (item.get("container-title") or [journal.get("full_name", issn)])[0]

        articles.append(JournalArticle(
            title=title,
            doi=doi,
            journal=journal_name,
            authors=authors,
            published=_pub_date(item),
            abstract=abstract,
            abstract_digest=_digest_abstract(abstract),
            tags=extract_tags(combined),
            url=f"https://doi.org/{doi}" if doi else item.get("URL", ""),
        ))

    return articles


async def fetch_all() -> dict[str, list[JournalArticle]]:
    journals = _load_journals()
    email = _crossref_email()
    sem = asyncio.Semaphore(2)
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[_fetch_journal(client, sem, j, email) for j in journals])
    return {j["name"]: arts for j, arts in zip(journals, results)}


def format_articles_md(results: dict[str, list[JournalArticle]]) -> str:
    if not any(results.values()):
        return ""

    lines = ["\n## 文獻速報 — CrossRef 期刊\n"]
    lines.append("> 資料來源：CrossRef API · 關鍵詞預篩後由 LLM 在報告生成時確認腦中風／腦血管相關性\n")

    for journal_name, articles in results.items():
        if not articles:
            lines.append(f"\n### {journal_name}\n\n_本期未取得相關論文_\n")
            continue

        with_abstract = [a for a in articles if a.abstract_digest]
        without = [a for a in articles if not a.abstract_digest]

        lines.append(f"\n### {journal_name}（{len(articles)} 篇候選）\n")

        for a in with_abstract[:10]:
            lines.append(f"#### [{a.title}]({a.url})")
            lines.append(f"_{', '.join(a.authors)}_ · {a.published or '—'} · {a.journal}")
            lines.append("")
            lines.append(f"> {a.abstract_digest}")
            if a.tags:
                lines.append(f"\n`{'` `'.join(a.tags[:5])}`")
            lines.append("")

        if without:
            lines.append("**摘要未提供：**\n")
            for a in without[:8]:
                lines.append(f"- [{a.title}]({a.url}) — _{', '.join(a.authors)}_ ({a.published or '—'})")
            lines.append("")

    return "\n".join(lines)
