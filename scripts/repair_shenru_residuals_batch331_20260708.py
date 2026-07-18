# -*- coding: utf-8 -*-
"""Narrow 深人 -> 深入 residual repairs backed by OCR/context."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "shenru_residuals_batch331_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "shenru_residuals_batch331_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_深入残留补修第三百三十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("深人人心", "深入人心", "PaddleOCR 中/part02/page_0442、下/part01/page_0054 均有“深入人心”；固定搭配。"),
    ("深人全面地开展增产节约", "深入全面地开展增产节约", "PaddleOCR 上/part01/page_0086 为“深入全面地开展增产节约”。"),
    ("逐步深人，有效控制", "逐步深入，有效控制", "PaddleOCR 上/part01/page_0272 为“逐步深入，有效控制”。"),
    ("持续深人地开展爱鸟", "持续深入地开展爱鸟", "PaddleOCR 上/part02/page_0122 为“持续深入地开展爱鸟”。"),
    ("改革的不断深人", "改革的不断深入", "PaddleOCR 上/part02/page_0138、0169 与下/part02/page_0049 为“改革的不断深入”。"),
    ("改革开放的不断深人", "改革开放的不断深入", "PaddleOCR 上/part02/page_0169 为“改革开放的不断深入”。"),
    ("客观、深人的分析", "客观、深入的分析", "PaddleOCR 上/part02/page_0169 为“客观、深入的分析”。"),
    ("深人化工、纺织、机械", "深入化工、纺织、机械", "PaddleOCR 上/part02/page_0181 为“深入化工、纺织、机械”。"),
    ("经济体制改革的深人", "经济体制改革的深入", "PaddleOCR 中/part02/page_0267 为“经济体制改革的深入”。"),
    ("催调人员要深人矿区", "催调人员要深入矿区", "PaddleOCR 中/part02/page_0267 为“催调人员要深入矿区”。"),
    ("革的深人，计划管理部分", "革的深入，计划管理部分", "固定搭配；同页 PaddleOCR 仍为深人但语境为改革深入。"),
    ("广泛深人地开展社会主义", "广泛深入地开展社会主义", "PaddleOCR 中/part02/page_0424 为“广泛深入地开展社会主...”。"),
    ("继续深人地开展“活学活用”", "继续深入地开展“活学活用”", "PaddleOCR 中/part02/page_0424 为“继续深入地开展‘活学活用’”。"),
    ("造运动深人，市委", "造运动深入，市委", "PaddleOCR 中/part02/page_0441 为“造运动深入，市委”。"),
    ("每季度深人县区联系一次", "每季度深入县区联系一次", "固定搭配；政协委员联系语境。"),
    ("深人海岛、山村和盐场", "深入海岛、山村和盐场", "PaddleOCR 下/part02/page_0033 为“深入海岛、山村和盐场”。"),
    ("两次深人徐圩盐场演出", "两次深入徐圩盐场演出", "PaddleOCR 下/part02/page_0034 为“深入徐圩盐场演出”。"),
    ("深人沿海各盐场", "深入沿海各盐场", "PaddleOCR 下/part02/page_0035 为“深入沿海各盐场”。"),
    ("深人广矿乡镇演出", "深入厂矿乡镇演出", "PaddleOCR 下/part02/page_0049 为“深入厂矿乡镇演出”。"),
    ("深人盐滩采访", "深入盐滩采访", "PaddleOCR 下/part02/page_0162 为“深入盐滩采访”。"),
    ("体育深人社会、深人家庭", "体育深入社会、深入家庭", "PaddleOCR 下/part02/page_0229 为“体育深入社会、深入家庭”。"),
    ("深人敌后开展斗争", "深入敌后开展斗争", "PaddleOCR 下/part02/page_0359 为“深入敌后开展斗争”。"),
    ("深人民间以德政", "深入民间以德政", "固定搭配；任后深入民间教导开化语境。"),
    ("深人渔村、海岛、船舶", "深入渔村、海岛、船舶", "PaddleOCR 中/part01/page_0494 为“深入渔村、海岛、船舶”。"),
    ("深人三县灾区", "深入三县灾区", "PaddleOCR 下/part01/page_0030 为“深入三县灾区”。"),
    ("深人单位检查", "深入单位检查", "PaddleOCR 下/part01/page_0092 为“深入单位检查”。"),
    ("运动不断深人", "运动不断深入", "PaddleOCR 下/part01/page_0110/上下文为“不断深入”固定搭配。"),
    ("深人敌占区", "深入敌占区", "PaddleOCR 下/part01/page_0305 为“深入敌占区”。"),
    ("朱土坦、孙光等深人连云港", "朱士坦、孙光等深入连云港", "PaddleOCR 下/part01/page_0305 为“朱士坦、孙光等深入连云港”。"),
    ("深人厂矿演出", "深入厂矿演出", "PaddleOCR 下/part01/page_0328 为“深入厂矿演出”。"),
    ("活动深人开", "活动深入开", "PaddleOCR 下/part01/page_0335 为“活动深入开...”。"),
    ("者深人生活", "者深入生活", "PaddleOCR 下/part01/page_0344 为“者深入生活”。"),
    ("广泛深人地开展教学改革", "广泛深入地开展教学改革", "PaddleOCR 下/part01/page_0370 为“广泛深入地开展教学改革”。"),
    ("深人实际", "深入实际", "固定搭配；已在前批处理同类，残留兜底。"),
    ("深人农村", "深入农村", "PaddleOCR 多页为“深入农村”。"),
    ("深人盐场", "深入盐场", "PaddleOCR 多页为“深入盐场”。"),
    ("深人发展", "深入发展", "固定搭配。"),
    ("深人至", "深入至", "固定搭配。"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_replacements() -> tuple[list[dict], int]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        original = text
        for old, new, evidence in sorted(REPLACEMENTS, key=lambda item: len(item[0]), reverse=True):
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                changes.append({
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "old": old,
                    "new": new,
                    "count": count,
                    "evidence": evidence,
                })
        if text != original:
            path.write_text(text, encoding="utf-8")
    residual = sum(read(path).count("深人") for path in TARGETS if path.exists())
    return changes, residual


def render(changes: list[dict], residual: int) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 深入残留补修 batch331",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正文汇总与上中下相关分册源稿；正式阅读 HTML 本批无 `深人` 命中。",
        "- 原则：只处理 OCR 或固定搭配明确支撑的 `深人 -> 深入` 及同句错字；不处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", "", f"- `深人`：{residual}"])
    return "\n".join(lines) + "\n"


def append_memory(total: int, residual: int) -> None:
    marker = "## 2026-07-08 深入残留补修第三百三十一批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 与固定搭配，补修正文汇总和相关分册源稿 `深人 -> 深入` 残留，共 {total} 处。
- 代表修复：`深人人心 -> 深入人心`、`深人矿区/盐滩/敌后/敌占区/渔村/厂矿/生活 -> 深入...`，并同步 `深人广矿乡镇 -> 深入厂矿乡镇`、`朱土坦 -> 朱士坦`。
- 本批后检查范围 `深人` 残留 {residual} 处；报告：`output/reports/shenru_residuals_batch331_20260708.md`；进度：`output/reports/progress/20260708_深入残留补修第三百三十一批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residual = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "residual": residual, "changes": changes}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    content = render(changes, residual)
    REPORT.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")
    append_memory(total, residual)
    print(f"total={total}")
    print(f"residual={residual}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
