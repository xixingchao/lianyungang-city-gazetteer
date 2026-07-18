# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed `方吨/方大卡` residues in reader/body text."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_wandun_paddle_backed_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_wandun_paddle_backed_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_方吨残留PaddleOCR证据修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("食品罐头年产能力", "年产能力为1.5方吨", "年产能力为1.5万吨", "workbench/ocr/paddle_ocr/中/part01/page_0085.txt"),
    ("白酒生产能力", "白酒生产能力3.5方吨", "白酒生产能力3.5万吨", "workbench/ocr/paddle_ocr/中/part01/page_0085.txt"),
    ("啤酒扩建能力", "年增1方吨啤酒能力", "年增1万吨啤酒能力", "workbench/ocr/paddle_ocr/中/part01/page_0086.txt"),
    ("啤酒年产能力", "年产能力增到1.5方吨", "年产能力增到1.5万吨", "workbench/ocr/paddle_ocr/中/part01/page_0087.txt"),
    ("啤酒总能力", "年产能力4.5方吨", "年产能力4.5万吨", "workbench/ocr/paddle_ocr/中/part01/page_0087.txt"),
    ("水产冻品", "加工水产冻品2.95方吨", "加工水产冻品2.95万吨", "workbench/ocr/paddle_ocr/中/part01/page_0109.txt"),
    ("石灰膏", "年产1方吨石灰膏", "年产1万吨石灰膏", "workbench/ocr/paddle_ocr/中/part01/page_0279.txt"),
    ("石灰总产量", "年总产量达11.43方吨", "年总产量达11.43万吨", "workbench/ocr/paddle_ocr/中/part01/page_0279.txt"),
    ("水泥年产能力", "形成5方吨年产能力", "形成5万吨年产能力", "workbench/ocr/paddle_ocr/中/part01/page_0280.txt"),
    ("水泥年产能力换行", "形成5方吨年", "形成5万吨年", "workbench/ocr/paddle_ocr/中/part01/page_0280.txt"),
    ("磷酸厂", "锦屏磷矿1.5方吨磷酸厂", "锦屏磷矿1.5万吨磷酸厂", "workbench/ocr/paddle_ocr/中/part01/page_0299.txt"),
    ("冷水机组", "3×100方大卡冷水机组", "3×100万大卡冷水机组", "workbench/ocr/paddle_ocr/中/part01/page_0320.txt"),
    ("发酵间", "1.5方吨发酵间", "1.5万吨发酵间", "workbench/ocr/paddle_ocr/中/part01/page_0320.txt"),
    ("包装间", "3方吨包装间", "3万吨包装间", "workbench/ocr/paddle_ocr/中/part01/page_0320.txt"),
    ("水晶储量", "水晶总储量25.54方吨", "水晶总储量25.54万吨", "workbench/ocr/paddle_ocr/中/part01/page_0391.txt"),
    ("水晶可采资源", "可采资源总量约2.55方吨", "可采资源总量约2.55万吨", "workbench/ocr/paddle_ocr/中/part01/page_0391.txt"),
    ("玄武岩开采量", "年开采量30方吨，生产石块", "年开采量30万吨，生产石块", "workbench/ocr/paddle_ocr/中/part01/page_0393.txt"),
    ("港口重点建设项目", "重点建设项自之一", "重点建设项目之一", "workbench/ocr/paddle_ocr/中/part01/page_0437.txt"),
    ("深水泊位", "4个方吨级以上深水", "4个万吨级以上深水", "workbench/ocr/paddle_ocr/中/part01/page_0437.txt"),
    ("船舶吨级", "2.5方吨级船舶", "2.5万吨级船舶", "workbench/ocr/paddle_ocr/中/part01/page_0438.txt"),
    ("煤炭堆场", "堆存10方吨煤炭", "堆存10万吨煤炭", "workbench/ocr/paddle_ocr/中/part01/page_0444.txt"),
    ("民国26年上半年输出煤", "14.7方吨", "14.7万吨", "workbench/ocr/paddle_ocr/中/part01/page_0451.txt"),
    ("枣庄煤输出", "达118方吨", "达118万吨", "workbench/ocr/paddle_ocr/中/part01/page_0451.txt"),
    ("1953年出口数量", "数量为22.17方吨", "数量为22.17万吨", "workbench/ocr/paddle_ocr/中/part01/page_0451.txt"),
    ("1953年出口数量换行", "22.17方吨", "22.17万吨", "workbench/ocr/paddle_ocr/中/part01/page_0451.txt"),
    ("磷矿石输出", "磷矿石33方吨", "磷矿石33万吨", "workbench/ocr/paddle_ocr/中/part01/page_0457.txt"),
    ("外轮载重", "载重1.08方吨", "载重1.08万吨", "workbench/ocr/paddle_ocr/中/part01/page_0457.txt"),
    ("淮北海盐", "准北海盐5.62方吨", "准北海盐5.62万吨", "workbench/ocr/paddle_ocr/中/part01/page_0459.txt"),
    ("出口煤炭", "出口煤炭122.66方吨", "出口煤炭122.66万吨", "workbench/ocr/paddle_ocr/中/part01/page_0471.txt"),
    ("出口煤炭换行", "122.66方吨", "122.66万吨", "workbench/ocr/paddle_ocr/中/part01/page_0471.txt"),
]

