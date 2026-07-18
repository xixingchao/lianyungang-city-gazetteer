# -*- coding: utf-8 -*-
"""Narrow source-backed repairs for 朐山 and 擅长三玄 residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "qushan_shanchang_batch299_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "qushan_shanchang_batch299_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_朐山与擅长三玄残字补修第二百九十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("城东北90里有胸山（今海州锦屏山）", "城东北90里有朐山（今海州锦屏山）", "《汉书》曲阳地理语境，锦屏山古名朐山。"),
    ("周改胸县为朐山县", "周改朐县为朐山县", "北周改朐县为朐山县，PaddleOCR 同文为朐县。"),
    ("北周改胸山", "北周改朐山", "建置沿革中北周改朐山/朐山县。"),
    ("省胸山县人州", "省朐山县入州", "明初省朐山县入州，修正胸/人 OCR 残字。"),
    ("海州领胸山、龙直、新", "海州领朐山、龙直、新", "唐武德四年海州领朐山等县。"),
    ("胸山穿鱼洞西北峰", "朐山穿鱼洞西北峰", "崇祯十四年山崩条，PaddleOCR 同文为朐山。"),
    ("知州孙明忠将胸山改称锦屏山", "知州孙明忠将朐山改称锦屏山", "康熙十三年改称锦屏山，古名朐山。"),
    ("在胸山组风化剥蚀面上", "在朐山组风化剥蚀面上", "第一卷地层说明，对应朐山组。"),
    ("Ar -- Pt 胸山组", "Ar -- Pt 朐山组", "表1-1续表地层名称应为朐山组。"),
    ("Ar -- Pt\n胸山组", "Ar -- Pt\n朐山组", "表1-1续表地层名称应为朐山组。"),
    ("东海胸山崩", "东海朐山崩", "《后汉书》地震记录，PaddleOCR 同文为东海朐山崩。"),
    ("在今市境海州置胸县", "在今市境海州置朐县", "建置概述，秦置朐县。"),
    ("今连云港市境内置胸县", "今连云港市境内置朐县", "第五十八卷概述同正式阅读版，秦代置朐县。"),
    ("故城在胸山西侧", "故城在朐山西侧", "《水经注》朐山西侧有朐县故城。"),
    ("在今海州置县，属东海郡。\"胸山", "在今海州置朐县，属东海郡。\"朐山", "第二卷正文承接《水经注》朐县/朐山。"),
    ("立石东海胸界中", "立石东海朐界中", "秦东门文献作朐界。"),
    ("其中胸、利城", "其中朐、利城", "汉东海郡领县含朐。"),
    ("\"胸山西山侧有", "\"朐山西山侧有", "《水经注》引文。"),
    ("胸县故城", "朐县故城", "《水经注》朐县故城。"),
    ("东海郡领县：\n胸、郏", "东海郡领县：\n朐、郏", "表格线性残文中东海郡领县为朐。"),
    ("移镇胸山后", "移镇朐山后", "州郡志地名朐山。"),
    ("改琅邪为胸\n山郡，改朐县为胸山县", "改琅邪为朐\n山郡，改朐县为朐山县", "北周改琅邪为朐山郡、朐县为朐山县。"),
    ("取县内胸山为名也", "取县内朐山为名也", "北周地理志说明。"),
    ("领胸山、东海", "领朐山、东海", "建置表区域范围。"),
    ("领胸山、沐阳", "领朐山、沐阳", "建置表区域范围；沐阳另需页证，不在本批处理。"),
    ("治胸山，景定", "治朐山，景定", "南宋海州治朐山。"),
    ("东海县并人胸\n海宁州\n山", "东海县并入朐\n海宁州\n山", "元代东海县并入朐山，修正胸/人残字。"),
    ("以州治胸山县省入", "以州治朐山县省入", "明史地理志语境。"),
    ("宋海州胸山人", "宋海州朐山人", "人物籍贯，PaddleOCR 同文及地名为朐山。"),
    ("在胸山东20里处", "在朐山东20里处", "杜令昭筑堤，地名朐山。"),
    ("北与胸山相接", "北与朐山相接", "杜令昭筑堤，地名朐山。"),
    ("后任胸山县令", "后任朐山县令", "刘彝任朐山县令。"),
    ("胸山亘其南", "朐山亘其南", "海州志序地理语境。"),
    ("立石胸山，称\"秦东门\"", "立石朐山，称\"秦东门\"", "军事概述秦东门地名。"),
    ("魏梁胸山之战", "魏梁朐山之战", "军事战事条目，北魏/梁朐山之战。"),
    ("攻打南朝梁的胸山城", "攻打南朝梁的朐山城", "军事战事条目。"),
    ("胸山成主刘晰", "朐山城主刘晰", "军事战事条目，兼修成/城 OCR 残字。"),
    ("在胸山屯守", "在朐山屯守", "军事战事条目。"),
    ("胸山战场", "朐山战场", "军事战事条目。"),
    ("驻扎于胸山", "驻扎于朐山", "宋金战事语境。"),
    ("在胸山县南30公里", "在朐山县南30公里", "古城位置语境。"),
    ("建胸\n山书院", "建朐\n山书院", "书院名为朐山书院。"),
    ("重建胸山书院", "重建朐山书院", "书院名为朐山书院。"),
    ("胸山小学", "朐山小学", "教育表格残文校名，地名朐山。"),
    ("胸山中学", "朐山中学", "教育表格残文校名，地名朐山。"),
    ("《东海县胸山磷灰石矿》", "《东海县朐山磷灰石矿》", "地矿著作名，PaddleOCR 同页为朐山磷灰石矿。"),
    ("善长三玄", "擅长三玄", "人物道教语境，常用谓语为擅长三玄。"),
]


def apply_replacements() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    residuals: dict[str, int] = {}
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
    for old, _new, _reason in REPLACEMENTS:
        residuals[old] = 0
        for path in TARGETS:
            if path.exists():
                residuals[old] += path.read_text(encoding="utf-8", errors="ignore").count(old)
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 朐山与擅长三玄残字补修 batch299",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书 HTML、正式全书正文汇总、下册 part02 正文源稿。",
        "- 原则：只处理已由页级 OCR、同文上下文或固定表达闭合的窄短语；不全局替换 `胸山`、`沐阳`、`述阳`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['reason']}")
    lines.extend(["", "## 残留计数", ""])
    bad = {k: v for k, v in residuals.items() if v}
    if not bad:
        lines.append("- 本批目标短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-07 朐山与擅长三玄残字补修第二百九十九批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据页级 OCR、同文上下文与固定表达，窄语境补修 `胸山/胸县/胸山县/胸山组 -> 朐山/朐县/朐山县/朐山组` 相关短语，以及道教人物段 `善长三玄 -> 擅长三玄`，共 {total} 处。
- 报告：`output/reports/qushan_shanchang_batch299_20260707.md`；进度：`output/reports/progress/20260707_朐山与擅长三玄残字补修第二百九十九批.md`。
- `沐阳`、`述阳`、`了若指掌` 等未回源前不处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
    print(f"residuals_nonzero={ {k:v for k,v in residuals.items() if v} }")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
