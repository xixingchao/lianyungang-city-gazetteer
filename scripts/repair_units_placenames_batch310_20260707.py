# -*- coding: utf-8 -*-
"""Narrow OCR-backed unit, kindergarten, and place-name residual repairs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "units_placenames_batch310_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "units_placenames_batch310_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_单位地名残留补修第三百一十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("陆域100多方平方米", "陆域100多万平方米", "PaddleOCR 上/part01/page_0105 为“陆域100多万平方米”。"),
    ("购地1方平方米", "购地1万平方米", "PaddleOCR 中/part01/page_0024 为“购地1万平方米”。"),
    ("建筑面积482.61方平方米", "建筑面积482.61万平方米", "PaddleOCR 下/part01/page_0093 为“建筑面积482.61万平方米”。"),
    ("面积约2方平方米", "面积约2万平方米", "PaddleOCR 下/part02/page_0077 为“面积约2万平方米”。"),
    ("130579干瓦", "130579千瓦", "PaddleOCR 上/part03/page_0030/page_0040 为“130579千瓦”。"),
    ("人园幼儿1.5万余人", "入园幼儿1.5万余人", "PaddleOCR 下/part01/page_0336 为“入园幼儿1.5万余人”。"),
    ("人园率43%", "入园率43%", "PaddleOCR 下/part01/page_0336 为“入园率43%”。"),
    ("建国前岁已日渐衰退", "建国前夕已日渐衰退", "PaddleOCR 下/part02/page_0029 为“建国前夕”。"),
    ("春节前岁，团市", "春节前夕，团市", "PaddleOCR 下/part01/page_0324 为“春节前夕”。"),
    ("胸山（今锦屏山）西山侧", "朐山（今锦屏山）西山侧", "PaddleOCR 上/part01/page_0214 为“朐山(今锦屏山)西山侧”。"),
    ("有胸县故城", "有朐县故城", "PaddleOCR 上/part01/page_0214 为“有朐县故城”。"),
    ("东海胸界中", "东海朐界中", "PaddleOCR 上/part01/page_0214 为“东海朐界中”。"),
    ("其中胸、利城", "其中朐、利城", "PaddleOCR 上/part01/page_0214 为“其中朐、利城”。"),
    ("其时胸、利城", "其时朐、利城", "PaddleOCR 上/part01/page_0214 为“其时朐、利城”。"),
    ("领胸、郑、兰陵", "领朐、郯、兰陵", "PaddleOCR 上/part01/page_0214 为“领朐、郯、兰陵”。"),
    ("领胸、郏、兰陵", "领朐、郯、兰陵", "PaddleOCR 上/part01/page_0214 为“领朐、郯、兰陵”。"),
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
        "# 单位地名残留补修 batch310",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/下册 HTML、正式正文汇总及对应分册正文源稿。",
        "- 依据：PaddleOCR 上/part01/page_0105/page_0214/page_0261、上/part03/page_0030/page_0040、中/part01/page_0024、下/part01/page_0093/page_0324/page_0336、下/part02/page_0029/page_0077。",
        "- 原则：只处理页级 OCR 明确支持的窄短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：其它 `方平方米`、`胸/朐`、`人学` 等未逐页确认的残留不在本批推断处理。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['reason']}")
    lines.extend(["", "## 残留计数", ""])
    bad = {key: value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-07 单位地名残留补修第三百一十批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 页级文本，窄语境补修单位、幼教与建置地名残留：`方平方米 -> 万平方米`、`干瓦 -> 千瓦`、`人园 -> 入园`、`前岁 -> 前夕`、建置页 `胸山/胸县/东海胸界 -> 朐山/朐县/东海朐界` 等，共 {total} 处。
- 报告：`output/reports/units_placenames_batch310_20260707.md`；进度：`output/reports/progress/20260707_单位地名残留补修第三百一十批.md`。
- 其它 `方平方米`、`胸/朐`、`人学` 等未逐页确认的残留不在本批推断处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
