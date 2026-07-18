# -*- coding: utf-8 -*-
"""Repair source-backed postwar garrison subhead boundaries in volume 45."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume45_military_garrison_postwar_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume45_military_garrison_postwar_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十五卷军事驻防第三节标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

H4 = '<h4 id="第四十五卷-第二章驻防-第三节解放后驻防及人民武装机关">第三节解放后驻防及人民武装机关</h4>\n'
REPAIRS = [
    {
        "old": "<p>解放后驻防及人民武装机关第三节一、驻防华东野战军独立旅民国37年（1948年）11月，",
        "new": H4 + "<h5>一、驻防</h5>\n<p>华东野战军独立旅民国37年（1948年）11月，",
        "heading": "第三节解放后驻防及人民武装机关 / 一、驻防",
        "source": f"{SOURCE}:9592-9593",
    },
    {
        "old": "<p>二、人民武装机关连云港市人民武装部1950年成立新海连市人民武装部，",
        "new": "<h5>二、人民武装机关</h5>\n<p>连云港市人民武装部1950年成立新海连市人民武装部，",
        "heading": "二、人民武装机关",
        "source": f"{SOURCE}:9631",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    if text.count(H4) != 1:
        raise RuntimeError(f"expected one postwar garrison h4, got {text.count(H4)}")
    text = text.replace(H4, "", 1)
    fixed: list[dict[str, str]] = []
    for item in REPAIRS:
        count = text.count(item["old"])
        if count != 1:
            raise RuntimeError(f"expected one match for {item['heading']}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"heading": item["heading"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十五卷军事：第二章驻防第三节",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["移动后置 h4 到源文节首；拆出两个编号子目标题；不改正文内容。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十五卷军事驻防第三节标题边界补修

- 时间：{now}
- 范围：第四十五卷军事，第二章驻防第三节。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 将后置节标题移回源文对应位置。\n- 拆出 `一、驻防`、`二、人民武装机关` 两个编号子目标题。\n- 不重写驻防条目正文，不猜改 OCR 内容。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十五卷军事驻防第三节标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十五卷军事第二章驻防第三节 2 处标题边界：`第三节解放后驻防及人民武装机关 / 一、驻防`、`二、人民武装机关`。
- 依据 `{SOURCE}:9592-9631` 源文独立标题行；仅移动后置 h4 并拆出 h5，不改正文内容。
- 报告：`output/reports/reader_readability_volume45_military_garrison_postwar_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
