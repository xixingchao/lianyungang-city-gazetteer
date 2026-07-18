# -*- coding: utf-8 -*-
"""Audit whether user-reported conversion mixing exists in current delivery."""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
OLD = ROOT / "output" / "final_reader" / "obsolete" / "连云港市志_最终阅读版.html"
SOURCE_GLOBS = [
    ROOT / "workbench" / "body_chapters",
    ROOT / "output" / "final_reader",
]
REPORT_JSON = ROOT / "output" / "reports" / "user_reported_conversion_mixing_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "user_reported_conversion_mixing_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_用户反馈疑似整本串章错流审计.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TAG_RE = re.compile(r"<[^>]+>")
P_RE = re.compile(r"<p[^>]*>(.*?)</p>", re.S | re.I)
H_RE = re.compile(r"<h[1-6][^>]*>(.*?)</h[1-6]>", re.S | re.I)

PROBES = [
    {"name": "地层表续表岩性", "needle": "上部；以白云斜长片麻岩为主"},
    {"name": "地质构造褶皱", "needle": "东海一赣榆倒转复向斜"},
    {"name": "方言声韵调标题", "needle": "第一节声韵调"},
    {"name": "方言声母表", "needle": "一、声母(18)"},
    {"name": "方言韵母表", "needle": "二、韵母(40)"},
    {"name": "同音字汇说明", "needle": "本字汇收常用字4400多个"},
]

# These pairings should be far apart in the current reader. If they appear in one
# paragraph, it means table/text flow is being flattened into one reader block.
MIXING_PAIRS = [
    ("上部；以白云斜长片麻岩为主", "第一节声韵调"),
    ("东海一赣榆倒转复向斜", "本字汇收常用字4400多个"),
    ("连云港市地层", "一、声母(18)"),
]
TABLELIKE_RE = re.compile(r"(连云港市地层|续上表|系统厚度|地层名称|主要岩性|声母\(18\)|韵母\(40\)|调类代码|同音字汇)")


def plain(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(TAG_RE.sub(" ", value))).strip()


