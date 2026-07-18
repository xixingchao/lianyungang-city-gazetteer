# -*- coding: utf-8 -*-
"""Append Batch 46/47 notes to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第四十六批：文化绘画残留短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch46_culture_painting_residue_20260706.py`，据页级 PaddleOCR 对照修复主阅读版 5 个文化卷书法、绘画、雕塑残留短片段。
- 证据页包括 `workbench/ocr/paddle_ocr/下/part02/page_0021.txt`、`page_0022.txt`、`page_0023.txt`。
- 主要修复：`王寿暖书法遗作展览` -> `王寿谖书法遗作展览`；绘画人才段补回 `张霭楼`、`一批美术新苗茁壮成长`、`王寿谖`、`程民义、陈学慈、花千红、石仁勇`、油画与水彩水粉画分组；修复 `《收海带》` 书名号、`《习作》`、`《先驱者》、《李白》`。
- 用户贴出的地质表、构造段、方言声韵段，经检索在最终 HTML 中分别位于自然环境卷和方言卷正常章节；当前未证实为全书级混流故障。后续继续按源页证据逐项清理零散 OCR 残留，不做无证全局替换。
- 边界：每项旧串唯一命中；只处理下册文化卷 `page_0021` 至 `page_0023` 已闭合短片段；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第四十六批_文化绘画残留短片段.md`。

## 2026-07-06 高置信 OCR 错字补修第四十七批：工厂与千瓦单位短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch47_units_factories_20260706.py`，据页级 PaddleOCR 和同页单位体系对照修复主阅读版 17 个工厂/千瓦单位 OCR 残留。
- 证据页包括中册 `workbench/ocr/paddle_ocr/中/part01/page_0225.txt`、`page_0284.txt`、`page_0321.txt`、`page_0365.txt`、`page_0366.txt`、`page_0375.txt`、`page_0377.txt`、`page_0392.txt`、`page_0448.txt`、`page_0449.txt`，以及下册 `workbench/ocr/paddle_ocr/下/part01/page_0189.txt`。
- 主要修复：`该广/专业工广/加工广` -> `该厂/专业工厂/加工厂`，`方于瓦/于瓦/干瓦/方千瓦` -> 对应 `万千瓦/千瓦/万千瓦时/千瓦时` 等单位。
- 边界：不全局替换 `广/于/干/方`；暂不处理仅 raw OCR 可见且 raw 本身仍错的石灰厂段 `市石灰广/烟简/第建筑公司/进行商`。未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第四十七批_工厂与千瓦单位短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第四十七批：工厂与千瓦单位短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
