# -*- coding: utf-8 -*-
"""Thirty-fourth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch34_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch34_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十四批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "庙岭新港区陆域面积单位",
        "old": "陆域100多方平方米",
        "new": "陆域100多万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0105.txt:11",
    },
    {
        "label": "区属中小学校园占地单位",
        "old": "校园占地29.5方平方米",
        "new": "校园占地29.5万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0237.txt:20",
    },
    {
        "label": "海州区环卫清扫面积单位",
        "old": "道路清扫面积93方平方米",
        "new": "道路清扫面积93万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part02/page_0075.txt:18",
    },
    {
        "label": "云台区苗圃面积单位",
        "old": "苗圃1.6方平方米",
        "new": "苗圃1.6万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part02/page_0085.txt:32",
    },
    {
        "label": "生产绿地面积单位",
        "old": "生产绿地38方平方米",
        "new": "生产绿地38万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part02/page_0085.txt:35",
    },
    {
        "label": "造纸厂占地面积单位",
        "old": "占地面积0.7方平方米",
        "new": "占地面积0.7万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part03/page_0181.txt:4",
    },
    {
        "label": "印刷厂建筑面积单位",
        "old": "建筑面积0.81方平方米",
        "new": "建筑面积0.81万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part03/page_0188.txt:34",
    },
    {
        "label": "玻璃马赛克产能单位",
        "old": "彩色玻璃马赛克15方平方米、工艺玻璃器血50方只",
        "new": "彩色玻璃马赛克15万平方米、工艺玻璃器皿50万只",
        "source": "workbench/ocr/paddle_ocr/上/part03/page_0197.txt:24",
    },
    {
        "label": "精密仪器厂建筑面积单位",
        "old": "建筑面积0.2方平方米",
        "new": "建筑面积0.2万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part03/page_0225.txt:25",
    },
    {
        "label": "麻纺织厂占地面积单位",
        "old": "占地面积11.4方平方米",
        "new": "占地面积11.4万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part03/page_0262.txt:20",
    },
    {
        "label": "皮鞋二厂占地面积单位",
        "old": "厂区占地面积0.6方平方米",
        "new": "厂区占地面积0.6万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part03/page_0281.txt:38",
    },
    {
        "label": "东方拉链厂占地面积单位",
        "old": "企业区占地面积0.5方平方米",
        "new": "企业厂区占地面积0.5万平方米",
        "source": "workbench/ocr/paddle_ocr/上/part03/page_0293.txt:24",
    },
    {
        "label": "肉类加工建筑面积单位",
        "old": "建筑面积10.7方平方米",
        "new": "建筑面积10.7万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0070.txt:13-14",
    },
    {
        "label": "釉面砖产量单位",
        "old": "生产0.62方平方米",
        "new": "生产0.62万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0291.txt:5",
    },
    {
        "label": "西小区建筑面积单位",
        "old": "建筑面积10方平方来",
        "new": "建筑面积10万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0305.txt:5-6",
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
        "scope": "第三十四批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复页级 Paddle OCR 直接证明的面积/数量单位残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三十四批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 Paddle OCR 直接证明的面积/数量单位残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：`方人`、人物传 `加人中国共产党`、`准海战役` 等仍需另批逐页核源。",
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

    marker = "## 2026-07-04 第三十四批正文残留回源修复"
    memory = f"""
{marker}
- 修复页级 Paddle OCR 直接证明的面积/数量单位残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/上/part01/page_0105.txt`、`page_0237.txt`，`workbench/ocr/paddle_ocr/上/part02/page_0075.txt`、`page_0085.txt`，`workbench/ocr/paddle_ocr/上/part03/page_0181.txt`、`page_0188.txt`、`page_0197.txt`、`page_0225.txt`、`page_0262.txt`、`page_0281.txt`、`page_0293.txt`，`workbench/ocr/paddle_ocr/中/part01/page_0070.txt`、`page_0291.txt`、`page_0305.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓 `方人`、人物传 `加人中国共产党`、`准海战役` 等另批逐页核源。
- 报告：`output/reports/reader_readability_source_backed_batch34_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
