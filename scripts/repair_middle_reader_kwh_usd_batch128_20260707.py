# -*- coding: utf-8 -*-
"""Repair narrowly verified middle-reader kWh/USD unit residues, batch 128."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_kwh_usd_batch128_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_kwh_usd_batch128_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册电量外汇单位残字回源补修第一百二十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "新浦热电厂1987年发电量",
        "old": "224万于瓦时",
        "new": "224万千瓦时",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:19427，同段 1988/1990 发电量单位为万千瓦时",
    },
    {
        "label": "水电站1990年发电量",
        "old": "7万于瓦时",
        "new": "7万千瓦时",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:19467，同段最高年发电80万千瓦时",
    },
    {
        "label": "全年供电量",
        "old": "113858万于瓦时",
        "new": "113858万千瓦时",
        "source": "output/final_reader/连云港市志_中册.html 电网段；同章供电、用电统计均用千瓦时",
    },
    {
        "label": "全年供电量 HTML 拆段",
        "old": "113858万于</p><p>瓦时",
        "new": "113858万千</p><p>瓦时",
        "source": "output/final_reader/连云港市志_中册.html；纯文本对应全年供电113858万千瓦时",
    },
    {
        "label": "主变损失",
        "old": "53万于瓦时",
        "new": "53万千瓦时",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:20358，同句35千伏线路损耗37万千瓦时、合计90万千瓦时",
    },
    {
        "label": "民国34年年用电",
        "old": "475万于瓦时",
        "new": "475万千瓦时",
        "source": "output/final_reader/连云港市志_中册.html 用电沿革段；同段年发电550万千瓦时",
    },
    {
        "label": "民国34年年用电 HTML 拆段",
        "old": "475万于瓦</p><p>时",
        "new": "475万千瓦</p><p>时",
        "source": "output/final_reader/连云港市志_中册.html；纯文本对应年用电475万千瓦时",
    },
    {
        "label": "1949年全省用电量",
        "old": "15711万于瓦时",
        "new": "15711万千瓦时",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:20560，同句人均用量4.5千瓦时",
    },
    {
        "label": "1985年农村用电",
        "old": "19377万于瓦时",
        "new": "19377万千瓦时",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:20714，同段排灌用电1642万千瓦时、农村用电15153万千瓦时",
    },
    {
        "label": "电度表现场校验阈值",
        "old": "10万于瓦时及以上半年1次",
        "new": "10万千瓦时及以上半年1次",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:20966，同句100万千瓦时、50万千瓦时、10万千瓦时以下",
    },
    {
        "label": "1957年灌溉电价",
        "old": "每干瓦时0.105元",
        "new": "每千瓦时0.105元",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:21001，前后电价均为每千瓦时",
    },
    {
        "label": "丹麦杀菌温度测试仪用汇",
        "old": "用汇1.09方美元",
        "new": "用汇1.09万美元",
        "source": "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:11118-11119，同段外汇单位为万美元/美元/马克",
    },
    {
        "label": "丹麦杀菌温度测试仪用汇 HTML 拆段",
        "old": "用汇1.09方</p><p>美元",
        "new": "用汇1.09万</p><p>美元",
        "source": "output/final_reader/连云港市志_中册.html；纯文本对应用汇1.09万美元",
    },
]

LEFT_UNTOUCHED = [
    "不处理其他 `于瓦`、`方美元`、`方元`、`干瓦` 候选，除非另有逐条证据。",
    "本批没有打开、展示或嵌入图片。",
]
CUMULATIVE_FIXED = 22


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
        "scope": "narrow middle reader kWh/USD residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "cumulative_fixed": CUMULATIVE_FIXED,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册电量、外汇单位残字补修第一百二十八批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿、中册 part01/part02 正文源稿、全书正文汇总。",
        "- 只处理同段单位体系能明确证明的固定短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本批累计命中：{CUMULATIVE_FIXED} 处",
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
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`；证据：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百二十八批：中册电量、外汇单位残字"
    upsert_memory(marker, f"""
{marker}

- 补修中册电力章 `万于瓦时/每干瓦时` 与外贸章 `用汇1.09方美元` 固定短语残字，改为 `万千瓦时/每千瓦时/万美元`。
- 本批证据短语 {len(REPLACEMENTS)} 项，累计命中 {CUMULATIVE_FIXED} 处；报告：`output/reports/middle_reader_kwh_usd_batch128_20260707.md`。
- 未处理其他未逐条核实的 `于瓦/方美元/方元/干瓦` 候选；未打开、展示或嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "cumulative_fixed": CUMULATIVE_FIXED, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
