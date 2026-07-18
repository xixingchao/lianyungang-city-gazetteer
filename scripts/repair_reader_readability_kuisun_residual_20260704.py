# -*- coding: utf-8 -*-
"""Repair source-backed 亏损 OCR residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_kuisun_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_kuisun_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_亏损错识残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "渔业制冰机亏损停机",
        "old": "成本过高，号损严重而停机",
        "new": "成本过高，亏损严重而停机",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:50120; workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:7207",
    },
    {
        "label": "天鹅牌内销卫生纸亏损停产",
        "old": "生纸因号损而停产",
        "new": "生纸因亏损而停产",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:54545; workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:10663",
    },
    {
        "label": "地毯厂1974至1976年亏损",
        "old": "1974~1976年号亏损19.52万元",
        "new": "1974~1976年亏损19.52万元",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0044.txt:14",
    },
    {
        "label": "赣榆县瓷厂全年亏损",
        "old": "全年号损120.11万元",
        "new": "全年亏损120.11万元",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0048.txt:23",
    },
    {
        "label": "墟沟制冰厂亏损停产",
        "old": "后因号损停产",
        "new": "后因亏损停产",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0090.txt:35",
    },
    {
        "label": "新浦光学仪器厂多年亏损",
        "old": "多年号损的新浦光学仪器厂",
        "new": "多年亏损的新浦光学仪器厂",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0115.txt:8",
    },
    {
        "label": "港口1968和1969年连续亏损",
        "old": "1969年连续两年号亏损",
        "new": "1969年连续两年亏损",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0465.txt:36",
    },
    {
        "label": "公司亏损财政弥补",
        "old": "号损由国家财政按月弥补",
        "new": "亏损由国家财政按月弥补",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0485.txt:13",
    },
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
        "scope": "亏损 OCR 错识残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "仅修复 PaddleOCR 分页或同锚 PaddleOCR 正文明确证明的 `号损/号亏损` 错识；未闭合的商业百货 `当年号损1000多元` 暂缓。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 亏损错识残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：仅修复 PaddleOCR 分页或同锚 PaddleOCR 正文明确证明的 `号损/号亏损` 错识。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：商业百货 `当年号损1000多元` 尚未取得页级 OCR 证据闭合。",
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

    marker = "## 2026-07-04 亏损错识残留回源修复"
    memory = f"""
{marker}
- 依据上册 PaddleOCR 汇总/正文和中册 part01 分页 PaddleOCR，修复 `号损/号亏损` 为 `亏损`，共 {total} 处。
- 同步目标：主阅读版、全书正文汇总、上册正文汇总、上册第十至第十六卷分卷、中册第十七至第二十九卷分卷。
- 暂缓商业百货 `当年号损1000多元`，因尚未取得页级 OCR 证据闭合。
- 报告：`output/reports/reader_readability_kuisun_residual_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
