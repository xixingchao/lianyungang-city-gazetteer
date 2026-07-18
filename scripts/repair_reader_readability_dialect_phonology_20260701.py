# -*- coding: utf-8 -*-
"""Verify the repaired dialect phonology layout in the final reader.

The heavy OCR-linearized repair for 第五十九卷方言 has already been applied in
this worktree. This script is intentionally idempotent: it verifies the repaired
state, refreshes the repair report, and fails with a clear message if the old
linearized source state reappears.
"""

from __future__ import annotations

import json
from datetime import datetime
from html import unescape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_dialect_phonology_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_dialect_phonology_20260701.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260701_第五十九卷方言音系与同音字汇版式修复.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

REQUIRED_MARKERS = [
    '<h5>一、声母(18)</h5>',
    '<caption>声母(18)</caption>',
    '<h5>二、韵母(40)</h5>',
    '<caption>韵母(40)</caption>',
    '<h5>三、声调(5)</h5>',
    '<caption>声调(5)</caption>',
    'class="dialect-phonology-table"',
]

OLD_LINEARIZED_MARKERS = [
    "一、声母(18)p帮鼻板布别",
    "二、韵母(40)1 资支词四事",
    "三、声调(5)调类代码",
    "1③你里理鲤俚狸狐",
]

STYLE_BLOCK = """
.dialect-phonology-table{width:100%;border-collapse:collapse;margin:10px 0 12px;font-size:10pt;line-height:1.55;font-family:SimSun,"Noto Serif SC",serif}
.dialect-phonology-table caption{font-weight:600;text-align:left;margin-bottom:4px}
.dialect-phonology-table th{background:#f1f4f7;border:1px solid #c9c9c9;padding:4px 8px;text-align:left;white-space:nowrap}
.dialect-phonology-table td{border:1px solid #c9c9c9;padding:4px 8px;vertical-align:top;word-break:break-word}
.dialect-word-list{margin:8px 0 14px;font-size:10pt;line-height:1.7;font-family:SimSun,"Noto Serif SC",serif}
.dialect-word-list p{margin:3px 0;text-indent:0}
.dialect-word-head{font-weight:600;margin-right:0.5em}
""".strip()


def strip_tags(html: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html))).strip()


def ensure_style(html: str) -> tuple[str, bool]:
    if ".dialect-phonology-table" in html:
        return html, False
    if "</style>" not in html:
        raise RuntimeError("final reader style block not found")
    return html.replace("</style>", STYLE_BLOCK + "\n</style>", 1), True


def verify_and_refresh() -> dict[str, object]:
    html = HTML_PATH.read_text(encoding="utf-8")
    html, style_added = ensure_style(html)
    plain = strip_tags(html)
    old_present = [marker for marker in OLD_LINEARIZED_MARKERS if marker in plain]
    missing = [marker for marker in REQUIRED_MARKERS if marker not in html]
    if old_present or missing:
        raise RuntimeError(
            "dialect phonology repair is not in the expected current state; "
            f"old_present={old_present}; missing={missing}"
        )
    if style_added:
        HTML_PATH.write_text(html, encoding="utf-8")
    return {
        "style_added": style_added,
        "old_linearized_markers_present": old_present,
        "missing_required_markers": missing,
        "initial_rows": html.count("<caption>声母(18)</caption>"),
        "vowel_rows": html.count("<caption>韵母(40)</caption>"),
        "tone_rows": html.count("<caption>声调(5)</caption>"),
        "replacements": 0,
    }


def write_reports(result: dict[str, object]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第五十九卷方言 第二章声韵调、第三章同音字汇首页",
        "html_path": str(HTML_PATH),
        "source_ocr": [
            "workbench/ocr/paddle_ocr/下/part02/page_0300.txt",
            "workbench/ocr/paddle_ocr/下/part02/page_0301.txt",
            "workbench/ocr/paddle_ocr/下/part02/page_0303.txt",
        ],
        "principle": "按源 OCR 行列重排专业版式，不改写音标和字汇内容；本次运行验证已修复状态。",
        "result": result,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第五十九卷方言音系与同音字汇版式修复报告

生成时间：{now}

## 修复对象

- `第一节声韵调` 中声母、韵母、声调三处被 OCR 压成普通段落的表格。
- `第三章同音字汇` 首页首段被压成超长段落的字汇块。

## 当前状态

- 声母、韵母、声调表格化标记均存在。
- 旧线性化残文标记未检出。
- 本次运行新增样式：{result['style_added']}。

## 源证据

- `workbench/ocr/paddle_ocr/下/part02/page_0300.txt`
- `workbench/ocr/paddle_ocr/下/part02/page_0301.txt`
- `workbench/ocr/paddle_ocr/下/part02/page_0303.txt`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS_PATH.write_text(md, encoding="utf-8")


def update_memory() -> None:
    marker = "## 2026-07-01 第五十九卷方言音系与同音字汇版式修复"
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 脚本：`scripts/repair_reader_readability_dialect_phonology_20260701.py`。
- 验证最终阅读版第五十九卷方言中 `第一节声韵调` 的声母表、韵母表、声调表已经表格化，旧线性化残文不再出现。
- 源证据：`workbench/ocr/paddle_ocr/下/part02/page_0300.txt`、`page_0301.txt`、`page_0303.txt`。
- 报告：`output/reports/reader_readability_dialect_phonology_20260701.md`。
"""
    MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = verify_and_refresh()
    write_reports(result)
    update_memory()
    print("dialect phonology readability already repaired")
    print("replacements=0")
    print(f"style_added={int(result['style_added'])}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
