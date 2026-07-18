# -*- coding: utf-8 -*-
"""Repair source-backed subheading boundaries in volumes 42 and 46."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume42_46_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume42_46_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十二四十六卷小标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPAIRS = [
    {
        "heading": "一、第六届人民代表大会常务委员会",
        "old": "<p>一、第六届人民代表大会常务委员会第一次会议于1980年2月12日举行",
        "new": "<h5>一、第六届人民代表大会常务委员会</h5>\n<p>第一次会议于1980年2月12日举行",
        "source": "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33005-33006",
    },
    {
        "heading": "二、军队转业干部培训",
        "old": "<p>二、军队转业干部培训连云港市对军队转业干部的培训方式分省办班和市办班两种。",
        "new": "<h5>二、军队转业干部培训</h5>\n<p>连云港市对军队转业干部的培训方式分省办班和市办班两种。",
        "source": "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:10780-10781",
    },
]

DEFERRED = [
    "训练与扑救：当前汇总源文仍为同一行粘连，需页级/版面证据再拆。",
    "企业存款、金融机构存款：当前汇总源文仍为同一行粘连，需更强源文边界证据。",
    "国家周转油脂库存/油脂库存：疑似标题重复或表格残留，本批不猜修。",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed = []
    for item in REPAIRS:
        count = text.count(item["old"])
        if count != 1:
            raise RuntimeError(f"expected one match for {item['heading']!r}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"heading": item["heading"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十二卷政务、第四十六卷人事：源文独立行可证明的小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "deferred": DEFERRED,
        "notes": ["仅按源文独立行恢复标题边界，不改正文文字；证据不足的相似段暂缓。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十二、四十六卷小标题边界修复

- 时间：{now}
- 范围：第四十二卷政务、第四十六卷人事。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 暂缓\n\n"
    md += "".join(f"- {item}\n" for item in DEFERRED)
    md += "\n## 说明\n\n- 只恢复源文独立行可证明的版式边界，不改正文文字。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十二、四十六卷小标题边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复 `一、第六届人民代表大会常务委员会`、`二、军队转业干部培训` 2 处小标题粘正文问题。
- 依据 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`、`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md` 中独立行，只恢复标题边界，不改正文文字。
- 暂缓 `训练与扑救`、`企业存款/金融机构存款`、`国家周转油脂库存/油脂库存` 等源文证据不足或疑似表格残留项。
- 报告：`output/reports/reader_readability_volume42_46_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
