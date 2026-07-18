# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in Volume 18 food industry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_food_industry_batch_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_food_industry_batch_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第十八卷食品工业高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第十八卷-食品工业">第十八卷食品工业</h2>'
SCOPE_END = '<h2 id="第十九卷-医药">第十九卷医药</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0062.txt:25-34; page_0064.txt:13; page_0067.txt:6-8; page_0068.txt:4-7; page_0070.txt:14; page_0071.txt:4-29; page_0073.txt:29-37; page_0074.txt:6; page_0076.txt:11,39; page_0077.txt:20-22; page_0080.txt:19-24; page_0082.txt:66; page_0083.txt:29-31; page_0085.txt:17-19; page_0087.txt:26-27"
REPLACEMENTS = [
    ("冷冻加工厂", "水产品冷冻加工广", "水产品冷冻加工厂"),
    ("食品业门类缺漏", "豆制品加工业1品业拥有职工1.8万人", "豆制品加工业1个，乳制品加工业3个，水产品加工业7个，糖加工业1个，蔬菜冷冻加工业1个。全市食品业拥有职工1.8万人"),
    ("全民职工万人", "全民企业职工1.25方人", "全民企业职工1.25万人"),
    ("糕点产值", "完成产值39.3方元", "完成产值39.3万元"),
    ("襄河乳品厂面积", "占地面积2方平方米", "占地面积2万平方米"),
    ("东海食品厂产值", "产值103方元", "产值103万元"),
    ("畜禽加工建筑面积", "建筑面积10.7方平方米", "建筑面积10.7万平方米"),
    ("猪肉技改投资", "投资40多方元", "投资40多万元"),
    ("白条肉万吨", "加工白条肉1.74方吨", "加工白条肉1.74万吨"),
    ("灌云食品产值", "产值807方元", "产值807万元"),
    ("猪头吊烫机投入", "猪头吊烫机投人使用", "猪头吊烫机投入使用"),
    ("肉联厂建筑面积", "建筑面积3.46方平方米", "建筑面积3.46万平方米"),
    ("年宰量", "年宰量36方头生猪", "年宰量36万头生猪"),
    ("开发区肉联厂", "开发区肉联广有5000吨", "开发区肉联厂有5000吨"),
    ("肉联产值", "当年产值5222方元", "当年产值5222万元"),
    ("罐头建筑面积", "建筑面积5.05方平方米", "建筑面积5.05万平方米"),
    ("肉罐头产值", "实现产值2050.9方元", "实现产值2050.9万元"),
    ("罐头能力", "年产能力为1.5方吨", "年产能力为1.5万吨"),
    ("果酒投入", "果酒投人批量生产", "果酒投入批量生产"),
    ("酿酒投入原料", "多投人原料400公斤", "多投入原料400公斤"),
    ("洪门酒厂", "洪门酒广由4锅", "洪门酒厂由4锅"),
    ("白酒能力", "白酒生产能力3.5方吨", "白酒生产能力3.5万吨"),
    ("啤酒投资", "投资295方元新建", "投资295万元新建"),
    ("啤酒能力", "年产能力增到1.5方吨", "年产能力增到1.5万吨"),
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    original = text[start:end]
    segment = original
    counts: dict[str, int] = {}
    for label, old, new in REPLACEMENTS:
        count = segment.count(old)
        if count:
            segment = segment.replace(old, new)
        elif new not in segment:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    if segment != original:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [new for _label, _old, new in REPLACEMENTS if new not in segment]
    residuals = [old for _label, old, _new in REPLACEMENTS if old in segment]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(counts.values())
    payload = {
        "time": now,
        "scope": "第十八卷食品工业",
        "source": SOURCE,
        "reader_path": str(HTML),
        "total_replacements": total,
        "counts": counts,
        "principle": "仅修复页级 OCR 清楚给出正确写法的第十八卷错识；未核定疑点保留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第十八卷食品工业高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本次替换：{total} 处",
        "- 重点：补回总述中乳制品、水产品、糖、蔬菜冷冻加工业等缺漏项；修正多处 `方/万`、`广/厂`、`投人/投入`。",
        "- 保留：源 OCR 未能直接确认的其它疑点不凭猜测修。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-03 第十八卷食品工业高置信错识回源修复

- 对第十八卷食品工业进行小批回源修复，范围限定在 `第十八卷-食品工业` 到 `第十九卷-医药` 前。
- 源文依据：`{SOURCE}`。
- 修复重点：补回总述中 `乳制品加工业3个，水产品加工业7个，糖加工业1个，蔬菜冷冻加工业1个` 等缺漏；修正 `方元/方吨/方平方米/方头`、`投人`、`广` 等错识。
- 本次替换 {total} 处；未能在页级 OCR 中直接确认的候选保留。
- 报告：`output/reports/reader_readability_food_industry_batch_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第十八卷食品工业高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"total_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
