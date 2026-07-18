# -*- coding: utf-8 -*-
"""Twenty-fifth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch25_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch25_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十五批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "民政烈士褒扬小标题",
        "old": "三、烈土褒扬",
        "new": "三、烈士褒扬",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0024.txt:24",
    },
    {
        "label": "抗日山烈士陵园建筑句",
        "old": "由抗日烈土纪念塔、纪念亭、纪念堂、纪念碑等建筑物",
        "new": "由抗日烈士纪念塔、纪念亭、纪念堂、纪念碑等建筑物",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0024.txt:33",
    },
    {
        "label": "灌云县烈士陵园陈列与墓句",
        "old": "陈列灌云县烈土事迹。园后建有烈土墓",
        "new": "陈列灌云县烈士事迹。园后建有烈士墓",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0024.txt:40",
    },
    {
        "label": "侍庄乡烈士墓数量",
        "old": "有烈土墓28座",
        "new": "有烈士墓28座",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0025.txt:16",
    },
    {
        "label": "白蚬乡烈士公墓句",
        "old": "白乡建成烈土公墓，占地1亩，内有烈土墓6座",
        "new": "白蚬乡建成烈士公墓，占地1亩，内有烈士墓6座",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0025.txt:16-17",
    },
    {
        "label": "白蚬乡烈士公墓句正文换行残留",
        "old": "白乡建成烈\n土公墓，占地1亩，内有烈土墓6座",
        "new": "白蚬乡建成烈士公墓，占地1亩，内有烈士墓6座",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0025.txt:16-17",
    },
    {
        "label": "红领巾禁赌宣传队",
        "old": "红领币禁赌宣传队",
        "new": "红领巾禁赌宣传队",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0084.txt:13",
    },
    {
        "label": "李迪仁追认为革命烈士",
        "old": "道认李迪仁为革命烈土",
        "new": "追认李迪仁为革命烈士",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0373.txt:14",
    },
]

STRUCTURAL_RISK_NOTE = """用户本轮贴出的地质、方言正文样例呈现跨章节/跨段粘连风险；本批只修可由页级 OCR 直接证明的字形残留，结构级问题另列风险，不用局部替换掩盖。"""


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
        "scope": "第二十五批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复下册页级 OCR 可直接证明的烈士、红领巾、追认残留。",
        "structural_risk_note": STRUCTURAL_RISK_NOTE,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十五批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修下册页级 OCR 可直接证明的烈士、红领巾、追认残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        f"- 结构风险说明：{STRUCTURAL_RISK_NOTE}",
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
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-04 第二十五批正文残留回源修复"
    memory = f"""
{marker}
- 修复下册页级 OCR 直接证明的 8 类残留：民政章 `烈土/烈士`、`白乡/白蚬乡`，治安章 `红领币/红领巾`，人物传 `道认/追认` 与 `革命烈土/革命烈士`。
- 依据页：`workbench/ocr/paddle_ocr/下/part01/page_0024.txt`、`page_0025.txt`、`page_0084.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0373.txt`。
- 用户贴出的正文样例提示跨章节/跨段粘连风险；本批已在报告中单独标注，不用局部错字替换掩盖结构级问题。
- 报告：`output/reports/reader_readability_source_backed_batch25_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
