# -*- coding: utf-8 -*-
"""Repair sixth source-verified batch in Volume 25 power industry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_power_batch6_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_power_batch6_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十五卷电力工业断裂句及高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十五卷-电力工业">第二十五卷电力工业</h2>'
SCOPE_END = '<h2 id="第二十六卷-矿产">第二十六卷矿产</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0332.txt; page_0333.txt; page_0335.txt; page_0337.txt; page_0338.txt; page_0348.txt; page_0364.txt"

REPLACEMENTS = [
    ("新东公司资本", "筹股7.4方元（银元）", "筹股7.4万元（银元）"),
    ("新东公司发电机", "<p>年均收入2.88万元。民国25年（1936年）", "<p>新东公司装有1台76千瓦交流220伏的蒸汽机发电机组，电力用户不足200户，公司年均收入2.88万元。民国25年（1936年）"),
    ("电灯厂", "电灯广又改为华北电业股份有限公司", "电灯厂又改为华北电业股份有限公司"),
    ("海州发电所漏句", "另外在东海所），占地面积4.76万平方米。", "另外在东海县申北乡（即海州北门外现新海发电厂址）设立海州发电所和东海营业所（隶属海州出张所），占地面积4.76万平方米。"),
    ("第一期工程漏句", "<p>（后编为2号机和3号炉）", "<p>民国29年（1940年）10月，日军在海州发电所着手建新电厂。第一期工程为1台德国A.E.G公司生产的容量510千瓦、电压2300伏的汽轮发电机组和1台5.1吨/时锅炉（后编为2号机和3号炉）"),
    ("元旦", "民国38年（1949年）元且", "民国38年（1949年）元旦"),
    ("韩庄电厂", "调迁韩庄电厂广，1959年3月", "调迁韩庄电厂，1959年3月"),
    ("检修组织断词", "工作。-1957年，成立检修分场", "工作。1957年，成立检修分场"),
    ("安全隐患", "事故隐惠为主", "事故隐患为主"),
    ("茅赣线断裂", "因35千伏新（浦）赣（榆）线卡脖子，1977年行，至当年12月11日恢复为110千伏运行。海赣线起于新海发电厂110千伏升压站，止基，铁塔7基，11个耐张段。", "因35千伏新（浦）赣（榆）线卡脖子，1977年4月20日将海赣线与35千伏新赣线在富安村北的交叉处连接，海赣线降压为35千伏运行，至当年12月11日恢复为110千伏运行。海赣线起于新海发电厂110千伏升压站，止于110千伏赣榆变电所，全长28.98公里。全线共有121基杆塔，其中钢筋混凝土杆114基，铁塔7基，11个耐张段。"),
    ("茅赣线供电断裂", "赣榆变电所改由茅口变电所供长21.14公里。", "赣榆变电所改由茅口变电所供电，将原海赣40号杆处断开与新架的茅口至此的线路接通，组成110千伏茅赣线，线路全长21.14公里。"),
    ("厂内", "广内设置无事故奖金", "厂内设置无事故奖金"),
    ("并开展", "并并展季节性安全大检查", "并开展季节性安全大检查"),
]

SKIPPED = [
    "`双千瓦机组...` 段源 OCR 仍有不确定处，本批暂不固化修订，待页图/更强证据专项处理。",
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
    residuals = [old for _label, old, new in REPLACEMENTS if old in segment and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第二十五卷电力工业",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "counts": counts,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 可直接支持的断裂句与短错识；证据不足的电气系统残句暂留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第二十五卷电力工业断裂句及高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：补回新东公司设备、海州发电所、茅赣线等断裂句，修正 `电灯广/元且/隐惠/广内/并并展` 等错识。",
        "- 保留：`双千瓦机组...` 电气系统残句待更强证据专项处理。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第二十五卷电力工业断裂句及高置信错识回源修复

- 继续对第二十五卷电力工业做小批回源修复，范围限定在 `第二十五卷-电力工业` 到 `第二十六卷-矿产` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：补回新东公司 `1台76千瓦交流220伏的蒸汽机发电机组` 句、海州发电所设立句、茅赣线降压/恢复/线路长度句；修正 `电灯广/元且/隐惠/广内/并并展` 等错识。
- `双千瓦机组...` 电气系统残句因源 OCR 仍有疑点，本批暂留，后续用页图或更强证据处理。
- 报告：`output/reports/reader_readability_power_batch6_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第二十五卷电力工业断裂句及高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
