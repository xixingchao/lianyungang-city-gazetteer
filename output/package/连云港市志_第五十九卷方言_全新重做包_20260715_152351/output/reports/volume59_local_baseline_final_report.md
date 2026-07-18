# 第59卷本地完成态核验报告

生成时间：2026-07-15 15:23:44

## 结论

本地维护基线完成；OCR草稿需人工双审后才能作为最终文本。

本轮第59卷已经在本地统一为全新重做维护基线：重新抽取源页、重新渲染页图、重新生成 OCR 草稿、建立页级分流和方言路由清单，并形成可重打包的本地项目。

重要边界：当前 OCR 草稿不能冒充最终双审文本。第59卷含大量音标、声韵调表、同音字汇和方言词汇，后续正式正文/字典数据必须回看页图进行人工分块、结构化和双审。

## 证据链核对

- 项目根目录：`E:\codex_Learing\17_project_数字化工作站\projects\lianyungang-city-gazetteer-volume59-fresh`
- 抽页源 PDF：`E:\codex_Learing\17_project_数字化工作站\projects\lianyungang-city-gazetteer-volume59-fresh\input\source\连云港市志_第五十九卷方言_源页_全新重做.pdf`（43.06 MB）
- 卷内页数：48 页
- 页图：原图 48 页，裁切图 48 页
- RapidOCR：48 页
- 方言分流 inventory：48 页
- HTML 草稿：`E:\codex_Learing\17_project_数字化工作站\projects\lianyungang-city-gazetteer-volume59-fresh\output\reader\连云港市志_第五十九卷方言_全新OCR草稿.html`
- Markdown 草稿：`E:\codex_Learing\17_project_数字化工作站\projects\lianyungang-city-gazetteer-volume59-fresh\output\reader\连云港市志_第五十九卷方言_全新OCR草稿.md`

## OCR 风险统计

- dialect_layout_risk: 9 页
- high_ocr_risk: 35 页
- review_required: 4 页

- 全卷平均 OCR 置信度：0.7168
- 高 OCR 风险页：2, 3, 4, 5, 8, 10, 11, 14, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45
- 方言版式风险页：6, 7, 9, 12, 13, 16, 17, 18, 19

## 方言路由统计

- dictionary_mode: 16 页
- mixed_dialect_prose: 6 页
- phonology_tables_or_prose: 26 页

## 本地 QA

- 缺失项数量：0
- 源 PDF、页图、OCR、方言清单、读者文件均已核对存在。

## 后续维护口径

1. 后续上传 GitHub 时，以本项目最新 `output/package/` 里的包作为第59卷维护基线。
2. 不再把旧 OCR、旧 redo 台账、旧验收状态作为本轮第59卷依据。
3. 如果要生成最终正式文本，应从本包继续：先做版面分块，再做 dictionary mode 结构化，再做两轮双审。
