

## 2026-07-01 全量已核结构化表格嵌回主阅读版

- 新增脚本：`scripts/embed_verified_tables_into_reader.py`。
- 将结构化表格站中 `verified` 状态且有数据行的表格按卷归组嵌回 `output/final_reader/连云港市志_全书.html`，每卷末尾生成 `已核结构化表格` 小节。
- 本轮嵌回表格 307 张；未能自动归组表格：无。
- 嵌回表格使用 `class="structured-table"`，保留表ID和源页，不暴露内部 notes；脚本以 `VERIFIED-STRUCTURED-TABLES-START/END` 标记块保持幂等。
- 进度报告：`output/reports/progress/20260701_全量已核结构化表格嵌回主阅读版.md`。
