# -*- coding: utf-8 -*-
"""Third source-backed 人/入 repair batch for final reader/body text."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_renru_ziji_batch3_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_renru_ziji_batch3_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_人入自己第三批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "竹柳铺并入新浦竹藤生产合作组",
        "old": "私营竹柳铺并人新浦竹藤生产合作组",
        "new": "私营竹柳铺并入新浦竹藤生产合作组",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0034.txt:22"],
    },
    {
        "label": "烈军属竹藤条叶厂并入新浦竹藤社",
        "old": "烈军属竹藤条叶厂30多人并人新浦竹藤社",
        "new": "烈军属竹藤条叶厂30多人并入新浦竹藤社",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0034.txt"],
    },
    {
        "label": "新浦绣品厂转入出口服装生产",
        "old": "新浦绣品厂全部转人出口服装生产",
        "new": "新浦绣品厂全部转入出口服装生产",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0042.txt:17"],
    },
    {
        "label": "肉联厂调拨列入省市计划",
        "old": "其生产、调拨列人省、市计划",
        "new": "其生产、调拨列入省、市计划",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0074.txt:30"],
    },
    {
        "label": "东华酱园并入酿化厂",
        "old": "东华酱园并人该厂",
        "new": "东华酱园并入该厂",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0102.txt:8"],
    },
    {
        "label": "蛋制品进入机械化制作阶段",
        "old": "蛋制品进人机械化制作阶段",
        "new": "蛋制品进入机械化制作阶段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0104.txt"],
    },
    {
        "label": "新浦淀粉厂并入制冰厂",
        "old": "新浦淀粉广并人新浦制冰厂",
        "new": "新浦淀粉厂并入新浦制冰厂",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0107.txt:17"],
    },
    {
        "label": "蔬菜速冻技改列入七五重点工程",
        "old": "并列人省“七五重点技改工程",
        "new": "并列入省“七五”重点技改工程",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0111.txt:16"],
    },
    {
        "label": "制碘厂发电机并入10千伏配电网",
        "old": "投产后并人地区10千伏配电网运行",
        "new": "投产后并入地区10千伏配电网运行",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0344.txt:7"],
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
        "scope": "人/入第三批回源修复",
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "targets": targets,
        "principle": "只修中册 part01 PaddleOCR 可闭合的竹藤、服装、食品、电力短句。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人入自己第三批回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修中册 part01 PaddleOCR 可闭合的竹藤、服装、食品、电力短句。",
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
        "- 本批不处理跨页错乱、地质/方言等大段正文串页问题，需另行按页级源文本重建或分章审计。",
        "",
    ]
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-05 人入自己第三批回源修复"
    memory = f"""
{marker}
- 依据中册 part01 PaddleOCR 证据，修复竹藤、服装、食品、电力章节 `并人/转人/列人/进人` 残留及 `淀粉广/七五` 漏误，共 {total} 处。
- 证据集中在 `workbench/ocr/paddle_ocr/中/part01/page_0034.txt`、`page_0042.txt`、`page_0074.txt`、`page_0102.txt`、`page_0104.txt`、`page_0107.txt`、`page_0111.txt`、`page_0344.txt`。
- 用户指出可能存在整本 PDF 转换级正文错乱；本批只处理已闭合小错，大段串页/错章另列为后续专项。
- 报告：`output/reports/reader_readability_renru_ziji_batch3_20260705.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
