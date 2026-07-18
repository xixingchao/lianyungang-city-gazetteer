# -*- coding: utf-8 -*-
"""Verify table 46-17 party organization evolution continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

PATCHES = {
    "LYG-下-T028": {
        "title": "建国后中共连云港市委工作机构、直属单位、群团组织沿革表（续表）",
        "table_number": "表46-17",
        "page": 2193,
        "pages": [2193],
        "columns": ["机构名称", "沿革"],
        "rows": [
            ["《连云港报》社", "《新海连市报》社(1958.3~1958.5)、《新海连日报》社(1958.5~1961.10)、《连云港日报》社(1961.10~1967.1)、《连云港报》社(1969.3~1972.9、1979.3~)"],
            ["讲师团", "讲师团(1986.5~)"],
            ["纪律检查委员会", "纪律检查委员会(1950.5~1956.1)、监察委员会(1956.1~1966.5)、市委纪律检查委员会(1979.4~1983.9)、市纪律检查委员会(1983.10~)升格为市五套班子之一"],
            ["市总工会", "职工运动委员会(市职工总会、职工筹委会1949.11~1952.4)、市总工会(1949.11~1953.12)、市工会联合会(1953.12~1959.1)、市总工会(1962.9~1966.5、1973.7~)"],
            ["团市委", "青年工作委员会(1949.11前沿袭前青年工作委员会~1957.4)、团市委(1949.12~1966.3、1973.1~)"],
            ["市妇女联合会", "妇女工作委员会(1949.11~1952.4)、市民主妇女联合会(1951.3~1957.9)、市妇女联合会(1957.9~1966.5、1973.7~)"],
            ["市科学技术协会", "科学技术普及协会(1956.11~1958)、市科学技术协会(1958~1966.5、1977.12~)"],
            ["市文学艺术界联合会", "市文学艺术界联合会(1979.10~)"],
            ["市归国华侨联合会", "市归国华侨联合会小组(1980.9~1983.7)、市归国华侨联合会(1983.7~)"],
            ["市哲学社会科学联合会", "市哲学社会科学研究会(1979.12~1982.8)、市社会科学联合会(1982.8~1985.12)、市哲学社会科学联合会(1985.12~)"],
            ["市工商业联合会", "特区工商联合会筹委会(1949.10~1952.6)、市工商业联合会(1952.6~1966.5、1981.1~)"],
            ["市老龄工作委员会", "市老龄工作委员会(1986.7~)"],
            ["市五讲四美三热爱办公室", "市五讲四美三热爱办公室(1984.12~1987)"],
            ["市经济案件办公室", "市经济案件领导小组办公室(1982.2~1983.6)、市经济案件办公室(1983.6~1987)"],
            ["市贫下中农协会", "市农民协会筹委会(1949.11~1965.11)、市贫下中农协会筹委会(1965.11~1966.5)、市贫下中农协会(1977.7~1983.5)"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/下/part01/page_0222.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T028_2193.txt。表题和表号依据表46-17首页 workbench/ocr/paddle_ocr/下/part01/page_0221.txt；本页为续上表。多行机构名称与跨行沿革说明按版面合并，未增补源页外信息。",
    }
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
