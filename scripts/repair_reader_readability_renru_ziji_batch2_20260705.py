# -*- coding: utf-8 -*-
"""Second source-backed 人/入 and 自/己 repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_renru_ziji_batch2_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_renru_ziji_batch2_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_人入自己第二批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "运输机械厂并入水泵厂",
        "old": "运输机械厂并人水泵厂",
        "new": "运输机械厂并入水泵厂",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0193.txt:14"],
    },
    {
        "label": "连云港电机厂并入变压器厂",
        "old": "1962年并人连云港变压器厂",
        "new": "1962年并入连云港变压器厂",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0220.txt:25"],
    },
    {
        "label": "水表厂并入金属容器厂",
        "old": "水表厂并人连云港市新浦金属容器厂",
        "new": "水表厂并入连云港市新浦金属容器厂",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0230.txt:20"],
    },
    {
        "label": "水表厂划出并入新浦开关厂",
        "old": "划出并人新浦开关厂",
        "new": "划出并入新浦开关厂",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0230.txt:20-21"],
    },
    {
        "label": "硅稳压二极管转入晶体管厂",
        "old": "产品转人市晶体管厂生产",
        "new": "产品转入市晶体管厂生产",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0252.txt:17"],
    },
    {
        "label": "继电器产品列入省计划",
        "old": "产品列人省计划",
        "new": "产品列入省计划",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0256.txt:20"],
    },
    {
        "label": "市石灰厂自己建淋化车间",
        "old": "市石灰厂自已建了一个淋化车间",
        "new": "市石灰厂自己建了一个淋化车间",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0279.txt:14"],
    },
    {
        "label": "肖岭水电站并入35千伏电网",
        "old": "1973年4月并人地区35千伏电网运行",
        "new": "1973年4月并入地区35千伏电网运行",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0342.txt:7"],
    },
    {
        "label": "炼糖厂自备电站并入35千伏电网",
        "old": "发电后并人地区35千伏电网运行",
        "new": "发电后并入地区35千伏电网运行",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0343.txt:61"],
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(target["changed"] for target in targets)
    payload = {
        "time": now,
        "scope": "人/入、自/己第二批回源修复",
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "targets": targets,
        "principle": "只修中册 part01 raw/PaddleOCR 可闭合的工业、电力、建材短句。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人入自己第二批回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修中册 part01 raw/PaddleOCR 可闭合的工业、电力、建材短句。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                evidence = "；".join(f"`{source}`" for source in item["evidence"])
                lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`；{target['target']} 命中 {item['count']} 处；证据：{evidence}。")
    lines += [
        "",
        "## 暂缓",
        "- 食品加工、竹藤、服装等候选项暂未逐条闭合页级证据，本批不修。",
        "",
    ]
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-05 人入自己第二批回源修复"
    memory = f"""
{marker}
- 依据中册 part01 PaddleOCR/raw 证据，修复机械、电子、建材、电力章节 `并人/转人/列人/自已` 残留，共 {total} 处。
- 证据集中在 `workbench/ocr/paddle_ocr/中/part01/page_0193.txt`、`page_0220.txt`、`page_0230.txt`、`page_0252.txt`、`page_0256.txt`、`page_0279.txt`、`page_0342.txt`、`page_0343.txt` 等。
- 食品加工、竹藤、服装等候选项暂未逐条闭合页级证据，本批不修。
- 报告：`output/reports/reader_readability_renru_ziji_batch2_20260705.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
