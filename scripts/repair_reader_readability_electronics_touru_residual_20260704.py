# -*- coding: utf-8 -*-
"""Repair source-checked 投人 -> 投入 OCR slips in the electronics volume."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_electronics_touru_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_electronics_touru_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_电子工业投人投入残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

START = '<h2 id="第二十二卷-电子工业">第二十二卷电子工业</h2>'
END = '<h2 id="第二十三卷-建材工业">第二十三卷建材工业</h2>'
SOURCE = (
    "workbench/ocr/paddle_ocr/中/part01/page_0237.txt:15,22,25,31; "
    "page_0238.txt:9,36; page_0239.txt:6; page_0249.txt:28,31; "
    "page_0250.txt:37; page_0251.txt:10; page_0254.txt:12,29; "
    "page_0255.txt:12; page_0259.txt:5"
)

REPLACEMENTS = [
    ("无线电话机未投产", "没有投人正式生产", "没有投入正式生产", "中/part01/page_0237.txt:15"),
    ("电子管收音机投产", "投人生产", "投入生产", "中/part01/page_0237.txt:22; page_0238.txt:36; page_0251.txt:10"),
    ("收音机正式投产", "正式投人生产", "正式投入生产", "中/part01/page_0237.txt:25"),
    ("晶体管收音机小批量", "投人小批量生产", "投入小批量生产", "中/part01/page_0237.txt:31; page_0249.txt:28"),
    ("电子产品投入市场", "大量投人市场", "大量投入市场", "中/part01/page_0238.txt:9"),
    ("收录机试生产", "投人试生产", "投入试生产", "中/part01/page_0239.txt:6; page_0259.txt:5"),
    ("元器件陆续批产", "陆续投人批量生产", "陆续投入批量生产", "中/part01/page_0249.txt:31"),
    ("元器件批量生产", "投人批量生产", "投入批量生产", "中/part01/page_0249.txt:28,31; page_0254.txt:12,29; page_0259.txt:5"),
    ("电视天线散件组装", "投人组装试生产", "投入组装试生产", "中/part01/page_0250.txt:37"),
    ("设备投入使用", "投人使用", "投入使用", "中/part01/page_0255.txt:12"),
    ("晶体管开始批产", "开始投人批量生产", "开始投入批量生产", "中/part01/page_0259.txt:5"),
]


def split_section(text: str) -> tuple[str, str, str]:
    start = text.index(START)
    end = text.index(END, start)
    return text[:start], text[start:end], text[end:]


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    before, section, after = split_section(text)
    counts: dict[str, int] = {}
    original_residuals = section.count("投人")
    for label, old, new, _source in REPLACEMENTS:
        count = section.count(old)
        if count:
            section = section.replace(old, new)
        elif new not in section:
            raise RuntimeError(f"neither old nor new text found in electronics volume: {label}")
        counts[label] = count
    if section.count("投人") != 0:
        raise RuntimeError(f"electronics volume still has 投人 residuals: {section.count('投人')}")
    HTML.write_text(before + section + after, encoding="utf-8")
    counts["电子工业卷原始投人残留"] = original_residuals
    return counts


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    items = [
        {"label": label, "old": old, "new": new, "source": source, "count": counts[label]}
        for label, old, new, source in REPLACEMENTS
    ]
    payload = {
        "time": now,
        "scope": "第二十二卷电子工业 `投人` 残留",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(item["count"] for item in items),
        "original_electronics_residuals": counts["电子工业卷原始投人残留"],
        "items": items,
        "principle": "仅修复第二十二卷电子工业内源页明确为 `投入` 的 `投人`；其它卷残留另行回源。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 电子工业投人/投入残留回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验条目：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        f"- 电子工业卷修复前 `投人` 残留：{payload['original_electronics_residuals']} 处，修复后 0 处。",
        "- 其它卷 `投人/收人/纳人` 残留未在本批处理。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 电子工业投人/投入残留回源修复

- 对第二十二卷电子工业 `投人` 残留做章节限定修复。
- 源文依据：`{SOURCE}`。
- 修复 `没有投人正式生产/投人生产/正式投人生产/投人小批量生产/大量投人市场/投人试生产/投人批量生产/投人组装试生产/投人使用/开始投人批量生产` 等 20 处为 `投入`。
- 其它卷 `投人/收人/纳人` 残留继续逐页核证后再处理。
- 报告：`output/reports/reader_readability_electronics_touru_residual_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 电子工业投人/投入残留回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(v for k, v in counts.items() if k != "电子工业卷原始投人残留"), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
