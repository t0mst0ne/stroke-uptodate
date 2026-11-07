# CLAUDE.md — Stroke & Cerebrovascular Weekly Report

## Project Purpose

Auto-generate weekly Markdown reports on stroke and cerebrovascular disease treatment & research trends from:
- OpenEvidence MCP (`mcp__openevidence__oe_ask`)
- PubMed MCP (`mcp__claude_ai_PubMed__search_articles`)
- ClinicalTrials.gov MCP (`mcp__claude_ai_Clinical_Trials__search_trials`)
- CrossRef API (via `uv run python main.py journals` — *Stroke*, *Lancet Neurology*, *JAMA Neurology*, *Neurology*, *JNNP*, *Int J Stroke*, *European Stroke Journal*, *JNIS*)
- Web news (NeurologyLive, Medscape Neurology, AHA/Stroke News, ESO, Healio Neurology via `uv run python main.py scrape`)

---

## Before Writing a New Report

**MANDATORY — do this BEFORE writing a single word of content:**

```bash
# 1. Find the latest report
PREV=$(ls reports/ -t | head -1)
echo "Previous report: $PREV"

# 2. Read it fully — note every trial, guideline update, device/drug approval, and section topic covered
# 3. Grep key trial names to see what's already documented
grep -E "ANGEL-ASPECT|SELECT2|TENSION|LASTE|TESLA|DISTAL|ESCAPE-MeVO|DISCOUNT|ENRICH|ANNEXA-I|INTERACT|OCEANIC-STROKE|LIBREXIA|TIMELESS|TRACE|AcT|ELAN|OPTIMAS|ARCADIA" reports/$PREV
```

After reading the previous report, answer these before writing:
- Which trials were already covered with final/mature data? → **skip entirely**
- Which trials had interim or conference abstract data last week? → include only if full manuscript or new subgroup/follow-up published
- Which drug/device approvals or guidelines were already documented? → **skip unless indication expanded**

**Do NOT repeat** any finding with identical numbers. Mark new follow-up or secondary analysis data explicitly: `[更新]` before the subsection heading, and state what changed vs last week.

If a section has no genuinely new data this week: write `_本週無新訊號_` and move on.

---

## Report File Naming

```
reports/YYYY-WNN.md
```

Use ISO week number: `python3 -c "from datetime import date; d=date.today(); print(f'{d.year}-W{d.isocalendar()[1]:02d}')"`.

---

## Report Structure

### Required Sections (繁體中文)

```markdown
# 腦中風與腦血管疾病趨勢週報 — YYYY-WNN

> 生成日期：YYYY-MM-DD｜資料來源：OpenEvidence、PubMed、CrossRef（Stroke / Lancet Neurol / JAMA Neurol 等）、NeurologyLive、AHA/ASA、ESO、ClinicalTrials.gov
> 涵蓋期間：...

---

## 摘要
（本週五大訊號 — bullet points, concrete numbers: OR/RR/HR, 95% CI, mRS 0-1 / 0-2, sICH, mortality）

## 一、靜脈血栓溶解治療 (IVT：Tenecteplase / Alteplase / 延長時間窗)
## 二、動脈機械取栓與神經介入 (EVT：LVO / Large Core / MeVO / BAO)
## 三、抗血小板與急性／次級預防 (DAPT / 靜脈抗血小板 / 顱內外動脈狹窄 ICAD & Carotid)
## 四、心房顫動抗凝血與 Factor XIa 抑制劑 (DOAC 時機 / FXIa / ESUS)
## 五、出血性中風與腦血管外科 (ICH 血壓與逆轉劑 / 微創手術 / SAH 與腦動脈瘤)
## 六、腦小血管疾病、血管性失智與神經保護復健 (CSVD / CAA / Neuroprotection / 復健科技)
## 七、神經影像、AI 輔助診斷與到院前照護系統 (CTP / ASPECTS / Mobile Stroke Unit / 轉診流程)
## 八、進行中高優先臨床試驗追蹤
## 九、台灣臨床情境備註 (健保給付規範、tPA/TNK 與 EVT 時間窗、本土登錄研究與指引對照)
## 十、本週 Key Takeaways

## 十一、蜥蜴LLM 點評
（OpenEvidence分類：practice-changing vs hypothesis-generating vs context-dependent）

## 十二、媒體動態
（NeurologyLive / Medscape / AHA / ESO / Healio news table）

## 文獻速報 — CrossRef 期刊
（LLM-filtered articles from Stroke, Lancet Neurology, JAMA Neurology, Neurology, JNNP, Int J Stroke, ESJ, JNIS）
```

