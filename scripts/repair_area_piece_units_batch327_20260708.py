# -*- coding: utf-8 -*-
"""Narrow area and piece-unit residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "area_piece_units_batch327_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "area_piece_units_batch327_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_面积件数单位残留补修第三百二十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_上册.html",
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
    ("彩色玻璃马赛克15方平方米、工艺玻璃器血50方只（件）", "彩色玻璃马赛克15万平方米、工艺玻璃器皿50万只（件）", "PaddleOCR 上/part03/page_0197 为“彩色玻璃马赛克15万平方米、工艺玻璃器皿50万只(件)”。"),
    ("该企业区占地面积0.5方平方米", "该企业厂区占地面积0.5万平方米", "PaddleOCR 上/part03/page_0293 为“该企业厂区占地面积0.5万平方米”。"),
    ("新建、扩建厂房14.5方平方米", "新建、扩建厂房14.5万平方米", "PaddleOCR 上/part03/page_0227 为“新建、扩建厂房14.5万平方米”。"),
    ("加固建筑物122.1方平方米", "加固建筑物122.1万平方米", "PaddleOCR 下/part01/page_0456 为“加固建筑物122.1万平方米”。"),
    ("厂区占地面积0.6方平方米", "厂区占地面积0.6万平方米", "PaddleOCR 上/part03/page_0281 为“厂区占地面积0.6万平方米”。"),
    ("该广占地面积0.7方平方米", "该厂占地面积0.7万平方米", "PaddleOCR 上/part03/page_0181 为“该厂占地面积0.7万平方米”。"),
    ("建筑面积0.81方平方米", "建筑面积0.81万平方米", "PaddleOCR 上/part03/page_0188 为“建筑面积0.81万平方米”。"),
    ("年印能力增至30方色令", "年印能力增至30万色令", "PaddleOCR 上/part03/page_0188 为“年印能力增至30万色令”。"),
    ("占地面积11.4方平方米", "占地面积11.4万平方米", "PaddleOCR 上/part03/page_0262 为“占地面积11.4万平方米”。"),
    ("占地面积0.8方平方米", "占地面积0.8万平方米", "PaddleOCR 上/part03/page_0241 为“占地面积0.8万平方米”。"),
    ("人造革2方平方米", "人造革2万平方米", "PaddleOCR 上/part03/page_0287 为“人造革2万平方米”。"),
    ("市场面积111方平方米", "市场面积111万平方米", "PaddleOCR 上/part02/page_0198 为“市场面积111万平方米”。"),
    ("积10.7方平方米", "积10.7万平方米", "PaddleOCR 中/part01/page_0070 为“积10.7万平方米”。"),
    ("建筑面积3.46方平方米", "建筑面积3.46万平方米", "PaddleOCR 中/part01/page_0073 为“建筑面积3.46万平方米”。"),
    ("建筑面积5.05方平方米", "建筑面积5.05万平方米", "PaddleOCR 中/part01/page_0076 为“建筑面积5.05万平方米”。"),
    ("存栏羊达8.11方只", "存栏羊达8.11万只", "PaddleOCR 上/part03/page_0076 为“存栏羊达8.11万只”。"),
    ("年均产中空瓶24方只", "年均产中空瓶24万只", "PaddleOCR 上/part03/page_0287 为“年均产中空瓶24万只”。"),
    ("累计出口162.4方只", "累计出口162.4万只", "PaddleOCR 中/part01/page_0245 为“累计出口162.4万只”。"),
    ("扬声器30方只", "扬声器30万只", "PaddleOCR 中/part01/page_0249 为“扬声器30万只”。"),
    ("硅整流器284.5方只", "硅整流器284.5万只", "PaddleOCR 中/part01/page_0252 为“硅整流器284.5万只”。"),
    ("活鸡12.2方只", "活鸡12.2万只", "PaddleOCR 中/part02/page_0142 为“活鸡12.2万只”。"),
    ("海参大耳幼体30方只", "海参大耳幼体30万只", "PaddleOCR 下/part01/page_0438 为“海参大耳幼体30万只”。"),
    ("幼蟹6.4方只", "幼蟹6.4万只", "PaddleOCR 下/part01/page_0438 为“幼蟹6.4万只”。"),
]

CHECK_TERMS = ["方平方米", "方色令"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_replacements() -> tuple[list[dict], dict[str, int], dict[str, int]]:
    changes: list[dict] = []
    ordered = sorted(REPLACEMENTS, key=lambda item: len(item[0]), reverse=True)
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        original = text
        for old, new, reason in ordered:
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
                residuals[old] += read(path).count(old)

    term_totals: dict[str, int] = {}
    for term in CHECK_TERMS:
        term_totals[term] = sum(read(path).count(term) for path in TARGETS if path.exists())
    unit_fangzhi_total = 0
    for old, _new, _reason in REPLACEMENTS:
        if "方只" in old:
            unit_fangzhi_total += residuals[old]
    term_totals["本批方只单位短语"] = unit_fangzhi_total
    return changes, residuals, term_totals


def fmt(value: str) -> str:
    return value.replace("\n", "\\n")


def render(changes: list[dict], residuals: dict[str, int], term_totals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 面积件数单位残留补修 batch327",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式阅读 HTML、全书正文汇总、上中下相关分册源稿。",
        "- 依据：PaddleOCR 上/part02/page_0198，上/part03/page_0076、0181、0188、0197、0227、0241、0262、0281、0287、0293，中/part01/page_0070、0073、0076、0245、0249、0252，中/part02/page_0142，下/part01/page_0438、0456。",
        "- 原则：只处理 OCR 可证的面积、件数和数量单位短语；`秘方只传`、`甲方只付`、`双方只有`、`外方只点` 等非本批单位短语不处理。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            lines.append(f"- `{item['path']}`：`{fmt(item['old'])}` -> `{fmt(item['new'])}`；次数 {item['count']}；依据：{item['reason']}")
    else:
        lines.append("- 本批没有新增替换。")

    lines.extend(["", "## 残留计数", ""])
    bad = {key: value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{fmt(key)}`：{value}")
    lines.append("")
    for term, value in term_totals.items():
        lines.append(f"- `{term}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int, term_totals: dict[str, int]) -> None:
    marker = "## 2026-07-08 面积件数单位残留补修第三百二十七批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    totals = "，".join(f"`{term}` {count}" for term, count in term_totals.items())
    block = f"""
{marker}

- 依据 PaddleOCR 上/part02/page_0198，上/part03/page_0076、0181、0188、0197、0227、0241、0262、0281、0287、0293，中/part01/page_0070、0073、0076、0245、0249、0252，中/part02/page_0142，下/part01/page_0438、0456，窄语境补修面积、印量、件数和数量单位残留，共 {total} 处。
- 代表修复：`方平方米 -> 万平方米`、`30方色令 -> 30万色令`、`8.11/24/162.4/30/284.5方只 -> 万只`、`活鸡12.2方只 -> 活鸡12.2万只`、`海参大耳幼体30方只/幼蟹6.4方只 -> 万只`。
- 本批检查范围内剩余：{totals}。
- 报告：`output/reports/area_piece_units_batch327_20260708.md`；进度：`output/reports/progress/20260708_面积件数单位残留补修第三百二十七批.md`。
- 未作 `方/万` 全局替换；`秘方只传`、`甲方只付`、`双方只有`、`外方只点` 等非本批单位短语保留；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals, term_totals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "term_totals": term_totals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals, term_totals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    append_memory(total, term_totals)
    print(f"total={total}")
    print(f"residuals_nonzero={ {k: v for k, v in residuals.items() if v} }")
    print(f"term_totals={term_totals}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
