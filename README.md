# Stroke & Cerebrovascular Weekly Trend Reporter

自動生成腦中風與腦血管疾病（Stroke & Cerebrovascular Disease）每週治療與研究趨勢報告，以繁體中文撰寫（英文醫學名詞與試驗縮寫保留原文）。

目前設定：**腦中風與腦血管疾病（Acute Ischemic Stroke · ICH/SAH · Neurointervention · Secondary Prevention）**

資料來源：OpenEvidence AI · CrossRef 期刊（Stroke, Lancet Neurology, JAMA Neurology, Neurology, JNNP, Int J Stroke, ESJ, JNIS）· NeurologyLive · Medscape Neurology · AHA/ASA · ESO · ClinicalTrials.gov

---

## 快速開始

```bash
# 安裝 uv（Python 套件管理）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安裝相依套件
uv sync

# 執行網路媒體爬蟲（NeurologyLive / Medscape / AHA / ESO / Healio）
uv run python main.py scrape

# 抓取腦中風與神經醫學核心期刊最新文獻（CrossRef API）
uv run python main.py journals

# 生成報告（需手動補充 OpenEvidence 段落，或直接在 Claude Code 中執行）
uv run python main.py report
```

報告輸出至 `reports/YYYY-Wxx.md`，push 到 `main` 後 GitHub Actions 自動發布至 Wiki。

---

## 專案結構

```
.
├── source/                   ← 所有可調整參數（不需改 Python）
│   ├── keywords.yml          ← 腦中風／腦血管疾病相關關鍵詞（過濾與標籤用）
│   ├── drug_groups.yml       ← 治療／介入分組 + 國際會議關鍵詞
│   ├── journals.yml          ← CrossRef 追蹤期刊清單與 ISSN
│   ├── search_queries.yml    ← Twitter/X 搜尋 query
│   ├── web_sources.yml       ← 爬蟲來源（RSS URL、Google News site + query）
│   └── twitter.yml           ← GraphQL op_id、cookie skip 清單
├── config/
│   └── seeds.txt             ← 腦中風領域 KOL 與學會 Twitter 帳號種子清單
├── src/
│   ├── config.py             ← YAML 載入器（lru_cache）
│   ├── webscraper.py         ← 網路爬蟲（driven by web_sources.yml）
│   ├── crossref_fetcher.py   ← CrossRef 期刊文獻抓取與預篩（driven by journals.yml）
│   ├── fetcher.py            ← Twitter 爬蟲（driven by twitter.yml）
│   ├── reporter.py           ← 推文聚合報告生成
│   ├── discover.py           ← KOL 自動發掘
│   └── db.py                 ← SQLite 儲存
├── reports/                  ← 產出的週報（push 即觸發 wiki 發布）
├── main.py                   ← CLI 入口
└── .github/workflows/
    └── publish-wiki.yml      ← 自動發布 wiki 的 GitHub Action
```

---

## 追蹤主題與期刊設定

### 1. 核心追蹤領域（`source/drug_groups.yml` & `source/keywords.yml`）

- **靜脈血栓溶解治療（Intravenous Thrombolysis, IVT）**：Tenecteplase (TNK)、Alteplase (rt-PA)、Reteplase、延長時間窗（Extended Window）、合併影像篩選（如 TIMELESS、TRACE、AcT、ORIGINAL）。
- **動脈機械取栓與神經介入（Endovascular Thrombectomy, EVT）**：大血管阻塞（LVO）、大型梗塞核心（Large Core：ANGEL-ASPECT、SELECT2、TENSION、LASTE、TESLA）、中小型血管阻塞（MeVO：DISTAL、ESCAPE-MeVO、DISCOUNT）、基底動脈阻塞（BAO）。
- **抗血小板與次級預防（Antiplatelet Therapy）**：DAPT（Aspirin、Clopidogrel、Ticagrelor、Cilostazol）、急性期微血管灌流與靜脈抗血小板藥物（Tirofiban、Eptifibatide、Glenzocimab）、CHANCE / POINT / THALES / INSPIRES。
- **抗凝血與 Factor XIa 抑制劑（Anticoagulation & Factor XIa）**：心房顫動（AF）相關中風預防、DOAC 啟用時機（ELAN、OPTIMAS）、次世代 Factor XIa 抑制劑（Asundexian、Milvexian、Abelacimab；OCEANIC-STROKE、LIBREXIA-STROKE）、ESUS（ARCADIA）。
- **出血性中風（ICH & SAH）**：腦內出血（ICH）組合式照護（INTERACT3、INTERACT4）、抗凝血劑逆轉劑（Andexanet alfa / ANNEXA-I、Idarucizumab）、微創血塊清除手術（ENRICH）、減壓性顱骨切除術（SWITCH）、蜘蛛膜下腔出血（SAH）與腦動脈瘤治療。
- **頸動脈與顱內動脈狹窄（Carotid & ICAD）**：CEA、CAS、TCAR、顱內動脈粥狀硬化（ICAD）、毛毛樣腦血管疾病（Moyamoya disease）。
- **腦小血管疾病與血管性認知障礙（CSVD & VCI）**：白質病變（WMH）、腔隙性梗塞（Lacunar stroke）、CADASIL、類澱粉血管病變（CAA）、神經保護與復健（Nerinetide、Edaravone、VNS、BCI）。