Sections without new data this week should say: `_本週無新訊號_`

---

## Writing Style

- Language: **繁體中文**，英文醫學術語與指標保留原文（AIS, ICH, SAH, LVO, MeVO, IVT, EVT, TNK, tPA, DAPT, DOAC, mRS, NIHSS, ASPECTS, sICH, TICI / eTICI 等）
- Every clinical claim must cite trial name + author + journal + DOI
- Tables: use Markdown tables for comparative data (intervention vs control arm, mRS shift, sICH%, 90-day mortality)
- Numbers: always include OR / cOR / RR / HR, 95% CI, p-value, and absolute percentages when available
- Avoid vague superlatives; every "significant" needs a number

---

## Data Pipeline

Run in order before writing:

```bash
uv run python main.py scrape          # NeurologyLive + Medscape + AHA + ESO + Healio news
uv run python main.py journals        # Stroke / Lancet Neurol / JAMA Neurol / etc. via CrossRef
```

For full pipeline (including Twitter if credentials available):

```bash
uv run python main.py run
```

Cached data locations:
- `data/webscrape_cache.json` — web news articles
- `data/journals_cache.json` — CrossRef journal articles (pre-screened, not yet final-filtered)

**CrossRef filtering note:** For general neurology journals (*Lancet Neurology*, *JAMA Neurology*, *Neurology*, *JNNP*), the Python fetcher applies a two-tier keyword pre-screen (`_STROKE_DIRECT`).
When writing the report, read `data/journals_cache.json` and **filter in-session** — discard any article whose primary topic is not stroke or cerebrovascular disease (e.g. MS, epilepsy, Alzheimer's, or general cardiology articles without cerebrovascular outcomes).
Only include articles confirmed stroke/cerebrovascular-relevant in the `## 文獻速報` section.

---

## 蜥蜴LLM 點評 Section

Use `mcp__openevidence__oe_ask` with a prompt like:

```
Based on the following stroke and cerebrovascular findings from this week, classify each as:
- Practice-changing (changes standard of care NOW)
- Hypothesis-generating (promising but needs confirmation)
- Context-dependent (changes practice for specific subgroup or workflow only)

[list findings with trial names and key numbers]
```

Extract result with: `result.extracted_answer_raw`

---

## After Writing

1. Check word count: report should be 3000–8000 words
2. Verify every table has header separators (`|---|---|`)
3. Run `uv run python main.py report` if auto-generating from DB
4. Commit: `git add reports/YYYY-WNN.md && git commit -m "report: YYYY-WNN"`
5. Push → GitHub Action auto-publishes to Wiki

---

## Duplicate-Avoidance Checklist

Before finalising, cross-check against the previous report:

```bash
PREV=$(ls reports/ -t | head -2 | tail -1)
# Check trial names
grep -E "ANGEL-ASPECT|SELECT2|TENSION|LASTE|TESLA|DISTAL|ESCAPE-MeVO|DISCOUNT|ENRICH|ANNEXA-I|INTERACT|OCEANIC-STROKE|LIBREXIA|TIMELESS|TRACE|AcT|ELAN|OPTIMAS|ARCADIA" reports/$PREV
# Check outcome numbers — if same numbers appear, it's a repeat
grep -E "OR [0-9]|RR [0-9]|HR [0-9]|mRS [0-9]|sICH [0-9]" reports/$PREV | head -20
```

Rules:
- Same trial + same numbers → **delete the section**
- Same trial + new data (updated follow-up, secondary subgroup analysis, guideline adoption) → keep with `[更新]` tag
- Brand new trial → include normally
