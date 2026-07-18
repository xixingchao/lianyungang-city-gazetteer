# -*- coding: utf-8 -*-
"""Thirty-second source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch32_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch32_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十二批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "序言结语正文汇总同步",
        "old": "进一一步发挥自已的聪明才智",
        "new": "进一步发挥自己的聪明才智",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:1485",
    },
    {
        "label": "民盟市委盟员入党",
        "old": "有10名盟员加人中国共产党",
        "new": "有10名盟员加入中国共产党",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0469.txt:4",
    },
    {
        "label": "孙笃生入党",
        "old": "孙笃生加人中国共产党",
        "new": "孙笃生加入中国共产党",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0357.txt:6",
    },
    {
        "label": "优秀团员入党",
        "old": "送300多名优秀团员加人中国共产党",
        "new": "送300多名优秀团员加入中国共产党",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0321.txt:19",
    },
    {
        "label": "李登先籍贯与入党地区",
        "old": "李登先（1926～）准安县人。民国29年（1940年）参加革命，民国31年加人中国共产党。1975年任准阴地区革委会副主任。",
        "new": "李登先（1926～）淮安县人。民国29年（1940年）参加革命，民国31年加入中国共产党。1975年任淮阴地区革委会副主任。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0393.txt:5-6",
    },
    {
        "label": "徐进德籍贯",
        "old": "徐进德(1921 ~）山东省营南县人。",
        "new": "徐进德(1921 ~）山东省莒南县人。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0390.txt:13",
    },
    {
        "label": "程锡美籍贯与入党",
        "old": "程锡美（1927～）女，山东省营南县十字路人。民国32年（1943年）加人中国共产党。",
        "new": "程锡美（1927～）女，山东省莒南县十字路人。民国32年（1943年）加入中国共产党。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0393.txt:16-17",
    },
    {
        "label": "程锡美护理与津贴",
        "old": "到新海连特区医院担任护土，将自已的津贴补助伤员。",
        "new": "到新海连特区医院担任护士，将自己的津贴补助伤员。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0393.txt:18-19",
    },
    {
        "label": "宋玉斋医护职称与入党",
        "old": "先后任护土、医土、医生等。1966年调东海县医院任眼科医师。1979年，破格晋升为副主任医师，同年加人中国共产党。",
        "new": "先后任护士、医士、医生等。1966年调东海县医院任眼科医师。1979年，破格晋升为副主任医师，同年加入中国共产党。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0395.txt:4-5",
    },
    {
        "label": "杨佃池少年英雄",
        "old": "杨池（1975～1988）连云港市徐圩小学学生。1988年6月4日，在放学回家途中，见到小同学不慎落水，立即跳水营救，倾力将落水同学推到岸边得救，而自已却因疲劳沉人水底，",
        "new": "杨佃池（1975～1988）连云港市徐圩小学学生。1988年6月4日，在放学回家途中，见到小同学不慎落水，立即跳水营救，倾力将落水同学推到岸边得救，而自己却因疲劳沉入水底，",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:8-10",
    },
    {
        "label": "前进社孙炳中棉袄",
        "old": "由于冷，眼看就要冻死。社员孙炳中捡粪遇到，就将自已的棉秩脱下来包着小牛，",
        "new": "由于天冷，眼看就要冻死。社员孙炳中捡粪遇到，就将自己的棉袄脱下来包着小牛，",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0418.txt:12-13",
    },
]


def append_memory(path: Path, marker: str, content: str) -> None:
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
        "scope": "第三十二批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复页级 OCR 或 Paddle 汇总可直接证明的人物、序言与入党残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三十二批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 OCR 或 Paddle 汇总可直接证明的人物、序言与入党残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：仍未逐页核到的其它 `加人中国共产党`、`准海战役`、通用 `自已/进人/投人` 残留。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                lines.append(
                    f"- {item['label']}：依据 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。"
                )
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 第三十二批正文残留回源修复"
    memory = f"""
{marker}
- 修复页级 OCR 或 Paddle 汇总直接证明的人物、序言与入党残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md`、`workbench/ocr/paddle_ocr/中/part02/page_0469.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0321.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0357.txt`、`page_0390.txt`、`page_0393.txt`、`page_0395.txt`、`page_0401.txt`、`page_0418.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓仍未逐页核到的其它 `加人中国共产党`、`准海战役`、通用 `自已/进人/投人` 残留。
- 报告：`output/reports/reader_readability_source_backed_batch32_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
