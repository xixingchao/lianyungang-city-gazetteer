# -*- coding: utf-8 -*-
"""Narrow OCR-backed repairs after user sample residue review."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "user_sample_residues_batch304_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "user_sample_residues_batch304_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_用户样本残字补修第三百零四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("论陷时期", "沦陷时期", "PaddleOCR 中/part01/page_0377、下/part01/page_0303 等为“沦陷时期”。"),
    ("市境论陷", "市境沦陷", "PaddleOCR 中/part01/page_0456 为“连云港市境沦陷”。"),
    ("境内论陷", "境内沦陷", "PaddleOCR 中/part02/page_0281/page_0286 等为“境内沦陷”。"),
    ("连云港论陷", "连云港沦陷", "PaddleOCR 中/part01/page_0497、下/part01/page_0220/page_0303 等为“连云港沦陷”。"),
    ("清朝未年", "清朝末年", "PaddleOCR 同类页多处为“清朝末年”；当前源稿该处为明显字形残留。"),
    ("光绪未年", "光绪末年", "PaddleOCR 上/part01/page_0247 为“清光绪末年”。"),
    ("解放前岁", "解放前夕", "PaddleOCR 上/part01/page_0247、下/part01/page_0303、下/part02/page_0070 为“解放前夕”。"),
    ("人学率", "入学率", "PaddleOCR 中/part02/page_0480、下/part01/page_0152/page_0348/page_0355、上/part01/page_0237/page_0247/page_0248 等为“入学率”。"),
    ("进人百姓家", "进入百姓家", "PaddleOCR 上/part01/page_0247 为“进入百姓家”。"),
    ("深人工厂", "深入工厂", "PaddleOCR 中/part02/page_0483 为“深入工厂”。"),
    ("4.5方公斤", "4.5万公斤", "PaddleOCR 中/part02/page_0316 为“4.5万公斤”。"),
    ("贸易粮5方公斤", "贸易粮5万公斤", "PaddleOCR 中/part02/page_0485 为“贸易粮5万公斤”。"),
    ("运肥1250方公斤", "运肥1250万公斤", "PaddleOCR 下/part01/page_0333 为“运肥1250万公斤”。"),
]

CHECK_TERMS = [old for old, _new, _reason in REPLACEMENTS]


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
    for term in CHECK_TERMS:
        residuals[term] = 0
        for path in TARGETS:
            if path.exists():
                residuals[term] += path.read_text(encoding="utf-8", errors="ignore").count(term)
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 用户样本残字补修 batch304",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/中册/下册 HTML、正式正文汇总及对应分册正文源稿。",
        "- 依据：PaddleOCR 页级文本对同页或同上下文给出的 `沦陷`、`末年`、`解放前夕`、`入学率`、`进入百姓家`、`深入工厂`、`万公斤`。",
        "- 原则：只处理用户样本复核后证据明确的窄短语；不处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：`入口门廊迁回曲折` 因页级 OCR 也读作 `迁回曲折`，未作推断替换。",
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
    marker = "## 2026-07-07 用户样本残字补修第三百零四批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据用户贴出的串页/正文残字样本继续复核，确认当前正式 reader 未出现该类地质表与方言表跨段混杂；在正式 reader 与正文源稿中窄语境补修 `论陷 -> 沦陷`、`未年 -> 末年`、`解放前岁 -> 解放前夕`、`人学率 -> 入学率`、`进人百姓家 -> 进入百姓家`、`深人工厂 -> 深入工厂`、`方公斤 -> 万公斤` 等，共 {total} 处。
- 报告：`output/reports/user_sample_residues_batch304_20260707.md`；进度：`output/reports/progress/20260707_用户样本残字补修第三百零四批.md`。
- `入口门廊迁回曲折` 因页级 OCR 也读作 `迁回曲折`，未作推断替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
