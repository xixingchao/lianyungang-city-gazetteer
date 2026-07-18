# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern prose residues, batch 94."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "paddle_上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_PaddleOCR正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch94_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch94_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_现代正文残留Paddle回源补修第九十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "海堤低标准",
        "old": "低标淮海堤",
        "new": "低标准海堤",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上_part02_PaddleOCR汇总.md:22679",
    },
    {
        "label": "专业炼糖企业序数",
        "old": "全国第家专业炼糖企业一连云港市糖厂",
        "new": "全国第一家专业炼糖企业一连云港市糖厂",
        "source": "同章前文 output/final_reader/连云港市志_全书.html:8432 与 OCR 汇总均读 全国第一家专业炼糖企业",
    },
    {
        "label": "孙中山建港夙愿",
        "old": "巨轮的凤愿",
        "new": "巨轮的夙愿",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0437.txt:29",
    },
    {
        "label": "港口概述断裂段 HTML",
        "old": "连云港港已经发1977年前，连云港港始终以内贸运输为主体，1977年后，外贸运输所占比重直线上1984年上升到49.4%",
        "new": "连云港港已经发展成为具有一定规模的内外贸易综合性港口，为国内外所瞩目。1977年前，连云港港始终以内贸运输为主体，1977年后，外贸运输所占比重直线上升。1977年比1976年上升14.1个百分点（1976年外贸吞吐量占总吞吐量的21.08%），1984年上升到49.4%",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0437.txt:35-39",
    },
    {
        "label": "港口概述断裂段 源稿换行",
        "old": "连云港港已经发\n1977年前，连云港港始终以内贸运输为主体，1977年后，外贸运输所占比重直线上\n1984年上升到49.4%",
        "new": "连云港港已经发展成为具有一定规模的内外贸易综合性港口，为国内外所瞩目。\n1977年前，连云港港始终以内贸运输为主体，1977年后，外贸运输所占比重直线上\n升。1977年比1976年上升14.1个百分点（1976年外贸吞吐量占总吞吐量的21.08%），\n1984年上升到49.4%",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0437.txt:35-39",
    },
    {
        "label": "日军海陆军共同管理",
        "old": "由自军的海、陆军共同管理",
        "new": "由日军的海、陆军共同管理",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0449.txt:36",
    },
    {
        "label": "渔船出海口不同情况",
        "old": "根据出海口的不筒情况",
        "new": "根据出海口的不同情况",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0499.txt:10",
    },
    {
        "label": "走私限制作用",
        "old": "起到一一定的作用",
        "new": "起到一定的作用",
        "source": "same paragraph; duplicated 一 is OCR residue after source-backed neighboring repair",
    },
    {
        "label": "邮路干线",
        "old": "二级于线邮路",
        "new": "二级干线邮路",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0067.txt:28",
    },
    {
        "label": "秦山岛海市蜃楼",
        "old": "会出现海市楼，更增加了几分神秘色彩",
        "new": "会出现海市蜃楼，更增加了几分神秘色彩",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0115.txt:10",
    },
    {
        "label": "西游记作者吴承恩",
        "old": "据初步考证，西游记》的作者昊承恩",
        "new": "据初步考证，《西游记》的作者吴承恩",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0018.txt:40",
    },
    {
        "label": "赵明诚李清照",
        "old": "赵明诚、季清照夫妇",
        "new": "赵明诚、李清照夫妇",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0021.txt:22; page_0103.txt:16",
    },
    {
        "label": "米芾墓志残碑正文",
        "old": "米蒂题写的墓志残碑",
        "new": "米芾题写的墓志残碑",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0021.txt:23",
    },
    {
        "label": "米芾墓志残碑标题",
        "old": "米蒂书墓志残碑",
        "new": "米芾书墓志残碑",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0117.txt:31",
    },
    {
        "label": "米芾墓志残碑引文",
        "old": "涟水军使米蒂",
        "new": "涟水军使米芾",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0117.txt:31-32 and related title",
    },
    {
        "label": "李瑞清题刻",
        "old": "季瑞清的“环瀛仰镜”题刻",
        "new": "李瑞清的“环瀛仰镜”题刻",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0021.txt:24; page_0105.txt:37",
    },
]

LEFT_UNTOUCHED = [
    "`停泊3000～5000万吨货轮`、`标石英`、医疗检验名等仍无更强证据，本批未猜改。",
    "`海市楼` 在大事记等多处旧 OCR 中仍见，本批只修对应 Paddle 页明确的秦山岛正文段。",
    "旧转换版/旧 OCR 原文中的大段混乱不作为当前主交付直接证据，继续以 `连云港市志_全书.html` 为主审计对象。",
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
        "scope": "Source-backed modern prose and culture-name residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with Paddle OCR or same-book cross evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 现代正文残留补修第九十四批：Paddle 回源与同书互证",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的少量现代正文残留、断裂句和文化专名错字。",
        "- 只处理 PaddleOCR 页级文本或同书上下文能够闭合的精确短语。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第九十四批：现代正文与文化专名"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续以当前主交付 `output/final_reader/连云港市志_全书.html` 为准，按 Paddle 页级文本和同书互证修复第 94 批残留：`低标淮海堤 -> 低标准海堤`、港口概述 `凤愿 -> 夙愿` 及断裂句、`由自军 -> 由日军`、`不筒情况 -> 不同情况`、`二级于线邮路 -> 二级干线邮路`、秦山岛 `海市蜃楼`、`吴承恩/李清照/米芾/李瑞清` 等。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch94_20260706.md`。
- 边界：`停泊3000～5000万吨货轮`、`标石英`、医疗检验名、书末序跋/古文等无强证据项继续保留；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
