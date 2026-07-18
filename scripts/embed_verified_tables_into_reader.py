# -*- coding: utf-8 -*-
"""Embed verified structured tables back into the final reader by volume."""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
TABLE_ROOT = ROOT / "workbench" / "table_entries"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260701_全量已核结构化表格嵌回主阅读版.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

EMBED_START = "<!-- VERIFIED-STRUCTURED-TABLES-START -->"
EMBED_END = "<!-- VERIFIED-STRUCTURED-TABLES-END -->"

VOLUME_IDS = {
    1: "第一卷-自然环境",
    2: "第二卷-建置区划",
    3: "第三卷-区县概况",
    4: "第四卷-人口",
    5: "第五卷-城乡建设",
    6: "第六卷-环境保护",
    7: "第七卷-经济综情",
    8: "第八卷-经济综合管理",
    9: "第九卷-农林业",
    10: "第十卷-水利",
    11: "第十一卷-畜牧业",
    12: "第十二卷-水产",
    13: "第十三卷-盐业",
    14: "第十四卷-轻-手-工业",
    15: "第十五卷-纺织工业",
    16: "第十六卷-皮塑工业",
    17: "第十七卷-工艺美术",
    18: "第十八卷-食品工业",
    19: "第十九卷-医药",
    20: "第二十卷-化学工业",
    21: "第二十一卷-机械工业",
    22: "第二十二卷-电子工业",
    23: "第二十三卷-建材工业",
    24: "第二十四卷-建筑业",
    25: "第二十五卷-电力工业",
    26: "第二十六卷-矿产",
    27: "第二十七卷-乡镇企业",
    28: "第二十八卷-开发区",
    29: "第二十九卷-口岸",
    30: "第三十卷-交通运输",
    31: "第三十一卷-邮电",
    32: "第三十二卷-名胜旅游",
    33: "第三十三卷-商业",
    34: "第三十四卷-供销",
    35: "第三十五卷-对外经济贸易",
    36: "第三十六卷-粮油购销",
    37: "第三十七卷-物资流通",
    38: "第三十八卷-财政",
    39: "第三十九卷-税务",
    40: "第四十卷-金融",
    41: "第四十一卷-政党",
    42: "第四十二卷-政务",
    43: "第四十三卷-民政-信访",
    44: "第四十四卷-治安司法",
    45: "第四十五卷-军事",
    46: "第四十六卷-人事",
    47: "第四十七卷-劳动",
    48: "第四十八卷-外事侨务",
    49: "第四十九卷-社团",
    50: "第五十卷-教育",
    51: "第五十一卷-科技",
    52: "第五十二卷-文化",
    53: "第五十三卷-文物",
    54: "第五十四卷-报刊广播-电视",
    55: "第五十五卷-卫生",
    56: "第五十六卷-体育",
    57: "第五十七卷-宗教",
    58: "第五十八卷-民俗",
    59: "第五十九卷-方言",
    60: "第六十卷-人物",
}

PAGE_RANGES = [
    (124, 212, 1), (213, 231, 2), (232, 278, 3), (279, 300, 4),
    (301, 400, 5), (401, 459, 6), (460, 510, 7), (511, 594, 8),
    (595, 652, 10), (653, 705, 12), (706, 750, 13), (751, 810, 14),
    (811, 903, 15), (904, 924, 16), (925, 984, 17), (985, 1018, 18),
    (1019, 1046, 19), (1047, 1117, 20), (1118, 1160, 21), (1161, 1193, 22),
    (1194, 1222, 23), (1223, 1258, 24), (1259, 1315, 25), (1316, 1330, 26),
    (1331, 1355, 27), (1356, 1372, 28), (1373, 1455, 30), (1456, 1510, 31),
    (1511, 1530, 32), (1531, 1603, 33), (1604, 1629, 35), (1630, 1697, 36),
    (1698, 1718, 37), (1719, 1755, 38), (1756, 1797, 39), (1798, 1849, 40),
    (1850, 1888, 41), (1889, 1988, 42), (1989, 2047, 43), (2048, 2140, 44),
    (2141, 2185, 45), (2186, 2215, 46), (2216, 2265, 47), (2266, 2290, 48),
    (2291, 2336, 49), (2337, 2386, 50), (2387, 2430, 51), (2431, 2495, 52),
    (2496, 2550, 53), (2551, 2590, 54), (2591, 2655, 55), (2656, 2690, 56),
    (2691, 2720, 57), (2721, 2740, 58), (2741, 2820, 59), (2821, 2860, 60),
]


def chinese_volume_from_table_number(table_number: str) -> int | None:
    match = re.search(r"表\s*(\d+)", table_number or "")
    if not match:
        return None
    major = int(match.group(1))
    return major if major in VOLUME_IDS else None


def volume_from_page(page: int) -> int | None:
    for start, end, volume in PAGE_RANGES:
        if start <= page <= end:
            return volume
    return None


def table_sort_key(table: dict) -> tuple[int, str]:
    pages = table.get("pages") or []
    page = int(table.get("page") or (pages[0] if pages else 999999))
    return page, str(table.get("table_id", ""))


def load_tables() -> list[dict]:
    tables: list[dict] = []
    for path in sorted(TABLE_ROOT.glob("*/*/*.json")):
        table = json.loads(path.read_text(encoding="utf-8"))
        if table.get("status") != "verified":
            continue
        rows = table.get("rows") or []
        if not rows:
            continue
        tables.append(table)
    return tables


