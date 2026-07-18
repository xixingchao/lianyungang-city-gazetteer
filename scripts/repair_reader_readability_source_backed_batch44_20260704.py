# -*- coding: utf-8 -*-
"""Forty-fourth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch44_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch44_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十四批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "1990年财政收入", "old": "财政收入39808方元", "new": "财政收入39808万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0279.txt:19"},
    {"label": "1990年财政支出", "old": "支出38583方元", "new": "支出38583万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0279.txt:20"},
    {"label": "赣榆县契税牙税", "old": "契税、牙税7.28方元", "new": "契税、牙税7.28万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0289.txt:11"},
    {"label": "1958年工业部门基建支出", "old": "其中工业部门1885方元", "new": "其中工业部门1885万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0294.txt:18"},
    {"label": "其它部门基建支出", "old": "其它部门支出2540方元", "new": "其它部门支出2540万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0295.txt:6"},
    {"label": "1984年科技三项费用", "old": "1984年支出274方元", "new": "1984年支出274万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0295.txt:30"},
    {"label": "科技三项费用累计", "old": "科技三项费用支出3022方元", "new": "科技三项费用支出3022万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0295.txt:32"},
    {"label": "工业部门流动资金", "old": "工业部门3061方元", "new": "工业部门3061万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0295.txt:38"},
    {"label": "畜牧事业费", "old": "畜牧事业费613\n方元", "new": "畜牧事业费613\n万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0296.txt:17-18"},
    {"label": "教育经费", "old": "教育经费46477方元", "new": "教育经费46477万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0297.txt:11"},
    {"label": "专项支出", "old": "支出共9054方元", "new": "支出共9054万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0298.txt:19"},
    {"label": "技改企业免税", "old": "免税450方元", "new": "免税450万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0337.txt:5"},
    {"label": "减免税款", "old": "减免税款4720方元", "new": "减免税款4720万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0337.txt:19"},
    {"label": "税前还贷", "old": "税前还贷509方元", "new": "税前还贷509万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0337.txt:19"},
    {"label": "出口产品退税", "old": "出口产品退税670.5方元", "new": "出口产品退税670.5万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0337.txt:20"},
    {"label": "外贸企业出口退税", "old": "出口退税1347.9方元", "new": "出口退税1347.9万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0337.txt:28"},
    {"label": "贸易公司偷漏税", "old": "偷漏税241方元", "new": "偷漏税241万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0341.txt:31"},
    {"label": "1976年存款余额", "old": "存款余额为7579方元", "new": "存款余额为7579万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0354.txt:7"},
    {"label": "1957年贷款余额", "old": "贷款余额4862方元", "new": "贷款余额4862万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0389.txt:10"},
    {"label": "节约建设资金", "old": "节约建设资金10841方元", "new": "节约建设资金10841万元", "source": "workbench/ocr/paddle_ocr/中/part02/page_0390.txt:38"},
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
        "scope": "第四十四批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "依据中册 PaddleOCR 分页文本修复财政、税务、金融金额单位残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十四批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：依据中册 PaddleOCR 分页文本修复财政、税务、金融金额单位残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
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

    marker = "## 2026-07-04 第四十四批正文残留回源修复"
    memory = f"""
{marker}
- 依据中册 PaddleOCR 分页文本，修复财政、税务、金融段 `方元` 金额单位残留，共 {total} 处。
- 涉及证据页：`workbench/ocr/paddle_ocr/中/part02/page_0279.txt`、`page_0289.txt`、`page_0294.txt`、`page_0295.txt`、`page_0296.txt`、`page_0297.txt`、`page_0298.txt`、`page_0337.txt`、`page_0341.txt`、`page_0354.txt`、`page_0389.txt`、`page_0390.txt`。
- 未处理 `交通27方`：PaddleOCR 仅见 `交通27万`，仍缺完整单位闭合，留待单独核对。
- 报告：`output/reports/reader_readability_source_backed_batch44_20260704.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