### 2. 追蹤期刊（`source/journals.yml`）

預設透過 CrossRef API 追蹤以下神經血管與神經醫學頂尖期刊：

| 期刊簡稱 | 完整名稱 | ISSN | 預篩模式 |
|----------|----------|------|----------|
| **Stroke** | *Stroke* (AHA/ASA) | `0039-2499` | 全收錄 (`topic_filter: false`) |
| **Lancet Neurology** | *The Lancet Neurology* | `1474-4422` | 腦中風／腦血管關鍵詞過濾 |
| **JAMA Neurology** | *JAMA Neurology* | `2168-6149` | 腦中風／腦血管關鍵詞過濾 |
| **Neurology** | *Neurology* (AAN) | `0028-3878` | 腦中風／腦血管關鍵詞過濾 |
| **JNNP** | *Journal of Neurology, Neurosurgery & Psychiatry* | `0022-3050` | 腦中風／腦血管關鍵詞過濾 |
| **Int J Stroke** | *International Journal of Stroke* (WSO) | `1747-4930` | 全收錄 (`topic_filter: false`) |
| **European Stroke Journal** | *European Stroke Journal* (ESO) | `2396-9873` | 全收錄 (`topic_filter: false`) |
| **JNIS** | *Journal of NeuroInterventional Surgery* | `1759-8478` | 腦中風／腦血管關鍵詞過濾 |

> 亦可於 `source/journals.yml` 取消註解啟用 *NEJM* (`0028-4793`)、*The Lancet* (`0140-6736`)、*JAMA* (`0098-7484`)、*Annals of Neurology* (`0364-5134`)、*Cerebrovascular Diseases* (`1015-9770`)、*SVIN* (`2694-5746`)。

---

## 客製化與延伸其他神經科／醫學主題

所有領域知識皆集中在 `source/` 下的 YAML 檔案，調整追蹤範圍只需修改設定檔：

1. **`source/keywords.yml`**：新增或調整疾病、藥物、醫材或臨床試驗關鍵詞。
2. **`source/drug_groups.yml`**：定義報告中的治療分類與國際學會會議標籤（如 `#ISC26`、`#ESOC`、`#WSC`、`#SVIN`）。
3. **`source/journals.yml`**：新增期刊 ISSN，設定 `days_back`、`max_items` 與 `topic_filter`。
4. **`source/web_sources.yml`**：設定醫學新聞來源（支援 `type: rss` 與 `type: google_news`，可透過 `query` 自訂搜尋條件）。
5. **`source/search_queries.yml` & `config/seeds.txt`**：調整 X/Twitter 搜尋語法與追蹤之 KOL 清單。

---

## 常見維護任務

| 問題 | 解法 |
|------|------|
| Twitter API 回 404 | 更新 `source/twitter.yml` 的 `op_id` |
| 某新試驗或新藥沒被捕捉 | 加進 `source/keywords.yml` 和對應 `source/drug_groups.yml` |
| 新增期刊來源 | 在 `source/journals.yml` 加上期刊名稱與 ISSN |
| 新增爬蟲來源 | 在 `source/web_sources.yml` 加一筆 `type: rss` 或 `type: google_news` |
| 查詢字串太雜 | 修改 `source/search_queries.yml` 或 `source/web_sources.yml` 的 `noise_filter` |
| Wiki 沒更新 | 確認 push 路徑含 `reports/*.md`；或手動跑 Actions → `workflow_dispatch` |

---

## GitHub Actions — Wiki 自動發布

每次 push 包含 `reports/*.md` 的 commit 到 `main`，`.github/workflows/publish-wiki.yml` 自動：

1. 把新報告複製到 wiki repo
2. 重建 `Home.md` 索引（最新在前）
3. Force-push 到 wiki `master` branch

手動觸發：Actions → **Publish Reports to Wiki** → **Run workflow**

---

## 授權

MIT
