# -*- coding: utf-8 -*-
"""Repair narrowly Paddle-backed OCR residues, batch 115 follow-up."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_tax_health_batch115_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_tax_health_batch115_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_筵席税与副溶血性弧菌残留回源补修第一百一十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
FIRST_RUN_CHANGED = 19

REPLACEMENTS = [
    {
        "label": "动植物检疫机构牌子",
        "old": "个机构两块牌子一一-中华人民共和国南京商品检验局连云港商品检验处",
        "new": "一个机构两块牌子———中华人民共和国南京商品检验局连云港商品检验处",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0513.txt:33；raw 同页漏作个机构并误识破折号",
    },
    {
        "label": "进口检疫雏鸡",
        "old": "维鸡4批2.14万只",
        "new": "雏鸡4批2.14万只",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0513.txt:34；raw 同页误作维鸡",
    },
    {
        "label": "出口商品生产基地扶持物资补贴漏行",
        "old": "发放工业贷款8212万元，化肥\n虾、水貂、肉鸡养殖及芦笋、棉花种植等生产基地16个",
        "new": "发放工业贷款8212万元，化肥\n2657吨，钢材228吨，对出口商品生产企业实行价格之外的补贴667万元，从而形成了对\n虾、水貂、肉鸡养殖及芦笋、棉花种植等生产基地16个",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0177.txt:4-7；raw 漏 `2657吨...从而形成了对`",
    },
    {
        "label": "出口商品生产基地扶持物资补贴漏行 HTML",
        "old": "发放工业贷款8212万元，化肥虾、水貂、肉鸡养殖及芦笋、棉花种植等生产基地16个",
        "new": "发放工业贷款8212万元，化肥2657吨，钢材228吨，对出口商品生产企业实行价格之外的补贴667万元，从而形成了对虾、水貂、肉鸡养殖及芦笋、棉花种植等生产基地16个",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0177.txt:4-7；raw 漏 `2657吨...从而形成了对`",
    },
    {
        "label": "饮食服务业筵席",
        "old": "包办链席的聚乐园",
        "new": "包办筵席的聚乐园",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0151.txt:76；raw 同页误作链席",
    },
    {
        "label": "筵席娱乐税题名",
        "old": "链席、娱乐、文化娱乐税",
        "new": "筵席、娱乐、文化娱乐税",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0323.txt:37",
    },
    {
        "label": "筵席税按价",
        "old": "链席税按价",
        "new": "筵席税按价",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0323.txt:38",
    },
    {
        "label": "筵席起征点",
        "old": "链席起征点",
        "new": "筵席起征点",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0324.txt:6",
    },
    {
        "label": "筵席及娱乐税",
        "old": "链席及娱乐税",
        "new": "筵席及娱乐税",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0332.txt:13",
    },
    {
        "label": "副溶血性弧菌污染",
        "old": "副溶血性孤菌污染",
        "new": "副溶血性弧菌污染",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0170.txt:7；raw 同页误作孤菌",
    },
    {
        "label": "副溶血性弧菌污染断行残留",
        "old": "副溶血性孤菌污",
        "new": "副溶血性弧菌污",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0170.txt:7；正文源/下册读者断行导致未命中完整词",
    },
]

LEFT_UNTOUCHED = [
    "下册科技页 `中国对虾孤菌病防治研究` 的 Paddle 与 raw 同读作 `孤菌病`，本批不凭常识改为弧菌。",
    "`防碍交通安全运行` 和 `中西合壁` 在可用 OCR 中同形，继续保留边界。",
    "乱码文件名下的旧 HTML/旧正文副本不作为当前主交付目标。",
    "本批不使用、不展示页图。",
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
        if not target.exists():
            continue
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
        "scope": "Paddle-backed repair for batch 115 and follow-up OCR residues",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "first_run_changed": FIRST_RUN_CHANGED,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 筵席税与副溶血性弧菌残留补修第一百一十五批：Paddle 回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 当前主阅读版、当前中/下册阅读版，以及对应正文源稿和全书正文汇总。",
        "- 仅处理 Paddle 页级 OCR 明确反证 raw/正文残留的词句。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 首跑替换：{FIRST_RUN_CHANGED} 处",
        f"- 本次复跑替换：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        if target["changed"]:
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百一十五批：筵席税与副溶血性弧菌残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按主阅读版、当前分册阅读版和正文源稿做 Paddle 页级回源补修，处理税务/饮食服务业 `链席 -> 筵席`，卫生正文源稿 `副溶血性孤菌污染 -> 副溶血性弧菌污染`，并补入中册动植物检疫页 `雏鸡4批`、机构牌子破折号，以及外贸机构页 `化肥2657吨，钢材228吨，对出口商品生产企业实行价格之外的补贴667万元，从而形成了对虾...` 漏行。
- 本批证据短语 {len(REPLACEMENTS)} 项，报告：`output/reports/reader_paddle_backed_tax_health_batch115_20260706.md`。
- 边界：下册科技页 `中国对虾孤菌病防治研究` 的 Paddle 与 raw 同读作 `孤菌病`，本批不凭常识改；`防碍交通安全运行`、`中西合壁` 继续保留；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
