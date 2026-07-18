# -*- coding: utf-8 -*-
"""Repair source-backed factory-name and quote residues for batch 396."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_quote_batch396_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_quote_batch396_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名与六通一平引号残留补修第三百九十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名与六通一平引号残留补修第三百九十六批"

ALL = [MID1, FULL_SRC, MID_READER, FULL_READER]

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    (ALL, "电子机械广", "电子机械厂", "灌云县酒厂晶体管车间后独立为县电子机械厂"),
    (ALL, "连珠机械广", "连珠机械厂", "黑龙江连珠机械厂奶粉加工设备"),
    ([MID1, FULL_SRC], "化工机械广投资", "化工机械厂投资", "市化工机械厂投资制氧车间"),
    (ALL, "新浦跃进机械广", "新浦跃进机械厂", "新浦跃进机械厂改名为新浦水泵厂"),
    (ALL, "新浦水泵广划归", "新浦水泵厂划归", "新浦水泵厂划归市机械工业局"),
    (ALL, "船舶修造广", "船舶修造厂", "灌云县船舶修造厂"),
    (ALL, "等六通一平”工程", "等“六通一平”工程", "开发区六通一平工程左引号"),
    (ALL, "范围内的六通一平”及", "范围内的“六通一平”及", "起步区六通一平左引号"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/中/part01/page_0093.txt", [24]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0113.txt", [8]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0154.txt", [29]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0211.txt", [15, 16]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0203.txt", [30]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0419.txt", [21]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0431.txt", [35]),
]

RESIDUES = [
    "电子机械广",
    "连珠机械广",
    "化工机械广投资",
    "新浦跃进机械广",
    "新浦水泵广划归",
    "船舶修造广",
    "等六通一平”工程",
    "范围内的六通一平”及",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_one(path: Path, old: str, new: str, label: str) -> dict[str, object]:
    text = read(path)
    old_count = text.count(old)
    if old_count:
        text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
        status = "fixed"
    elif new in text:
        status = "already_fixed"
    else:
        status = "not_present"
    after = read(path)
    return {"path": rel(path), "label": label, "status": status, "fixed": old_count, "new_hits": after.count(new)}


def evidence_lines() -> list[str]:
    out: list[str] = []
    for rel_path, nums in OCR_EVIDENCE:
        path = ROOT / rel_path
        lines = read(path).splitlines()
        for num in nums:
            if 1 <= num <= len(lines):
                out.append(f"{rel_path}:{num}: {lines[num - 1].strip()}")
    return out


def residue_counts() -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for path in ALL:
        text = read(path)
        out[rel(path)] = {needle: text.count(needle) for needle in RESIDUES}
    return out


def write_report(results: list[dict[str, object]], residues: dict[str, dict[str, int]]) -> None:
    lines = [
        "# 厂名与六通一平引号残留补修 batch396",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行中册正文源稿、全书正文汇总、当前中册/全书 reader。",
        "- 修复：可由页级 PaddleOCR 证实的 `广 -> 厂` 厂名残留，以及开发区 `六通一平` 两处缺左引号。",
        "- 保留：未逐页证实的 `市机械修配广`、南小区 `水泵广` 等零散命中留待后续核对；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(f"- `{item['path']}`：{item['label']}，状态 {item['status']}，本次替换 {item['fixed']} 处，新文本命中 {item['new_hits']}。")
    lines.extend(["", "## OCR 证据摘录"])
    for hit in evidence_lines():
        lines.append(f"- {hit}")
    lines.extend(["", "## 残留复扫"])
    for path, counts in residues.items():
        shown = ", ".join(f"{key}={value}" for key, value in counts.items())
        lines.append(f"- `{path}`：{shown}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results, "evidence": evidence_lines(), "residues": residues}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 依据中册 PaddleOCR page_0093、0113、0154、0203、0211、0419、0431，补修可证厂名形近残留与 `“六通一平”` 缺左引号。
- 修复范围为现行中册正文源稿、全书正文汇总、当前中册/全书 reader；未逐页证实的 `市机械修配广`、南小区 `水泵广` 等保留待核。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_factory_quote_batch396_20260708.md`；进度：`output/reports/progress/20260708_厂名与六通一平引号残留补修第三百九十六批.md`。
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
    results: list[dict[str, object]] = []
    for paths, old, new, label in REPLACEMENTS:
        for path in paths:
            results.append(apply_one(path, old, new, label))
    residues = residue_counts()
    write_report(results, residues)
    update_memory()
    print("results=" + json.dumps(results, ensure_ascii=False))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
