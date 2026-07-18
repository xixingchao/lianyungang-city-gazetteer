# -*- coding: utf-8 -*-
"""Repair reader Huaiyin/Huaihai salt OCR residues, batch 132."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_huaiyin_huaihai_batch132_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_huaiyin_huaihai_batch132_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_淮阴淮海盐残字回源补修第一百三十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "桐木厂联营县名", "old": "涟水、赣榆、准阴、灌南、准阳", "new": "涟水、赣榆、淮阴、灌南、淮阳"},
    {"label": "桐木厂联营县名分段", "old": "涟水、赣榆、</p><p>准阴、灌南、准阳", "new": "涟水、赣榆、</p><p>淮阴、灌南、淮阳"},
    {"label": "桐木厂联营淮阳县名补漏", "old": "淮阴、灌南、准阳等县", "new": "淮阴、灌南、淮阳等县"},
    {"label": "准阴电子工业局", "old": "准阴电子工业局", "new": "淮阴电子工业局"},
    {"label": "准阴电子工业局分段", "old": "准阴电子工业</p><p>局", "new": "淮阴电子工业</p><p>局"},
    {"label": "淮海输变电工程地区", "old": "准阴、连云港、盐城", "new": "淮阴、连云港、盐城"},
    {"label": "准海盐电网", "old": "准海盐电网", "new": "淮海盐电网"},
    {"label": "准海盐电网分段", "old": "准海盐</p><p>电网", "new": "淮海盐</p><p>电网"},
    {"label": "准海盐电网并入分段", "old": "准海盐电</p><p>网并人省电网", "new": "淮海盐电</p><p>网并入省电网"},
    {"label": "准阴电网联络", "old": "准阴电网联络", "new": "淮阴电网联络"},
    {"label": "准阴电网联络分段", "old": "准阴电</p><p>网联络", "new": "淮阴电</p><p>网联络"},
    {"label": "起准阴客运线", "old": "起准阴，经", "new": "起淮阴，经"},
    {"label": "客运路线扩展", "old": "客运路线扩展至准阴", "new": "客运路线扩展至淮阴"},
    {"label": "准阴汽车运输处", "old": "准阴汽车运输处", "new": "淮阴汽车运输处"},
    {"label": "准阴汽车运输处分段", "old": "移交准</p><p>阴汽车运输处", "new": "移交淮</p><p>阴汽车运输处"},
    {"label": "新浦至准阴石坝", "old": "新浦至准阴石坝", "new": "新浦至淮阴石坝"},
    {"label": "准阴航运局", "old": "准阴航运局", "new": "淮阴航运局"},
    {"label": "盐河运经准阴", "old": "运经准阴", "new": "运经淮阴"},
    {"label": "准阴方向载波机", "old": "准阴方向", "new": "淮阴方向"},
    {"label": "新浦经准阴至南京", "old": "新浦经准阴至南京", "new": "新浦经淮阴至南京"},
    {"label": "粮食调拨徐州准阴", "old": "徐州750吨、准阴500吨", "new": "徐州750吨、淮阴500吨"},
    {"label": "准阴地区民政局", "old": "准阴地区民政局", "new": "淮阴地区民政局"},
    {"label": "准阴专区", "old": "准阴专区", "new": "淮阴专区"},
    {"label": "进驻准阴", "old": "进驻准阴", "new": "进驻淮阴"},
    {"label": "准阴人防办", "old": "准阴人防办", "new": "淮阴人防办"},
    {"label": "准阴地区选调", "old": "准阴地区选调", "new": "淮阴地区选调"},
    {"label": "江苏准阴粮食技工学校", "old": "江苏准阴粮食技工学校", "new": "江苏淮阴粮食技工学校"},
    {"label": "去准阴访问", "old": "去准阴访问", "new": "去淮阴访问"},
    {"label": "去准阴访问分段", "old": "去</p><p>准阴访问", "new": "去</p><p>淮阴访问"},
    {"label": "准阴地区评为", "old": "准阴地区评为", "new": "淮阴地区评为"},
    {"label": "原准阴粮食技工学校", "old": "原准阴粮食技工学校", "new": "原淮阴粮食技工学校"},
    {"label": "准阴师范", "old": "准阴师范", "new": "淮阴师范"},
    {"label": "准阴地区推广", "old": "准阴地区推广", "new": "淮阴地区推广"},
    {"label": "准阴平原坡地", "old": "准阴平原坡地", "new": "淮阴平原坡地"},
    {"label": "徐州准阴盐城", "old": "徐州、准阴、盐城", "new": "徐州、淮阴、盐城"},
    {"label": "准阴地区会演", "old": "准阴地区会演", "new": "淮阴地区会演"},
    {"label": "从准阴购进", "old": "从准阴购进", "new": "从淮阴购进"},
    {"label": "省内准阴", "old": "省内准阴", "new": "省内淮阴"},
    {"label": "准阴东60里", "old": "准阴东60里", "new": "淮阴东60里"},
    {"label": "任准阴地区", "old": "任准阴地区", "new": "任淮阴地区"},
]

LEFT_UNTOUCHED = [
    "本批只处理固定地名、机构名、电网名短语，不做裸词全局替换。",
    "本批没有打开、展示或嵌入图片。",
]


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        applied.append({"target": str(target), "changed": sum(i["count"] for i in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = sum(t["changed"] for t in applied)
    payload = {
        "time": now,
        "scope": "reader Huaiyin and Huaihai salt OCR residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 淮阴、淮海盐残字补修第一百三十二批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 只处理固定地名、机构名、电网名短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次替换：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        if target["changed"]:
            lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百三十二批：淮阴、淮海盐残字"
    upsert_memory(marker, f"""
{marker}

- 补修当前全书/中册/下册阅读稿中 `准阴/准海盐` 固定地名、机构名、电网名残字，改为 `淮阴/淮海盐`。
- 本批证据短语 {len(REPLACEMENTS)} 项，替换 {changed} 处；报告：`output/reports/reader_huaiyin_huaihai_batch132_20260707.md`。
- 未做裸词全局替换；未打开、展示或嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
