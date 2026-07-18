# -*- coding: utf-8 -*-
"""Remove the decorative OCR noise line before Volume 59 title."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
NOISE = "83383833838383838383838338383338383838383838 38383838383938838\n"
REPORT_MD = ROOT / "output" / "reports" / "volume59_intro_noise_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "volume59_intro_noise_20260709.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷卷首OCR噪声清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"


def main() -> None:
    changes = []
    for path in FILES:
        text = path.read_text(encoding="utf-8")
        start = text.index("<!-- page-anchor: LYG-2727 -->")
        title = text.index("第五十九卷", start)
        end = text.index("第六十卷", start)
        block = text[start:end]
        count = block.count(NOISE)
        if count:
            text = text[:start] + block.replace(NOISE, "") + text[end:]
            path.write_text(text, encoding="utf-8")
        changes.append({"path": str(path.relative_to(ROOT)), "removed": count})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "noise": NOISE.strip(), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = "\n".join(f"| `{item['path']}` | {item['removed']} |" for item in changes)
    md = f"""# 第五十九卷卷首OCR噪声清理

- 时间：{now}
- 范围：第五十九卷方言卷首。

## 动作

删除卷题前的装饰/OCR噪声行：

`{NOISE.strip()}`

## 结果

| 文件 | 删除行数 |
|---|---:|
{rows}

本批不改方言正文、音标、词条和阅读器 HTML。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-09 第五十九卷卷首OCR噪声清理"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in memory:
        entry = f"""
{marker}

- 删除第五十九卷方言卷题前装饰/OCR噪声行 `{NOISE.strip()}`。
- 范围：下册 part02 现行正文源稿与全书正文汇总；不改方言正文、音标、词条和阅读器 HTML。
- 报告：`output/reports/volume59_intro_noise_20260709.md`；进度：`output/reports/progress/20260709_第五十九卷卷首OCR噪声清理.md`。
"""
        MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")

    print("volume59 intro noise repaired")
    for item in changes:
        print(f"{item['path']}: removed={item['removed']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
