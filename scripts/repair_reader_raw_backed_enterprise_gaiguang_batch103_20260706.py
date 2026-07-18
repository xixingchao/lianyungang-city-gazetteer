# -*- coding: utf-8 -*-
"""Repair narrowly source-backed enterprise `该广` residues, batch 103."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_raw_backed_enterprise_gaiguang_batch103_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_raw_backed_enterprise_gaiguang_batch103_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_企业段该广残留回源补修第一百零三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "羽毛画实习工厂该厂",
        "old": "季道池主持该广工作后",
        "new": "季道池主持该厂工作后",
        "source": "workbench/ocr/raw/中/part01/page_0027.txt:8-15；同页多处称该厂",
    },
    {
        "label": "东海县工艺绣品联营厂收回",
        "old": "东海县外贸公司将该广从牛山镇收回",
        "new": "东海县外贸公司将该厂从牛山镇收回",
        "source": "workbench/ocr/raw/中/part01/page_0041.txt:16-21；上下文为联营厂",
    },
    {
        "label": "市刺绣厂双面绣",
        "old": "该广生产的“台鱼戏水”双面绣",
        "new": "该厂生产的“台鱼戏水”双面绣",
        "source": "workbench/ocr/raw/中/part01/page_0042.txt:29-34；上下文为市刺绣厂",
    },
    {
        "label": "赣榆县石英厂学艺",
        "old": "1975年5月，该广派46人去临沂八块石瓷厂学习制瓷技艺",
        "new": "1975年5月，该厂派46人去临沂八块石瓷厂学习制瓷技艺",
        "source": "workbench/ocr/raw/中/part01/page_0048.txt:7-12；上下文为赣榆县石英厂/陶瓷厂",
    },
    {
        "label": "赣榆县石英厂学艺断行",
        "old": "1975年5月，该广派46人去临沂八块石瓷厂学习制瓷技",
        "new": "1975年5月，该厂派46人去临沂八块石瓷厂学习制瓷技",
        "source": "workbench/ocr/raw/中/part01/page_0048.txt:7-12；源稿断行形态",
    },
    {
        "label": "印铁厂茶叶盒包装",
        "old": "该广“茶叶盒礼品包装”获省轻工系统优秀设计奖",
        "new": "该厂“茶叶盒礼品包装”获省轻工系统优秀设计奖",
        "source": "workbench/ocr/raw/中/part01/page_0051.txt:59-65；上下文为市印铁厂",
    },
]

LEFT_UNTOUCHED = [
    "其余 `该广` 尚未逐页闭合，继续保留候选，不做全局替换。",
    "本批证据主要来自 raw OCR，同页上下文多处 `该厂` 互证；未使用或展示页图。",
    "`一一批/一一些` 类残留仍按高风险项处理，等待更强源页证据。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


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
        verify = target.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        for item in items:
            item["verified"] = verify.count(item["new"])
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Raw OCR context-backed enterprise `该广` residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact enterprise contexts with same-page OCR context are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 企业段该广残留补修第一百零三批：raw OCR 同页互证",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应中册正文源稿/全书汇总中的企业段 `该广` OCR 残留。",
        "- 只处理同页上下文能确认为 `该厂` 的精确短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次运行新增替换：{payload['changed_this_run']} 处",
        f"- 当前核验覆盖：{payload['verified_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百零三批：企业段该广残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做回源修复，处理工艺美术/轻工企业段 5 个 `该广 -> 该厂` 残留：羽毛画、东海县工艺绣品联营厂、市刺绣厂、赣榆县石英厂/陶瓷厂、市印铁厂。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_raw_backed_enterprise_gaiguang_batch103_20260706.md`。
- 边界：其余 `该广` 不做全局替换；`一一批/一一些` 继续等待更强源页证据；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
