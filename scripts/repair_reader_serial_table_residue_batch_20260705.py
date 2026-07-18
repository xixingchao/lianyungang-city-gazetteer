# -*- coding: utf-8 -*-
"""Remove a small batch of source-confirmed serialized table residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_serial_table_residue_batch_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_serial_table_residue_batch_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_阅读版表格串行残片小批清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

WATER_FULL = """<p>（米）</p>
<p>（公里）</p>
<p>（米）</p>
<p>（米）</p>
<p>（米）</p>

<p>（个）</p>
<p>（米）</p>
<p>（米）</p>
<p>（米）</p>
<p>（米）</p>
<p>（米）</p>
<p>（米）</p>
<p>（米）</p>
<p>（米）</p>



<p>（83 公里）</p>
<p>（92 公里）</p>
<p>（109公里）</p>
<p>（113 公里）</p>
<p>（127 公里）</p>
<p>项目6000流量水位线8.307.937.26.656.135.65堤顶高程（米）</p>

<p>8.08.08.08.08.08.0后战以上堤坡1：31：31：31：31：31：3后战顶高程（米）</p>
<p>8.37.937.26.65后战顶宽（米）</p>
<p>8.08.08.08.0战顶以下边坡1：51：51：51：51：51：5</p>
"""

WATER_TAIL = """<p>（83 公里）</p>
<p>（92 公里）</p>
<p>（109公里）</p>
<p>（113 公里）</p>
<p>（127 公里）</p>
<p>项目6000流量水位线8.307.937.26.656.135.65堤顶高程（米）</p>

<p>8.08.08.08.08.08.0后战以上堤坡1：31：31：31：31：31：3后战顶高程（米）</p>
<p>8.37.937.26.65后战顶宽（米）</p>
<p>8.08.08.08.0战顶以下边坡1：51：51：51：51：51：5</p>
"""

BUILDING_TAIL = """<p>2525混合市海监局A型住宅楼连云区院前建筑公司1990市海监局B型住宅楼混合1663连云区院前建筑公司1990框架市第一建筑工程公司18781990海州邮电楼市房屋修公司二号楼混合19901800云台区二建公司3300混合市车辆厂住宅楼海州区建安装璜公司1990混合赣榆县一建二处（欢墩）</p>
<p>19902093市计生委办公楼1700框架1990赣榆县一建四处（金山）</p>
<p>赣榆县中国人民银行营业楼混合赣榆县一建五处(沙河)1990市人大微机楼1700框架19904062市海监局办公楼赣榆县一建三处（大岭）</p>
<p>混合赣榆县青口镇建筑公司19901267赣榆县福利院综合楼混合东海县酿造综合楼19901017东海县二建二处</p>
"""

RAIL_TABLE = """<p>1957平行于1+9299451 ~ 21957连云港港务局（卸3)卸0+2967151957连云港港务局（卸4)1 ~ 2连云港港务局（卸5)221平行于2+1701957281连云港港务局码头（1道）</p>
<p>1957连云港站102号岔连云港港务局二码头（4道）</p>
<p>连云港站116号岔6081957.11连云港港务局二码头（5道）</p>
<p>6481 ~ 2连云港站122号岔1957.11连云港港务局二码头（6道）</p>
<p>393连云港站120号岔1957.11磷矿专用线37 + 771111701958.2平行于0+450连云港渔业线15道2251959新海电厂一道磷厂1+817.13371963.8新海电厂二道磷矿 1 +735.14991963.3302军用线磷矿6+0161901963.4磷矿0+9494261963.8煤建公司专用线23 + 815.5盐坨盐场专用线9451963. 12磷矿9+9895647102油库线2~61971平行于7+413.5外贸墟沟冷库线6201977.5连云港港务局一码头（2道）</p>
<p>连云港站102号岔2831979.81979.8连云港港务局一码头（3道）</p>
<p>连云港站108号岔6281 ~ 2连云港港务局一码头（4道）</p>
<p>619连云港站106号岔1979.8连云港站112号岔连云港港务局二码头（1道）</p>
<p>5291~ 21979.8连云港站110号岔585连云港港务局二码头（2道）</p>
<p>1979.8连云港站118号岔连云港港务局二码头（3道）</p>
<p>6161 ~ 21979.8外贸连云港市包装公司66032 + 096.61 ~ 21979平行于7+630外贸墟沟冷库线8531979陶庵专用线6 + 3764541~ 31983轻工业库专用线31 + 02616021984.11商业库专用线30 + 1371 ~ 225321984.11商业库0+460省库专用线18581984.1124 + 013物资库专用线31331984.11铁二局盐坨材料线124 + 7843211984.12</p>
"""

TRIAL_UNITS = """<p>(件)(件)(件)（件）</p>



<p>（件）</p>
<p>（件)（件）</p>
<p>(件)(件)（件）</p>
"""

ITEMS = [
    {
        "key": "volume10_xinshu_river_table_tail",
        "desc": "第十卷新沭河治理前表格单位/参数串行残片",
        "source": "workbench/body_chapters/连云港市志_上册_PaddleOCR正文汇总.md:32001-32026",
        "candidates": [WATER_FULL, WATER_TAIL],
    },
    {
        "key": "volume24_building_list_tail",
        "desc": "第二十四卷主要建筑一览表尾部串行残片",
        "source": "workbench/table_entries/中/data/LYG-中-T133.json; workbench/ocr/paddle_ocr/中/part01/page_0308.txt",
        "candidates": [BUILDING_TAIL],
    },
    {
        "key": "volume30_private_railway_table",
        "desc": "第三十卷非路产专用线宽表串行残片",
        "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:60546-60598",
        "candidates": [RAIL_TABLE],
    },
    {
        "key": "volume44_trial_table_units",
        "desc": "第四十四卷审判统计表单位/表头残片",
        "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:157149-157156",
        "candidates": [TRIAL_UNITS],
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for item in ITEMS:
        present = [(candidate, html.count(candidate)) for candidate in item["candidates"] if html.count(candidate)]
        if len(present) == 1 and present[0][1] == 1:
            html = html.replace(present[0][0], "", 1)
            status = "changed"
            changed = 1
        elif not present:
            status = "already_absent"
            changed = 0
        else:
            raise RuntimeError(f"expected unique residue block for {item['key']}, got {[count for _, count in present]}")
        changes.append({k: item[k] for k in ("key", "desc", "source")} | {"status": status, "changed": changed})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    changed_total = sum(item["changed"] for item in changes)
    lines = [
        "# 阅读版表格串行残片小批清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：撤出 4 组经源文确认的表格串行残片；只清理不可读残文，不改周边正文和结构化表数据。",
        f"- 状态：本次变更 {changed_total} 组；脚本可重复运行。",
        "",
        "## 明细",
        "",
    ]
    for item in changes:
        lines.append(f"- `{item['key']}`：{item['status']}；{item['desc']}；源证据 `{item['source']}`。")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-05 阅读版表格串行残片小批清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_serial_table_residue_batch_20260705.py`，从最终阅读版撤出 4 组源文证实为表格区的串行残片：第十卷新沭河治理前参数残段、第二十四卷主要建筑一览表尾段、第三十卷非路产专用线宽表残段、第四十四卷审判统计表单位/表头残段。
- 本批只清理读者不可读残文，不改周边正文，不补猜宽表数据；已有结构化表数据保持不变。
- 报告：`output/reports/reader_serial_table_residue_batch_20260705.md`。
""",
    )

    print("reader_serial_table_residue_batch_repaired")
    print(f"changed={changed_total}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
