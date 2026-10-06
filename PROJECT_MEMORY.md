# 连云港市志数字化 项目记忆

## 2026-10-06 当前状态（全书缺表二次清零）

- **表**：正文 716 张已核结构化表格全部内联于 reader 正文原位（表格站 719 条，含 3 条站点独有：表4-4 取代的旧表 T008、表55-1 重复残录 T083/T084）。缺表清单 `workbench/table_entries/missing_tables_20261005.json` 共 293 条，全部结清：291 张回源重建 + 方言卷表59-2/59-11 两张 IPA 音系表按决策保持压平（skip）。
- **两轮补缺**：①2026-10-05 专项（278 张：上册清零→中卷清零→下卷清零，含双漏 表29-18/29-20/44-31/54-6主表/56-3/56-10 与 表41-6）；②2026-10-06 二次盘点（**表号 OCR 空格变体盲区**「表 25  3」类致首轮漏检，复扫再补 12 张：表44-13/44-14/44-23/44-24/46-13/47-4/47-15/25-3/29-22/40-10/42-1/13-1）；③2026-10-06 第三轮内容级/图形级审计（上册 OCR 数字比对 + 中下表格线检测）再补 **表40-18**（OCR 粘连号「表4018」）。图（图表/照片）不在交付范围。
- **正文真值**：`workbench/body_chapters_v2/` 分卷 Markdown（含页锚与 `{{STRUCTURED_TABLE:…}}` 占位）；阅读版 `output/final_reader/连云港市志_全书.html`；线上 https://xixingchao.github.io/lianyungang-city-gazetteer/ （docs/ 同步）。
- **门禁**：`scripts/audit_delivery_quality.py`、`scripts/audit_full_reader.py`、`scripts/audit_flattened_remnants_20261006.py` 全部 issues=0；每批修改均 reader+v2 双端同步。
- **照录原则**：原书印误（数字矛盾、届次错位、用字不一、OCR 空格表号等）一律照录并在表 JSON notes 注明，不静默改写。
- 交付包：`output/package/` 下最新一版（reader HTML + PDF + 表格站 + 报告）。留痕教训：盘点表号必须用容错正则；检测脚本改后先用已知正反例自检再执行删除。

## 2026-07-01 全量已核结构化表格嵌回主阅读版

- 新增脚本：`scripts/embed_verified_tables_into_reader.py`。
- 将结构化表格站中 `verified` 状态且有数据行的表格按卷归组嵌回 `output/final_reader/连云港市志_全书.html`，每卷末尾生成 `已核结构化表格` 小节。
- 本轮嵌回表格 307 张；未能自动归组表格：无。
- 嵌回表格使用 `class="structured-table"`，保留表ID和源页，不暴露内部 notes；脚本以 `VERIFIED-STRUCTURED-TABLES-START/END` 标记块保持幂等。
- 进度报告：`output/reports/progress/20260701_全量已核结构化表格嵌回主阅读版.md`。
