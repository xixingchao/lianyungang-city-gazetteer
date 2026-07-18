# -*- coding: utf-8 -*-
"""Verify selected transport, commerce, and finance tables from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T060": {
        "title": "1990年新浦汽车站客运发车情况表",
        "table_number": "表30-6",
        "page": 1451,
        "pages": [1451],
        "columns": ["到达站", "里程(公里)", "班次"],
        "rows": [
            ["上海", "566", "2"],
            ["杭州", "654", "1"],
            ["苏州", "541", "1"],
            ["无锡", "424", "1"],
            ["常州", "411", "1"],
            ["扬州", "298", "1"],
            ["南京", "322", "3"],
            ["南通", "395", "2"],
            ["盐城", "196", "2"],
            ["阜宁", "136", "2"],
            ["济南", "394", "1"],
            ["烟台", "490", "1"],
            ["青岛", "315", "2"],
            ["胶县", "247", "1"],
            ["潍坊", "307", "1"],
            ["泰安", "314", "1"],
            ["阜阳", "455", "1"],
            ["沂水", "182", "1"],
            ["淮阴", "125", "6"],
            ["涟水", "124", "2"],
            ["陈港", "124", "2"],
            ["射阳", "184", "1"],
            ["泗阳", "167", "1"],
            ["淮安", "143", "1"],
            ["宿县", "341", "1"],
            ["兖州", "286", "1"],
            ["曲阜", "270", "1"],
            ["滨海", "111", "4"],
            ["沭阳", "103", "4"],
            ["合肥", "525", "1"],
            ["徐州", "223", "1"],
            ["赣榆站", "42", "18"],
            ["东海站", "52", "15"],
            ["灌云站", "37", "32"],
            ["连云港", "35", "50"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0031.txt。原表为三组横排，本轮展开为到达站、里程、班次三列。",
    },
    "LYG-中-T070": {
        "title": "1981~1990年连云港市集体商业网点人员数",
        "table_number": "表33-3",
        "page": 1545,
        "pages": [1545],
        "columns": ["地区", "项目", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990"],
        "rows": [
            ["市区", "网点", "253", "399", "473", "678", "895", "982", "1136", "1131", "1143", "1081"],
            ["市区", "人员", "1985", "2739", "2406", "3638", "6975", "6574", "7901", "8318", "9520", "9699"],
            ["赣榆", "网点", "546", "568", "608", "968", "986", "1094", "1148", "1058", "1100", ""],
            ["赣榆", "人员", "1245", "1257", "1065", "2715", "2758", "3186", "3264", "3026", "3007", ""],
            ["东海", "网点", "463", "619", "658", "1197", "1187", "1201", "1313", "1154", "1141", ""],
            ["东海", "人员", "985", "1329", "1435", "2939", "3789", "4073", "4771", "4455", "4211", ""],
            ["灌云", "网点", "597", "654", "673", "1106", "1112", "951", "953", "983", "833", ""],
            ["灌云", "人员", "2917", "2757", "3843", "5936", "6034", "6109", "6309", "6622", "6182", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0125.txt。单位为个、人；源页 OCR 未给出赣榆、东海、灌云 1990 年列数值，按源可见文本保留空白。",
    },
    "LYG-中-T108": {
        "title": "1984~1990年连云港市金融机构存款统计表",
        "table_number": "表40-2",
        "page": 1775,
        "pages": [1775],
        "columns": ["种类", "单位", "1984", "1985", "1986", "1987", "1988", "1989", "1990"],
        "rows": [
            ["法定准备金", "市工商行", "2881", "3675", "5045", "7341", "8776", "9510", "11182"],
            ["法定准备金", "市农行", "2239", "1722", "3182", "5869", "6534", "8553", "10029"],
            ["法定准备金", "市中行", "3068", "418", "444", "625", "767", "1225", "2118"],
            ["法定准备金", "市建行", "", "2659", "3441", "1994", "1911", "2253", "4084"],
            ["法定准备金", "市交行", "", "", "", "300", "300", "", "3443"],
            ["法定准备金", "非银行金融机构", "", "", "", "269", "407", "354", "368"],
            ["法定准备金", "合计", "8188", "8474", "12112", "16098", "18695", "22195", "31224"],
            ["支付准备金", "市工商行", "1430", "2091", "549", "255", "848", "1872", ""],
            ["支付准备金", "市农行", "1758", "4815", "2275", "802", "1565", "1437", ""],
            ["支付准备金", "市中行", "619", "667", "744", "801", "2414", "3340", ""],
            ["支付准备金", "市建行", "1464", "1106", "2050", "861", "2138", "2983", ""],
            ["支付准备金", "市交行", "", "", "", "1537", "4505", "3631", ""],
            ["支付准备金", "非银行金融机构", "", "", "", "308", "482", "1266", "1777"],
            ["支付准备金", "合计", "5271", "8679", "5926", "4738", "12736", "15040", ""],
            ["特种存款", "农村信用社", "", "", "", "426", "451", "417", "650"],
            ["特种存款", "信托投资公司", "", "", "", "", "27", "", ""],
            ["特种存款", "合计", "", "", "", "426", "478", "417", "650"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0355.txt。单位为万元；多层表头展开为种类、单位、年份列，源页未列数值的单元格保留空白。",
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
    for table_id in PATCHES:
        path = DATA_DIR / f"{table_id}.json"
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
