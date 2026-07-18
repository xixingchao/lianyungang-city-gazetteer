# -*- coding: utf-8 -*-
"""Forty-ninth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch49_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch49_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十九批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "医用敷料收购值断行", "old": "医用敷料有3个品种，主要是药棉、药用纱布及手术垫。1990年收购值为1550.17\n\n<!-- page-anchor: LYG-1608 -->\n\n方元，创汇420万美元。", "new": "医用敷料有3个品种，主要是药棉、药用纱布及手术垫。1990年收购值为1550.17\n\n<!-- page-anchor: LYG-1608 -->\n\n万元，创汇420万美元。", "source": "workbench/ocr/paddle_ocr/中/part02/page_0187.txt:40 + page_0188.txt:3"},
    {"label": "物资企业借入资金", "old": "借入资金10029方元", "new": "借入资金10029万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0260.txt:46"},
    {"label": "物资企业折旧资金", "old": "1541方元。仓库面积", "new": "1541万元。仓库面积", "source": "workbench/ocr/paddle_ocr/中/part02/page_0261.txt:4"},
    {"label": "戏剧小品剧名", "old": "《小路弯弯》《方元户的追求》", "new": "《小路弯弯》、《万元户的追求》", "source": "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:11"},
    {"label": "业余文艺骨干训练班经费", "old": "经费200方元（旧人民市）", "new": "经费200万元（旧人民币）", "source": "workbench/ocr/paddle_ocr/下/part02/page_0051.txt:22"},
    {"label": "新东电灯股份公司筹股", "old": "筹股7.4方元（银元）", "new": "筹股7.4万元（银元）", "source": "workbench/ocr/paddle_ocr/中/part01/page_0332.txt:13"},
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(target["changed"] for target in targets)
    payload = {
        "time": now,
        "scope": "第四十九批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "依据中册 part01/part02、下册 part02 PaddleOCR 分页文本修复强证据方元残留。",
        "deferred": ["国营蔬菜公司销售额70多方元：当前 OCR 仍为旧串，缺少直接闭合证据。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十九批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：依据中册 part01/part02、下册 part02 PaddleOCR 分页文本修复强证据 `方元` 残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：国营蔬菜公司销售额 `70多方元` 当前 OCR 仍为旧串，缺少直接闭合证据。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                lines.append(f"- {item['label']}：依据 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。")
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 第四十九批正文残留回源修复"
    memory = f"""
{marker}
- 依据中册 part01/part02、下册 part02 PaddleOCR 分页文本，修复强证据 `方元` 残留及同源行币种/剧名错字，共 {total} 处。
- 同步目标：`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`、`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`、`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`；最终阅读版未命中这些旧串。
- 暂缓国营蔬菜公司销售额 `70多方元`，当前 OCR 仍为旧串，缺少直接闭合证据。
- 报告：`output/reports/reader_readability_source_backed_batch49_20260704.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
