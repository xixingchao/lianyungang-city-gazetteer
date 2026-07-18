# -*- coding: utf-8 -*-
"""Verify LYG-下-T089/T090 international sports results table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_FILES = {
    "LYG-下-T089": ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T089.json",
    "LYG-下-T090": ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T090.json",
}

COLUMNS = ["姓名", "类别", "年份", "地点", "项目", "成绩"]
PATCHES = {
    "LYG-下-T089": {
        "title": "连云港籍运动员参加国际比赛成绩一览表",
        "table_number": "表56-7",
        "page": 2679,
        "pages": [2679],
        "columns": COLUMNS,
        "rows": [
            ["韩永年", "亚洲新兴力量运动会", "1966", "柬埔寨", "800米、1500米", "第一名、第二名"],
            ["谭红海", "国际田径赛", "1981", "墨西哥", "跳远", "第二名"],
            ["谭红海", "泰国国际田径邀请赛", "1981", "曼谷", "跳远", "第一名"],
            ["谭红海", "国际田径邀请赛", "1982", "北京", "跳远", "第二名"],
            ["谭红海", "第九届亚运会", "1982", "印度", "跳远", "第四名"],
            ["谭红海", "国际田径邀请赛", "1983", "罗马尼亚", "200米", "第一名"],
            ["谭红海", "“奥林匹克日”田径赛", "1983", "德国", "跳远", "第七名"],
            ["谭红海", "罗申斯基纪念赛", "1983", "捷克", "跳远、200米", "第二名、第五名"],
        ],
        "status": "verified",
        "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T089_2679.txt；原JSON为单列待录入骨架。页首含上一表续表残段，本轮仅录入表56-7；续表见LYG-下-T090。",
    },
    "LYG-下-T090": {
        "title": "连云港籍运动员参加国际比赛成绩一览表（续表）",
        "table_number": "表56-7",
        "page": 2680,
        "pages": [2680],
        "columns": COLUMNS,
        "rows": [
            ["陈玉霞", "第十届亚运会", "1986", "汉城", "自行车64公里", "第五名"],
            ["张六如", "国际女子篮球赛", "1987", "西安", "代表江苏省队参赛", "团体第三名"],
            ["许学宁", "第十一届亚运会", "1990", "北京", "重剑", "第六名"],
            ["赵德岭", "第十一届亚运会", "1990", "北京", "拳击91公斤以上级", "第二名"],
        ],
        "status": "verified",
        "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T090_2680.txt；原JSON为单列待录入骨架。本页为表56-7续表。",
    },
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


def patch_entry(entry: dict) -> bool:
    patch = PATCHES.get(entry.get("table_id"))
    if not patch:
        return False
    changed = False
    for key, value in patch.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    changed = 0
    for path in DATA_FILES.values():
        data = json.loads(path.read_text(encoding="utf-8"))
        if patch_entry(data):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    return changed


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise SystemExit("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = 0
    for table in tables:
        if patch_entry(table):
            changed += 1
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
