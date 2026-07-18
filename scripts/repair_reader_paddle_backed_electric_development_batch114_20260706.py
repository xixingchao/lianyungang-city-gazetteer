# -*- coding: utf-8 -*-
"""Repair narrowly Paddle-backed electric/development OCR residues, batch 114."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_electric_development_batch114_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_electric_development_batch114_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_电力电网与开发区残留回源补修第一百一十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
FIRST_RUN_CHANGED = 32

REPLACEMENTS = [
    {
        "label": "淮海盐电网概述",
        "old": "准阴、连云港、盐城组成了以110千伏设备为主要骨架的准海盐电网",
        "new": "淮阴、连云港、盐城组成了以110千伏设备为主要骨架的淮海盐电网",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0330.txt:29-30",
    },
    {
        "label": "淮海盐电网并入省网",
        "old": "1982年，准海盐电网并人省电网运行",
        "new": "1982年，淮海盐电网并入省电网运行",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0331.txt:4-5；page_0353.txt:24",
    },
    {
        "label": "电网线路长度公里",
        "old": "长180.9公单；110千伏变电所5座；35千伏变电所24座",
        "new": "长180.9公里；110千伏变电所5座；35千伏变电所24座",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0346.txt:29-30",
    },
    {
        "label": "淮海盐电网联入省网",
        "old": "淮海盐电网联入省电网",
        "new": "淮海盐电网联入省电网",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0346.txt:33；本项用于记录该处已正确，不产生替换",
    },
    {
        "label": "地区电网联入省系统",
        "old": "地区电网联人省220千伏系统运行",
        "new": "地区电网联入省220千伏系统运行",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0346.txt:35",
    },
    {
        "label": "供电量万千瓦时",
        "old": "全年供电121800万于瓦时",
        "new": "全年供电121800万千瓦时",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0347.txt:9",
    },
    {
        "label": "调度沿革淮海盐电网",
        "old": "1970年，建成准海盐电网，调度业务直接受准海盐电力调度组领导",
        "new": "1970年，建成淮海盐电网，调度业务直接受淮海盐电力调度组领导",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0353.txt:18-19",
    },
    {
        "label": "运行方式淮海盐电网",
        "old": "通过110千伏淮海线并人准海盐电网运行",
        "new": "通过110千伏淮海线并入淮海盐电网运行",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0354.txt:11",
    },
    {
        "label": "运行方式淮海盐供电",
        "old": "部分由准海盐电网供电",
        "new": "部分由淮海盐电网供电",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0354.txt:12",
    },
    {
        "label": "海磷线联络淮海盐电网",
        "old": "与准海盐电网联络的关系",
        "new": "与淮海盐电网联络的关系",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0354.txt:15",
    },
    {
        "label": "淮阴电网联络",
        "old": "经灌云变电所和准阴电网联络",
        "new": "经灌云变电所和淮阴电网联络",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0354.txt:22",
    },
    {
        "label": "载波通信淮海盐/淮阴",
        "old": "载波通信1970年，准海盐电力调度组安装ZS-1型电力载波机，开通了准阴发电",
        "new": "载波通信1970年，淮海盐电力调度组安装ZS-1型电力载波机，开通了淮阴发电",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0355.txt:31",
    },
    {
        "label": "线损淮海盐网损",
        "old": "为准海盐网损",
        "new": "为淮海盐网损",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0362.txt:11",
    },
    {
        "label": "线损调度所淮海盐",
        "old": "1982年撤销准海盐调度所后，原110千伏刘灌线",
        "new": "1982年撤销淮海盐调度所后，原110千伏刘灌线",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0362.txt:21",
    },
    {
        "label": "线损节电万千瓦时",
        "old": "节电809万于瓦时",
        "new": "节电809万千瓦时",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0362.txt:36",
    },
    {
        "label": "开发区起步区平方公里",
        "old": "起步区0.65平方公单范围内的六通一平”及相应设施已基本完成",
        "new": "起步区0.65平方公里范围内的“六通一平”及相应设施已基本完成",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0431.txt:34-35；raw 同页误作平方公单",
    },
]

LEFT_UNTOUCHED = [
    "表格 `起准阴，经五里庄...` 仍需单独按表页坐标核验，本批不处理。",
    "司法劳改段 `并人徐州第四监狱` 既往列为边界，本批不凭常识改。",
    "其他 `准阴/准海/并人/联人/万于瓦时` 只保留候选，不做全局替换。",
    "本批不使用、不展示页图。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count and item["old"] != item["new"]:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": 0 if item["old"] == item["new"] else count})
        target.write_text(text, encoding="utf-8")
        applied.append({"target": str(target), "changed": sum(i["count"] for i in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = sum(t["changed"] for t in applied)
    payload = {
        "time": now,
        "scope": "Paddle-backed repair for electric grid and development-zone OCR residues",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "first_run_changed": FIRST_RUN_CHANGED,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 电力电网与开发区残留补修第一百一十四批：Paddle 回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 当前主阅读版、当前中册阅读版、电力/开发区正文源稿和全书正文汇总。",
        "- 仅处理 Paddle 页级 OCR 明确反证 raw/正文残留的电网名、地名、单位和面积短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 首跑替换：{FIRST_RUN_CHANGED} 处",
        f"- 本次复跑替换：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        if target["changed"]:
            lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百一十四批：电力电网与开发区残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按主阅读版、当前中册阅读版和正文源稿做 Paddle 页级回源补修，处理电力章 `准海盐/准阴/公单/万于瓦时/并人/联人` 等限定上下文残留，统一为 Paddle 可证的 `淮海盐/淮阴/公里/万千瓦时/并入/联入`。
- 同步修复开发区项目引进段 `0.65平方公单范围内的六通一平` 为 `0.65平方公里范围内的“六通一平”`，证据为 `workbench/ocr/paddle_ocr/中/part01/page_0431.txt:34-35`。
- 本批证据短语 {len(REPLACEMENTS)} 项，报告：`output/reports/reader_paddle_backed_electric_development_batch114_20260706.md`。
- 边界：表格 `起准阴`、司法劳改段 `并人徐州第四监狱` 和其他分散 `准阴/准海/并人/联人` 暂不批量处理；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
