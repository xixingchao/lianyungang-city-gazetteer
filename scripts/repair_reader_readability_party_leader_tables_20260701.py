# -*- coding: utf-8 -*-
"""Remove duplicated flattened party leader table residues from the final reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_party_leader_tables_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_party_leader_tables_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第四十一卷历任领导人表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

VERIFIED_TABLES = [
    {
        "table_id": "LYG-中-T115",
        "title": "表41-8 历任特委、市（县）委书记表",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0427.txt",
    },
    {
        "table_id": "LYG-中-T116",
        "title": "表41-10 历任市委常委表",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0429.txt",
    },
    {
        "table_id": "LYG-中-T117",
        "title": "表41-10 历任市委常委表（续表）",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0430.txt",
    },
]

RESIDUE_PATTERNS = [
    {
        "name": "secretary_table_flattened_tail",
        "table_ids": ["LYG-中-T115"],
        "pattern": re.compile(
            r"\n?<p>1948\.12 ~ 1949\.10书记梁如仁1948\.12 ~ 1949\.8江苏东海云台工委书记苏羽河南沁阳1949\.11 ~ 1950\.5新海连市委山东牟平书记新海县委刁一民1950\.5 ~ 1950\.12.*?书记上海市1989\.9 ~秦兆祯</p>\s*",
            re.S,
        ),
    },
    {
        "name": "standing_committee_flattened_intro",
        "table_ids": ["LYG-中-T116", "LYG-中-T117"],
        "pattern": re.compile(
            r"\n?<p>1971\.6 ~ 1983\.2叶志俊1983\.2 ~1977\.1 ~ 1983\.2耿志英（女）</p>\s*",
            re.S,
        ),
    },
    {
        "name": "standing_committee_flattened_tail",
        "table_ids": ["LYG-中-T116", "LYG-中-T117"],
        "pattern": re.compile(
            r"\n?<p>张洪儒于同祯1971\.6 ~ 1974\. 10耿杰民1983\.9 ~ 1986\.51977\.5 ~ 1983\.2季允石雷成堂王成瑞1977\.5 ~ 1983\.21984\.7 ~ 1989\.91971\.6 ~ 1972\.12.*?王遐松1983\.2 ~ 1986\.1林永龚来宝1983\.2 ~1975\. 12 ~ 1983\.2</p>\s*",
            re.S,
        ),
    },
]


def assert_verified_blocks_present(text: str) -> None:
    missing = []
    for table in VERIFIED_TABLES:
        if f'id="table-{table["table_id"]}"' not in text:
            missing.append(table["table_id"])
    if missing:
        raise SystemExit(f"verified table blocks missing from reader: {', '.join(missing)}")


def remove_residues() -> list[dict[str, object]]:
    text = HTML.read_text(encoding="utf-8")
    assert_verified_blocks_present(text)
    removals: list[dict[str, object]] = []
    for item in RESIDUE_PATTERNS:
        new_text, count = item["pattern"].subn("\n", text)
        removals.append(
            {
                "name": item["name"],
                "table_ids": item["table_ids"],
                "removed": count,
            }
        )
        text = new_text
    if any(int(item["removed"]) for item in removals):
        HTML.write_text(text, encoding="utf-8")
    return removals


def write_reports(removals: list[dict[str, object]]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    residue_present_after = {
        "secretary_tail": "1948.12 ~ 1949.10书记梁如仁" in HTML.read_text(encoding="utf-8"),
        "standing_committee_intro": "1971.6 ~ 1983.2叶志俊1983.2 ~1977.1 ~ 1983.2耿志英" in HTML.read_text(encoding="utf-8"),
        "standing_committee_tail": "张洪儒于同祯1971.6 ~ 1974. 10耿杰民" in HTML.read_text(encoding="utf-8"),
    }
    result = {
        "time": now,
        "reader": "output/final_reader/连云港市志_全书.html",
        "verified_tables": VERIFIED_TABLES,
        "removals": removals,
        "total_removed": sum(int(item["removed"]) for item in removals),
        "residue_present_after_repair": residue_present_after,
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    table_lines = "\n".join(
        f"- `{table['table_id']}`：{table['title']}；源 OCR：`{table['source']}`。" for table in VERIFIED_TABLES
    )
    removal_lines = "\n".join(
        f"- `{item['name']}`：删除 {item['removed']} 组；覆盖表：{', '.join(item['table_ids'])}。" for item in removals
    )
    md = f"""# 第四十一卷历任领导人表残文修复

- 时间：{now}
- 阅读版：`output/final_reader/连云港市志_全书.html`

## 覆盖依据

{table_lines}

## 修复动作

{removal_lines}

## 核对说明

- 本次只撤出已经由 verified 表覆盖的线性化残文，保留阅读版后部结构化表展示。
- `市委下辖机关、企事业单位党组织沿革表（二）` 与区委、公社党委沿革表尚未确认有 verified 结构化表覆盖，本次未删除。
- 修复后目标残文检测：{json.dumps(residue_present_after, ensure_ascii=False)}。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(removals: list[dict[str, object]]) -> None:
    marker = "## 2026-07-01 第四十一卷历任领导人表残文修复"
    removed = sum(int(item["removed"]) for item in removals)
    entry = f"""
{marker}

- 针对第四十一卷第三节“历任领导人”中重复保留的表格线性化残文，确认 `LYG-中-T115`、`LYG-中-T116`、`LYG-中-T117` 已在阅读版后部以 verified 结构化表展示。
- 从 `output/final_reader/连云港市志_全书.html` 精确撤出书记表残文与市委常委表残文共 {removed} 组；不重录、不改结构化表数据。
- 暂未处理 `市委下辖机关、企事业单位党组织沿革表（二）` 及区委、公社党委沿革表残文，因为尚未确认现有 verified 表覆盖。
- 报告：`output/reports/reader_readability_party_leader_tables_20260701.md`。
"""
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in memory:
        MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    removals = remove_residues()
    write_reports(removals)
    update_memory(removals)
    print(f"reader_residue_blocks_removed={sum(int(item['removed']) for item in removals)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
