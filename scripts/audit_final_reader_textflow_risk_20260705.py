# -*- coding: utf-8 -*-
"""Audit text-flow risks across final-reader HTML files.

This is intentionally small: count reader-facing long paragraphs and table-like
paragraphs, and distinguish the current packaged reader from older siblings.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL_DIR = ROOT / "output" / "final_reader"
CURRENT_READER = FINAL_DIR / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "final_reader_textflow_risk_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "final_reader_textflow_risk_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_阅读版文本流风险审计.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TAG_RE = re.compile(r"<[^>]+>")
P_RE = re.compile(r"<p[^>]*>(.*?)</p>", re.S | re.I)
H_RE = re.compile(r"<h([23])[^>]*>(.*?)</h\1>", re.S | re.I)
TABLE_TOKENS = re.compile(r"(表\s*\d+[-－]\d+|续上表|系统|地层名称|主要岩性|声母|韵母|调类|例字|同音字汇|开口呼|齐齿呼|合口呼|撮口呼)")
ANCHORS = [
    "表1-1 连云港市地层系统表",
    "东海一赣榆倒转复向斜",
    "第一节声韵调",
    "第三章同音字汇",
]


def plain(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(TAG_RE.sub(" ", value))).strip()


def excerpt(value: str, limit: int = 160) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[: limit - 1] + "..."


def scan_file(path: Path) -> dict:
    html = path.read_text(encoding="utf-8", errors="ignore")
    text = plain(html)
    headings = [plain(m.group(2)) for m in H_RE.finditer(html)]
    paragraphs = [plain(m.group(1)) for m in P_RE.finditer(html)]
    long_ps = [p for p in paragraphs if len(p) >= 2500]
    very_long_ps = [p for p in paragraphs if len(p) >= 8000]
    table_like = [p for p in paragraphs if len(p) >= 800 and len(TABLE_TOKENS.findall(p)) >= 3]
    anchor_positions = {anchor: text.find(anchor) for anchor in ANCHORS}
    samples = []
    for p in sorted(table_like, key=len, reverse=True)[:10]:
        samples.append({
            "chars": len(p),
            "token_hits": len(TABLE_TOKENS.findall(p)),
            "excerpt": excerpt(p),
        })
    top_long = []
    for p in sorted(long_ps, key=len, reverse=True)[:10]:
        top_long.append({"chars": len(p), "excerpt": excerpt(p)})
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "is_current_reader": path == CURRENT_READER,
        "bytes": path.stat().st_size,
        "h2_h3": len(headings),
        "paragraphs": len(paragraphs),
        "long_paragraphs_ge_2500": len(long_ps),
        "very_long_paragraphs_ge_8000": len(very_long_ps),
        "table_like_paragraphs": len(table_like),
        "anchor_positions": anchor_positions,
        "table_like_samples": samples,
        "top_long_samples": top_long,
    }


def render(data: dict) -> str:
    rows = sorted(data["files"], key=lambda item: (not item["is_current_reader"], -item["table_like_paragraphs"], item["path"]))
    current = next(item for item in rows if item["is_current_reader"])
    old_risky = [item for item in rows if not item["is_current_reader"] and item["table_like_paragraphs"]]
    lines = [
        "# 阅读版文本流风险审计",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 当前交付脚本使用：`{CURRENT_READER.relative_to(ROOT).as_posix()}`",
        "",
        "## 结论",
        "",
        f"- 当前主交付 `output/final_reader/连云港市志_全书.html`：超长段落 {current['long_paragraphs_ge_2500']} 个，疑似表格压扁段落 {current['table_like_paragraphs']} 个。",
        f"- 同目录存在旧阅读版/分册 HTML，其中 {len(old_risky)} 个文件仍有疑似表格压扁段落；用户若打开旧 `连云港市志_最终阅读版.html`，会看到地层表、方言表等压成正文长段的问题。",
        "- 这次不删除旧文件，只记录风险；后续建议把当前主交付重打包，并在说明里避免把旧 HTML 当最终版。",
        "- 本报告只做文本流风险计数，不代表逐字校勘完成。",
        "",
        "## 文件统计",
        "",
        "| 文件 | 当前主交付 | 大小 | 段落 | >=2500字段落 | >=8000字段落 | 疑似表格压扁段落 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in rows:
        lines.append(
            f"| `{item['path']}` | {'是' if item['is_current_reader'] else '否'} | {item['bytes']} | {item['paragraphs']} | {item['long_paragraphs_ge_2500']} | {item['very_long_paragraphs_ge_8000']} | {item['table_like_paragraphs']} |"
        )
    lines.extend(["", "## 锚点位置", "", "| 文件 | 锚点 | 字符位置 |", "|---|---|---:|"])
    for item in rows:
        for anchor, pos in item["anchor_positions"].items():
            if pos >= 0:
                lines.append(f"| `{item['path']}` | {anchor} | {pos} |")
    lines.extend(["", "## 疑似表格压扁样例", "", "| 文件 | 字符数 | 命中词数 | 摘录 |", "|---|---:|---:|---|"])
    for item in rows:
        for sample in item["table_like_samples"][:3]:
            text = sample["excerpt"].replace("|", "\\|")
            lines.append(f"| `{item['path']}` | {sample['chars']} | {sample['token_hits']} | {text} |")
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    files = sorted(FINAL_DIR.glob("*.html"))
    data = {"files": [scan_file(path) for path in files]}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(data)
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-05 阅读版文本流风险审计"
    append_once(MEMORY, marker, f"""
{marker}
- 新增并运行 `scripts/audit_final_reader_textflow_risk_20260705.py`，审计 `output/final_reader/*.html` 的超长段落和疑似表格压扁段落。
- 当前交付脚本使用 `output/final_reader/连云港市志_全书.html`；旧 `output/final_reader/连云港市志_最终阅读版.html` 仍在目录内，且含地层表、方言表等压成段落的历史风险。
- 报告：`output/reports/final_reader_textflow_risk_20260705.md`。
""")

    current = next(item for item in data["files"] if item["is_current_reader"])
    risky = sum(1 for item in data["files"] if item["table_like_paragraphs"])
    print(f"files={len(data['files'])}")
    print(f"current_table_like_paragraphs={current['table_like_paragraphs']}")
    print(f"current_long_paragraphs_ge_2500={current['long_paragraphs_ge_2500']}")
    print(f"files_with_table_like_paragraphs={risky}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
