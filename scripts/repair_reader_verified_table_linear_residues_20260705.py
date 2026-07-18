# -*- coding: utf-8 -*-
"""Remove verified table linear residues from the current full reader.

These ranges are already represented in structured tables or prior residue
reports; the reader should keep surrounding prose only.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_verified_table_linear_residues_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_verified_table_linear_residues_20260705.md"

RANGES = [
    {
        "name": "涉外保险两表线性残留",
        "start": "<p>1974~1990年中国人民保险公司连云港分公司涉外保险业务统计表</p>",
        "end": "<p>一、供应范围连云港对外供应机构成立于1963年3月·4日",
        "evidence": [
            "output/reports/multi_volume_table_residue_batch_removed.md",
            "workbench/table_entries/中/data/LYG-中-T052.json",
        ],
    },
    {
        "name": "市区水产品零售量表线性残留",
        "start": "<p>1949~1990年部分年份连云港市区水产品（咸、淡）零售量统计表</p>",
        "end": "<p>民国38年（1949年）市区有饮食服务网点473个",
        "evidence": ["output/reports/remaining_reader_residue_removed.md"],
    },
    {
        "name": "粮油征购与合同定购统计表线性残留",
        "start": "<p>1953~1984年连云港市粮油征购入库统计表</p>",
        "end": "<p>销售历史上，粮食通过市场调剂余缺",
        "evidence": [
            "output/reports/volume36_grain_table_residue_removed.md",
            "workbench/table_entries/中/data/LYG-中-T095.json",
        ],
    },
    {
        "name": "工资分实物折价表压扁残留",
        "start": "<p>新海连市工资分与实物折价对照计算表（民国38年7月8日制）</p>",
        "end": "<p>由于各地区的称谓不同，有的称工资分",
        "evidence": [
            "workbench/table_entries/下/data/LYG-下-T037.json",
            "output/reports/progress/20260630_工资分实物折价对照表回源核录出队.md",
        ],
    },
    {
        "name": "硫酸盐酸磷酸产量表残余表头",
        "start": "<p>年份硫酸(100%)盐酸（100%）</p>",
        "end": "<p>二、碱主要利用海盐资源进行生产。",
        "evidence": [
            "output/reports/multi_volume_table_residue_batch2_removed.md",
            "output/reports/acid_output_full_table_20260705.md",
        ],
    },
    {
        "name": "机械工业主要企业表残余表头",
        "start": "<p>主要产品年份(人)（万元）</p>\n<p>（万元）</p>",
        "end": "<p>（万元）</p>",
        "include_end": True,
        "evidence": ["output/reports/remaining_reader_residue_removed.md"],
    },
    {
        "name": "农业税征收统计表残余表头",
        "start": "<p>实际征收（正税）</p>",
        "end": "<p>2.1951年开始查田定产海州区每亩49.5公斤",
        "evidence": ["output/reports/remaining_reader_residue_removed.md"],
    },
    {
        "name": "外贸运输仓储表残余单位行",
        "start": "<p>1974~1988年，共熏蒸各类进出口物资计178万吨，累计创利润150万元，经熏蒸的船舶达50艘。</p>",
        "end": "<h4 id=\"第二十九卷-第二章港口运输-第六节货运代理\">第六节货运代理</h4>",
        "keep_start": True,
        "keep_end": True,
        "evidence": ["短单位行夹在外贸仓储正文中，前后为连续叙述段；仅撤出单位残行"],
    },
]


def remove_range(html: str, item: dict) -> tuple[str, dict]:
    start = html.find(item["start"])
    if start < 0:
        return html, {
            "name": item["name"],
            "removed_chars": 0,
            "removed_excerpt": "already absent",
            "evidence": item["evidence"],
        }
    end = html.find(item["end"], start)
    if end < 0:
        raise RuntimeError(f"end anchor not found: {item['name']}")
    if item.get("keep_start"):
        start += len(item["start"])
    if item.get("include_end"):
        end += len(item["end"])
    if item.get("keep_end"):
        pass
    removed = html[start:end]
    if "VERIFIED-STRUCTURED-TABLES-START" in removed or "VERIFIED-STRUCTURED-TABLES-END" in removed:
        raise RuntimeError(f"refusing to remove structured table block: {item['name']}")
    return html[:start] + html[end:], {
        "name": item["name"],
        "removed_chars": len(removed),
        "removed_excerpt": " ".join(removed.replace("\n", " ").split())[:240],
        "evidence": item["evidence"],
    }


def main() -> None:
    html = READER.read_text(encoding="utf-8")
    removals = []
    for item in RANGES:
        html, removal = remove_range(html, item)
        removals.append(removal)
    tmp = READER.with_name(READER.name + ".tmp")
    tmp.write_text(html, encoding="utf-8")
    os.replace(tmp, READER)

    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(READER.relative_to(ROOT)).replace("\\", "/"),
        "removals": removals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 已核表格线性残留清理",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 文件：`{READER.relative_to(ROOT).as_posix()}`",
        "",
        "## 清理项",
        "",
        "| 项目 | 删除字符数 | 依据 | 摘录 |",
        "|---|---:|---|---|",
    ]
    for item in removals:
        evidence = "<br>".join(f"`{path}`" for path in item["evidence"])
        excerpt = item["removed_excerpt"].replace("|", "\\|")
        lines.append(f"| {item['name']} | {item['removed_chars']} | {evidence} | {excerpt} |")
    lines.extend([
        "",
        "## 说明",
        "",
        "本轮仅撤出主阅读页中已由结构化表或旧清理报告覆盖的线性表格残留，不重建表格、不改周边正文。",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"removed={len(removals)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
