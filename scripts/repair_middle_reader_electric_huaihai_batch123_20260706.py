# -*- coding: utf-8 -*-
"""Repair Paddle-backed middle-reader 淮阴/淮海盐/输入 residues, batch 123."""

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
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_electric_huaihai_batch123_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_electric_huaihai_batch123_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_中册淮阴淮海盐输入残字回源补修第一百二十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "桐木厂联营县名",
        "old": "涟水、赣榆、准阴、灌南、准阳等县15个单位",
        "new": "涟水、赣榆、淮阴、灌南、淮阳等县15个单位",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0053.txt:16",
    },
    {
        "label": "复印机鉴定单位",
        "old": "1977年11月由准阴电子工业局组织技术鉴定",
        "new": "1977年11月由淮阴电子工业局组织技术鉴定",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0242.txt:10",
    },
    {
        "label": "有线广播箱输入阻抗",
        "old": "变压器输人阻抗57K",
        "new": "变压器输入阻抗57K",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0250.txt:12",
    },
    {
        "label": "电位器鉴定站",
        "old": "产品经准阴电子产品试验站鉴定",
        "new": "产品经淮阴电子产品试验站鉴定",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0254.txt:15",
    },
    {
        "label": "平板玻璃销地",
        "old": "主要销往准阴及浙江等地",
        "new": "主要销往淮阴及浙江等地",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0285.txt:31",
    },
    {
        "label": "淮海盐电网概述",
        "old": "淮海输变电工程，准阴、连云港、盐城组成了以110千伏设备为主要骨架的准海盐电网",
        "new": "淮海输变电工程，淮阴、连云港、盐城组成了以110千伏设备为主要骨架的淮海盐电网",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0330.txt:26",
    },
    {
        "label": "新海发电厂并网",
        "old": "新海发电厂并入准海盐电网",
        "new": "新海发电厂并入淮海盐电网",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0335.txt:4",
    },
    {
        "label": "淮海盐电网骨架",
        "old": "组成以110千伏设备为主要骨架的准海盐电网",
        "new": "组成以110千伏设备为主要骨架的淮海盐电网",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0346.txt:21-22",
    },
    {
        "label": "淮海盐电网联入省网",
        "old": "准海盐电网联人省电网",
        "new": "淮海盐电网联入省电网",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0346.txt:35",
    },
    {
        "label": "淮海盐主通道",
        "old": "为准海盐电网的主通道之一",
        "new": "为淮海盐电网的主通道之一",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0347.txt:36",
    },
    {
        "label": "电网输入电能",
        "old": "连云港地区电网输人电能的一个主要关口",
        "new": "连云港地区电网输入电能的一个主要关口",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0351.txt:26-27",
    },
    {
        "label": "调度业务淮海盐",
        "old": "1970年，建成准海盐电网，调度业务直接受准海盐电力调度组领导",
        "new": "1970年，建成淮海盐电网，调度业务直接受淮海盐电力调度组领导",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0353.txt:17-18",
    },
    {
        "label": "调度业务淮海盐跨行",
        "old": "1970年，建成准海盐电网，调度业务直接\n受准海盐电力调度组领导",
        "new": "1970年，建成淮海盐电网，调度业务直接\n受淮海盐电力调度组领导",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0353.txt:17-18",
    },
    {
        "label": "调度业务淮海盐 HTML 跨段",
        "old": "1970年，建成准海盐电网，调度业务直接</p><p>受准海盐电力调度组领导",
        "new": "1970年，建成淮海盐电网，调度业务直接</p><p>受淮海盐电力调度组领导",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0353.txt:17-18",
    },
    {
        "label": "调度所撤销",
        "old": "准海盐电网调度所被撤销",
        "new": "淮海盐电网调度所被撤销",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0353.txt:23-24",
    },
    {
        "label": "淮海线并入电网",
        "old": "通过110千伏淮海线并人准海盐电网运行",
        "new": "通过110千伏淮海线并入淮海盐电网运行",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0354.txt:11",
    },
    {
        "label": "淮海线并入电网跨行",
        "old": "过110千伏淮海线并人准海盐电网运行",
        "new": "过110千伏淮海线并入淮海盐电网运行",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0354.txt:11",
    },
    {
        "label": "部分由淮海盐供电",
        "old": "部分由准海盐电网供电",
        "new": "部分由淮海盐电网供电",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0354.txt:13",
    },
    {
        "label": "淮阴电网联络",
        "old": "经灌云变电所和准阴电网联络",
        "new": "经灌云变电所和淮阴电网联络",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0354.txt:24",
    },
    {
        "label": "远动信号送调度所",
        "old": "送至准海盐电网调度所",
        "new": "送至淮海盐电网调度所",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0356.txt:35",
    },
    {
        "label": "负荷分配淮海盐",
        "old": "连云港电网并入准海盐电网运行，电力负荷由准海盐电网中心调度所实行统一分配，连云港地区负荷分配比例占准海盐电网总负荷的30.7%。1979年，准海盐电",
        "new": "连云港电网并入淮海盐电网运行，电力负荷由淮海盐电网中心调度所实行统一分配，连云港地区负荷分配比例占淮海盐电网总负荷的30.7%。1979年，淮海盐电",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0371.txt:20-21",
    },
    {
        "label": "负荷分配并入淮海盐电网",
        "old": "连云港电网并入准海盐电网运行",
        "new": "连云港电网并入淮海盐电网运行",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0371.txt:20",
    },
    {
        "label": "负荷分配调度中心",
        "old": "准海盐电网中心调度所",
        "new": "淮海盐电网中心调度所",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0371.txt:20",
    },
    {
        "label": "负荷分配总负荷",
        "old": "准海盐电网总负荷",
        "new": "淮海盐电网总负荷",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0371.txt:21",
    },
    {
        "label": "省网分配并入",
        "old": "准海盐电网并人省电网运行",
        "new": "淮海盐电网并入省电网运行",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0371.txt:21；page_0331.txt:5",
    },
    {
        "label": "港口供电输入交流电",
        "old": "港口供电由海州发电厂输人交流电",
        "new": "港口供电由海州发电厂输入交流电",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0447.txt:35",
    },
]

