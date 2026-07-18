# -*- coding: utf-8 -*-
"""Extract a candidate structure for LYG-上-T004 from PaddleOCR geometry.

This script builds a reviewable candidate, not a final verified table. The table
uses vertical merged cells in the source image, so station/disaster labels are
carried forward by geometry and must still be source-checked.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OCR_DIR = ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01"
OUT_CSV = ROOT / "output" / "reports" / "t004_candidate_from_ocr.csv"
OUT_JSON = ROOT / "output" / "reports" / "t004_candidate_from_ocr.json"
OUT_MD = ROOT / "output" / "reports" / "t004_candidate_from_ocr.md"

PAGES = [175, 176, 177]
COLUMNS = [
    "站名",
    "年份",
    "灾害性质",
    "1月",
    "2月",
    "3月",
    "4月",
    "5月",
    "6月",
    "7月",
    "8月",
    "9月",
    "10月",
    "11月",
    "12月",
    "年雨量",
    "最大日雨量",
    "最大日雨量发生日期",
    "高水位",
    "高水位发生日期",
    "源扫描页",
]

# Column centers observed from page_0175/page_0176/page_0177 geometry.
CENTERS = {
    "站名": 304,
    "年份": 374,
    "灾害性质": 449,
    "1月": 521,
    "2月": 593,
    "3月": 666,
    "4月": 738,
    "5月": 811,
    "6月": 884,
    "7月": 956,
    "8月": 1028,
    "9月": 1100,
    "10月": 1173,
    "11月": 1246,
    "12月": 1319,
    "年雨量": 1394,
    "最大日雨量": 1475,
    "最大日雨量发生日期": 1554,
    "高水位": 1634,
    "高水位发生日期": 1726,
}

SKIP_TOKENS = {
    "续上表", "站", "年", "名", "份", "灾害", "性质", "降", "雨", "量", "最大", "发生", "年量",
    "年雨量", "日期", "日雨量", "高水位", "(月·日)", "（月·日）", "1", "2", "3", "4", "5", "6",
    "7", "8", "9", "10", "11", "12", "第五章", "水系", "水文", "连云港市志·自然环境", "•", "148", "149", "147",
}
YEAR_RE = re.compile(r"^(19\d{2})$")


def center(box: list[list[int]]) -> tuple[float, float]:
    xs = [point[0] for point in box]
    ys = [point[1] for point in box]
    return sum(xs) / 4, sum(ys) / 4


def nearest_col(x: float) -> str | None:
    col, dist = min(((col, abs(x - center_x)) for col, center_x in CENTERS.items()), key=lambda item: item[1])
    return col if dist <= 38 else None


def group_rows(items: list[tuple[float, float, str]]) -> list[tuple[float, list[tuple[float, str]]]]:
    items.sort(key=lambda item: (item[0], item[1]))
    groups: list[list] = []
    for y, x, text in items:
        if not groups or abs(groups[-1][0] - y) > 18:
            groups.append([y, [(x, text)]])
        else:
            groups[-1][1].append((x, text))
            groups[-1][0] = (groups[-1][0] + y) / 2
    return [(group[0], sorted(group[1])) for group in groups]


def normalize_cell(value: str) -> str:
    value = value.strip()
    value = value.replace("75 :4", "75.4")
    value = value.replace("25. 14", "25.14")
    return value


def extract() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current_station = ""
    current_disaster = ""
    pending_station_parts: list[str] = []
    pending_disaster = ""

    for page in PAGES:
        data = json.loads((OCR_DIR / f"page_{page:04d}.json").read_text(encoding="utf-8"))
        items = []
        for line in data["lines"]:
            text = str(line["text"]).strip()
            if not text:
                continue
            x, y = center(line["box"])
            items.append((y, x, text))

        for _y, cells in group_rows(items):
            by_col: dict[str, list[str]] = {}
            for x, text in cells:
                text = normalize_cell(text)
                if text in SKIP_TOKENS:
                    continue
                col = nearest_col(x)
                if not col:
                    continue
                by_col.setdefault(col, []).append(text)

            station_text = "".join(by_col.pop("站名", []))
            if station_text and not YEAR_RE.match(station_text):
                pending_station_parts.append(station_text)

            disaster_text = "".join(by_col.pop("灾害性质", []))
            if disaster_text in {"旱", "洪", "涝", "洪涝"}:
                pending_disaster += disaster_text
                if pending_disaster == "洪涝":
                    current_disaster = pending_disaster
                    pending_disaster = ""
                elif disaster_text == "旱":
                    current_disaster = "旱"
                    pending_disaster = ""
            elif disaster_text:
                pending_disaster += disaster_text

            year_values = by_col.get("年份", [])
            year = next((v for v in year_values if YEAR_RE.match(v)), "")
            if not year:
                continue

            if pending_station_parts:
                current_station = "".join(pending_station_parts)
                pending_station_parts = []

            row = {col: "" for col in COLUMNS}
            row["站名"] = current_station
            row["年份"] = year
            row["灾害性质"] = current_disaster
            row["源扫描页"] = str(page)
            for col in COLUMNS:
                if col in {"站名", "年份", "灾害性质", "源扫描页"}:
                    continue
                values = [v for v in by_col.get(col, []) if v not in SKIP_TOKENS]
                if values:
                    row[col] = " ".join(values)
            rows.append(row)
    return rows


def main() -> None:
    rows = extract()
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    OUT_JSON.write_text(json.dumps({"table_id": "LYG-上-T004", "columns": COLUMNS, "rows": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    missing_station = sum(1 for row in rows if not row["站名"])
    missing_disaster = sum(1 for row in rows if not row["灾害性质"])
    lines = [
        "# LYG-上-T004 OCR几何抽取候选",
        "",
        "## 说明",
        "",
        "- 本文件是候选抽取结果，不等同于已核表。",
        "- 站名和灾害性质来自源表竖排合并单元格，已按几何位置向下继承，但必须人工回源复核。",
        "",
        "## 统计",
        "",
        f"- 候选数据行：{len(rows)}",
        f"- 缺站名行：{missing_station}",
        f"- 缺灾害性质行：{missing_disaster}",
        f"- CSV：`{OUT_CSV.relative_to(ROOT)}`",
        f"- JSON：`{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## 前20行预览",
        "",
        "| 站名 | 年份 | 灾害性质 | 年雨量 | 最大日雨量 | 最大日雨量发生日期 | 高水位 | 高水位发生日期 | 源扫描页 |",
        "|---|---:|---|---:|---:|---|---:|---|---:|",
    ]
    for row in rows[:20]:
        lines.append(
            f"| {row['站名']} | {row['年份']} | {row['灾害性质']} | {row['年雨量']} | {row['最大日雨量']} | {row['最大日雨量发生日期']} | {row['高水位']} | {row['高水位发生日期']} | {row['源扫描页']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"rows={len(rows)}")
    print(f"missing_station={missing_station}")
    print(f"missing_disaster={missing_disaster}")
    print(f"csv={OUT_CSV}")
    print(f"report={OUT_MD}")


if __name__ == "__main__":
    main()
