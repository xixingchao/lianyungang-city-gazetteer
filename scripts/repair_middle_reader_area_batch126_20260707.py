# -*- coding: utf-8 -*-
"""Repair Paddle-backed middle-reader area/person unit residues, batch 126."""

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
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_area_batch126_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_area_batch126_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册面积人口单位残字回源补修第一百二十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "味精厂建筑面积",
        "old": "建筑面积1.25方平方米",
        "new": "建筑面积1.25万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0103.txt:19",
    },
    {
        "label": "无线电元件四厂建筑面积",
        "old": "建筑面积2.3方平方米",
        "new": "建筑面积2.3万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0257.txt:18",
    },
    {
        "label": "釉面砖产量面积",
        "old": "0.62方平方米",
        "new": "0.62万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0291.txt:5",
    },
    {
        "label": "建筑设计能力",
        "old": "年设计能力达60方平方米",
        "new": "年设计能力达60万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0296.txt:23-24",
    },
    {
        "label": "建筑施工工人",
        "old": "全市建筑施工工人约20方人",
        "new": "全市建筑施工工人约20万人",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0296.txt:25",
    },
    {
        "label": "工程质量监督面积",
        "old": "建筑面积76方平方米",
        "new": "建筑面积76万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0324.txt:32",
    },
    {
        "label": "蛇纹石矿占地",
        "old": "矿山占地23方平方米",
        "new": "矿山占地23万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0388.txt:14",
    },
    {
        "label": "乡镇企业竣工面积",
        "old": "竣工面积1449.5方平方米",
        "new": "竣工面积1449.5万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0398.txt:14",
    },
    {
        "label": "航务航道基地陆域",
        "old": "10方平方米的陆域",
        "new": "10万平方米的陆域",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0440.txt:17",
    },
    {
        "label": "航务工程预制厂区",
        "old": "8.24方平方米钢筋混凝土预制厂区",
        "new": "8.24万平方米钢筋混凝土预制厂区",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0440.txt:23",
    },
    {
        "label": "外贸仓库道路占地",
        "old": "道路占地总面积13.89方平方米",
        "new": "道路占地总面积13.89万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0467.txt:4",
    },
    {
        "label": "外贸仓库使用面积",
        "old": "使用总面积为12.8方平方来",
        "new": "使用总面积为12.8万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0467.txt:4",
    },
]

LEFT_UNTOUCHED = [
    "`陵园总面积21.06方平方米` 源页 Paddle 跨行显示 `21.06万平`，本批先不处理跨行残词。",
    "下册 `方平方米` 四处缺少 Paddle 反证，本批不凭常识替换。",
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
        "scope": "Paddle-backed middle-reader area/person unit residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册面积、人口单位残字补修第一百二十六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书阅读稿、当前中册阅读稿、中册正文源稿和全书正文汇总。",
        "- 只处理 Paddle 页级 OCR 可证的 `方平方米/方人/方平方来 -> 万平方米/万人` 限定上下文。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百二十六批：中册面积、人口单位残字"
    upsert_memory(marker, f"""
{marker}

- 按 Paddle 页级 OCR 补修中册 `方平方米/方人/方平方来` 面积和人口单位残字，覆盖 `page_0103`、`page_0257`、`page_0291`、`page_0296`、`page_0324`、`page_0388`、`page_0398`、`page_0440`、`page_0467`。
- 本批证据短语 {len(REPLACEMENTS)} 项，首跑替换 {changed} 处；报告：`output/reports/middle_reader_area_batch126_20260707.md`。
- 下册四处 `方平方米` 以及 `陵园总面积21.06方平方米` 继续保留为逐页核对候选；本批未使用、未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