LEFT_UNTOUCHED = [
    "其他分散 `准阴` 多属跨章地名残字候选，本批只处理已定位到中册 Paddle 页级 OCR 的上下文。",
    "`准海线`、交通表里的 `起准阴` 等边界不在本批处理范围。",
    "本批未使用、未展示、未嵌入任何图片。",
]


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        applied.append({"target": str(target), "changed": sum(i["count"] for i in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = sum(t["changed"] for t in applied)
    payload = {
        "time": now,
        "scope": "Paddle-backed middle reader 淮阴/淮海盐/输入 residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册淮阴、淮海盐、输入残字补修第一百二十三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书阅读稿、当前中册阅读稿、中册正文源稿、全书正文汇总。",
        "- 只处理 Paddle 页级 OCR 可证的 `准阴/准海盐/输人/并人/联人` 限定上下文。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次替换：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        if target["changed"]:
            lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`；证据：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百二十三批：中册淮阴、淮海盐、输入残字"
    upsert_memory(marker, f"""
{marker}

- 按 Paddle 页级 OCR 继续补修中册当前阅读稿和正文源稿里遗留的 `准阴/准海盐/输人/并人/联人` 限定上下文，统一为 `淮阴/淮海盐/输入/并入/联入`。
- 证据覆盖 `workbench/ocr/paddle_ocr/中/part01/page_0053.txt`、`page_0242.txt`、`page_0250.txt`、`page_0254.txt`、`page_0285.txt`、`page_0330.txt`、`page_0335.txt`、`page_0346.txt`、`page_0347.txt`、`page_0351.txt`、`page_0353.txt`、`page_0354.txt`、`page_0356.txt`、`page_0371.txt`、`page_0447.txt`。
- 本批证据短语 {len(REPLACEMENTS)} 项，首跑替换 {changed} 处；报告：`output/reports/middle_reader_electric_huaihai_batch123_20260706.md`。
- 未处理：`准海线`、交通表 `起准阴`、其他跨章分散地名残字候选；本批未使用、未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
