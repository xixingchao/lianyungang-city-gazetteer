# -*- coding: utf-8 -*-
"""Repair source-backed cross-volume Shu-name leftovers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_crossvolume_shu_batch362_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_crossvolume_shu_batch362_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总跨卷沭临沭残留补修第三百六十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总跨卷沭临沭残留补修第三百六十二批"

FULL_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
UP_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
UP_PART02 = ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md"

CHECK_FILES = [
    FULL_SUMMARY,
    UP_SUMMARY,
    UP_PART02,
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
]

CHECK_TERMS = [
    "新述河",
    "新沐河",
    "述南",
    "述北",
    "沐南",
    "沐北",
    "临沐县",
    "沂述",
    "沂沐",
    "人海口",
    "沐阳县",
]


@dataclass(frozen=True)
class Replacement:
    path: Path
    old: str
    new: str
    evidence: str


REPLACEMENTS = [
    Replacement(FULL_SUMMARY, "五、新述河柴地归属争议", "五、新沭河柴地归属争议", "上 part01 merged OCR lines 14674-14675 明确为“新沭河柴地”“新沭河北侧”。"),
    Replacement(FULL_SUMMARY, "新沐河北侧", "新沭河北侧", "上 part01 merged OCR lines 14674-14675 明确为“新沭河北侧”。"),
    Replacement(FULL_SUMMARY, "1975年石安河建成，部分农田划归沐南灌区", "1975年石安河建成，部分农田划归沭南灌区", "上 part03 merged OCR line 2776 明确为“沭南灌区”。"),
    Replacement(FULL_SUMMARY, "输水渠6.8公里、述北\n第一截洪沟", "输水渠6.8公里、沭北\n第一截洪沟", "上 part03 merged OCR lines 5105、5113、5118 明确为“沭北第一截洪沟”。"),
    Replacement(FULL_SUMMARY, "配套续建述北第一截洪沟", "配套续建沭北第一截洪沟", "上 part03 merged OCR line 5113 明确为“配套续建沭北第一截洪沟”。"),
    Replacement(FULL_SUMMARY, "述北第一截洪沟底宽", "沭北第一截洪沟底宽", "上 part03 merged OCR line 5118 明确为“沭北第一截洪沟底宽”。"),
    Replacement(FULL_SUMMARY, "为加强新述河、青口河、朱稽河、东门河的水情测报，增设黄川（新沐河）", "为加强新沭河、青口河、朱稽河、东门河的水情测报，增设黄川（新沭河）", "上 part03 merged OCR line 5356 明确为“新沭河”“黄川（新沭河）”。"),
    Replacement(FULL_SUMMARY, "岳庄（新沐河）", "岳庄（新沭河）", "上 part03 merged OCR line 5356 同段水文站语境为新沭河。"),
    Replacement(FULL_SUMMARY, "乾隆十二年（1747年），新述河暴涨", "乾隆十二年（1747年），新沭河暴涨", "上 part03 merged OCR line 6015 明确为“新沭河暴涨”。"),
    Replacement(FULL_SUMMARY, "新沂河、新述河、蕃薇河等主要河道堤防", "新沂河、新沭河、蔷薇河等主要河道堤防", "上 part03 merged OCR line 6022 明确为“新沂河、新沭河、蔷薇河”。"),
    Replacement(FULL_SUMMARY, "述南、述北灌区", "沭南、沭北灌区", "上 part03 merged OCR line 6027 明确为“沭南、沭北灌区”。"),
    Replacement(FULL_SUMMARY, "临沐县种鸡场", "临沭县种鸡场", "上 part03 merged OCR line 6276 明确为“临沭县种鸡场”。"),
    Replacement(FULL_SUMMARY, "白塔埠的新述河边", "白塔埠的新沭河边", "中册 source 第三十卷至第四十二卷（中part02） line 2121 为“新沭河边”。"),
    Replacement(FULL_SUMMARY, "沐阳县20个供销社，山东省临沐县8个供销社", "沭阳县20个供销社，山东省临沭县8个供销社", "中册 source 第三十卷至第四十二卷（中part02） line 7418 为“沭阳县”“临沭县”。"),
    Replacement(FULL_SUMMARY, "新述河扩大工程：1972年开工", "新沭河扩大工程：1972年开工", "中册 source 第三十卷至第四十二卷（中part02） line 15776 为“新沭河扩大工程”。"),
    Replacement(FULL_SUMMARY, "新述河工程662万元", "新沭河工程662万元", "中册 source 第三十卷至第四十二卷（中part02） line 24651 为“新沭河工程662万元”。"),
    Replacement(FULL_SUMMARY, "临沐县法院院长", "临沭县法院院长", "下册 source 第五十二卷至第六十卷及附录（下part02） line 17693 为“临沭县法院院长”。"),
    Replacement(FULL_SUMMARY, "调临沐县时宅子园艺场", "调临沭县时宅子园艺场", "下册 source 第五十二卷至第六十卷及附录（下part02） line 17693 为“临沭县时宅子园艺场”。"),
    Replacement(FULL_SUMMARY, "沂述河、善后河", "沂沭河、善后河", "下册 source 第四十三卷至第五十一卷（下part01） line 9844 为“沂沭河、善后河”。"),
    Replacement(FULL_SUMMARY, "灌云段的新沐河筑堤", "灌云段的新沭河筑堤", "下册 source 第四十三卷至第五十一卷（下part01） line 24689 为“新沭河筑堤”。"),
    Replacement(FULL_SUMMARY, "1952年新沐河\n开通", "1952年新沭河\n开通", "下册 source 第四十三卷至第五十一卷（下part01） lines 24689-24690 为“1952年新沭河/开通”。"),
    Replacement(FULL_SUMMARY, "挖疏浚新沐河等河道50余条", "挖疏浚新沭河等河道50余条", "下册 source 第四十三卷至第五十一卷（下part01） line 24693 为“新沭河等河道”。"),
    Replacement(UP_SUMMARY, "就水利而言的沐南地区", "就水利而言的沭南地区", "上 part02 merged OCR line 22068 明确为“沭南地区”。"),
    Replacement(UP_SUMMARY, "沐北洼地除涝工程", "沭北洼地除涝工程", "上 part02 merged OCR lines 22317、22331 明确为“沭北洼地除涝工程”。"),
    Replacement(UP_PART02, "沐南、沐北通航闸各1座", "沭南、沭北通航闸各1座", "上 part02 merged OCR line 18921 明确为“沭南、沭北通航闸”。"),
    Replacement(UP_PART02, "沐北放水涵洞", "沭北放水涵洞", "上 part02 merged OCR line 19163 明确为“沭北放水涵洞”。"),
    Replacement(UP_PART02, "沐北通航闸", "沭北通航闸", "上 part02 merged OCR line 19172 明确为“沭北通航闸”。"),
    Replacement(UP_PART02, "沐南灌溉涵洞", "沭南灌溉涵洞", "上 part02 merged OCR line 19233 明确为“沭南灌溉涵洞”。"),
    Replacement(UP_PART02, "沐南通航闸", "沭南通航闸", "上 part02 merged OCR line 19242 明确为“沭南通航闸”。"),
    Replacement(UP_PART02, "就水利而言的沐南地区", "就水利而言的沭南地区", "上 part02 merged OCR line 22068 明确为“沭南地区”。"),
    Replacement(UP_PART02, "解除沐南地区洪水灾害", "解除沭南地区洪水灾害", "上 part02 merged OCR line 22116 明确为“解除沭南地区洪水灾害”。"),
    Replacement(UP_PART02, "沐北洼地除涝工程", "沭北洼地除涝工程", "上 part02 merged OCR lines 22317、22331 明确为“沭北洼地除涝工程”。"),
    Replacement(UP_PART02, "连云港市沐北引排干河基本情况表", "连云港市沭北引排干河基本情况表", "上 part02 merged OCR line 22333 明确为“沭北引排干河基本情况表”。"),
    Replacement(UP_PART02, "沐北一级", "沭北一级", "上 part02 merged OCR line 22445 明确为“沭北一级”。"),
    Replacement(UP_PART02, "沐北二级", "沭北二级", "上 part02 merged OCR line 22459 明确为“沭北二级”。"),
    Replacement(UP_PART02, "沐北运河", "沭北运河", "上 part02 merged OCR line 22495 明确为“沭北运河”。"),
    Replacement(UP_PART02, "沐北闸", "沭北闸", "上 part02 merged OCR line 22493 明确为“沭北闸”。"),
    Replacement(UP_PART02, "见沐南除涝", "见沭南除涝", "上 part02 merged OCR line 22940 明确为“见沭南除涝”。"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[list[dict], dict[str, dict[str, int]]]:
    changes: list[dict] = []
    by_path: dict[Path, list[Replacement]] = {}
    for item in REPLACEMENTS:
        by_path.setdefault(item.path, []).append(item)

    for path, replacements in by_path.items():
        if not path.exists():
            continue
        text = read(path)
        updated = text
        for item in replacements:
            count = updated.count(item.old)
            if count:
                updated = updated.replace(item.old, item.new)
                changes.append({
                    "path": rel(path),
                    "old": item.old,
                    "new": item.new,
                    "count": count,
                    "evidence": item.evidence,
                })
        if updated != text:
            path.write_text(updated, encoding="utf-8")

    residuals: dict[str, dict[str, int]] = {}
    for path in CHECK_FILES:
        if not path.exists():
            continue
        text = read(path)
        hits = {term: text.count(term) for term in CHECK_TERMS if text.count(term)}
        if hits:
            residuals[rel(path)] = hits
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, dict[str, int]]) -> str:
    total = sum(c["count"] for c in changes)
    lines = [
        "# 全书汇总跨卷沭临沭残留补修 batch362",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总、上册正文汇总及上册水利直接源稿中已由 OCR 或同卷正确稿确认的完整短语。",
        "- 依据：上册 part01/part02/part03 merged OCR，以及中册、下册对应 source 正文。",
        "- 原则：只修完整短语；不作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换；题名/书名和未定位 OCR 的 `沐北航道` 暂不处理。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            old = item["old"].replace("\n", "\\n")
            new = item["new"].replace("\n", "\\n")
            lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['evidence']}")
    else:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 残留检查", ""])
    if residuals:
        for path, hits in residuals.items():
            compact = "，".join(f"`{term}` {count}" for term, count in hits.items())
            lines.append(f"- `{path}`：{compact}")
    else:
        lines.append("- 检查范围未见目标残留词。")
    lines.extend([
        "",
        "## 保留边界",
        "",
        "- 正式 reader 的 `沐北航道` 未找到页级 OCR 证据，本批继续保留。",
        "- `沂沐偏重筹泄...`、`人海口` 等题名/表段未在本批处理。",
        "- 未处理 OCR 源文件、backup、obsolete、历史交付包。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, dict[str, int]]) -> None:
    full_hits = residuals.get(rel(FULL_SUMMARY), {})
    up_hits = residuals.get(rel(UP_SUMMARY), {})
    block = f"""{MARKER}