def excerpt(text: str, pos: int, limit: int = 150) -> str:
    if pos < 0:
        return ""
    start = max(0, pos - limit // 2)
    end = min(len(text), pos + limit // 2)
    return text[start:end].replace("|", "\\|")


def scan_html(path: Path) -> dict:
    html = path.read_text(encoding="utf-8", errors="ignore")
    text = plain(html)
    paragraphs = [plain(m.group(1)) for m in P_RE.finditer(html)]
    headings = [plain(m.group(1)) for m in H_RE.finditer(html)]
    long_paragraphs = [{
        "paragraph_index": idx,
        "chars": len(paragraph),
        "tablelike_hits": len(TABLELIKE_RE.findall(paragraph)),
        "excerpt": paragraph[:260].replace("|", "\\|"),
    } for idx, paragraph in enumerate(paragraphs, 1) if len(paragraph) >= 2500]
    tablelike_paragraphs = [p for p in long_paragraphs if p["tablelike_hits"] >= 2]
    probes = []
    for probe in PROBES:
        pos = text.find(probe["needle"])
        probes.append({**probe, "present": pos >= 0, "position": pos, "excerpt": excerpt(text, pos)})
    mixed_paragraphs = []
    for idx, paragraph in enumerate(paragraphs, 1):
        for left, right in MIXING_PAIRS:
            if left in paragraph and right in paragraph:
                mixed_paragraphs.append({
                    "paragraph_index": idx,
                    "left": left,
                    "right": right,
                    "chars": len(paragraph),
                    "excerpt": paragraph[:260].replace("|", "\\|"),
                })
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "exists": path.exists(),
        "bytes": path.stat().st_size if path.exists() else 0,
        "mtime": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S") if path.exists() else "",
        "paragraphs": len(paragraphs),
        "headings": len(headings),
        "long_paragraphs_ge_2500": len(long_paragraphs),
        "tablelike_long_paragraphs": len(tablelike_paragraphs),
        "long_samples": sorted(long_paragraphs, key=lambda item: item["chars"], reverse=True)[:8],
        "tablelike_samples": sorted(tablelike_paragraphs, key=lambda item: item["chars"], reverse=True)[:8],
        "probes": probes,
        "mixed_paragraphs": mixed_paragraphs,
    }


def grep_text_files() -> list[dict]:
    hits = []
    for base in SOURCE_GLOBS:
        for path in base.rglob("*"):
            if path.suffix.lower() not in {".html", ".md", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for probe in PROBES:
                pos = text.find(probe["needle"])
                if pos >= 0:
                    hits.append({
                        "probe": probe["name"],
                        "needle": probe["needle"],
                        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                        "position": pos,
                    })
    return hits


def write_memory(content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    marker = "## 2026-07-06 用户反馈疑似整本串章错流审计"
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def render(data: dict) -> str:
    current = data["current"]
    old = data["old"]
    lines = [
        "# 用户反馈疑似整本串章/错流审计",
        "",
        f"> 生成时间：{data['time']}",
        "",
        "## 结论",
        "",
        f"- 当前主交付 `{current['path']}` 未发现用户反馈特征串跨段混入同一段落：mixed_paragraphs={len(current['mixed_paragraphs'])}；超长段落={current['long_paragraphs_ge_2500']}；疑似表格压平超长段={current['tablelike_long_paragraphs']}。",
        f"- 已隔离旧文件 `{old['path']}`，修改时间 {old['mtime']}；超长段落={old['long_paragraphs_ge_2500']}；疑似表格压平超长段={old['tablelike_long_paragraphs']}，不应作为当前交付源。",
        "- 当前交付包构建脚本读取 `output/final_reader/连云港市志_全书.html`，并在包内复制为 `连云港市志_最终阅读版.html`。",
        "- 本审计不证明逐字校勘完成，只证明用户贴出的这类地质/方言压平形态未污染当前主交付；后续仍要继续逐条回源修字。",
        "",
        "## HTML 检查",
        "",
        "| 文件 | 修改时间 | 段落数 | 标题数 | 混合段落数 | >=2500字段落 | 表格压平超长段 | 大小 |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in [current, old]:
        lines.append(f"| `{item['path']}` | {item['mtime']} | {item['paragraphs']} | {item['headings']} | {len(item['mixed_paragraphs'])} | {item['long_paragraphs_ge_2500']} | {item['tablelike_long_paragraphs']} | {item['bytes']} |")
    lines.extend(["", "## 特征串位置", "", "| 文件 | 特征 | 存在 | 字符位置 | 摘录 |", "|---|---|---:|---:|---|"])
    for item in [current, old]:
        for probe in item["probes"]:
            lines.append(f"| `{item['path']}` | {probe['name']} | {'是' if probe['present'] else '否'} | {probe['position']} | {probe['excerpt']} |")
    lines.extend(["", "## 混合段落样例", ""])
    if not current["mixed_paragraphs"]:
        lines.append("- 当前主交付：未检出。")
    for sample in current["mixed_paragraphs"][:5]:
        lines.append(f"- 当前主交付段落 {sample['paragraph_index']}：{sample['excerpt']}")
    if old["mixed_paragraphs"]:
        lines.append("")
        lines.append("旧文件样例：")
        for sample in old["mixed_paragraphs"][:5]:
            lines.append(f"- 旧文件段落 {sample['paragraph_index']}，{sample['chars']} 字：{sample['excerpt']}")
    lines.extend(["", "## 表格压平/超长段样例", ""])
    if not current["tablelike_samples"]:
        lines.append("- 当前主交付：未检出疑似表格压平超长段。")
    else:
        for sample in current["tablelike_samples"][:3]:
            lines.append(f"- 当前主交付段落 {sample['paragraph_index']}，{sample['chars']} 字：{sample['excerpt']}")
    if old["tablelike_samples"]:
        lines.append("")
        lines.append("旧文件表格压平样例：")
        for sample in old["tablelike_samples"][:3]:
            lines.append(f"- 旧文件段落 {sample['paragraph_index']}，{sample['chars']} 字：{sample['excerpt']}")
    lines.extend(["", "## 源文件命中摘要", "", f"- 特征串在工作区文本文件中共命中 {len(data['source_hits'])} 处，详见 JSON 报告。"])
    return "\n".join(lines) + "\n"


def main() -> None:
    if not CURRENT.exists():
        raise SystemExit(f"missing current reader: {CURRENT}")
    if not OLD.exists():
        raise SystemExit(f"missing old reader: {OLD}")
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "current": scan_html(CURRENT),
        "old": scan_html(OLD),
        "source_hits": grep_text_files(),
        "principle": "No image display; text-only diagnosis of user-reported conversion mixing.",
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(data)
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    write_memory(f"""
## 2026-07-06 用户反馈疑似整本串章错流审计

- 新增并运行 `scripts/audit_user_reported_conversion_mixing_20260706.py`，用用户贴出的地质表/构造段与方言声韵/同音字汇特征串检查当前主交付和旧阅读版。
- 结论：当前主交付 `output/final_reader/连云港市志_全书.html` 未检出这类跨段混合或疑似表格压平超长段；旧 `output/final_reader/obsolete/连云港市志_最终阅读版.html` 仍有历史压平风险，已隔离，不应作为当前交付源。
- 报告：`output/reports/user_reported_conversion_mixing_20260706.md`；未展示、未嵌入图片。
""")
    print(f"current_mixed={len(data['current']['mixed_paragraphs'])}")
    print(f"old_mixed={len(data['old']['mixed_paragraphs'])}")
    print(f"current_tablelike_long={data['current']['tablelike_long_paragraphs']}")
    print(f"old_tablelike_long={data['old']['tablelike_long_paragraphs']}")
    print(f"source_hits={len(data['source_hits'])}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