def make_table_html(table: dict) -> str:
    title = str(table.get("title") or "").strip()
    number = str(table.get("table_number") or "").strip()
    caption = f"{number} {title}".strip()
    table_id = html.escape(str(table.get("table_id") or ""))
    pages = "、".join(str(p) for p in (table.get("pages") or []))
    headers = table.get("columns") or []
    rows = table.get("rows") or []
    ths = "".join(f"<th>{html.escape(str(col))}</th>" for col in headers)
    body_rows = []
    for row in rows:
        body_rows.append("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>")
    meta = f'<div class="structured-table-meta">表ID：{table_id}；源页：{html.escape(pages)}</div>'
    return (
        f'<section class="verified-table-block" id="table-{table_id}">'
        f'{meta}'
        f'<table class="structured-table"><caption>{html.escape(caption)}</caption>'
        f'<thead><tr>{ths}</tr></thead><tbody>{"".join(body_rows)}</tbody></table>'
        f'</section>'
    )


def make_volume_block(volume_id: str, tables: list[dict]) -> str:
    rendered = "\n".join(make_table_html(table) for table in sorted(tables, key=table_sort_key))
    return (
        f"\n{EMBED_START}\n"
        f'<section class="verified-structured-tables" id="{volume_id}-已核结构化表格">\n'
        f"<h3>已核结构化表格</h3>\n"
        f'<p class="structured-table-note">本节汇集已回源核录的结构化表格，表内数据可追溯到随表记录的源页。</p>\n'
        f"{rendered}\n"
        f"</section>\n"
        f"{EMBED_END}\n"
    )


def remove_existing_embeds(text: str) -> str:
    return re.sub(rf"\n?{re.escape(EMBED_START)}.*?{re.escape(EMBED_END)}\n?", "\n", text, flags=re.S)


def group_tables(tables: list[dict]) -> tuple[dict[str, list[dict]], list[str]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    unplaced: list[str] = []
    for table in tables:
        pages = table.get("pages") or []
        page = int(table.get("page") or (pages[0] if pages else 0))
        volume = chinese_volume_from_table_number(str(table.get("table_number") or "")) or volume_from_page(page)
        if volume is None:
            unplaced.append(str(table.get("table_id")))
            continue
        grouped[VOLUME_IDS[volume]].append(table)
    return grouped, unplaced


def embed() -> tuple[int, list[str]]:
    tables = load_tables()
    grouped, unplaced = group_tables(tables)
    text = remove_existing_embeds(HTML_PATH.read_text(encoding="utf-8"))
    headings = list(re.finditer(r'<h2 id="([^"]+)">[^<]+</h2>', text))
    output = []
    last = 0
    embedded_count = 0
    for idx, heading in enumerate(headings):
        volume_id = heading.group(1)
        end = headings[idx + 1].start() if idx + 1 < len(headings) else len(text)
        output.append(text[last:end])
        if volume_id in grouped:
            output.append(make_volume_block(volume_id, grouped[volume_id]))
            embedded_count += len(grouped[volume_id])
        last = end
    output.append(text[last:])
    HTML_PATH.write_text("".join(output), encoding="utf-8")
    return embedded_count, unplaced


def write_progress(embedded_count: int, unplaced: list[str]) -> None:
    content = f"""# 全量已核结构化表格嵌回主阅读版

- 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
- 脚本：`scripts/embed_verified_tables_into_reader.py`
- 主阅读版：`output/final_reader/连云港市志_全书.html`

## 完成动作

- 将结构化表格站中 `verified` 状态且有数据行的表格按卷归组嵌回主阅读版。
- 嵌回位置为各 H2 卷章末尾的 `已核结构化表格` 小节。
- 本轮嵌回表格：{embedded_count} 张。
- 未能自动归组表格：{', '.join(unplaced) if unplaced else '无'}。

## 结构化口径

- 表格使用 `class="structured-table"`，与交付质量门禁的表内长数字排除规则一致。
- 每张表保留表ID和源页信息，表格内部 notes 不暴露到主阅读版。
- 脚本以 `VERIFIED-STRUCTURED-TABLES-START/END` 标记块实现幂等复跑。

## 验收

- 后续复跑 `audit_delivery_quality.py`、`audit_full_reader.py`、`audit_table_delivery_readiness.py` 和交付包构建脚本确认无回退。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(embedded_count: int, unplaced: list[str]) -> None:
    entry = f"""
## 2026-07-01 全量已核结构化表格嵌回主阅读版

- 新增脚本：`scripts/embed_verified_tables_into_reader.py`。
- 将结构化表格站中 `verified` 状态且有数据行的表格按卷归组嵌回 `output/final_reader/连云港市志_全书.html`，每卷末尾生成 `已核结构化表格` 小节。
- 本轮嵌回表格 {embedded_count} 张；未能自动归组表格：{', '.join(unplaced) if unplaced else '无'}。
- 嵌回表格使用 `class="structured-table"`，保留表ID和源页，不暴露内部 notes；脚本以 `VERIFIED-STRUCTURED-TABLES-START/END` 标记块保持幂等。
- 进度报告：`output/reports/progress/20260701_全量已核结构化表格嵌回主阅读版.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-07-01 全量已核结构化表格嵌回主阅读版"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    embedded_count, unplaced = embed()
    write_progress(embedded_count, unplaced)
    update_memory(embedded_count, unplaced)
    print(f"embedded={embedded_count}")
    print(f"unplaced={len(unplaced)}")
    if unplaced:
        print("unplaced_ids=" + ",".join(unplaced))
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
