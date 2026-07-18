# -*- coding: utf-8 -*-
"""Narrow unit, militia, and martyr residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "units_militia_martyrs_batch320_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "units_militia_martyrs_batch320_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_单位民兵烈士残留补修第三百二十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    (
        "搏博斗中牺牲",
        "搏斗中牺牲",
        "PaddleOCR 下/part01/page_0184 为“搏斗中牺牲”。",
    ),
    (
        "共出动民兵62方人次",
        "共出动民兵62万人次",
        "PaddleOCR 下/part01/page_0184 为“共出动民兵62万人次”。",
    ),
    (
        "被追认为革命烈土",
        "被追认为革命烈士",
        "PaddleOCR 下/part01/page_0184 为“被追认为革命烈士”。",
    ),
    (
        "床单80方条",
        "床单80万条",
        "PaddleOCR 上/part03/page_0254 为“床单80万条”。",
    ),
    (
        "灌云县12方条",
        "灌云县12万条",
        "PaddleOCR 上/part03/page_0249 为“灌云县12万条”。",
    ),
    (
        "4方余人",
        "4万余人",
        "PaddleOCR 上/part01/page_0077 为“4万余人”。",
    ),
    (
        "10人为革命烈土",
        "10人为革命烈士",
        "PaddleOCR 上/part01/page_0105 为“10人为革命烈士”。",
    ),
    (
        "追认朱爱周为革命烈土",
        "追认朱爱周为革命烈士",
        "PaddleOCR 上/part01/page_0111 为“追认朱爱周为革命烈士”。",
    ),
    (
        "道认李迪仁为革命烈土",
        "追认李迪仁为革命烈士",
        "PaddleOCR 下/part02/page_0373 为“追认李迪仁为革命烈士”。",
    ),
    (
        "两名万徒搏\n斗",
        "两名歹徒搏\n斗",
        "PaddleOCR 上/part01/page_0105 为“与盗窃枪支的两名歹徒搏斗中牺牲”。",
    ),
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
                changes.append(
                    {
                        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                        "old": old,
                        "new": new,
                        "count": count,
                        "reason": reason,
                    }
                )
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
        "# 单位民兵烈士残留补修 batch320",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/中册/下册 HTML、正式正文汇总及相关分册正文源稿。",
        "- 依据：PaddleOCR 下/part01/page_0184，下/part02/page_0373，上/part01/page_0077、0105、0111，上/part03/page_0249、0254。",
        "- 原则：只处理完整短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：`打人敌伪内部`、`编人中国国民党中央军` 等需要更大段落补写或 OCR 自身不稳的条目留待单独核对。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        old = item["old"].replace("\n", "\\n")
        new = item["new"].replace("\n", "\\n")
        lines.append(
            f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['reason']}"
        )
    lines.extend(["", "## 残留计数", ""])
    bad = {key.replace("\n", "\\n"): value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-07 单位民兵烈士残留补修第三百二十批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据多页 PaddleOCR 文本，窄语境补修单位、民兵和烈士相关残留：`搏博斗中牺牲 -> 搏斗中牺牲`、`62方人次 -> 62万人次`、`烈土 -> 烈士`、`床单80方条 -> 床单80万条`、`灌云县12方条 -> 灌云县12万条`、`4方余人 -> 4万余人`、`两名万徒搏斗 -> 两名歹徒搏斗` 等，共 {total} 处。
- 报告：`output/reports/units_militia_martyrs_batch320_20260707.md`；进度：`output/reports/progress/20260707_单位民兵烈士残留补修第三百二十批.md`。
- `打人敌伪内部`、`编人中国国民党中央军` 等需要更大段落补写或 OCR 自身不稳的条目留待单独核对；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
    }
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
