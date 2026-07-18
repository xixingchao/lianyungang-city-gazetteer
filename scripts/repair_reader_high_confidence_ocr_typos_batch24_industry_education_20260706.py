# -*- coding: utf-8 -*-
"""Twenty-fourth batch: PaddleOCR-backed industry, education, and technology fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch24_industry_education_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch24_industry_education_20260706.json"

CHANGES = [
    {
        "old": "1982年，连云港市农业机械广试制成功由中国林业科学院南京林化研究所、连云港市农业机械厂",
        "new": "1982年，连云港市农业机械厂试制成功由中国林业科学院南京林化研究所、连云港市农业机械厂",
        "section": "机械工业松针粉加工成套设备段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0200.txt:35 raw 作农业机械广",
            "workbench/ocr/paddle_ocr/中/part01/page_0200.txt:37 与 page_0201.txt:4 PaddleOCR 作农业机械厂",
        ],
    },
    {
        "old": "1975年更名为连云港市农业机械广。产品有脱粒机、弹花机、空气锤等农业机械",
        "new": "1975年更名为连云港市农业机械厂。产品有脱粒机、弹花机、空气锤等农业机械",
        "section": "机械工业连云港市农业机械厂简介",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0202.txt:5 raw 作农业机械广",
            "workbench/ocr/paddle_ocr/中/part01/page_0202.txt:4 PaddleOCR 作农业机械厂",
        ],
    },
    {
        "old": "厂内设12个科室和农业机械、铸造、畜牧机械3个分广",
        "new": "厂内设12个科室和农业机械、铸造、畜牧机械3个分厂",
        "section": "机械工业赣榆县农业机械修理制造厂简介",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0202.txt:32 raw 作分广",
            "workbench/ocr/paddle_ocr/中/part01/page_0202.txt:27 PaddleOCR 作分厂",
        ],
    },
    {
        "old": "上海客车厂联营成立上海客车厂连云港分广，开始生产",
        "new": "上海客车厂联营成立上海客车厂连云港分厂，开始生产",
        "section": "机械工业汽车制造段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0207.txt:25 raw 作分广",
            "workbench/ocr/paddle_ocr/中/part01/page_0207.txt:26 PaddleOCR 作分厂",
        ],
    },
    {
        "old": "江苏省汽车运输公司连云港分公司修理广3家",
        "new": "江苏省汽车运输公司连云港分公司修理厂3家",
        "section": "机械工业汽车制造段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0207.txt:29 raw 作修理广",
            "workbench/ocr/paddle_ocr/中/part01/page_0207.txt:30 PaddleOCR 作修理厂",
        ],
    },
    {
        "old": "附属电机厂从新海电广划出，成立新海连市电机制造厂",
        "new": "附属电机厂从新海电厂划出，成立新海连市电机制造厂",
        "section": "机械工业电动机段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0220.txt:22 raw 作新海电广",
            "workbench/ocr/paddle_ocr/中/part01/page_0220.txt:22 PaddleOCR 作新海电厂",
        ],
    },
    {
        "old": "连云港市锦屏机械广、赣榆县农机修造厂生产电动机1381台",
        "new": "连云港市锦屏机械厂、赣榆县农机修造厂生产电动机1381台",
        "section": "机械工业电动机段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0220.txt:28 raw 作机械广",
            "workbench/ocr/paddle_ocr/中/part01/page_0220.txt:28 PaddleOCR 作机械厂",
        ],
    },
    {
        "old": "成立连云港电线电缆总户，下设电线分厂、电缆分广、电磁线分广",
        "new": "成立连云港电线电缆总厂，下设电线分厂、电缆分厂、电磁线分厂",
        "section": "电工电器及材料电线电缆段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0221.txt:38 raw 作总户/分广",
            "workbench/ocr/paddle_ocr/中/part01/page_0221.txt:38 PaddleOCR 作总厂/分厂",
        ],
    },
    {
        "old": "南京无线电广转让的“熊猫”牌SL8611双卡立体声电脑选曲收录机",
        "new": "南京无线电厂转让的“熊猫”牌SL861-1双卡立体声电脑选曲收录机",
        "section": "电子工业收录机段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0238.txt:35 raw 作无线电广/SL8611",
            "workbench/ocr/paddle_ocr/中/part01/page_0238.txt:36 PaddleOCR 作无线电厂/SL861-1",
        ],
    },
    {
        "old": "市无线电专用设备厂迁入新广址生产",
        "new": "市无线电专用设备厂迁入新厂址生产",
        "section": "电子专用设备冲床段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0263.txt:37 raw 作新广址",
            "workbench/ocr/paddle_ocr/中/part01/page_0263.txt:38 PaddleOCR 作新厂址",
        ],
    },
    {
        "old": "同年，房山镇成立房山采石厂广",
        "new": "同年，房山镇成立房山采石厂",
        "section": "建材工业石材段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0276.txt:17 raw 作采石厂广",
            "workbench/ocr/paddle_ocr/中/part01/page_0276.txt:17 PaddleOCR 作采石厂",
        ],
    },
    {
        "old": "东海县洪庄、石湖、驼峰、石榴、浦南第二砖广等",
        "new": "东海县洪庄、石湖、驼峰、石榴、浦南第二砖厂等",
        "section": "乡镇企业砖瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0399.txt:24 raw 作砖广",
            "workbench/ocr/paddle_ocr/中/part01/page_0399.txt:24 PaddleOCR 作砖厂",
        ],
    },
    {
        "old": "乡办工厂的第一代职工。人厂社员农忙务农，农闲务工",
        "new": "乡办工厂的第一代职工。入厂社员农忙务农，农闲务工",
        "section": "乡镇企业职工构成段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0410.txt:8 raw 作人厂社员",
            "workbench/ocr/paddle_ocr/中/part01/page_0410.txt:7 PaddleOCR 作入厂社员",
        ],
    },
    {
        "old": "认识实习一般为2周时间，生产实习一一般为8周时间",
        "new": "认识实习一般为2周时间，生产实习一般为8周时间",
        "section": "中等专业学校课程段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0386.txt:11 raw 作一一般",
            "workbench/ocr/paddle_ocr/下/part01/page_0386.txt:11 PaddleOCR 作一般",
        ],
    },
    {
        "old": "一、能源1960年，新海发电广改设计循环水泵水封及真空系统",
        "new": "一、能源1960年，新海发电厂改设计循环水泵水封及真空系统",
        "section": "科技工业能源段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0441.txt:22 raw 作新海发电广",
            "workbench/ocr/paddle_ocr/下/part01/page_0441.txt:24 PaddleOCR 作新海发电厂",
        ],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}: {change['old']}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修 raw OCR 与页级 PaddleOCR 对照闭合的工业、教育和科技短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十四批：工业、教育与科技短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- {item['section']}：`{item['old']}` -> `{item['new']}`（命中 {item['count']} 处）")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版；不改中间 OCR 原文。",
        "- 未批量替换全部 `广/厂`、`人/入`、`一一般/一般`，只处理本批已回源闭合项。",
        "- 人大视察段的 `新海发电广` 因本地缺对应页级 PaddleOCR 单页文本，本批暂缓。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
