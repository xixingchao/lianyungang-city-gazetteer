# -*- coding: utf-8 -*-
"""Repair a twelfth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch11_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch11_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十二批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "机关干部文化学校",
        "机关于部文化学校",
        "机关干部文化学校",
        "workbench/ocr/paddle_ocr/中/part02/page_0442.txt:35",
    ),
    (
        "要求干部系统地学点马列主义",
        "要求于部系统地学点马列主义",
        "要求干部系统地学点马列主义",
        "workbench/ocr/paddle_ocr/中/part02/page_0443.txt:29",
    ),
    (
        "轮训干部11400多人次",
        "轮训于部11400多人次",
        "轮训干部11400多人次",
        "workbench/ocr/paddle_ocr/中/part02/page_0446.txt:10",
    ),
    (
        "11名干部参加二年以上学习",
        "11名于部参加二年以上的学习",
        "11名干部参加二年以上的学习",
        "workbench/ocr/paddle_ocr/中/part02/page_0446.txt:18",
    ),
    (
        "党员干部以权谋私",
        "党员于部以权谋私",
        "党员干部以权谋私",
        "workbench/ocr/paddle_ocr/中/part02/page_0448.txt:14",
    ),
    (
        "党员干部调离审评制度",
        "党员于部调离审评制度",
        "党员干部调离审评制度",
        "workbench/ocr/paddle_ocr/中/part02/page_0448.txt:18",
    ),
    (
        "调整领导骨干",
        "调整领导骨于",
        "调整领导骨干",
        "workbench/ocr/paddle_ocr/中/part02/page_0449.txt:36",
    ),
    (
        "老干部局归口市委领导",
        "老于部局归口市委领导",
        "老干部局归口市委领导",
        "workbench/ocr/paddle_ocr/中/part02/page_0451.txt:9",
    ),
    (
        "基层干部分批参加",
        "基层于部分批参加",
        "基层干部分批参加",
        "workbench/ocr/paddle_ocr/中/part02/page_0469.txt:5",
    ),
    (
        "基层干部分批参加-换行版",
        "基层于部分批\n参加四省七市民盟工作经验交流会",
        "基层干部分批\n参加四省七市民盟工作经验交流会",
        "workbench/ocr/paddle_ocr/中/part02/page_0469.txt:5",
    ),
    (
        "专职宣传干部24人",
        "专职宣传于部24人",
        "专职宣传干部24人",
        "workbench/ocr/paddle_ocr/下/part01/page_0149.txt:15",
    ),
    (
        "上调学习的干部有343人",
        "上调学习的于部有343人",
        "上调学习的干部有343人",
        "workbench/ocr/paddle_ocr/下/part01/page_0203.txt:40",
    ),
    (
        "学习的干部共有3773人次",
        "学习的千部共有3773人次",
        "学习的干部共有3773人次",
        "workbench/ocr/paddle_ocr/下/part01/page_0203.txt:42",
    ),
    (
        "649名干部在市党校干校轮训",
        "有649名部在市党校、干校轮训",
        "有649名干部在市党校、干校轮训",
        "workbench/ocr/paddle_ocr/下/part01/page_0203.txt:45",
    ),
    (
        "机关干部和基层领导参加学习",
        "机关千部和基层领导参加学习",
        "机关干部和基层领导参加学习",
        "workbench/ocr/paddle_ocr/下/part01/page_0203.txt:47",
    ),
    (
        "参加学习的干部",
        "参加学习的千部",
        "参加学习的干部",
        "workbench/ocr/paddle_ocr/下/part01/page_0203.txt:49",
    ),
    (
        "15760名干部参加",
        "15760名于部参加",
        "15760名干部参加",
        "workbench/ocr/paddle_ocr/下/part01/page_0203.txt:54",
    ),
    (
        "中青年干部到中央省委党校",
        "中青年于部到中央、省委党校",
        "中青年干部到中央、省委党校",
        "workbench/ocr/paddle_ocr/下/part01/page_0203.txt:56",
    ),
    (
        "文艺干部",
        "文艺于部",
        "文艺干部",
        "workbench/ocr/paddle_ocr/下/part02/page_0046.txt:25",
    ),
    (
        "基层宣传干部",
        "基层宣传于部",
        "基层宣传干部",
        "workbench/ocr/paddle_ocr/下/part02/page_0143.txt:9",
    ),
    (
        "新闻干部",
        "新闻于部",
        "新闻干部",
        "workbench/ocr/paddle_ocr/下/part02/page_0161.txt:7",
    ),
    (
        "药政管理专职干部",
        "药政管理专职于部",
        "药政管理专职干部",
        "workbench/ocr/paddle_ocr/下/part02/page_0197.txt:17",
    ),
    (
        "干部疗养院",
        "于部疗养院",
        "干部疗养院",
        "workbench/ocr/paddle_ocr/下/part02/page_0206.txt:6",
    ),
]

SKIPPED = [
    "`党政机关于部经商办企业` 仅在正文汇总残留，本批未取得同页强证据，暂缓。",
    "继续避免 `于部` 全局替换，只处理页级 PaddleOCR 明确支撑的长上下文问题。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["changed"] for item in targets)
    payload = {
        "time": now,
        "scope": "第十二批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十二批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 PaddleOCR 明确支撑的长上下文问题。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项"])
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    lines.extend(["", "## 暂缓"])
    for item in SKIPPED:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-04 第十二批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围集中在 `于部/千部/骨于` 误识别为 `干部/骨干` 的长上下文残留，覆盖政党、人事、文化、新闻、卫生等章节。
- 依据：`output/reports/reader_readability_source_backed_batch11_20260704.md`。
- 暂缓：未取得同页强证据的 `党政机关于部经商办企业` 等残留。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第十二批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
