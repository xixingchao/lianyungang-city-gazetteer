# -*- coding: utf-8 -*-
"""Repair source-backed middle-reader money/power unit residues, batch 127."""

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
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_money_power_batch127_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_money_power_batch127_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册金额电力单位残字回源补修第一百二十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "刺绣厂电脑绣花机购置", "old": "用7.3方元", "new": "用7.3万元", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:1487"},
    {"label": "刺绣厂利税", "old": "利税总额14.16方元", "new": "利税总额14.16万元", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:1488"},
    {"label": "糕点加工产值", "old": "完成产值39.3方元", "new": "完成产值39.3万元", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:3361"},
    {"label": "东海食品厂产值", "old": "产值103方元", "new": "产值103万元", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:3503"},
    {"label": "灌云食品公司产值", "old": "产值807方元", "new": "产值807万元", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:3705"},
    {"label": "肉联厂产值", "old": "当年产值5222方元", "new": "当年产值5222万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:124185"},
    {"label": "肉类罐头产值", "old": "产值2050.9方元", "new": "产值2050.9万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:124518"},
    {"label": "啤酒厂投资", "old": "投资295方元", "new": "投资295万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:127513"},
    {"label": "果酒厂利税", "old": "利税172方元", "new": "利税172万元", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:5568"},
    {"label": "异维生素C钠技术转让", "old": "出资5方元", "new": "出资5万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:130550"},
    {"label": "酶制剂厂利税", "old": "利税365方元", "new": "利税365万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:126063"},
    {"label": "红旗化工厂党费", "old": "以5方元党费", "new": "以5万元党费", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:9035"},
    {"label": "化工厂固定资产", "old": "固定资产原值764方元", "new": "固定资产原值764万元", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:9819"},
    {"label": "电化厂产值", "old": "完成产值1524方元", "new": "完成产值1524万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:130333"},
    {"label": "江苏化肥厂投资", "old": "投资6341方元", "new": "投资6341万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:129548"},
    {"label": "市化工厂搬迁投资", "old": "投资256方元", "new": "投资256万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:130851"},
    {"label": "橡胶厂利税", "old": "利税106方元", "new": "利税106万元", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:12749"},
    {"label": "机械系统产值", "old": "工业总产值13650方元", "new": "工业总产值13650万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:133456"},
    {"label": "车辆厂亏损", "old": "亏损241方元", "new": "亏损241万元", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:133456"},
    {"label": "新海发电厂容量", "old": "8.6万干瓦", "new": "8.6万千瓦", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:139276-139277"},
    {"label": "6000千瓦机组", "old": "6000干瓦", "new": "6000千瓦", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:139362-139376"},
    {"label": "地区负荷", "old": "4.6万干瓦", "new": "4.6万千瓦", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:139308"},
    {"label": "水电站总容量", "old": "5580干瓦", "new": "5580千瓦", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:19446"},
    {"label": "最高负荷", "old": "750干瓦", "new": "750千瓦", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:139299"},
    {"label": "采盐业用电", "old": "5775万干瓦时", "new": "5775万千瓦时", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:20648"},
    {"label": "农副业用电", "old": "6932万干瓦时", "new": "6932万千瓦时", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:141271"},
    {"label": "农副业用电 HTML 跨段", "old": "6932万干</p><p>瓦时", "new": "6932万千</p><p>瓦时", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:141271"},
    {"label": "照明用电", "old": "11万干瓦时", "new": "11万千瓦时", "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:20740"},
    {"label": "海岸电台高频机", "old": "1.6干瓦高频", "new": "1.6千瓦高频", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:146708 近邻电信段；单位同段为千瓦"},
    {"label": "机修厂供电能力", "old": "1800干瓦", "new": "1800千瓦", "source": "workbench/body_chapters/连云港市志_全书_正文汇总.md:146708 近邻交通段；单位同段为千瓦"},
]

LEFT_UNTOUCHED = [
    "本批只处理可由正文源稿/全书正文汇总/Paddle 电力章交叉证明的固定短语。",
    "仍保留未逐条核实的 `方元`、`干瓦` 候选，不做全局替换。",
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
        "scope": "source-backed middle reader money/power unit residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册金额、电力单位残字补修第一百二十七批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书阅读稿、当前中册阅读稿、中册正文源稿和全书正文汇总。",
        "- 只处理正文源稿或全书正文汇总已给出正确形态的固定短语。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百二十七批：中册金额、电力单位残字"
    upsert_memory(marker, f"""
{marker}

- 按当前中册正文源稿、全书正文汇总和 Paddle 电力章证据，补修中册阅读稿/源稿中的 `方元/方美元/干瓦` 固定短语残字，统一为 `万元/万美元/千瓦/千瓦时`。
- 本批证据短语 {len(REPLACEMENTS)} 项，首跑替换 {changed} 处；报告：`output/reports/middle_reader_money_power_batch127_20260707.md`。
- 仍保留未逐条核实的其他 `方元/干瓦` 候选；本批未使用、未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
