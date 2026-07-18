# -*- coding: utf-8 -*-
"""Move verified Huaibei salt tax table to its reader location."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T104.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_huaibei_salt_tax_table_placement_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_huaibei_salt_tax_table_placement_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_淮北盐税收入统计表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TABLE_RE = re.compile(
    r"\n?<section class=\"verified-table-block\" id=\"table-LYG-中-T104\">.*?</section>\s*",
    re.S,
)

RESIDUE_RE = re.compile(
    r"\n?<p>占全国（%）</p>\s*"
    r"<p>民国3年1793\.5民国14年79510\.1民国4年11\.8民国15年70399512\.7"
    r"民国5年69311\.03496\.1民国16年民国6年4527\.0民国17年5589\.5"
    r"民国7年5608\.1民国18年82311\.3民国8年75910\.3民国19年121610\.910\.0"
    r"民国9年760民国20年117410\.5民国10年7\.8655民国21年1337民国11年6727\.6"
    r"民国22年2092民国12年5957\.5民国23年2192民国13年4846\.4民国24年1956"
    r"(?P<tail>民国28年（1939年）3月，淮北盐场被日军占领，7年中，被掠夺的准盐达3000多万担。"
    r"中国共产党发动广大盐区人民与敌伪展开争夺盐场和盐税斗争，民国29～34年，苏皖边区政府共征盐税3750万元（华中币），有力地支援了抗日战争。)</p>\s*",
    re.S,
)


def patch_reader() -> tuple[int, int]:
    text = HTML.read_text(encoding="utf-8")
    table_matches = list(TABLE_RE.finditer(text))
    if len(table_matches) != 1:
        raise RuntimeError(f"expected exactly one T104 table block, found {len(table_matches)}")
    table_block = table_matches[0].group(0).strip()

    without_old, removed = TABLE_RE.subn("\n", text, count=1)

    def repl(match: re.Match[str]) -> str:
        return "\n" + table_block + "\n<p>" + match.group("tail") + "</p>\n"

    new, replaced = RESIDUE_RE.subn(repl, without_old, count=1)
    if replaced != 1:
        raise RuntimeError(f"expected to replace one Huaibei salt tax residue, replaced {replaced}")
    HTML.write_text(new, encoding="utf-8")
    return removed, replaced


def write_reports(removed: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = json.loads(DATA.read_text(encoding="utf-8"))
    result = {
        "time": now,
        "table_id": "LYG-中-T104",
        "table_number": entry.get("table_number"),
        "title": entry.get("title"),
        "source_pages": entry.get("pages"),
        "existing_reader_table_blocks_moved": removed,
        "reader_flattened_blocks_replaced": replaced,
        "json_changed": False,
        "site_changed": False,
        "rows": entry.get("row_count"),
        "columns": entry.get("col_count"),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 淮北盐税收入统计表残文修复

- 时间：{now}
- 表ID：`LYG-中-T104`
- 表题：{entry.get('table_number')} `{entry.get('title')}`
- 源页：`workbench/table_entries/中/raw/LYG-中-T104_1708.txt`

## 修复动作

- 保持现有 verified 结构化表 `workbench/table_entries/中/data/LYG-中-T104.json` 不变。
- 从最终阅读版原“已核结构化表格”集合位置移出 `table-LYG-中-T104` 表块：{removed} 组。
- 将盐税收入段中 `占全国（%）` 和 `民国3年1793.5...民国24年1956` 的压平残文替换为同一 verified 表块：{replaced} 组。
- 将被粘在表尾的 `民国28年（1939年）3月，淮北盐场被日军占领...` 恢复为普通正文段落。

## 核对说明

- `LYG-中-T104` 已于前序任务回源核录，原表为两组“年份/全年税收数/占全国比例”并排版式，结构化为逐年三列记录。
- 本轮只调整阅读版位置并撤出压平残文，不修改表格数据或结构化表格站。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(removed: int, replaced: int) -> None:
    marker = "## 2026-07-01 淮北盐税收入统计表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的盐税收入段 `民国3年1793.5民国14年79510.1...民国24年1956` 压平残文处理。
- 确认该段已由 `workbench/table_entries/中/data/LYG-中-T104.json` 覆盖：{json.loads(DATA.read_text(encoding='utf-8')).get('table_number')}《民国3~24年准北盐税收入统计表》，22 行 3 列。
- 本轮未改表数据，仅将阅读版中已有 `table-LYG-中-T104` 表块移动到盐税收入正文位置，移除原位置 {removed} 组，并替换压平残文 {replaced} 组。
- 被粘到表尾的 `民国28年（1939年）3月...` 恢复为普通正文段落。
- 报告：`output/reports/reader_readability_huaibei_salt_tax_table_placement_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    removed, replaced = patch_reader()
    write_reports(removed, replaced)
    update_memory(removed, replaced)
    print(f"existing_reader_table_blocks_moved={removed}")
    print(f"reader_flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
