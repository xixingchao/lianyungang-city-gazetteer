# -*- coding: utf-8 -*-
"""Repair verified private-name vehicle registration OCR residue."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MID_SRC = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
EVIDENCE = ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0308.txt"
REPORT = ROOT / "output" / "reports" / "verified_private_car_registration_batch393_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_private_car_registration_batch393_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_私人名义入户公车残留补修第三百九十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 私人名义入户公车残留补修第三百九十三批"

OLD_SRC = """1989年起，全市县以上单位全面实行控制指标管理。11月，由市控办牵头，组织有关
人名义人户的公车62辆，决定将查出的车辆全部予以没收，罚没款150余万元。"""
NEW_SRC = """1989年起，全市县以上单位全面实行控制指标管理。11月，由市控办牵头，组织有关
部门对全市违纪购车的情况进行检查，重点检查以私人名义入户公车的问题，共查出以私
人名义入户的公车62辆，决定将查出的车辆全部予以没收，罚没款150余万元。"""
OLD_MID_READER = """<p>1989年起，全市县以上单位全面实行控制指标管理。11月，由市控办牵头，组织有关</p><p>人名义人户的公车62辆，决定将查出的车辆全部予以没收，罚没款150余万元。</p>"""
NEW_MID_READER = """<p>1989年起，全市县以上单位全面实行控制指标管理。11月，由市控办牵头，组织有关</p><p>部门对全市违纪购车的情况进行检查，重点检查以私人名义入户公车的问题，共查出以私</p><p>人名义入户的公车62辆，决定将查出的车辆全部予以没收，罚没款150余万元。</p>"""
OLD_FULL_READER = "<p>1989年起，全市县以上单位全面实行控制指标管理。11月，由市控办牵头，组织有关人名义人户的公车62辆，决定将查出的车辆全部予以没收，罚没款150余万元。</p>"
NEW_FULL_READER = "<p>1989年起，全市县以上单位全面实行控制指标管理。11月，由市控办牵头，组织有关部门对全市违纪购车的情况进行检查，重点检查以私人名义入户公车的问题，共查出以私人名义入户的公车62辆，决定将查出的车辆全部予以没收，罚没款150余万元。</p>"

FIXES = [
    (MID_SRC, OLD_SRC, NEW_SRC, "中册源稿"),
    (FULL_SRC, OLD_SRC, NEW_SRC, "全书正文汇总"),
    (MID_READER, OLD_MID_READER, NEW_MID_READER, "中册 reader"),
    (FULL_READER, OLD_FULL_READER, NEW_FULL_READER, "全书 reader"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needles: tuple[str, ...]) -> list[str]:
    hits = []
    for i, line in enumerate(read(path).splitlines(), 1):
        if any(needle in line for needle in needles):
            hits.append(f"{i}: {line.strip()}")
    return hits


def evidence_lines() -> list[str]:
    lines = read(EVIDENCE).splitlines()
    return [f"{i}: {lines[i - 1].strip()}" for i in range(18, 21)]


def apply_fix(path: Path, old: str, new: str, label: str) -> dict[str, object]:
    text = read(path)
    old_count = text.count(old)
    if old_count == 1:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        status = "fixed"
    elif old_count == 0 and new in text:
        status = "already_fixed"
    else:
        raise RuntimeError(
            f"{rel(path)} expected one old hit or existing new text for {label}, "
            f"got old={old_count}, new={text.count(new)}"
        )
    after = read(path)
    return {
        "path": rel(path),
        "label": label,
        "status": status,
        "fixed": old_count,
        "remaining_bad": after.count("人名义人户"),
        "new_hits": after.count("以私人名义入户"),
    }


def main() -> None:
    results = [apply_fix(path, old, new, label) for path, old, new, label in FIXES]
    residues = {
        rel(path): line_hits(path, ("人名义人户", "以私人名义入户", "违纪购车"))
        for path, _old, _new, _label in FIXES
    }
    evidence = evidence_lines()

    lines = [
        "# 私人名义入户公车残留补修 batch393",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：中册源稿、全书正文汇总、当前中册 reader、当前全书 reader。",
        "- 依据：新版页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0308.txt` 第 18-20 行。",
        "- 修复：补回 `组织有关部门对全市违纪购车的情况进行检查，重点检查以私人名义入户公车的问题，共查出以私人名义入户的公车62辆`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(
            f"- `{item['path']}`：{item['label']}，状态 {item['status']}，本次修复 {item['fixed']} 处；"
            f"剩余 `人名义人户` {item['remaining_bad']}，`以私人名义入户` 命中 {item['new_hits']}。"
        )

    lines.extend(["", "## 页级 OCR 证据"])
    for hit in evidence:
        lines.append(f"- {hit}")

    lines.extend(["", "## 复扫摘录"])
    for path, hits in residues.items():
        lines.append(f"### {path}")
        if not hits:
            lines.append("- 无。")
        else:
            for hit in hits:
                lines.append(f"- {hit}")

    report = "\n".join(lines) + "\n"
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results, "evidence": evidence, "residues": residues}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(report, encoding="utf-8")

    block = f"""{MARKER}

- 依据中册新版页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0308.txt` 第 18-20 行，补修社会集团购买力控购段高风险残留，共 4 处。
- 修复现行中册源稿、全书正文汇总、当前中册 reader、当前全书 reader 中 `组织有关人名义人户的公车62辆`，补回为 `组织有关部门对全市违纪购车的情况进行检查，重点检查以私人名义入户公车的问题，共查出以私人名义入户的公车62辆`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作 `人 -> 入` 全局替换；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_private_car_registration_batch393_20260708.md`；进度：`output/reports/progress/20260708_私人名义入户公车残留补修第三百九十三批.md`。
"""
    old_mem = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old_mem.find(MARKER)
    if start < 0:
        MEMORY.write_text(old_mem.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    else:
        next_start = old_mem.find("\n## ", start + 1)
        MEMORY.write_text(old_mem[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old_mem[next_start:]), encoding="utf-8")

    print("results=" + json.dumps(results, ensure_ascii=False))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
