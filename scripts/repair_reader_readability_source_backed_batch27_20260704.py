# -*- coding: utf-8 -*-
"""Twenty-seventh source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch27_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch27_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十七批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "妇女支前淮海战役前委",
        "old": "准海战役前委《淮海全党全民总动员支前方案》",
        "new": "淮海战役前委《淮海全党全民总动员支前方案》",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0332.txt:36-38",
    },
    {
        "label": "淮海妇救总会与告淮海妇联书",
        "old": "准海妇救总会发出《告准海妇联书》",
        "new": "淮海妇救总会发出《告淮海妇联书》",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0332.txt:37-38",
    },
    {
        "label": "妇女支援淮海前线",
        "old": "支援准海前线",
        "new": "支援淮海前线",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0332.txt:39-40",
    },
    {
        "label": "海州师范校友烈士",
        "old": "20多位烈土",
        "new": "20多位烈士",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0390.txt:16-18",
    },
    {
        "label": "淮海小戏定名",
        "old": "为其起名“准海小戏”",
        "new": "为其起名“淮海小戏”",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:3-5",
    },
    {
        "label": "淮海小戏定名断行",
        "old": "为其起名“准\n海小戏”",
        "new": "为其起名“淮\n海小戏”",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:3-5",
    },
    {
        "label": "淮海戏雏形",
        "old": "准海戏的锥形",
        "new": "淮海戏的雏形",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:7-9",
    },
    {
        "label": "淮海戏打门头辞",
        "old": "准海戏出现了“打门头辞”",
        "new": "淮海戏出现了“打门头辞”",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:11-12",
    },
    {
        "label": "淮海地区抗日民主政府",
        "old": "建立准海地区抗日民主政府",
        "new": "建立淮海地区抗日民主政府",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:28-31",
    },
    {
        "label": "淮海戏创作和演出",
        "old": "参加准海戏的创作和演出",
        "new": "参加淮海戏的创作和演出",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:32-34",
    },
    {
        "label": "剔除淮海戏封建糟粕",
        "old": "剔除准海戏中的封建糟粕",
        "new": "剔除淮海戏中的封建糟粕",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:33-34",
    },
    {
        "label": "剔除淮海戏封建糟粕断行",
        "old": "剔除准海戏中的封建糟\n粕",
        "new": "剔除淮海戏中的封建糟\n粕",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:33-34",
    },
    {
        "label": "淮海戏专业表演队伍",
        "old": "的海戏专业表演队伍",
        "new": "的淮海戏专业表演队伍",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:39-42",
    },
    {
        "label": "淮海戏专业表演队伍重复前缀清理",
        "old": "淮淮淮海戏专业表演队伍",
        "new": "淮海戏专业表演队伍",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:39-42",
    },
    {
        "label": "灌云县淮海剧团",
        "old": "灌云县准海剧团",
        "new": "灌云县淮海剧团",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:47-48; workbench/ocr/paddle_ocr/下/part02/page_0036.txt:32-35",
    },
    {
        "label": "市淮海剧团成立",
        "old": "市准海剧团成立后",
        "new": "市淮海剧团成立后",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0034.txt:19-21",
    },
    {
        "label": "文工团淮海戏队",
        "old": "准海戏三个队",
        "new": "淮海戏三个队",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0035.txt:15-17",
    },
    {
        "label": "淮北盐场淮海剧团名称",
        "old": "淮北盐场准海剧团",
        "new": "淮北盐场淮海剧团",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0035.txt:27-31",
    },
    {
        "label": "盐场淮海剧团称谓",
        "old": "盐场准海剧团",
        "new": "盐场淮海剧团",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0035.txt:29-31",
    },
    {
        "label": "县淮海剧团重建",
        "old": "重建县准海剧团",
        "new": "重建县淮海剧团",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0036.txt:32-35",
    },
    {
        "label": "东海县淮海戏小组",
        "old": "沭阳县准海戏小组",
        "new": "沭阳县淮海戏小组",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0037.txt:3-6",
    },
    {
        "label": "淮海戏演出区域",
        "old": "拓宽了准海戏的演出区域，扩大了准海戏的观众面",
        "new": "拓宽了淮海戏的演出区域，扩大了淮海戏的观众面",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0034.txt:8-10",
    },
    {
        "label": "淮海戏演出区域断行",
        "old": "拓宽了准海戏的演\n出区域，扩大了准海戏的观众面",
        "new": "拓宽了淮海戏的演\n出区域，扩大了淮海戏的观众面",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0034.txt:8-10",
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
        residuals = [
            item["old"]
            for item in REPLACEMENTS
            if item["old"] not in item["new"] and item["old"] in verify
        ]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(target["changed"] for target in targets)
    payload = {
        "time": now,
        "scope": "第二十七批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复下册页级 OCR 可直接证明的淮海战役、淮海戏、烈士残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十七批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修下册页级 OCR 可直接证明的淮海战役、淮海戏、烈士残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：未定位页级证据的其它 `准海/烈土/加人/方` 残留。",
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

    marker = "## 2026-07-04 第二十七批正文残留回源修复"
    memory = f"""
{marker}
- 修复下册页级 OCR 直接证明的淮海战役、淮海戏、烈士残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/下/part01/page_0332.txt`、`page_0390.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0027.txt`、`page_0034.txt`、`page_0035.txt`、`page_0036.txt`、`page_0037.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓未定位页级证据的其它 `准海/烈土/加人/方` 残留，不做整书推断替换。
- 报告：`output/reports/reader_readability_source_backed_batch27_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