SKIPPED_NOTE = "其余 `方吨` 残留未在本轮改动：部分可能为 `万立方米/万吨/万元` 等不同单位，需逐页回源。"


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        target_items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            target_items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [item[1] for item in REPLACEMENTS if item[1] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals}")
        covered = sum(verify.count(new) for _label, _old, new, _source in REPLACEMENTS)
        applied.append({
            "target": str(target),
            "items": target_items,
            "changed": sum(item["count"] for item in target_items),
            "covered_occurrences": covered,
        })

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "PaddleOCR-backed 方吨/方大卡 residue repair",
        "targets": applied,
        "verified_patterns": len(REPLACEMENTS),
        "current_run_replacements": sum(target["changed"] for target in applied),
        "covered_occurrences_after_repair": sum(target["covered_occurrences"] for target in applied),
        "principle": "Only exact long-context replacements with PaddleOCR evidence are changed.",
        "skipped": SKIPPED_NOTE,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 方吨残留 PaddleOCR 证据修复",
        "",
        f"- 时间：{now}",
        "- 范围：最终阅读版与正文汇总中的 `方吨/方大卡/重点建设项自之一` 小批残留。",
        "- 原则：只改 PaddleOCR 页文本能支撑的长上下文，不做全局 `方吨→万吨`。",
        f"- 证据短语：{payload['verified_patterns']} 项。" ,
        f"- 本次复跑实际替换：{payload['current_run_replacements']} 处。" ,
        f"- 修复后证据短语覆盖出现：{payload['covered_occurrences_after_repair']} 处。" ,
        f"- 暂缓：{SKIPPED_NOTE}",
        "",
        "## 文件",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-04 方吨残留 PaddleOCR 证据修复

- 对最终阅读版和正文汇总执行 PaddleOCR 证据支撑的 `方吨/方大卡` 小批修复；证据短语 {payload['verified_patterns']} 项，本次复跑实际替换 {payload['current_run_replacements']} 处，修复后覆盖出现 {payload['covered_occurrences_after_repair']} 处。
- 典型修复：白酒/啤酒/水产冻品/石灰/水泥/水晶储量/港口泊位与吞吐、煤盐矿石输出等上下文中的 `方吨` 改为 `万吨`，`3×100方大卡` 改为 `3×100万大卡`。
- 同步修复港口段 `重点建设项自之一` 为 `重点建设项目之一`。
- 报告：`output/reports/reader_readability_wandun_paddle_backed_20260704.md`。
- 暂缓未证实的其它 `方吨`：可能分别对应万吨、万立方米、万元等，后续按页回源，不做机械替换。
"""
    upsert_memory(MEMORY, "## 2026-07-04 方吨残留 PaddleOCR 证据修复", memory)
    print(json.dumps({
        "verified_patterns": payload["verified_patterns"],
        "current_run_replacements": payload["current_run_replacements"],
        "covered_occurrences_after_repair": payload["covered_occurrences_after_repair"],
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
