# -*- coding: utf-8 -*-
"""Repair the next source-backed readability residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("食品公司宰杀量", "当年宰杀22方头", "当年宰杀22万头", "workbench/ocr/paddle_ocr/中/part01/page_0073.txt:18"),
    ("粮食科学保粮", "1.5~2方吨大米", "1.5~2万吨大米", "workbench/ocr/paddle_ocr/中/part02/page_0244.txt:16"),
    ("粮食保粮数量", "保粮数量达到19.8方吨", "保粮数量达到19.8万吨", "workbench/ocr/paddle_ocr/中/part02/page_0244.txt:35"),
    ("物资计划外煤炭", "计划外煤炭64.19方吨", "计划外煤炭64.19万吨", "workbench/ocr/paddle_ocr/中/part02/page_0260.txt:20"),
    ("农业概述生猪", "生猪存栏101方头", "生猪存栏101万头", "workbench/ocr/paddle_ocr/中/part02/page_0494.txt:34"),
    ("农业概述水产品", "水产品9.1方吨", "水产品9.1万吨", "workbench/ocr/paddle_ocr/中/part02/page_0494.txt:34"),
    ("矿产暂不能利用储量", "暂不能利用储量905方吨", "暂不能利用储量905万吨", "workbench/ocr/paddle_ocr/下/part01/page_0442.txt:8"),
    ("城乡建设供水能力", "日供水能力达9方吨", "日供水能力达9万吨", "workbench/ocr/paddle_ocr/下/part01/page_0454.txt:32"),
    ("淮海戏移植剧目", "移植上演的剧自近于部", "移植上演的剧目近千部", "workbench/ocr/paddle_ocr/下/part02/page_0027.txt:41"),
    ("柳琴戏县名剧目", "山东省绑城县第八区柳琴戏班，曾编演过现代戏《拥军》、《拥抗》、《因祸得福）等剧自", "山东省郯城县第八区柳琴戏班，曾编演过现代戏《拥军》、《拥抗》、《因祸得福》等剧目", "workbench/ocr/paddle_ocr/下/part02/page_0030.txt:15"),
    ("柳琴戏剧目", "路》《牛栏补课》等剧自", "路》、《牛栏补课》等剧目", "workbench/ocr/paddle_ocr/下/part02/page_0030.txt:19"),
    ("淮海剧团杏花烟雨", "排演创作剧目《香花烟雨》，参加连云港市首届专业剧团创作剧自调演", "排演创作剧目《杏花烟雨》，参加连云港市首届专业剧团创作剧目调演", "workbench/ocr/paddle_ocr/下/part02/page_0034.txt:13"),
    ("淮海剧团魂断海州", "排演创作剧自《魂断海州》，参加市第二届专业剧团创作剧自调演", "排演创作剧目《魂断海州》，参加市第二届专业剧团创作剧目调演", "workbench/ocr/paddle_ocr/下/part02/page_0034.txt:15"),
    ("吕剧创作新剧目", "创作新剧自调演，被江苏省椰子剧团", "创作新剧目调演，被江苏省梆子剧团", "workbench/ocr/paddle_ocr/下/part02/page_0037.txt:20-21"),
    ("文工团创作节目", "排练一台创作节自，去南京参加全省专业文艺团体创作节目会演", "排练一台创作节目，去南京参加全省专业文艺团体创作节目会演", "workbench/ocr/paddle_ocr/下/part02/page_0035.txt:13-14"),
    ("文工团创作节目断行", "排练一台创作节自，去南", "排练一台创作节目，去南", "workbench/ocr/paddle_ocr/下/part02/page_0035.txt:13-14"),
    ("文化馆文艺节目", "编播本市新闻和文艺节自", "编播本市新闻和文艺节目", "workbench/ocr/paddle_ocr/下/part02/page_0046.txt:19"),
    ("群众文艺节目120", "演出各类节自120余个", "演出各类节目120余个", "workbench/ocr/paddle_ocr/下/part02/page_0048.txt:32"),
    ("群众文艺节目120断行", "节自120余个", "节目120余个", "workbench/ocr/paddle_ocr/下/part02/page_0048.txt:32"),
    ("群众文艺演出58个节目", "演出58个节自", "演出58个节目", "workbench/ocr/paddle_ocr/下/part02/page_0049.txt:18"),
    ("民间舞蹈节目", "近百个节自参加了演出", "近百个节目参加了演出", "workbench/ocr/paddle_ocr/下/part02/page_0048.txt:35"),
    ("民间舞蹈节目断行", "近百个节自参加", "近百个节目参加", "workbench/ocr/paddle_ocr/下/part02/page_0048.txt:35"),
    ("群众调演剧目节目", "会演的剧自和节自，形式多样，有准海戏", "会演的剧目和节目，形式多样，有淮海戏", "workbench/ocr/paddle_ocr/下/part02/page_0049.txt:26"),
    ("四人帮书名号", "《渔叉对准四人帮”>", "《渔叉对准“四人帮”》", "workbench/ocr/paddle_ocr/下/part02/page_0049.txt:28"),
    ("青年歌手", "第四届青年手大奖赛", "第四届青年歌手大奖赛", "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:8"),
    ("万元户小品", "《小路弯弯》《方元户的追求》", "《小路弯弯》、《万元户的追求》", "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:11"),
    ("冬夜参赛书名号", "《小路弯弯》、《冬夜参加华东戏剧小品比赛", "《小路弯弯》、《冬夜》参加华东戏剧小品比赛", "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:12"),
    ("徐淮盐连", "首届徐准盐连戏剧小品联谊赛", "首届徐淮盐连戏剧小品联谊赛", "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:15"),
    ("徐淮盐连断行", "首届徐准盐连戏剧小", "首届徐淮盐连戏剧小", "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:15"),
    ("最后一朵玫瑰", "选送的最后一朵玫瑰》等6个小品获奖", "选送的《最后一朵玫瑰》等6个小品获奖", "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:16"),
    ("最后一朵玫瑰断行", "选送的最后一朵玫瑰》等6", "选送的《最后一朵玫瑰》等6", "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:16"),
    ("元旦晚会", "元且文艺晚会", "元旦文艺晚会", "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:18"),
]

SKIPPED = [
    "`食盐积压5方吨`：本轮只找到 raw 同形，缺少 PaddleOCR 纠正证据，暂缓。",
    "`方吨啤酒灌装线`：需回看版面确认设备名，暂缓。",
    "矿产 `2253/1076/83方吨`：未取得 PaddleOCR 直接证据，暂缓。",
]


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
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["changed"] for item in targets)
    payload = {
        "time": now,
        "scope": "第二批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "仅修复 PaddleOCR/页文本明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修 PaddleOCR/页文本可证明的长上下文问题。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项"])
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    lines.extend(["", "## 暂缓"])
    for item in SKIPPED:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-04 第二批正文残留回源修复

- 对最终阅读版和正文汇总继续执行回源修复，核验项 {len(REPLACEMENTS)} 项，本次替换 {total} 处。
- 修复范围包括食品公司宰杀量、粮食科学保粮、物资计划外煤炭、农业概述、矿产储量、城乡建设供水，以及文化卷 `剧自/节自/方元户/元且` 等可读性残留。
- 依据：`output/reports/reader_readability_source_backed_batch_20260704.md`。
- 暂缓：`食盐积压5方吨`、`方吨啤酒灌装线`、矿产 `2253/1076/83方吨`，因本轮缺少足够强的异源证据。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第二批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
