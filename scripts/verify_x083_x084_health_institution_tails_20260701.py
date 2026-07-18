# -*- coding: utf-8 -*-
"""Verify LYG-下-T083/T084 health institution table tail pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

COLUMNS = ["源页", "源页行序", "机构分类名称", "源页可见数值序列", "说明"]
NOTE = "按页级OCR和 raw 坐标OCR 同行横向可见顺序保留；本表列数极多，未据合计关系反推缺失小格。"

ROWS_083 = [
    ["2646", "1", "乡卫生院计-市", "8、140、176、139、7、27、24、2、6、2、1、1、8、21、5、2、5、2、3、10、1、3、9、21、16", NOTE],
    ["2646", "2", "乡卫生院计-县", "74、1509、2761、2451、70、533、177、21、58、34、27、28、441、266、100、28、104、39、26、5、110、19、52、286、228、82", NOTE],
    ["2646", "3", "中心卫生院", "13、502、756、662、19、140、52、7、18、10、5、7、92、96、25、4、30、18、2、4、26、5、19、8、75、63、31", NOTE],
    ["2646", "4", "乡卫生院", "69、1147、2181、1928、58、420、149、16、46、26、23、22、357、191、80、26、79、23、27、1、94、14、34、22、220、186、67", NOTE],
    ["2646", "5", "3.其他医院计", "2、52、111、90、4、26、14、2、3、3、2、1、2、15、6、1、4、2、4、1、13、8", NOTE],
    ["2646", "6", "其他医院计-市", "2、52、111、90、4、26、14、2、3、3、2、1、2、15、6、1、4、2、4、1、13、8", NOTE],
    ["2646", "7", "综合医院", "2、52、111、90、4、26、14、2、3、3、2、1、2、15、6、1、4、2、4、1、13、8", NOTE],
    ["2646", "8", "二、疗养院所", "7、1175、614、210、10、59、47、1、10、8、4、7、39、2、2、1、5、1、1、13、10、102、292", NOTE],
    ["2646", "9", "三、门诊部、所合计", "449、119、1710、1586、23、591、149、10、33、17、7、9、265、125、12、40、21、5、2、36、2、19、14、206、82、42", NOTE],
    ["2646", "10", "门诊部、所合计-市", "301、99、1143、1055、15、476、92、6、26、9、6、3、178、82、7、25、15、4、1、17、1、5、5、82、58、30", NOTE],
    ["2646", "11", "门诊部、所合计-县", "148、20、567、531、8、115、57、4、7、8、1、6、87、43、5、15、6、1、1、19、14、9、124、24、12", NOTE],
    ["2646", "12", "幼儿园、托儿所卫生所室", "4、6、6、2、2、1、1", NOTE],
    ["2646", "13", "区、乡卫生所", "9、181、158、6、39、25、3、3、5、1、2、20、16、3、4、2、3、1、7、4、14、14、9", NOTE],
    ["2646", "14", "其他", "436、119、1523、1422、17、550、122、7、30、12、6、7、244、109、9、36、21、3、2、33、1、12、10、191、68、33", NOTE],
    ["2646", "15", "四、专科防治所、站", "4、97、68、30、3、1、2、12、5、7、3、1、1、1、2、18、11", NOTE],
    ["2646", "16", "麻风病防治所、站", "4、97、68、30、3、1、2、12、5、7、3、1、1、1、2、18、11", NOTE],
    ["2646", "17", "五、卫生防疫站", "11、424、301、125、10、40、7、71、1、23、4、2、18、21、48、54", NOTE],
    ["2646", "18", "县卫生防疫站", "3、185、129、52、4、11、1、41、13、2、2、3、6、23、27", NOTE],
]

ROWS_084 = [
    ["2647", "1", "卫生防疫站-其他", "8、239、172、73、6、29、6、30、1、10、2、15、15、25、27", NOTE],
    ["2647", "2", "六、妇幼保健所、站", "8、8、115、91、44、16、2、1、10、1、11、1、2、1、2、1、20、3", NOTE],
    ["2647", "3", "县妇幼保健所、站", "3、8、63、51、18、12、1、5、10、1、1、1、2、1、10、1", NOTE],
    ["2647", "4", "妇幼保健所、站-其他", "8、52、40、26、4、1、1、5、1、1、1", NOTE],
    ["2647", "5", "七、药品检验所、室", "4、45、32、9、13、2、2、1、2、1、1、8、5", NOTE],
    ["2647", "6", "县药品检验所、室", "3、17、14、4、5、1、2、1、1、2、1", NOTE],
    ["2647", "7", "药品检验所、室-其他", "1、28、18、5、8、2、2、1、6、4", NOTE],
    ["2647", "8", "八、其他卫生事业机构", "5、158、58、3、22、7、1、8、3、7、1、3、1、2、37、45、18", NOTE],
    ["2647", "9", "国境卫生检疫所", "1、23、13、6、2、1、2、2、9、1", NOTE],
    ["2647", "10", "输血站", "1、23、14、2、3、7、1、1、7、2", NOTE],
    ["2647", "11", "卫生干部进修学校", "2、81、12、7、1、4、35、24、10", NOTE],
    ["2647", "12", "县卫生进修学校", "1、31、19、3、7、1、1、1、2、1、1、2、2、5、5", NOTE],
    ["2647", "13", "九、医学科学研究机构", "1、30、22、13、2、4、1、2、1、1、2、1、5、3", NOTE],
    ["2647", "14", "十、中医药研究院、所", "1、30、22、13、2、4、1、2、1、1、2、1、5、3", NOTE],
    ["2647", "15", "十一、中等医药学校", "1、95、31、5、7、7、10、1、1、28、24、12", NOTE],
    ["2647", "16", "十二、个体开业人员合计", "46、46、2、8、1、4、20、11", NOTE],
    ["2647", "17", "个体开业人员合计-市", "22、22、2、8、4、5、2", NOTE],
    ["2647", "18", "个体开业人员合计-县", "24、24、15、9", NOTE],
]

PATCHES = {
    "LYG-下-T083": {
        "title": "1990年连云港市卫生机构、床位、人员统计表续表",
        "table_number": "表55-1",
        "page": 2646,
        "pages": [2646],
        "part": "part02",
        "vol": "下",
        "volume": "下",
        "columns": COLUMNS,
        "rows": ROWS_083,
        "row_count": len(ROWS_083),
        "col_count": len(COLUMNS),
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0214.txt；并参考 raw 坐标OCR workbench/ocr/raw/下/part02/page_0214.json。表题、表号和复合表头承接前页 workbench/ocr/paddle_ocr/下/part02/page_0213.txt；本页为表55-1续表，按机构行保留源页可见数值序列。",
    },
    "LYG-下-T084": {
        "title": "1990年连云港市卫生机构、床位、人员统计表续表",
        "table_number": "表55-1",
        "page": 2647,
        "pages": [2647],
        "part": "part02",
        "vol": "下",
        "volume": "下",
        "columns": COLUMNS,
        "rows": ROWS_084,
        "row_count": len(ROWS_084),
        "col_count": len(COLUMNS),
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0215.txt；并参考 raw 坐标OCR workbench/ocr/raw/下/part02/page_0215.json。表题、表号和复合表头承接前页 workbench/ocr/paddle_ocr/下/part02/page_0213.txt；本页为表55-1续表，按机构行保留源页可见数值序列。",
    },
}


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


def patch_jsons() -> int:
    changed = 0
    for table_id in PATCHES:
        data_path = DATA_DIR / f"{table_id}.json"
        data = json.loads(data_path.read_text(encoding="utf-8"))
        if patch_entry(data):
            data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
    print(f"json_files_changed={patch_jsons()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
