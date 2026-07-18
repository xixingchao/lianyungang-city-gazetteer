# -*- coding: utf-8 -*-
"""Repair narrowly Paddle-backed yiyi residues and one glass-fiber break, batch 107."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_yiyi_and_glass_batch107_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_yiyi_and_glass_batch107_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_一一批与玻璃纤维断句回源补修第一百零七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "玻璃纤维布1974年产量断句",
        "old": "1973年，连云港市“五七”厂用埚炉生产玻璃纤维，当年生产6.83吨。1974年，该广24.45万米。",
        "new": "1973年，连云港市“五七”厂用坩埚炉生产玻璃纤维，当年生产6.83吨。1974年，该厂除生产玻璃纤维11.8吨外，还安装了4台老式织布机，开始织造玻璃纤维布，年产玻纤布24.45万米。",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0286.txt:1973-1974玻璃纤维整句",
    },
    {
        "label": "玻璃纤维布1974年产量断行",
        "old": "1973年，连云港市“五七”厂用埚炉生产玻璃纤维，当年生产6.83吨。1974年，该广\n24.45万米。",
        "new": "1973年，连云港市“五七”厂用坩埚炉生产玻璃纤维，当年生产6.83吨。1974年，该厂除生产玻璃纤维11.8吨外，还安装了4台老式织布机，开始织造玻璃纤维布，年产玻纤布\n24.45万米。",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0286.txt；源稿断行形态",
    },
    {
        "label": "物资机电产品一批",
        "old": "调进一一批废旧机电产品",
        "new": "调进一批废旧机电产品",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0273.txt:调进一批废旧机电产品",
    },
    {
        "label": "干部培训一些业务基础知识",
        "old": "一一些业务基础知识",
        "new": "一些业务基础知识",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0445.txt:一些业务基础知识",
    },
    {
        "label": "整党整风第一批",
        "old": "第一一批以市级国家机关工作人员为主",
        "new": "第一批以市级国家机关工作人员为主",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0449.txt:第一批以市级国家机关工作人员为主",
    },
    {
        "label": "检察查处一批贪污贿赂",
        "old": "查处一一批贪污贿赂经济犯罪",
        "new": "查处一批贪污贿赂经济犯罪",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0108.txt:查处一批贪污贿赂经济犯罪",
    },
    {
        "label": "检察查处一批贪污贿赂断行",
        "old": "查处一一批贪污贿赂经济犯",
        "new": "查处一批贪污贿赂经济犯",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0108.txt；源稿断行形态",
    },
    {
        "label": "诗歌创作一批新苗",
        "old": "涌现出一一批诗歌创作新苗",
        "new": "涌现出一批诗歌创作新苗",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0018.txt:涌现出一批诗歌创作新苗",
    },
    {
        "label": "文化馆培养一批人才",
        "old": "培养了一一批美术、摄影、音乐、舞蹈、戏剧创作和表、导、演人才",
        "new": "培养了一批美术、摄影、音乐、舞蹈、戏剧创作和表、导、演人才",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0047.txt:培养了一批美术、摄影、音乐、舞蹈、戏剧创作和表、导、演人才",
    },
    {
        "label": "科技档案一些名特优产品",
        "old": "全市一一些名特优产品也建立了档案",
        "new": "全市一些名特优产品也建立了档案",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0060.txt:全市一些名特优产品也建立了档案",
    },
]

LEFT_UNTOUCHED = [
    "未处理地名、人名、古文中的正常 `广`。",
    "未对 `进人/收人/投人/并人/深人` 做全局替换。",
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
        "scope": "Paddle OCR-backed duplicate-one and glass-fiber paragraph repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with Paddle OCR evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 一一批与玻璃纤维断句补修第一百零七批：PaddleOCR 回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的 `一一批/一一些/第一一批` 残留。",
        "- 建材玻璃纤维段 1974 年断句缺文。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百零七批：一一批与玻璃纤维断句"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 PaddleOCR 回源修复，处理 `调进一一批废旧机电产品`、`一一些业务基础知识`、`第一一批`、检察/文化/档案段 `一一批/一一些` 残留，并补全建材玻璃纤维段 1974 年产量断句。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_yiyi_and_glass_batch107_20260706.md`。
- 边界：地名、人名、古文正常 `广` 未处理；`进人/收人/投人/并人/深人` 未做全局替换；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
