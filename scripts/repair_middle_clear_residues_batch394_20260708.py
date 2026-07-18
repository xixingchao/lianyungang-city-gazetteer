# -*- coding: utf-8 -*-
"""Repair source-backed middle-volume residue batch 394."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
MID2 = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
T031_JSON = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T031.json"
TABLE_SITE = ROOT / "output" / "structured_tables" / "index.html"
T031_SCRIPT = ROOT / "scripts" / "verify_t031_building_materials_awards_20260629.py"

REPORT = ROOT / "output" / "reports" / "middle_clear_residues_batch394_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "middle_clear_residues_batch394_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_中册可证清晰残留补修第三百九十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 中册可证清晰残留补修第三百九十四批"

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/中/part01/page_0422.txt", [52, 53, 54]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0423.txt", [16, 17, 18]),
]

REPLACEMENTS: list[tuple[Path, str, str, str]] = []

# Product name: source paragraph, extracted table text, structured table data/site, and verifier script.
for path in [MID1, FULL_SRC, MID_READER, FULL_READER, T031_JSON, TABLE_SITE, T031_SCRIPT]:
    REPLACEMENTS.append((path, "0.4级轻质漂株耐火砖", "0.4级轻质漂珠耐火砖", "漂珠耐火砖产品名"))

# Clear heading and terminology residues.
for path in [MID1, FULL_SRC, MID_READER, FULL_READER]:
    REPLACEMENTS.append((path, "三、实·施", "三、实施", "口岸联检小标题"))
for path in [MID2, FULL_SRC, MID_READER, FULL_READER]:
    REPLACEMENTS.append((path, "客房资信情况", "客户资信情况", "客户资信术语"))

# Development-zone text proven by PaddleOCR pages 0422 and 0423.
REPLACEMENTS.extend(
    [
        (
            MID1,
            "形成以出口创汇支柱产业为龙头的实体集团；发\n之，要以提高经济效益为中心",
            "形成以出口创汇支柱产业为龙头的实体集团；发挥开发区的区位优势和广阔经济腹地的资源优势，辟建出口加工区和保税工业小区。总\n之，要以提高经济效益为中心",
            "开发区八五规划漏句",
        ),
        (
            FULL_SRC,
            "形成以出口创汇支柱产业为龙头的实体集团；发\n之，要以提高经济效益为中心",
            "形成以出口创汇支柱产业为龙头的实体集团；发挥开发区的区位优势和广阔经济腹地的资源优势，辟建出口加工区和保税工业小区。总\n之，要以提高经济效益为中心",
            "开发区八五规划漏句",
        ),
        (
            MID_READER,
            "形成以出口创汇支柱产业为龙头的实体集团；发</p><p>之，要以提高经济效益为中心",
            "形成以出口创汇支柱产业为龙头的实体集团；发挥开发区的区位优势和广阔经济腹地的资源优势，辟建出口加工区和保税工业小区。总</p><p>之，要以提高经济效益为中心",
            "开发区八五规划漏句",
        ),
        (
            FULL_READER,
            "形成以出口创汇支柱产业为龙头的实体集团；发之，要以提高经济效益为中心",
            "形成以出口创汇支柱产业为龙头的实体集团；发挥开发区的区位优势和广阔经济腹地的资源优势，辟建出口加工区和保税工业小区。总之，要以提高经济效益为中心",
            "开发区八五规划漏句",
        ),
        (
            MID1,
            "抓好碳塑料、\n汽车零配件、电线电缆、菲律宾工业园、韩国工业园、氨纶三期工程、电脑芯片、齿轮加工中\n元和10个出口创汇过1000万美元的工业企业。",
            "抓好碳塑料、\n汽车零配件、电线电缆、菲律宾工业园、韩国工业园、氨纶三期工程、电脑芯片、齿轮加工中心等重点工业项目建设，到2000年逐步形成20个产值过亿元、20个实现利税过1000万\n元和10个出口创汇过1000万美元的工业企业。",
            "开发区九五规划断句漏文",
        ),
        (
            FULL_SRC,
            "抓好碳塑料、\n汽车零配件、电线电缆、菲律宾工业园、韩国工业园、氨纶三期工程、电脑芯片、齿轮加工中\n元和10个出口创汇过1000万美元的工业企业。",
            "抓好碳塑料、\n汽车零配件、电线电缆、菲律宾工业园、韩国工业园、氨纶三期工程、电脑芯片、齿轮加工中心等重点工业项目建设，到2000年逐步形成20个产值过亿元、20个实现利税过1000万\n元和10个出口创汇过1000万美元的工业企业。",
            "开发区九五规划断句漏文",
        ),
        (
            MID_READER,
            "<p>汽车零配件、电线电缆、菲律宾工业园、韩国工业园、氨纶三期工程、电脑芯片、齿轮加工中</p><p>元和10个出口创汇过1000万美元的工业企业。</p>",
            "<p>汽车零配件、电线电缆、菲律宾工业园、韩国工业园、氨纶三期工程、电脑芯片、齿轮加工中心等重点工业项目建设，到2000年逐步形成20个产值过亿元、20个实现利税过1000万</p><p>元和10个出口创汇过1000万美元的工业企业。</p>",
            "开发区九五规划断句漏文",
        ),
        (
            FULL_READER,
            "抓好碳塑料、汽车零配件、电线电缆、菲律宾工业园、韩国工业园、氨纶三期工程、电脑芯片、齿轮加工中元和10个出口创汇过1000万美元的工业企业。",
            "抓好碳塑料、汽车零配件、电线电缆、菲律宾工业园、韩国工业园、氨纶三期工程、电脑芯片、齿轮加工中心等重点工业项目建设，到2000年逐步形成20个产值过亿元、20个实现利税过1000万元和10个出口创汇过1000万美元的工业企业。",
            "开发区九五规划断句漏文",
        ),
    ]
)

RESIDUES = [
    "漂株",
    "实·施",
    "客房资信",
    "齿轮加工中元和",
    "齿轮加工中\n元和",
    "实体集团；发之",
    "实体集团；发\n之",
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
        raise RuntimeError(f"{rel(path)} missing old/new text for {label}")
    after = read(path)
    return {
        "path": rel(path),
        "label": label,
        "status": status,
        "fixed": old_count,
        "new_hits": after.count(new),
    }


def line_hits(path: Path, needles: list[str]) -> list[str]:
    hits: list[str] = []
    for i, line in enumerate(read(path).splitlines(), 1):
        if any(needle in line for needle in needles):
            hits.append(f"{i}: {line.strip()}")
    return hits[:20]


def evidence_lines() -> list[str]:
    out: list[str] = []
    for rel_path, nums in OCR_EVIDENCE:
        path = ROOT / rel_path
        lines = read(path).splitlines()
        for num in nums:
            if 1 <= num <= len(lines):
                out.append(f"{rel_path}:{num}: {lines[num - 1].strip()}")
    return out


def write_report(results: list[dict[str, object]], residues: dict[str, dict[str, int]]) -> None:
    evidence = evidence_lines()
    lines = [
        "# 中册可证清晰残留补修 batch394",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：中册正文源稿、全书正文汇总、当前中册/全书 reader、T031 结构化表格数据与同步脚本。",
        "- 修复：漂珠耐火砖、口岸联检小标题、客户资信、开发区规划漏句与断词残留。",
        "- 依据：同卷既有正文用语、PaddleOCR `page_0422.txt` 与 `page_0423.txt` 可见文本。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(
            f"- `{item['path']}`：{item['label']}，状态 {item['status']}，本次替换 {item['fixed']} 处，新文本命中 {item['new_hits']}。"
        )
    lines.extend(["", "## OCR 证据摘录"])
    for hit in evidence:
        lines.append(f"- {hit}")
    lines.extend(["", "## 残留复扫"])
    for path, counts in residues.items():
        shown = ", ".join(f"{k}={v}" for k, v in counts.items())
        lines.append(f"- `{path}`：{shown}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps(
            {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "results": results,
                "evidence": evidence,
                "residues": residues,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 本批补修中册清晰可证残留，覆盖 `漂株 -> 漂珠`、`三、实·施 -> 三、实施`、`客房资信情况 -> 客户资信情况`，并据 PaddleOCR 补回开发区“八五”“九五”规划两处漏句/断词。
- 开发区依据：`workbench/ocr/paddle_ocr/中/part01/page_0422.txt` 第 52-54 行、`workbench/ocr/paddle_ocr/中/part01/page_0423.txt` 第 16-18 行；其中 `齿轮加工中/元和10个` 修为 `齿轮加工中心等重点工业项目建设...万元和10个...`。
- 同步范围包括现行中册源稿、全书正文汇总、当前中册/全书 reader、`LYG-中-T031.json`、`output/structured_tables/index.html` 与 `scripts/verify_t031_building_materials_awards_20260629.py`；未处理 OCR 源文件、backup、obsolete、历史交付包。
- 未打开、展示或嵌入图片；报告：`output/reports/middle_clear_residues_batch394_20260708.md`；进度：`output/reports/progress/20260708_中册可证清晰残留补修第三百九十四批.md`。
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
    results = [apply_one(path, old, new, label) for path, old, new, label in REPLACEMENTS]
    residue_paths = [MID1, MID2, FULL_SRC, MID_READER, FULL_READER, T031_JSON, TABLE_SITE, T031_SCRIPT]
    residues = {rel(path): {needle: read(path).count(needle) for needle in RESIDUES} for path in residue_paths}
    write_report(results, residues)
    update_memory()
    print("results=" + json.dumps(results, ensure_ascii=False))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