- 依据上册 part01/part02/part03 merged OCR，以及中册、下册对应 source 正文，补修全书正文汇总、上册正文汇总及上册水利直接源稿中跨卷 `新沭河/沭南/沭北/临沭县` 可证残留，共 {total} 处。
- 代表修复：`新述河柴地 -> 新沭河柴地`、`新沐河北侧 -> 新沭河北侧`、`沐阳县20个供销社，山东省临沐县8个供销社 -> 沭阳县20个供销社，山东省临沭县8个供销社`、`沂述河、善后河 -> 沂沭河、善后河`、`沐北洼地除涝工程 -> 沭北洼地除涝工程`。
- 本批后全书汇总保留检查范围：`新述河` {full_hits.get('新述河', 0)}，`新沐河` {full_hits.get('新沐河', 0)}，`述南` {full_hits.get('述南', 0)}，`述北` {full_hits.get('述北', 0)}，`沐南` {full_hits.get('沐南', 0)}，`沐北` {full_hits.get('沐北', 0)}，`临沐县` {full_hits.get('临沐县', 0)}，`沂述` {full_hits.get('沂述', 0)}，`沂沐` {full_hits.get('沂沐', 0)}，`人海口` {full_hits.get('人海口', 0)}。
- 本批后上册正文汇总保留检查范围：`沐南` {up_hits.get('沐南', 0)}，`沐北` {up_hits.get('沐北', 0)}。
- 正式 reader 的 `沐北航道` 未找到页级 OCR 证据，本批继续保留；题名/书名和表段 `人海口` 未处理；未作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_crossvolume_shu_batch362_20260708.md`；进度：`output/reports/progress/20260708_全书汇总跨卷沭临沭残留补修第三百六十二批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:])
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    changes, residuals = apply_fix()
    total = sum(c["count"] for c in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "check_files": [rel(p) for p in CHECK_FILES if p.exists()],
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total, residuals)
    print(f"total={total}")
    print(json.dumps(residuals, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
