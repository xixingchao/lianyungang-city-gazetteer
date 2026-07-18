# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in Volume 20 chemical industry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_chemical_batch_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_chemical_batch_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十卷化学工业高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十卷-化学工业">第二十卷化学工业</h2>'
SCOPE_END = '<h2 id="第二十一卷-机械工业">第二十一卷机械工业</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0141.txt:18-27; page_0142.txt:17-34; page_0144.txt:30-31; page_0148.txt:24; page_0151.txt:4-7; page_0153.txt:5,34-40; page_0154.txt:4-7,34-36; page_0161.txt:33-41; page_0162.txt:1-15; page_0164.txt:9-15; page_0165.txt:10-33; page_0166.txt:23-26; page_0167.txt:22-39; page_0168.txt:4-33; page_0170.txt:1-40; page_0171.txt:1-40; page_0172.txt:1-5; page_0177.txt:3-38; page_0178.txt:1; page_0179.txt:31-40; page_0181.txt:34-35; page_0182.txt:17-19; page_0188.txt:19-20"
REPLACEMENTS = [
    ("党费单位", "5方元党费", "5万元党费"),
    ("小氮肥厂", "小氮肥广", "小氮肥厂"),
    ("进入全面发展", "进人全面发展的新时期", "进入全面发展的新时期"),
    ("氯化苄", "氯化苹等9个产品", "氯化苄等9个产品"),
    ("淮北盐场", "准北盐场", "淮北盐场"),
    ("溴素产能", "漠素年生产能力达到10吨", "溴素年生产能力达到10吨"),
    ("磷酸厂家缺句", "1990年全市磷酸年生产能力达到2.5万吨，实产1.41万吨。主要生产厂家有锦屏化业质量评比会上被评为省内同行业第一名，1982年获省优质产品称号，1987年获国家化学工业部优质产品称号。", "1990年全市磷酸年生产能力达到2.5万吨，实产1.41万吨。主要生产厂家有锦屏化工厂、红旗化工厂等，其中锦屏化工厂生产的“锦屏山”牌磷酸在1981年的江苏省磷酸行业质量评比会上被评为省内同行业第一名，1982年获省优质产品称号，1987年获国家化学工业部优质产品称号。"),
    ("GB196", "GB196一80标准", "GB196-80标准"),
    ("综合厂", "云台农场综合广", "云台农场综合厂"),
    ("单质溴素", "碘、漠素、活性炭", "碘、溴素、活性炭"),
    ("生产溴素", "开始生产漠素", "开始生产溴素"),
    ("海水化工一厂连字符", "市海水化工-厂", "市海水化工一厂"),
    ("提溴技改", "海水提漠生产装置", "海水提溴生产装置"),
    ("提溴耗电", "海水提漠比苦卤提漠", "海水提溴比苦卤提溴"),
    ("溴素车间", "对漠素车间进行技改", "对溴素车间进行技改"),
    ("溴素产能185", "使漠素年生产能力增至185吨", "使溴素年生产能力增至185吨"),
    ("化工机械厂", "市化工机械广投资23.7万元", "市化工机械厂投资23.7万元"),
    ("市化工厂", "市化工广（原新浦农药厂）", "市化工厂（原新浦农药厂）"),
    ("海水提溴车间", "海水提漠车间", "海水提溴车间"),
    ("溴化工产品", "漠化工产品", "溴化工产品"),
    ("海水厂该厂", "该广生产的溴系列产品", "该厂生产的溴系列产品"),
    ("溴甲烷", "漠甲烷", "溴甲烷"),
    ("八溴醚", "八漠醚", "八溴醚"),
    ("四溴苯酐", "四漠苯酐", "四溴苯酐"),
    ("溴乙烷", "漠乙烷", "溴乙烷"),
    ("黄海化工溴素", "氯化镁、漠素等产品", "氯化镁、溴素等产品"),
    ("黄海项目", "漠素等项自在1987年", "溴素等项目在1987年"),
    ("黄海固定资产", "固定资产原值764方元", "固定资产原值764万元"),
    ("海滨产值", "当年完成产值1524方元", "当年完成产值1524万元"),
    ("化肥投资", "投资6341方元", "投资6341万元"),
    ("磷肥厂", "磷肥广相继建立", "磷肥厂相继建立"),
    ("合成氨总述", "7.10方吨", "7.10万吨"),
    ("钙镁磷肥", "产量1.6方吨", "产量1.6万吨"),
    ("合成氨1990", "实产合成氨6.98方吨", "实产合成氨6.98万吨"),
    ("县化肥1980能力", "达3.6方吨", "达3.6万吨"),
    ("县化肥1980实产", "合成氨3.64方吨、碳铵14.70方吨", "合成氨3.64万吨、碳铵14.70万吨"),
    ("县化肥1987能力", "达5.6方吨", "达5.6万吨"),
    ("赣榆三万吨", "达到3方吨", "达到3万吨"),
    ("三县化肥厂", "3县化肥广", "3县化肥厂"),
    ("钾盐组组长", "钾盐组组：长单位", "钾盐组组长单位"),
    ("厂长陶文新", "广长陶文新", "厂长陶文新"),
    ("复合肥加入", "随之加人到复合肥", "随之加入到复合肥"),
    ("复合肥实产", "实产1.06方吨", "实产1.06万吨"),
    ("第二农药厂", "市第二农药广", "市第二农药厂"),
    ("辛硫磷投资", "投资256方元", "投资256万元"),
    ("辛硫磷苯乙腈", "无水乙醇、苯乙、乙基氯化物", "无水乙醇、苯乙腈、乙基氯化物"),
    ("克菌壮列入", "列人国*974·j家、省、市重大产品试产计划", "列入国家、省、市重大产品试产计划"),
    ("红旗化工厂饲料", "市红旗化工广应上海外贸公司", "市红旗化工厂应上海外贸公司"),
    ("饲料吨", "实产664饨", "实产664吨"),
    ("发酵厂", "连云港市发酵广", "连云港市发酵厂"),
    ("红旗化工厂柠檬酸", "市红旗化工广引进上海微生物", "市红旗化工厂引进上海微生物"),
    ("列入省新产品", "被列人省新产品开发计划", "被列入省新产品开发计划"),
    ("食品级磷酸氢钙投入", "正式投人批量生产", "正式投入批量生产"),
    ("GB10619", "GB10619－89.1989年", "GB10619-89。1989年"),
    ("锦屏化工厂食品磷酸", "市锦屏化工广成功研制食品级磷酸", "市锦屏化工厂成功研制食品级磷酸"),
    ("GB3149", "GB314982标准", "GB3149-82标准"),
    ("GB8848", "GB8848一88", "GB8848-88"),
    ("GB10620", "GB10620一89,", "GB10620-89,"),
    ("田菁投入", "并很快投人生产", "并很快投入生产"),
    ("热熔胶投入", "同年7月投人试产", "同年7月投入试产"),
    ("上海皮革化工厂", "上海皮革化工广", "上海皮革化工厂"),
    ("乙基麦芽酚投入", "1987年投人批量生产", "1987年投入批量生产"),
    ("第二橡胶利税", "利税106方元", "利税106万元"),
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
    current_changes = sum(counts.values())
    verified_items = len(REPLACEMENTS)
    payload = {
        "time": now,
        "scope": "第二十卷化学工业",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": verified_items,
        "current_run_replacements": current_changes,
        "counts": counts,
        "principle": "仅修复页级 OCR 清楚给出正确写法的第二十卷错识；大段断裂和表格残文未在本批猜修。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第二十卷化学工业高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{verified_items} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 重点：修正化工总述、化工原料、化肥农药、添加剂与胶粘剂等段落中的单位、厂名、溴字、投入/列入和 GB 标准号错识。",
        "- 补句：按源页补回磷酸主要生产厂家及锦屏山牌磷酸获奖短句。",
        "- 保留：第二十卷中仍有若干长段断裂和表格残文，未在本批凭猜测改写。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第二十卷化学工业高置信错识回源修复

- 对第二十卷化学工业进行小批回源修复，范围限定在 `第二十卷-化学工业` 到 `第二十一卷-机械工业` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`5方元党费`→`5万元党费`，`小氮肥广`→`小氮肥厂`，`漠素/漠甲烷/八漠醚`→`溴素/溴甲烷/八溴醚`，`GB314982标准`→`GB3149-82标准`，`投人/列人`→`投入/列入`。
- 补回磷酸段 `主要生产厂家有锦屏化工厂、红旗化工厂等，其中...` 短句；大段断裂与表格残文未在本批猜修。
- 本批核验修复 {verified_items} 项；报告：`output/reports/reader_readability_chemical_batch_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第二十卷化学工业高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
