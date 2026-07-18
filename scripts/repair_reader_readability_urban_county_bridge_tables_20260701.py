# -*- coding: utf-8 -*-
"""Repair reader residue for tables 5-6 and 5-7, and add verified bridge data."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_urban_county_bridge_tables_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_urban_county_bridge_tables_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第五卷市区县城桥梁表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = ["桥梁名称", "所处道路名称", "跨越河流名称", "长(米)", "宽(米)", "结构形式", "建设时间"]
COUNTY_COLUMNS = ["县城", "桥梁名称", "所处道路名称", "长(米)", "宽(米)", "结构形式", "建设时间"]

URBAN_ROWS = [
    ["甲子桥", "海州东大街", "排洪沟", "3.4", "7.0", "石板", "清嘉庆九年(1804年)拓建，1953年修建"],
    ["民主桥", "民主路", "盐河", "21.2", "6.0", "钢筋混凝土双曲拱", "民国26年(1937年)左右建，1972年改建"],
    ["龙尾桥", "民主路", "龙尾河", "14.1", "5.1", "钢筋混凝土板梁", "光绪末年建，民国26年改建石桥，1951年改建，1973年改建"],
    ["盐河桥", "海连路", "盐河", "42.0", "30.66", "中间双曲拱桥，边钢筋混凝土T梁", "40年代初建，1970年改建，1982年扩建"],
    ["幸福桥", "幸福路", "玉带河", "38.6；南引道164.5；北引道189.8", "21.0", "砼桁架拱", "1964年建，1975年重建"],
    ["沈圩桥", "新新路", "大浦河", "50.0", "4.0", "砼双曲拱", "1971年建"],
    ["洪门桥", "海青路", "蔷薇河", "145.3", "9.0", "砼梁式", "明万历年初建，崇祯五年(1632年)修建，清初重建，1960年改建"],
    ["江化桥", "江化路", "玉带河", "34.2", "8.1", "砼桁架拱", "1972年建"],
    ["海州桥", "新海路", "玉带河", "24.0", "10.0", "砼T梁", "1964年改建"],
    ["解放桥", "解放路", "盐河", "31.4", "14.4", "砼T梁", "1949年建，1963年重建"],
    ["北大桥", "海滨路", "盐河", "30.0", "5.0", "砼板梁", "1972年建"],
    ["利民桥", "利民路", "龙尾河", "13.5", "8.2", "中间砼T梁，边为木桥", "1984年建，1988年扩建"],
    ["北城桥", "北城路", "涧沟", "10.0", "20.0", "砼板梁", "1989年改建"],
    ["程庄桥", "中山路", "涧沟", "8.0", "28.0", "石拱", "1984年建"],
    ["北门桥", "新海路", "护城河", "5.0", "30.8", "砼板梁", "1986年建"],
    ["向阳桥", "锦屏路", "西门涧沟", "10.0", "9.2", "砼双曲拱", "1957年建，1967年改建"],
    ["和平桥", "解放路", "龙尾河", "16.6", "24.8", "砼T梁", "民国31年建，1957年重建，1979年扩建"],
    ["贾圩桥", "海连路", "龙尾河", "23.0", "25.0", "砼T梁", "1963年改建，1981年扩建"],
    ["庞沟桥", "中山路", "涧沟", "8.0", "28.0", "石拱", "1983年建"],
    ["石门桥", "中山路", "涧沟", "10.8", "33.0", "砼板梁", "1985年建"],
    ["跃进桥", "海棠路", "涧沟", "8.3", "10.5", "条石", "1975年改建"],
    ["砚台桥", "中山路", "涧沟", "5.0", "28.0", "石拱", "1983年建"],
    ["海棠南桥", "海棠路", "润沟", "6.0", "22.0", "砼板梁", "1988年建"],
    ["墟沟桥", "中山路", "涧沟", "6.0", "33.0", "石拱", "1963年改建，1985年扩建"],
]

COUNTY_ROWS = [
    ["赣榆县", "柘汪河桥", "通榆汾线", "43.9", "7.0", "T梁，灌注桩", "1966年建"],
    ["赣榆县", "青口生产桥", "", "100.0", "4.0", "石桥台、桥墩", "1974年建"],
    ["赣榆县", "青口大桥", "华中路", "98.0", "7.0", "钢筋混凝土桥面", "1958年建，1962年重建，1989年建"],
    ["赣榆县", "青口水漫桥", "东关路", "66.1", "9.0", "钢台板，重石", "1985年建"],
    ["赣榆县", "环城西路桥", "环城西路", "114.8", "12.0", "台墩梯形大梁", "1989年建"],
    ["东海县", "牛山桥", "牛山路北首", "29.8", "11.8", "石拱", "1958年建，1982年改建"],
    ["东海县", "钢铁桥", "钢铁西路与幸福南路交叉口", "21.2", "17.0", "石拱", "1953年建"],
    ["东海县", "和平桥", "和平西路与幸福路交叉口", "", "", "板梁桥", "1958年建"],
    ["东海县", "利民桥", "利民西路", "50.2", "10.0", "拱桥", "1984年建"],
    ["东海县", "幸福桥", "幸福路北首", "24.3", "10.0", "板梁桥", "1975年建"],
    ["灌云县", "双桥", "伊山路", "20.0", "25.0", "混凝土平板", "1976年建"],
    ["灌云县", "新建桥", "伊山路", "20.0", "15.0", "混凝土平板", "1976年建"],
    ["灌云县", "胜利桥", "胜利路", "40.0", "15.0", "混凝土石拱", "1955年建"],
    ["灌云县", "三桥", "向阳路", "20.0", "40.0", "混凝土平板", "1987年建"],
    ["灌云县", "北大桥", "向阳路", "40.0", "15.0", "混凝土石拱", "民国时期建，1952年改建，1988年改建"],
    ["灌云县", "新村桥", "新村路", "20.0", "20.0", "混凝土平板", "1985年建"],
    ["灌云县", "东方红桥", "淮连路", "40.0", "15.0", "混凝土石拱", "1966年建"],
    ["灌云县", "东门河桥", "淮连路", "50.0", "20.0", "混凝土石拱", "民国时期建，1956年、1984年改建"],
    ["灌云县", "伊山拱桥", "拱桥巷", "30.0", "10.0", "石拱", "明代建，1955年改建"],
    ["灌云县", "灌中桥", "灌中路", "20.0", "12.0", "混凝土平板", "民国时期建，1987年改建"],
    ["灌云县", "青龙桥", "青龙巷", "30.0", "7.0", "石桥", "明代建，清代改建"],
]

ENTRIES = [
    {
        "table_id": "LYG-上-T045",
        "title": "1990年连云港市市区桥梁情况表",
        "table_number": "表5-6",
        "page": 296,
        "pages": [296, 297],
        "part": "part02",
        "vol": "上",
        "columns": COLUMNS,
        "rows": URBAN_ROWS,
        "row_count": len(URBAN_ROWS),
        "col_count": len(COLUMNS),
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0051.txt、page_0052.txt；并参考 raw OCR：workbench/ocr/raw/上/part02/page_0051.txt。表5-6跨两页，page_0052为续上表。幸福桥长栏含桥长及南北引道长，按源页可见内容保留为序列。",
        "volume": "上",
    },
    {
        "table_id": "LYG-上-T046",
        "title": "1990年连云港市县城桥梁情况表",
        "table_number": "表5-7",
        "page": 298,
        "pages": [298],
        "part": "part02",
        "vol": "上",
        "columns": COUNTY_COLUMNS,
        "rows": COUNTY_ROWS,
        "row_count": len(COUNTY_ROWS),
        "col_count": len(COUNTY_COLUMNS),
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0053.txt；并参考 raw OCR：workbench/ocr/raw/上/part02/page_0053.txt。表5-7在同页结束，后接“二、隧道”正文。和平桥长、宽栏源页未见数值，保留空值。",
        "volume": "上",
    },
]

URBAN_RESIDUE_RE = re.compile(
    r"\s*<p>（米）</p>\s*"
    r"<p>甲子桥海州东大街排洪沟3\.47\.0石板清嘉庆九年（1804年）拓建，1953年修建民主桥民主路盐河21\.26\.0钢筋混凝土双曲民国26年（1937年）左右拱建，1972年改建光绪末年建，民国26年龙尾桥民主路龙尾河14\.15\.1钢筋混凝土板梁改建石桥，1951年改建，1973年改建</p>\s*"
    r"<p>（米）</p>\s*"
    r"<p>（米）</p>\s*",
    re.S,
)

COUNTY_RESIDUE_RE = re.compile(
    r"\s*<p>柘汪河桥通榆汾线43\.97\.0T梁，灌注桩1966年建赣青口生产桥100\.04\.01974年建.*?1990年9月25日凿通。</p>\s*",
    re.S,
)

TUNNEL_HTML = """
<p>二、隧道</p>
<p>1984年1月，江苏省人民防空设计院设计的连云至宿城隧道工程，由市人防办公室批准立项，命名为“841”工程，全长3641米，断面高8.6米，宽8.2米，为全国最长的城市道路隧道，平时作交通通道，战时作防空袭使用。1984年4月1日动工兴建，1990年9月25日凿通。</p>
""".strip()


def write_jsons() -> int:
    changed = 0
    for entry in ENTRIES:
        path = DATA_DIR / f"{entry['table_id']}.json"
        new = json.dumps(entry, ensure_ascii=False, indent=2) + "\n"
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if old != new:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    by_id = {entry["table_id"]: entry for entry in ENTRIES}
    changed = False
    seen = set()
    for idx, table in enumerate(tables):
        table_id = table.get("table_id")
        if table_id in by_id:
            seen.add(table_id)
            if table != by_id[table_id]:
                tables[idx] = by_id[table_id]
                changed = True
    for table_id, entry in by_id.items():
        if table_id not in seen:
            tables.append(entry)
            changed = True
    if changed:
        tables.sort(key=lambda t: (str(t.get("vol") or t.get("volume") or ""), int((t.get("pages") or [t.get("page") or 999999])[0]), str(t.get("table_id") or "")))
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
        return 1
    return 0


def repair_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    title_fixed = 0
    old = "<p>一、桥梁南宋景定四年（1263年），安抚使张英汉主持，在海州城内新建东市桥、清宁桥和西市</p>\n<p>桥。</p>"
    new = "<p>一、桥梁</p>\n<p>南宋景定四年（1263年），安抚使张英汉主持，在海州城内新建东市桥、清宁桥和西市桥。</p>"
    if old in text:
        text = text.replace(old, new, 1)
        title_fixed = 1
    text, urban_removed = URBAN_RESIDUE_RE.subn("\n", text, count=1)
    text, county_removed = COUNTY_RESIDUE_RE.subn("\n" + TUNNEL_HTML + "\n", text, count=1)
    HTML.write_text(text, encoding="utf-8")
    return {"heading_fixed": title_fixed, "urban_residue_removed": urban_removed, "county_residue_removed": county_removed}


def write_reports(json_changed: int, site_changed: int, reader_result: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "tables": [entry["table_id"] for entry in ENTRIES],
        "json_changed": json_changed,
        "site_changed": site_changed,
        **reader_result,
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第五卷市区县城桥梁表残文修复

- 时间：{now}
- 表ID：`LYG-上-T045`、`LYG-上-T046`
- 表题：表5-6 `1990年连云港市市区桥梁情况表`；表5-7 `1990年连云港市县城桥梁情况表`
- 源页：`workbench/ocr/paddle_ocr/上/part02/page_0051.txt`、`page_0052.txt`、`page_0053.txt`

## 修复动作

- 新增/更新 verified 结构化表：`workbench/table_entries/上/data/LYG-上-T045.json`、`workbench/table_entries/上/data/LYG-上-T046.json`。
- `表5-6` 核录 {len(URBAN_ROWS)} 行、{len(COLUMNS)} 列；`表5-7` 核录 {len(COUNTY_ROWS)} 行、{len(COUNTY_COLUMNS)} 列。
- 从最终阅读版撤出市区桥梁表首段残文 {reader_result['urban_residue_removed']} 组、县城桥梁表残文 {reader_result['county_residue_removed']} 组。
- 恢复被县城桥梁残文吞入的 `二、隧道` 正文，并拆开 `一、桥梁` 小标题粘连：{reader_result['heading_fixed']}。

## 核对说明

- `表5-6` 首页在 page_0051，续页在 page_0052。
- `表5-7` 位于 page_0053，同页在表后进入 `二、隧道`。
- 县城桥梁表中 `和平桥` 长、宽栏源页未见数值，保留空值。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(reader_result: dict[str, int]) -> None:
    marker = "## 2026-07-01 第五卷市区县城桥梁表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 针对正文可读性审计命中的第五卷城乡建设桥梁表线性化残文，回源 `workbench/ocr/paddle_ocr/上/part02/page_0051.txt`、`page_0052.txt`、`page_0053.txt` 核对。
- 新增 verified 表：`workbench/table_entries/上/data/LYG-上-T045.json`（表5-6《1990年连云港市市区桥梁情况表》）与 `workbench/table_entries/上/data/LYG-上-T046.json`（表5-7《1990年连云港市县城桥梁情况表》）。
- 从 `output/final_reader/连云港市志_全书.html` 撤出市区桥梁表首段残文 {reader_result['urban_residue_removed']} 组、县城桥梁表残文 {reader_result['county_residue_removed']} 组；恢复 `二、隧道` 正文并拆开 `一、桥梁` 小标题粘连。
- 报告：`output/reports/reader_readability_urban_county_bridge_tables_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    json_changed = write_jsons()
    site_changed = patch_site()
    reader_result = repair_reader()
    write_reports(json_changed, site_changed, reader_result)
    update_memory(reader_result)
    print(f"json_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"reader={reader_result}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
