# -*- coding: utf-8 -*-
"""Thirty-fifth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch35_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch35_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十五批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "徐州解放大会参加群众",
        "old": "参加群众达1.5方人",
        "new": "参加群众达1.5万人",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0070.txt:4",
    },
    {
        "label": "东海郡人口",
        "old": "27.17方人",
        "new": "27.17万人",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0280.txt:10",
    },
    {
        "label": "不在业人口在校学生",
        "old": "在校学生8.4方人",
        "new": "在校学生8.4万人",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0293.txt:5",
    },
    {
        "label": "1949年市区职工与个体劳动者",
        "old": "全民职工1.76方人，个体劳动者1.43方人",
        "new": "全民职工1.76万人，个体劳动者1.43万人",
        "source": "workbench/ocr/paddle_ocr/上/part02/page_0149.txt:13",
    },
    {
        "label": "供销系统职工",
        "old": "职工1.6方人，固定",
        "new": "职工1.6万人，固定",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0159.txt:13",
    },
    {
        "label": "食品业全民企业职工",
        "old": "全民企业职工1.25方人",
        "new": "全民企业职工1.25万人",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0062.txt:30",
    },
    {
        "label": "民兵水库建设出动人次",
        "old": "出动民兵62方人次",
        "new": "出动民兵62万人次",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0184.txt:27",
    },
    {
        "label": "山区水库水饮用人口",
        "old": "饮用山区水库水3.78方人",
        "new": "饮用山区水库水3.78万人",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0172.txt:17",
    },
    {
        "label": "低氟水受益人口",
        "old": "受益65.13方人",
        "new": "受益65.13万人",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0181.txt:22",
    },
    {
        "label": "贫协会员人数",
        "old": "贫协会员发展到10.8方人",
        "new": "贫协会员发展到10.8万人",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0343.txt:12",
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
        "scope": "第三十五批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复页级 Paddle OCR 直接证明的 `方人/方人次` 人口与职工单位残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三十五批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 Paddle OCR 直接证明的 `方人/方人次` 人口与职工单位残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：人物传 `加人中国共产党`、`自已/进人`、`准海战役` 等继续逐页核源。",
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

    marker = "## 2026-07-04 第三十五批正文残留回源修复"
    memory = f"""
{marker}
- 修复页级 Paddle OCR 直接证明的 `方人/方人次` 人口与职工单位残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/上/part01/page_0070.txt`、`page_0280.txt`、`page_0293.txt`，`workbench/ocr/paddle_ocr/上/part02/page_0149.txt`，`workbench/ocr/paddle_ocr/中/part01/page_0062.txt`，`workbench/ocr/paddle_ocr/中/part02/page_0159.txt`，`workbench/ocr/paddle_ocr/下/part01/page_0184.txt`、`page_0343.txt`，`workbench/ocr/paddle_ocr/下/part02/page_0172.txt`、`page_0181.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓人物传 `加人中国共产党`、`自已/进人`、`准海战役` 等继续逐页核源。
- 报告：`output/reports/reader_readability_source_backed_batch35_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
