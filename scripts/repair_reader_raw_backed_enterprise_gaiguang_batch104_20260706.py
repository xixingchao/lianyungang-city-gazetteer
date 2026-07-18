# -*- coding: utf-8 -*-
"""Repair narrowly source-backed enterprise and chemistry residues, batch 104."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_raw_backed_enterprise_gaiguang_batch104_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_raw_backed_enterprise_gaiguang_batch104_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_企业段该广与溴甲烷残留回源补修第一百零四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "连云港市冷冻加工厂开头",
        "old": "连云港市冷冻加工厂该广位于赣榆县徐福镇",
        "new": "连云港市冷冻加工厂该厂位于赣榆县徐福镇",
        "source": "workbench/ocr/raw/中/part01/page_0074.txt:7-15；企业简介开头",
    },
    {
        "label": "连云港市葡萄酒厂开头",
        "old": "连云港市葡萄酒厂该广位于新浦区幸福路9号",
        "new": "连云港市葡萄酒厂该厂位于新浦区幸福路9号",
        "source": "workbench/ocr/raw/中/part01/page_0093.txt:32-39；企业简介开头",
    },
    {
        "label": "连云港市酿化厂开头",
        "old": "连云港市酿化厂该广位于新浦海连中路26号",
        "new": "连云港市酿化厂该厂位于新浦海连中路26号",
        "source": "workbench/ocr/raw/中/part01/page_0102.txt:4-9；企业简介开头",
    },
    {
        "label": "洪门果酒厂协助该厂",
        "old": "洪门果酒广协助该广进行葡萄糖异构酶研制",
        "new": "洪门果酒厂协助该厂进行葡萄糖异构酶研制",
        "source": "workbench/ocr/raw/中/part01/page_0110.txt:13-16；上下文为洪门果酒厂/该厂",
    },
    {
        "label": "云雾茶该场投资",
        "old": "1984年，该广投资20万元，扩建更新全套生产设备",
        "new": "1984年，该场投资20万元，扩建更新全套生产设备",
        "source": "workbench/ocr/raw/中/part01/page_0112.txt:8-16；上文连续称江苏省南云台林场/该场",
    },
    {
        "label": "溴甲烷化工产品",
        "old": "市海水化工厂试制成漠甲烷",
        "new": "市海水化工厂试制成溴甲烷",
        "source": "workbench/ocr/raw/下/part01/page_0443.txt:28；化工品名，邻页列十溴二苯醚",
    },
]

LEFT_UNTOUCHED = [
    "其余 `该广`、企业名中的 `广` 仍需逐页闭合，继续保留候选。",
    "`一一批/一一些` 仍不做全局替换。",
    "本批未使用或展示页图。",
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
        "scope": "Raw OCR context-backed enterprise `该广` and bromomethane residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with source-page evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 企业段该广与溴甲烷残留补修第一百零四批：raw OCR 回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的企业简介开头、糖厂/茶叶段和科技推广化工品名残留。",
        "- 只处理源页上下文能够闭合的精确短语。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百零四批：企业段与溴甲烷残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做回源修复，处理冷冻加工厂、葡萄酒厂、酿化厂开头 `该广 -> 该厂`，糖厂段 `洪门果酒广/该广 -> 洪门果酒厂/该厂`，制茶段 `该广 -> 该场`，科技应用段 `漠甲烷 -> 溴甲烷`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_raw_backed_enterprise_gaiguang_batch104_20260706.md`。
- 边界：其余 `该广`、`一一批/一一些` 不做全局替换；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
