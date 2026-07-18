# -*- coding: utf-8 -*-
"""Repair civil-affairs and burial OCR residues for batch 411."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOWER_PART1 = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
LOWER_PART2 = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
LOWER_HTML = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL_HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_civil_affairs_burial_batch411_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_civil_affairs_burial_batch411_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_民政殡葬地名社团形近残留补修第四百一十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 民政殡葬地名社团形近残留补修第四百一十一批"

CURRENT_TARGETS = [LOWER_PART1, LOWER_PART2, FULL_SRC, LOWER_HTML, FULL_HTML]
PART1_TARGETS = [LOWER_PART1, FULL_SRC, LOWER_HTML, FULL_HTML]
PART2_TARGETS = [LOWER_PART2, FULL_SRC, LOWER_HTML, FULL_HTML]

REPLACEMENTS: list[tuple[list[Path], str, str, str, str]] = [
    (
        PART1_TARGETS,
        "火化户体",
        "火化尸体",
        "殡葬术语：火化尸体",
        "PaddleOCR 下/part01 page_0054、0055 多处作 `火化尸体`，`户体` 为形近误字。",
    ),
    (
        PART1_TARGETS,
        "化户体655具",
        "化尸体655具",
        "跨行残留：火化尸体655具",
        "`workbench/ocr/paddle_ocr/下/part01/page_0054.txt:21` 作 `化尸体655具`，源稿换行后残留 `化户体655具`。"
    ),
    (
        PART1_TARGETS,
        "化户体1964具",
        "化尸体1964具",
        "跨行残留：火化尸体1964具",
        "`workbench/ocr/paddle_ocr/下/part01/page_0054.txt:25` 作 `化尸体1964具`，源稿换行后残留 `化户体1964具`。"
    ),
    (
        PART1_TARGETS,
        "平攻20多万座",
        "平坟20多万座",
        "殡葬术语：平坟",
        "`workbench/ocr/paddle_ocr/下/part01/page_0054.txt:28` 作 `平坟20多万座`。",
    ),
    (
        PART1_TARGETS,
        "户体火化后",
        "尸体火化后",
        "殡葬术语：尸体火化后",
        "`workbench/ocr/paddle_ocr/下/part01/page_0055.txt:14` 作 `尸体火化后`。",
    ),
    (
        PART1_TARGETS,
        "砌攻头",
        "砌坟头",
        "殡葬术语：砌坟头",
        "`workbench/ocr/paddle_ocr/下/part01/page_0055.txt:14` 作 `砌坟头`。",
    ),
    (
        PART1_TARGETS,
        "攻墓，占地",
        "坟墓，占地",
        "殡葬术语：坟墓",
        "`workbench/ocr/paddle_ocr/下/part01/page_0055.txt:15` 作 `坟墓，占地`。",
    ),
    (
        PART1_TARGETS,
        "零星攻墓",
        "零星坟墓",
        "殡葬术语：零星坟墓",
        "`workbench/ocr/paddle_ocr/下/part01/page_0055.txt:21` 作 `零星坟墓`。",
    ),
    (
        PART1_TARGETS,
        "门牌人手清理",
        "门牌入手清理",
        "地名管理术语：入手清理",
        "`workbench/ocr/paddle_ocr/下/part01/page_0056.txt:34` 作 `门牌入手清理`。",
    ),
    (
        PART1_TARGETS,
        "社团管理于部",
        "社团管理干部",
        "社团管理术语：干部",
        "`workbench/ocr/paddle_ocr/下/part01/page_0058.txt:4` 作 `社团管理干部`，同章前文亦作 `社团管理干部培训班`。",
    ),
    (
        PART1_TARGETS,
        "信访工作受到干忧",
        "信访工作受到干扰",
        "信访术语：受到干扰",
        "同页同类句 `workbench/ocr/paddle_ocr/下/part01/page_0059.txt:21` 作 `信访工作受到干扰`，语义亦为干扰。",
    ),
    (
        PART1_TARGETS,
        "户体皆不准搬走",
        "尸体皆不准搬走",
        "抗战遇害语境：尸体",
        "遇害后遗体语境；OCR 汇总同误作 `户体`，本处按上下文和同批尸体术语精确修复。",
    ),
    (
        PART2_TARGETS,
        "死后移动户体",
        "死后移动尸体",
        "民俗术语：移动尸体",
        "`workbench/ocr/paddle_ocr/下/part02/page_0278.txt:29` 作 `死后移动尸体`。",
    ),
    (
        PART2_TARGETS,
        "人死后把户体装入棺材叫入。此后其子侄每天早晚到土地庙为亡人烧寞钱，俗称",
        "人死后把尸体装入棺材叫入殓。此后其子侄每天早晚到土地庙为亡人烧冥钱，俗称",
        "丧葬术语：入殓、冥钱",
        "`workbench/ocr/paddle_ocr/下/part02/page_0290.txt:13` 作 `把尸体装入棺材叫入殓`、`烧冥钱`。",
    ),
    (
        PART2_TARGETS,
        "火化户体已成为社会新习俗",
        "火化尸体已成为社会新习俗",
        "丧葬改革术语：火化尸体",
        "`workbench/ocr/paddle_ocr/下/part02/page_0290.txt:21` 作 `火化尸体已成为社会新习俗`。",
    ),
    (
        PART2_TARGETS,
        "放户体的门板",
        "放尸体的门板",
        "方言条目：放尸体的门板",
        "下册 part02 现行正文同条已作 `放尸体的门板`；全书汇总残留 `放户体` 为同步漏改。",
    ),
]

EVIDENCE_REFS = [
    ("workbench/ocr/paddle_ocr/下/part01/page_0054.txt", [6, 10, 21, 25, 28]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0055.txt", [10, 14, 15, 21]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0056.txt", [34]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0057.txt", [21, 22]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0058.txt", [4]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0059.txt", [5, 21]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0278.txt", [29]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0290.txt", [13, 21]),
    ("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md", [16248]),
]

RESIDUES = [
    "户体",
    "平攻",
    "攻墓",
    "砌攻头",
    "门牌人手清理",
    "社团管理于部",
    "干忧",
    "烧寞钱",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_one(path: Path, old: str, new: str, label: str, basis: str) -> dict[str, object]:
    text = read(path)
    old_count = text.count(old)
    if old_count:
        path.write_text(text.replace(old, new), encoding="utf-8")
        status = "fixed"
    elif new in text:
        status = "already_fixed"
    else:
        status = "not_present"
    after = read(path)
    return {
        "path": rel(path),
        "label": label,
        "basis": basis,
        "status": status,
        "fixed": old_count,
        "new_hits": after.count(new),
    }


def evidence_lines() -> list[str]:
    out: list[str] = []
    for rel_path, nums in EVIDENCE_REFS:
        path = ROOT / rel_path
        if not path.exists():
            out.append(f"{rel_path}: missing")
            continue
        lines = read(path).splitlines()
        for num in nums:
            if 1 <= num <= len(lines):
                out.append(f"{rel_path}:{num}: {lines[num - 1].strip()}")
    return out


def residue_counts() -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for path in CURRENT_TARGETS:
        if path.exists():
            text = read(path)
            out[rel(path)] = {needle: text.count(needle) for needle in RESIDUES}
    return out


def write_report(results: list[dict[str, object]], residues: dict[str, dict[str, int]]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# 民政殡葬地名社团形近残留补修 batch411",
        "",
        f"- 生成时间：{now}",
        "- 范围：下册 part01/part02 现行正文源稿、全书正文汇总、当前下册 reader、当前全书 reader。",
        "- 修复：精确短语级补修 `户体/尸体`、`攻/坟`、`人手/入手`、`于部/干部`、`干忧/干扰` 等残留。",
        "- 跳过：OCR 原始文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        if item["status"] == "not_present":
            continue
        lines.append(
            f"- `{item['path']}`：{item['label']}，状态 {item['status']}，"
            f"本次替换 {item['fixed']} 处，新文本命中 {item['new_hits']}。依据：{item['basis']}"
        )
    lines.extend(["", "## 证据摘录"])
    for hit in evidence_lines():
        lines.append(f"- {hit}")
    lines.extend(["", "## 残留复扫"])
    for path, counts in residues.items():
        shown = ", ".join(f"{key}={value}" for key, value in counts.items())
        lines.append(f"- `{path}`：{shown}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps(
            {"time": now, "results": results, "evidence": evidence_lines(), "residues": residues},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 依据下册 PaddleOCR `part01/page_0054-0059.txt`、`part02/page_0278.txt`、`page_0290.txt` 及现行正文互证，补修民政、殡葬、地名、社团、信访和民俗段落的精确形近残留：`户体 -> 尸体`、`平攻/攻墓/砌攻头 -> 平坟/坟墓/砌坟头`、`门牌人手清理 -> 门牌入手清理`、`社团管理于部 -> 社团管理干部`、`信访工作受到干忧 -> 信访工作受到干扰`。
- 同批补修丧葬民俗句 `人死后把户体装入棺材叫入。...烧寞钱 -> 人死后把尸体装入棺材叫入殓。...烧冥钱`；`户体皆不准搬走 -> 尸体皆不准搬走` 依据遇害后遗体语境和同批尸体术语精确修复。
- 修复范围为下册 part01/part02 现行正文源稿、全书正文汇总、当前下册/全书 reader；未处理 OCR 原始文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_civil_affairs_burial_batch411_20260708.md`；进度：`output/reports/progress/20260708_民政殡葬地名社团形近残留补修第四百一十一批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    if next_start < 0:
        MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    else:
        MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + old[next_start:], encoding="utf-8")


def main() -> None:
    results = []
    for paths, old, new, label, basis in REPLACEMENTS:
        for path in paths:
            results.append(apply_one(path, old, new, label, basis))
    residues = residue_counts()
    write_report(results, residues)
    update_memory()
    changed = sum(int(item["fixed"]) for item in results)
    print(json.dumps({"changed": changed, "report": str(REPORT), "progress": str(PROGRESS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
