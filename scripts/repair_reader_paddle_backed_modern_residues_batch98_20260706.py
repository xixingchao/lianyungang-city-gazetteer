# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern prose residues, batch 98."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch98_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch98_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_现代正文残留Paddle回源补修第九十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "罐头厂一些",
        "old": "但是一一些小罐头厂设备简陋",
        "new": "但是一些小罐头厂设备简陋",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0075.txt:84",
    },
    {
        "label": "制药企业一级信用",
        "old": "确认为一一级信用优良企业",
        "new": "确认为一级信用优良企业",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0128.txt:28",
    },
    {
        "label": "柠檬酸厂变电系统",
        "old": "1250干伏安变电系统",
        "new": "1250千伏安变电系统",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0163.txt:23",
    },
    {
        "label": "变压器生产能力",
        "old": "150万干伏安",
        "new": "150万千伏安",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0220.txt:13",
    },
    {
        "label": "电价十千伏以上",
        "old": "10干伏以上供电的降低5%",
        "new": "10千伏以上供电的降低5%",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0377.txt:23-24",
    },
    {
        "label": "电价十千伏以上分行",
        "old": "10干伏以上供电的降低\n5%",
        "new": "10千伏以上供电的降低\n5%",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0377.txt:23-24",
    },
    {
        "label": "乡镇企业一些村镇",
        "old": "市境-些村镇",
        "new": "市境一些村镇",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0414.txt:7",
    },
    {
        "label": "乡镇企业一批专业村",
        "old": "形成一一批专业村、专业组",
        "new": "形成一批专业村、专业组",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0414.txt:8",
    },
    {
        "label": "宋庄乡一些村民",
        "old": "宋庄乡一一些村民",
        "new": "宋庄乡一些村民",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0414.txt:13",
    },
    {
        "label": "军垦部队万亩滩涂",
        "old": "军部队承包方亩滩涂",
        "new": "军垦部队承包万亩滩涂",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0414.txt:13",
    },
    {
        "label": "文联深入生活",
        "old": "组织作者深人生活",
        "new": "组织作者深入生活",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0344.txt:30-31",
    },
    {
        "label": "文联徐淮地区",
        "old": "徐准地区创作交流会",
        "new": "徐淮地区创作交流会",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0344.txt:31-32",
    },
    {
        "label": "文联汪曾祺",
        "old": "注曾祺、王西彦",
        "new": "汪曾祺、王西彦",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0344.txt:32",
    },
    {
        "label": "文联一批作品",
        "old": "创作出一一批优秀的文艺作品",
        "new": "创作出一批优秀的文艺作品",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0344.txt:33",
    },
    {
        "label": "环保年代末",
        "old": "20世纪70年代未，市县环境保护监测部门",
        "new": "20世纪70年代末，市县环境保护监测部门",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0455.txt:5",
    },
    {
        "label": "环保徐淮连海岸带",
        "old": "江苏省徐准连海岸带、海涂环境污染状况调",
        "new": "江苏省徐淮连海岸带、海涂环境污染状况调",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0455.txt:6",
    },
    {
        "label": "环保而且提出",
        "old": "提出保护和治理意见，而宜提出可资改造区域环境的建",
        "new": "提出保护和治理意见，而且提出可资改造区域环境的建",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0455.txt:9",
    },
    {
        "label": "淮海工学院校名",
        "old": "准海工学院",
        "new": "淮海工学院",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0458.txt:16,18; 下/part02/page_0069.txt:20; 下/part02/page_0223.txt:38; 下/part02/page_0231.txt:6-13",
    },
    {
        "label": "淮海工学院断行校名",
        "old": "准海工学\n院",
        "new": "淮海工学\n院",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0395.txt:76-77",
    },
]

LEFT_UNTOUCHED = [
    "不处理用户贴出的混杂转换文本；那一段说明整书 OCR 噪声复杂，必须逐页核证。",
    "不全局替换 `一一`、`深人`、`准`、`干伏` 等高风险字形，只改本批证据闭合的精确上下文。",
    "`S7100/0.4~10` 等同段可疑技术型号未获证据闭合，保留原状。",
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
        "scope": "Source-backed modern prose, unit, proper-name, and environment-section OCR residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with Paddle OCR page evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 现代正文残留补修第九十八批：Paddle 页级回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的现代正文 OCR 残留、单位误识和校名误识。",
        "- 只处理 PaddleOCR 页级文本能够闭合的精确短语。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第九十八批：单位、专名与现代正文残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 Paddle 页级回源，修复 `一一些小罐头厂 -> 一些小罐头厂`、`一一级信用 -> 一级信用`、`干伏安 -> 千伏安`、乡镇企业段 `市境-些/一一批/一一些/军部队承包方亩` 等残留。
- 下册文联与环保段同步修复 `徐准地区 -> 徐淮地区`、`注曾祺 -> 汪曾祺`、`创作出一一批 -> 创作出一批`、`70年代未 -> 70年代末`、`而宜 -> 而且`；正文源稿中的 `准海工学院` 按页级证据修为 `淮海工学院`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch98_20260706.md`。
- 边界：用户贴出的混杂 OCR 段不直接批量修；仍坚持逐页证据闭合，未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
