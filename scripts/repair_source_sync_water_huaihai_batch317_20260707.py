# -*- coding: utf-8 -*-
"""Narrow source/reader sync repairs for water-system and Huaihai residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "source_sync_water_huaihai_batch317_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "source_sync_water_huaihai_batch317_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_水系淮海源稿同步补修第三百一十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("改造进人新港区", "改造进入新港区", "PaddleOCR 上/part01/page_0104 为“改造进入新港区”。"),
    ("沂、沐、泗水系", "沂、沭、泗水系", "PaddleOCR 上/part01/page_0029、page_0124 为“沂、沭、泗水系”。"),
    ("新述河、蔷薇河", "新沭河、蔷薇河", "PaddleOCR 上/part01/page_0029 为“新沭河、蔷薇河”。"),
    ("直接人海河道", "直接入海河道", "PaddleOCR 上/part01/page_0029 为“直接入海河道”。"),
    ("直接人海河流", "直接入海河流", "PaddleOCR 上/part01/page_0124 为“直接入海河流”。"),
    ("淮述新河", "淮沭新河", "PaddleOCR 上/part01/page_0124、中/part02/page_0047 为“淮沭新河”。"),
    ("导水人石梁河", "导水入石梁河", "PaddleOCR 上/part01/page_0168 为“导水入石梁河”。"),
    ("导述河洪水人海", "导沭河洪水入海", "PaddleOCR 上/part01/page_0168 为“导沭河洪水入海”。"),
    ("述河自山东省", "沭河自山东省", "PaddleOCR 上/part01/page_0168 为“沭河自山东省”。"),
    ("临述县大官庄", "临沭县大官庄", "PaddleOCR 上/part01/page_0071、page_0168 为“临沭县大官庄”。"),
    ("分述河上游", "分沭河上游", "PaddleOCR 上/part01/page_0168 为“分沭河上游”。"),
    ("临洪口人海", "临洪口入海", "PaddleOCR 上/part01/page_0168 为“临洪口入海”。"),
    ("人连云港市蕃薇河", "入连云港市蔷薇河", "PaddleOCR 中/part02/page_0047 为“入连云港市蔷薇河”。"),
    ("准海战役", "淮海战役", "PaddleOCR 中/part02/page_0034、page_0412 与下/part01/page_0332 为“淮海战役”。"),
    ("准海妇救总会", "淮海妇救总会", "PaddleOCR 下/part01/page_0332 为“淮海妇救总会”。"),
    ("《告准海妇联书》", "《告淮海妇联书》", "PaddleOCR 下/part01/page_0332 为“《告淮海妇联书》”。"),
    ("准海前线", "淮海前线", "PaddleOCR 下/part02/page_0165 为“淮海前线”。"),
    ("伪准海省在赣", "伪淮海省在赣", "PaddleOCR 中/part02/page_0212 为“伪淮海省在赣”。"),
    ("伪准海省立东海师范学校", "伪淮海省立东海师范学校", "PaddleOCR 下/part01/page_0390 为“伪淮海省立东海师范学校”。"),
    ("海、赣、述、灌地方组织", "海、赣、沭、灌地方组织", "PaddleOCR 下/part01/page_0390 为“海、赣、沭、灌地方组织”。"),
    ("三等功区抽出2976人", "三等功763人次，被华东野战军某部通令嘉奖，誉为“钢的担架队”。民国37年8月，竹庭县7个区抽出2976人", "PaddleOCR 中/part02/page_0412 补出缺失句。"),
    ("文派出万名民工", "又派出万名民工", "PaddleOCR 中/part02/page_0412 为“又派出万名民工”。"),
    ("路北东海县派出由4300余人、900辆大车，\n资。路南东海县", "路北东海县派出由4300余人、900辆大车，\n400副担架组成的3个运输团、1个担架团，另有近万名民工、数千辆小车运送军粮和物\n资。路南东海县", "PaddleOCR 中/part02/page_0412 补出缺失运输句。"),
    ("路北东海县派出由4300余人、900辆大车，资。路南东海县", "路北东海县派出由4300余人、900辆大车，400副担架组成的3个运输团、1个担架团，另有近万名民工、数千辆小车运送军粮和物资。路南东海县", "PaddleOCR 中/part02/page_0412 补出缺失运输句。"),
    ("路北东海县派出由4300余人、900辆大车，</p><p>资。路南东海县", "路北东海县派出由4300余人、900辆大车，</p><p>400副担架组成的3个运输团、1个担架团，另有近万名民工、数千辆小车运送军粮和物</p><p>资。路南东海县", "PaddleOCR 中/part02/page_0412 补出缺失运输句。"),
]


def apply_replacements() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new, reason in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                changes.append({
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "old": old,
                    "new": new,
                    "count": count,
                    "reason": reason,
                })
        if text != original:
            path.write_text(text, encoding="utf-8")

    residuals: dict[str, int] = {}
    for old, _new, _reason in REPLACEMENTS:
        residuals[old] = 0
        for path in TARGETS:
            if path.exists():
                residuals[old] += path.read_text(encoding="utf-8", errors="ignore").count(old)
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 水系淮海源稿同步补修 batch317",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/中册/下册 HTML、正式正文汇总及相关分册正文源稿。",
        "- 依据：PaddleOCR 上/part01/page_0029、0104、0124、0168；中/part02/page_0034、0047、0212、0412；下/part01/page_0332、0390；下/part02/page_0165。",
        "- 原则：只处理完整短语和同页 OCR 已证实的缺句，不处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：`伪准海省税务局` 未找到直接页级 OCR 命中，虽同段后文疑似应为 `伪淮海省税务局`，本批不作推断。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        old = item["old"].replace("\n", "\\n")
        new = item["new"].replace("\n", "\\n")
        lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['reason']}")
    lines.extend(["", "## 残留计数", ""])
    bad = {key: value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key.replace(chr(10), '\\n')}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-07 水系淮海源稿同步补修第三百一十七批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据多页 PaddleOCR 文本，窄语境同步补修水系、淮海战役、伪淮海省、海州师范、支前运输等残留：`进人 -> 进入`、`沐/述 -> 沭`、`人海 -> 入海`、`准海 -> 淮海`、`伪准海省立东海师范学校 -> 伪淮海省立东海师范学校`、中册政党页支前运输缺句等，共 {total} 处。
- 报告：`output/reports/source_sync_water_huaihai_batch317_20260707.md`；进度：`output/reports/progress/20260707_水系淮海源稿同步补修第三百一十七批.md`。
- `伪准海省税务局` 未找到直接页级 OCR 命中，本批不作推断；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    append_memory(total)
    print(f"total={total}")
    print(f"residuals_nonzero={ {k: v for k, v in residuals.items() if v} }")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
