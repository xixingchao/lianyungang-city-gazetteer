# -*- coding: utf-8 -*-
"""Repair source-backed subheading boundaries in volumes 12-13."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volumes12_13_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volumes12_13_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第十二至十三卷小标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>四、舟山渔场1960年冬，连云港市组织": "<h5>四、舟山渔场</h5>\n<p>1960年冬，连云港市组织",
    "<p>四、燕尾港渔港位于灌云县燕尾镇": "<h5>四、燕尾港渔港</h5>\n<p>位于灌云县燕尾镇",
    "<p>四、拖网作业拖网渔具是20世纪50年代后期": "<h5>四、拖网作业</h5>\n<p>拖网渔具是20世纪50年代后期",
    "<p>四、疾病防治1985年春天，全市3500亩海带": "<h5>四、疾病防治</h5>\n<p>1985年春天，全市3500亩海带",
    "<p>四、其它品种增殖真鲷人工育苗放流增殖1982年": "<h5>四、其它品种增殖</h5>\n<p>真鲷人工育苗放流增殖1982年",
    "<p>四、季节管理2～4月鳗鱼苗管理": "<h5>四、季节管理</h5>\n<p>2～4月鳗鱼苗管理",
    "<p>四、工艺海水煎煮煎盐原为直接煎煮海水为盐": "<h5>四、工艺</h5>\n<p>海水煎煮煎盐原为直接煎煮海水为盐",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:5815-5816",
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:6237-6238",
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:6384-6385",
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:6870-6871",
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:7180-7181",
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:7788-7789",
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:8548-8549",
]

SKIPPED = [
    "四、紫菜：最终版前有线性表格数字残文，本批不拆。",
    "四、羊饲养规模：本轮未在源文件中直接命中同名独立行，本批不猜。",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {old!r}, got {count}")
        text = text.replace(old, new, 1)
        changed += 1
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第十二卷水产、第十三卷盐业：残留小标题边界",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "skipped": SKIPPED,
        "notes": ["仅按 PaddleOCR 源文独立行恢复标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第十二至十三卷小标题边界修复

- 时间：{now}
- 范围：第十二卷水产、第十三卷盐业残留目级小标题。
- 本次修复边界：{changed} 处。

## 修复

- 恢复 `四、舟山渔场`、`四、燕尾港渔港`、`四、拖网作业`。
- 恢复 `四、疾病防治`、`四、其它品种增殖`、`四、季节管理`。
- 恢复第十三卷盐业 `四、工艺`。
- 仅恢复源文可证明的版式边界，不改正文文字。

## 暂缓

"""
    md += "".join(f"- {item}\n" for item in SKIPPED)
    md += "\n## 依据\n\n"
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第十二至十三卷小标题边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第十二卷水产、第十三卷盐业 7 处小标题粘正文问题。
- 覆盖 `四、舟山渔场`、`四、燕尾港渔港`、`四、拖网作业`、`四、疾病防治`、`四、其它品种增殖`、`四、季节管理`、`四、工艺`。
- 暂缓 `四、紫菜`（前有线性表格数字残文）和 `四、羊饲养规模`（本轮未直接命中源文同名独立行）。
- 报告：`output/reports/reader_readability_volumes12_13_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
