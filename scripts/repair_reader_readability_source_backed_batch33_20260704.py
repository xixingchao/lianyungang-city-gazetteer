# -*- coding: utf-8 -*-
"""Thirty-third source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch33_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch33_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十三批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "食品厂建筑面积单位",
        "old": "建筑面积1.25方平方米",
        "new": "建筑面积1.25万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0103.txt:19",
    },
    {
        "label": "电讯器材厂建筑面积单位",
        "old": "建筑面积2.3方平方米",
        "new": "建筑面积2.3万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0257.txt:18",
    },
    {
        "label": "抗日山烈士陵园题名",
        "old": "抗日山烈王陵园",
        "new": "抗日山烈士陵园",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0024.txt:29",
    },
    {
        "label": "抗日山烈士陵园面积单位",
        "old": "21.06方平方米",
        "new": "21.06万平方米",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0024.txt:31",
    },
    {
        "label": "工程质量监督审查面积单位",
        "old": "建筑面积76方平方米",
        "new": "建筑面积76万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0324.txt:31-32",
    },
    {
        "label": "矿山占地面积单位",
        "old": "矿山占地23方平方米",
        "new": "矿山占地23万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0388.txt:14",
    },
    {
        "label": "乡镇建筑企业竣工面积单位",
        "old": "竣工面积1449.5方平方米",
        "new": "竣工面积1449.5万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0398.txt:14",
    },
    {
        "label": "徐福酒厂占地建筑面积单位",
        "old": "占地1.98方平方米，建筑面积1.9方平方米",
        "new": "占地1.98万平方米，建筑面积1.9万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0094.txt:50-51",
    },
    {
        "label": "酒厂占地面积单位",
        "old": "占地2.5方平方米",
        "new": "占地2.5万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0094.txt:58-59",
    },
    {
        "label": "航务航道基地陆域面积单位",
        "old": "10方平方米的陆域",
        "new": "10万平方米的陆域",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0440.txt:17",
    },
    {
        "label": "航务工程预制厂区面积单位",
        "old": "8.24方平方米钢筋混凝土预制厂区",
        "new": "8.24万平方米钢筋混凝土预制厂区",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0440.txt:23",
    },
    {
        "label": "外贸仓库道路占地面积单位",
        "old": "道路占地总面积13.89方平方米",
        "new": "道路占地总面积13.89万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0467.txt:3",
    },
    {
        "label": "外贸仓库使用面积单位",
        "old": "使用总面积为12.8方平方来",
        "new": "使用总面积为12.8万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0467.txt:3",
    },
    {
        "label": "中药学校前身护士学校",
        "old": "人民医院护土学校",
        "new": "人民医院护士学校",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0393.txt:14",
    },
    {
        "label": "中药学校建筑面积单位",
        "old": "建筑面积1.03方平方米",
        "new": "建筑面积1.03万平方米",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0393.txt:18",
    },
    {
        "label": "唐贯淮入党",
        "old": "唐贯淮（1935～）灌云县人。1955年9月参加工作，1954年11月加人中国共产党。",
        "new": "唐贯淮（1935～）灌云县人。1955年9月参加工作，1954年11月加入中国共产党。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0396.txt:30-31",
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
        "scope": "第三十三批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复页级 Paddle OCR 可直接证明的面积单位、烈士/护士字形和单条入党残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三十三批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 Paddle OCR 可直接证明的面积单位、烈士/护士字形和单条入党残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：源页仍写作 `加人` 的徐进德条、未逐页核到的其它人物传和 `准海战役` 残留。",
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

    marker = "## 2026-07-04 第三十三批正文残留回源修复"
    memory = f"""
{marker}
- 修复页级 Paddle OCR 直接证明的面积单位、烈士/护士字形和唐贯淮入党残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/中/part01/page_0094.txt`、`page_0103.txt`、`page_0257.txt`、`page_0324.txt`、`page_0388.txt`、`page_0398.txt`、`page_0440.txt`、`page_0467.txt`，`workbench/ocr/paddle_ocr/下/part01/page_0024.txt`、`page_0393.txt`，`workbench/ocr/paddle_ocr/下/part02/page_0396.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓源页仍写作 `加人` 的徐进德条、未逐页核到的其它人物传和 `准海战役` 残留。
- 报告：`output/reports/reader_readability_source_backed_batch33_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
