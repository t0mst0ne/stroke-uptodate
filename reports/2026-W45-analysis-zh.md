# 腦中風與腦血管疾病週報（驗證版）— 2026-W45

把 stroke-uptodate 2026-W45 週報中的候選項目逐一和 CrossRef、PubMed、期刊頁面比對後整理。本週沒有新的 RCT；重點是觀察性研究與 registry 資料。不構成個別病人醫療建議。

- [本週五大訊號](#s0)
- [二、動脈機械取栓與神經介入](#s2)
- [四、心房顫動、抗凝血與病因](#s4)
- [復健與預後](#s6)
- [影像、生物標記與到院前分流](#s7)
- [文獻速覽（依期刊）](#s8)
- [排除項目](#s9)
- [資料來源](#s10)

<a id="s0"></a>

## 本週五大訊號

1. AF 病人發生 ischemic stroke 後 8 週內開始 early rhythm control，和較低的 stroke/SE 復發有關（HR 0.56, 95% CI 0.32–0.97）。這是日本 claims cohort，屬假說生成。Epub 2026-10-21，早於本週涵蓋期間，經本週 Medscape 報導才列入。
2. ASPERA-R：服用抗凝血劑仍發生中風（breakthrough）並出現 HT 的病人，重啟抗凝後出血風險較高（HR 3.39）。模型推估合併風險最低點約在第 10 天，但不確定性大，屬假說生成。
3. German Stroke Registry：ASPECTS 1–2 病人接受 EVT 後，90 天 mRS 0–3 為 20.2%，死亡 55.1%。研究沒有內科治療對照組，只能描述預後，不能推論療效。
4. 術前 CTA 測得的頸部血管 curvature 越大，越可能 recanalization 失敗（每單位 aOR 1.21）。單中心回溯、n=160，屬假說生成。
5. 8 電極乾式 EEG 加 ML 偵測前循環 LVO：AUC 0.85，sensitivity 69%（95% CI 44–86%）。LVO 僅 16 例，作者表示目前還不能用於臨床。

> 本 repo 的 reports/ 只有 2026-W45 一份，沒有前一週報告可去重，因此本頁沒有任何項目標記為 [更新]。

<a id="s2"></a>

## 二、動脈機械取栓與神經介入（EVT：Large Core）

### 大範圍梗塞（ASPECTS 0–5）EVT 後的功能預後與生活品質

- **研究設計：** German Stroke Registry–Endovascular Treatment 回溯分析（多中心 registry）
- **族群：** 前循環阻塞且接受 EVT。共篩選 18,069 人，納入分析 889 人：ASPECTS 1–2 有 89 人，3–5 有 800 人，沒有 ASPECTS 0 的病人
- **比較：** extensive（ASPECTS 0–2）對比 large（ASPECTS 3–5）。沒有內科治療對照組
- **終點：** 90 天 ordinal mRS；次要終點為 mRS 0–3、存活、EQ-5D-3L、居住狀況
- **結果：** ASPECTS 1–2：mRS 0–3 為 20.2%，90 天死亡 55.1%。infarct group 與 mRS 沒有顯著關聯（cOR 0.80, 0.53–1.23）。successful reperfusion 與較好結果相關（cOR 3.68, 2.31–5.85；mRS 0–3 aOR 4.10, 2.45–6.86）
- **安全性：** 摘要未報告 sICH（待確認）
- **限制：** 回溯設計、有選擇偏差、ASPECTS 1–2 樣本小、無對照組；EQ-5D 只有少數存活者有資料
- **分類：** 依情境而定
- **連結：** https://doi.org/10.1093/esj/aakag131 · PMID 42969847

臨床意義：這些數字可用於和家屬討論極大範圍梗塞的預後，但不能據此認定 EVT 對 ASPECTS 0–2 病人有效。

### 術前頸部血管 curvature 預測 recanalization 失敗

- **研究設計：** 單中心回溯 cohort（Barnes-Jewish Hospital，2019/5–2021/2）
- **族群：** 160 位前循環 LVO 病人，接受 mechanical thrombectomy
- **暴露：** 以術前 CTA 3D centerline 計算的 cervical curvature
- **終點：** mTICI ≥2b、intracranial access time
- **結果：** recanalization 成功率 86%；依 curvature 三分位分別為 91%／93%／75%（P=0.017）。每單位 aOR 1.21（1.02–1.43）；curvature >11.54 時 aOR 5.10（1.88–13.84）。access time 與 curvature 無關
- **限制：** 單中心、樣本小、閾值由資料推導（可能 overfitting），尚無外部驗證
- **分類：** 假說生成
- **連結：** https://doi.org/10.1161/strokeaha.126.055838 · PMID 42974688

<a id="s4"></a>

## 四、心房顫動、抗凝血與病因

### AF 合併 acute ischemic stroke：early rhythm control 對比 usual care

- **研究設計：** 日本全國 claims cohort（DeSC-IQVIA，2014–2025），採 landmark 分析與 propensity overlap weighting
- **族群：** 14,355 人在 8 週 landmark 前沒有發生事件；年齡中位數 83 歲，女性 48.3%
- **介入／比較：** 8 週內開始 rhythm control（抗心律不整藥物、ablation 或 cardioversion），共 268 人（1.9%），對比 usual care
- **終點：** 因 recurrent ischemic stroke/SE 住院；次要終點為 major bleeding、HF 住院、全死因死亡
- **結果：** stroke/SE HR 0.56（0.32–0.97）；5 年累積發生率 8.0% vs 13.8%。全死因死亡 HR 0.72（0.53–0.97）。major bleeding HR 1.44（0.74–2.82），HF 住院 HR 0.73（0.39–1.38），兩者皆無顯著關聯
- **限制：** 治療組人數少；claims 資料缺少 NIHSS、影像與 AF burden；可能有殘餘干擾與 healthy-user bias。期刊頁摘錄的 risk difference CI 為 −11.0 to 0.8，和 HR 顯著的結果不一致，待確認
- **日期：** Epub 2026-10-21；卷期 Neurology 2026-11-24, 107(10)。卷期日期在未來不代表尚未發表
- **分類：** 假說生成
- **連結：** https://doi.org/10.1212/WNL.0000000000218736 · PMID 42906070

### ASPERA-R：breakthrough ischemic stroke 合併 HT 後重啟抗凝的時機

- **研究設計：** 多中心 registry；重啟抗凝與否及時機由臨床醫師決定，未隨機分配
- **族群：** 1,555 位 breakthrough stroke 病人，其中 269 人（17.3%）發生 HT；170 人重啟抗凝
- **結果：** HT 組與非 HT 組的 90 天粗率：缺血事件 27.1% vs 13.8%、中重度出血 7.4% vs 2.8%、死亡 34.2% vs 17.7%。landmark 分析：缺血事件 HR 1.42（0.85–2.37），出血 HR 3.39（1.61–7.13）。模型推估合併風險最低點約在第 10 天
- **限制：** 非隨機、有 treatment-selection bias；第 10 天這個估計值不確定性大
- **分類：** 假說生成
- **連結：** https://doi.org/10.1177/17474930261502562 · PMID 42978151

<a id="s6"></a>

## 復健與預後

### 非步行亞急性中風病人的身體活動強度與早期獨立行走

- **研究設計：** 多中心（11 家機構）前瞻性 cohort；UMIN000058526
- **族群：** 389 人，入院時 FAC 1–2；1 個月內有 113 人達到 FAC ≥4
- **結果：** high-LPA（2.0–2.9 METs）每天每多 5 分鐘：RR 1.067（1.010–1.131）。≥2.0 METs 的 short-bout 次數：RR 1.208（1.060–1.375）。low-LPA、MVPA 與 long-bout 都沒有關聯
- **限制：** 觀察性設計，可能有反向因果（較能活動的病人本來就較快恢復）
- **分類：** 假說生成
- **連結：** https://doi.org/10.1161/strokeaha.126.056467 · PMID 42979715

背景：W45 週報列出 AHA 的「Key Patient Messages」頁面，屬病人衛教。對應的 2026 AHA/ASA Adult Stroke Rehabilitation and Recovery Guideline 於 2026-08-27 發表，不在本週涵蓋期間，不列為新訊號。網址：https://doi.org/10.1161/STR.0000000000000536

<a id="s7"></a>

## 影像、生物標記與到院前分流

### 以 EEG 加 machine learning 在超急性期偵測前循環 LVO

- **研究設計：** 診斷準確性研究，使用 ELECTRA-STROKE（NCT03699397）與 AI-STROKE（NCT05437237）資料，以 nested cross-validation 評估
- **族群：** 1,293 位疑似中風病人中有 336 人納入（74% 為到院前收案）；LVO-a 只有 16 例（5%）
- **結果：** Naïve Bayes AUC 0.85（0.77–0.93），sensitivity 69%（44–86%），specificity 86%（82–89%）
- **限制：** 陽性個案很少；疑似中風病人僅 26% 納入分析（納入條件包含需有乾淨 EEG 片段；各排除原因的人數待確認）；沒有外部驗證
- **分類：** 假說生成
- **連結：** https://doi.org/10.1093/esj/aakag134 · PMID 42993805

<a id="s8"></a>

## 文獻速覽（依期刊）

星等代表臨床閱讀優先順序，不代表證據確定性。下方譯文僅根據 CrossRef 或期刊頁取得的摘要，均非全文。

### Neurology（經 Medscape 報導）

★★★ Early Rhythm Control vs Usual Care After AIS in AF（Egashira S 等）。列為必讀的理由：直接涉及次級預防策略，且研究規模大。

【摘要譯文，取自期刊頁，Background 未完整取得】方法：這項全國 cohort 研究使用 DeSC-IQVIA 整合資料庫，這是涵蓋日本約 1,600 萬人的行政 claims 資料庫。納入 2014–2025 年間因 acute ischemic stroke 住院、且入院時已有 AF 的成人。暴露定義為入院 8 週內開始 rhythm control（抗心律不整藥物、catheter ablation 或電氣整流），對照為未開始者（usual care），在 landmark 時點評估。主要結果為因 recurrent ischemic stroke 或 SE 住院；次要結果包括 major bleeding、HF 住院與全死因死亡。以 propensity score overlap weighting 校正基線差異，並估計 cause-specific HR、以死亡為競爭風險的累積發生率，以及 5 年 risk difference。結果：14,355 位撐過 8 週 landmark 且未發生事件的病人（年齡中位數 83 歲；女性 48.3%）中，268 人（1.9%）接受 early rhythm control。追蹤 23,583 人年期間，early rhythm control 與較低的 stroke/SE 風險相關（HR 0.56；95% CI 0.32–0.97；加權 5 年累積發生率 8.0% vs 13.8%）。major bleeding（HR 1.44）與 HF 住院（HR 0.73）沒有關聯；全死因死亡較低（HR 0.72；0.53–0.97）。在 4–24 週的不同 landmark 下結果一致。討論：early rhythm control 可能成為另一項次級預防策略，且開始時機有彈性；但這些觀察性結果屬假說生成，需要 RCT 證實。

### International Journal of Stroke

★★★ Haemorrhagic Transformation in Breakthrough Ischemic Stroke — ASPERA-R（D'Anna L 等）。列為必讀的理由：重啟抗凝時機是臨床上每天都要做的決定。

【摘要譯文】背景與目的：病人在持續抗凝期間仍發生 ischemic stroke 並出現 HT 時，何時重啟抗凝仍不確定。本研究描述這類病人的特徵與預後，並探討重啟時機與模型推估的缺血／出血風險平衡之間的關係。方法：分析多中心 ASPERA-R registry 中正在接受抗凝治療的 breakthrough stroke 病人，重點放在 HT 病人。HT 依 Heidelberg 分類，以 24 小時內的影像判定，分為 HI 或 PH。是否重啟抗凝及其時機由臨床醫師決定，未隨機分配。以 landmark Cox 模型評估重啟後的缺血事件與中重度出血，並以 restricted cubic spline 與探索性 net clinical benefit 分析評估時機與合併風險的關係。結果：1,555 人中有 269 人（17.3%）發生 HT，其中 170 人（63.2%）重啟抗凝。90 天時，HT 組的缺血事件（27.1% vs 13.8%）、中重度出血（7.4% vs 2.8%）與死亡（34.2% vs 17.7%）粗率較高。landmark 分析中，HT 與缺血事件無關（HR 1.42, 0.85–2.37），但與出血強烈相關（HR 3.39, 1.61–7.13）。合併風險約在第 10 天最低，不確定性大。結論：HT 是預後不佳的指標；第 10 天的估計屬假說生成，需要前瞻性驗證。

### European Stroke Journal

★★ ASPECTS 0–5 EVT registry（Asperger H 等）。理由：可作為 large core 病人預後溝通的參考。

【摘要譯文】EVT 已用於 large infarct，但對 ASPECTS 0–2 的 extensive infarct 仍較保守，真實世界資料有限。本研究回溯分析 German Stroke Registry 中接受 EVT 的前循環阻塞病人，比較 ASPECTS 0–2 與 3–5。主要結果為 90 天 mRS 分布。篩選 18,069 人，分析 889 人（1–2 分 89 人，3–5 分 800 人，沒有 0 分）。ASPECTS 1–2 組 mRS 0–3 為 20.2%，90 天內死亡 55.1%。在納入 successful reperfusion 的模型中，infarct group 與 mRS 沒有顯著關聯（cOR 0.80；0.53–1.23；mRS 0–3 aOR 0.89；0.64–1.25），successful reperfusion 則與兩者相關（cOR 3.68；aOR 4.10）。存活者 EQ-5D 效用值中位數為 0.445 vs 0.541，居家比例為 51.5% vs 50.9%。結論：部分選擇過的病人仍可能有可接受的結果，特別是成功再灌流者；由於沒有內科治療對照，這些資料描述的是預後而非療效。

★★ EEG-based ML for LVO-a detection（Groenendijk E 等）。理由：與到院前分流有關，但仍在早期研究階段。

【摘要譯文】EEG 有潛力作為前循環 LVO 的到院前分流工具。本研究使用 ELECTRA-STROKE 與 AI-STROKE 的資料，以 8 個乾式電極錄製 2–3 分鐘 EEG，納入至少有 5 秒乾淨片段的病人，擷取對稱性特徵，並以 nested CV 評估多種模型。1,293 人中有 336 人納入（74% 到院前），年齡中位數 72 歲，男性 69%；LVO-a 16 人（5%）、非 LVO 缺血性中風 140 人、TIA 52 人、出血性中風 13 人、mimic 115 人。Naïve Bayes AUC 0.85（0.77–0.93），sensitivity 69%（44–86%），specificity 86%（82–89%）。結論：診斷準確性中等偏高，但在考慮臨床應用之前，需要先改善 EEG 資料擷取。

★ Serum BD-tau in lacunar stroke/CSVD（Gattringer T 等）：101 位 RSSI 病人的 baseline BD-tau 高於對照組（9.54 vs 7.75 pg/mL，P=.003），3 個月時回到對照水準，且與 CSVD 影像特徵及預後都無關。https://doi.org/10.1093/esj/aakag133 · PMID 42969846

### Stroke

★★ Cervical curvature and MT recanalization（Lee J 等）。理由：用術前 CTA 就能評估，但需要外部驗證。

【摘要譯文】背景：血管幾何可能阻礙導管在 MT 中的通行；本研究評估 cervical curvature 是否能預測 recanalization 成功。方法：單中心回溯 cohort，納入 160 位接受 MT 的前循環 LVO 病人（2019/5–2021/2），以術前 CTA 的 3D centerline 計算 curvature。主要結果為 mTICI ≥2b 與 intracranial access time，並以多變項迴歸（校正年齡、NIHSS、第一線器械與入路）及 Random Forest、Gradient Boosting 搭配 SHAP 分析。結果：平均年齡 67 歲，NIHSS 中位數 16，平均 curvature 9.80。access time 中位數 24 分鐘，與 curvature 無關（β=0.20，P=0.676）。成功率 86%，依三分位為 91%／93%／75%（P=0.017）。每單位 aOR 1.21（1.02–1.43），超過 11.54 時 aOR 5.10（1.88–13.84）。ML 也確認 curvature 是最主要的預測因子，SHAP 峰值在 11.65。結論：curvature 可獨立預測 MT 失敗，閾值約 11.6，可能有助於風險分層與擬定策略。

★★ Physical activity and early independent walking（Shimizu N 等）。理由：可直接轉化為住院復健的活動安排。

【摘要譯文】目的是找出與早期獨立行走相關的活動強度與頻率。11 家機構的前瞻性 cohort 研究，納入入住亞急性復健病房、FAC 1–2 的病人，以加速度計測量 1 週活動，結果為 1 個月時 FAC ≥4，使用 modified Poisson regression 分析。389 人（平均 68.1 歲，女性 45.0%）中有 113 人達到獨立行走。high-LPA 每天每 5 分鐘 RR 1.067（1.010–1.131），low-LPA 與 MVPA 無關；≥2.0 METs 的 short-bout 次數 RR 1.208（1.060–1.375），long-bout 無關。結論：累積 high-LPA 與短時段活動，和早期獨立行走相關。

★ MEP variability and recovery potential（Nucci L 等）：77 位亞急性病人中，baseline MEP variability 與 FMA-UE（P=2.76×10⁻⁷）及 Motor Recovery Index（P=0.009）相關。https://doi.org/10.1161/strokeaha.126.056786 · PMID 42974709

★ How Stroke Genetics Is Impacting Clinical Care（Markus H）：綜述，沒有新數據。https://doi.org/10.1161/strokeaha.126.051399

### JAMA Neurology／Neurology（其他）

★ Coupling of Neurologic and Physiatric Perspectives（Viewpoint），沒有數據。https://doi.org/10.1001/jamaneurol.2026.4055

★ Teaching NeuroImage：雙側小腦梗塞後的 cerebellar mutism，屬個案影像，卷期日期 2026-12-08。https://doi.org/10.1212/wnl.0000000000218713

<a id="s9"></a>

## 排除項目

- Eastern Long Island 中風神經科醫師與取栓中心頁面：屬徵才或宣傳
- 葡萄牙內科醫學會第 27 屆中風研討會：只有會議資訊，沒有研究結果
- AHA「Sexuality and Stroke」：病人衛教內容
- AHA「Cannabis use linked to CVD」新聞：W45 週報只提供 Google News 轉址，原始研究未在本次核對（待確認）

<a id="s10"></a>

## 資料來源

- **Repo：** t0mst0ne/stroke-uptodate（main）
- **週報路徑：** reports/2026-W45.md
- **File SHA：** f46c454ea802486c29a9dec11e7b89aa79dc9f36
- **涵蓋期間：** 2026-10-31 至 2026-11-07
- **前一週報告：** repo 中不存在，無法去重
- **驗證方式：** CrossRef API 取得摘要與發表日期；PubMed esearch／efetch 取得 PMID；期刊頁與 AHA newsroom

- [週報原始檔](https://github.com/t0mst0ne/stroke-uptodate/blob/main/reports/2026-W45.md)（GitHub）
- [Early rhythm control（Neurology）](https://doi.org/10.1212/WNL.0000000000218736)（Neurology）
- [ASPERA-R HT](https://doi.org/10.1177/17474930261502562)（IJS）
- [2026 AHA/ASA Rehabilitation Guideline](https://doi.org/10.1161/STR.0000000000000536)（Stroke）

本頁內容僅供文獻閱讀與教育參考，不構成個別病人醫療建議。
