# -*- coding: utf-8 -*-
"""Repair narrowly source-backed enterprise-name residues, batch 106."""

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
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_raw_backed_enterprise_gaiguang_batch106_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_raw_backed_enterprise_gaiguang_batch106_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_建材针织环保企业广残留回源补修第一百零六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "开发区肉联厂协作企业",
        "old": "大中型肉联广",
        "new": "大中型肉联厂",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:3791-3829；同段为开发区肉联厂/肉联厂协作关系",
    },
    {
        "label": "建材公司下辖企业",
        "old": "市制瓦广、市保温材料厂、市耐火材料广、市玻璃纤维广",
        "new": "市制瓦厂、市保温材料厂、市耐火材料厂、市玻璃纤维厂",
        "source": "workbench/ocr/raw/中/part01/page_0274.txt 与建材企业上下文；同章企业名均为厂",
    },
    {
        "label": "连云港制瓦厂成立",
        "old": "成立连云港制砖厂和连云港制瓦广",
        "new": "成立连云港制砖厂和连云港制瓦厂",
        "source": "workbench/ocr/raw/中/part01/page_0274.txt:1965年5月；下文为市制瓦厂",
    },
    {
        "label": "市水泥厂更名",
        "old": "1975年，该广更名为连云港市水泥厂",
        "new": "1975年，该厂更名为连云港市水泥厂",
        "source": "workbench/ocr/raw/中/part01/page_0284.txt；企业简介为连云港市水泥厂，该厂承前",
    },
    {
        "label": "水泥生产厂家",
        "old": "最大的生产广家",
        "new": "最大的生产厂家",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:15981-15983；水泥产业生产厂家语境",
    },
    {
        "label": "欢墩水泥厂更名",
        "old": "赣榆县欢墩水泥广更名为赣榆县第二水泥厂",
        "new": "赣榆县欢墩水泥厂更名为赣榆县第二水泥厂",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:15983；同章多处为欢墩水泥厂",
    },
    {
        "label": "全市水泥厂产量",
        "old": "全市8家水泥广生产水泥37.4万吨",
        "new": "全市8家水泥厂生产水泥37.4万吨",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:15988；上下文为水泥生产企业/水泥厂",
    },
    {
        "label": "混凝土构件厂简介",
        "old": "1990年，该广建筑面积6.1万平方米",
        "new": "1990年，该厂建筑面积6.1万平方米",
        "source": "workbench/ocr/raw/中/part01/page_0284.txt；前文为连云港市混凝土构件厂",
    },
    {
        "label": "玻璃纤维厂铂金埚",
        "old": "市玻璃纤维广开始更换使用铂金埚",
        "new": "市玻璃纤维厂开始更换使用铂金埚",
        "source": "workbench/ocr/raw/中/part01/page_0286.txt；前后均为市玻璃纤维厂/连云港市玻璃钢厂",
    },
    {
        "label": "玻璃纤维厂铂金埚断行",
        "old": "市玻璃纤维广开始",
        "new": "市玻璃纤维厂开始",
        "source": "workbench/ocr/raw/中/part01/page_0286.txt；源稿断行形态",
    },
    {
        "label": "耐火材料厂更名",
        "old": "更名为连云港市耐火材料广",
        "new": "更名为连云港市耐火材料厂",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:16350；同章企业名为耐火材料厂",
    },
    {
        "label": "耐火材料厂现状",
        "old": "连云港市耐火材料广已发展成为苏北地区唯一生产高铝质耐火材料的厂家",
        "new": "连云港市耐火材料厂已发展成为苏北地区唯一生产高铝质耐火材料的厂家",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:16360；同章企业名为耐火材料厂",
    },
    {
        "label": "耐火材料厂现状断行",
        "old": "连云港市耐火材料广已发展成为苏北地区唯一生产高铝质耐火材料的厂",
        "new": "连云港市耐火材料厂已发展成为苏北地区唯一生产高铝质耐火材料的厂",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:16360；源稿断行形态",
    },
    {
        "label": "东海县针织总厂获评",
        "old": "1989年该广被连云港市评为先进企业",
        "new": "1989年该厂被连云港市评为先进企业",
        "source": "workbench/ocr/raw/中/part01/page_0415.txt；标题为东海县针织总厂，下文为该厂有职工",
    },
    {
        "label": "东海县针织总厂获评断行",
        "old": "1989年该广被连云港市评为先进企",
        "new": "1989年该厂被连云港市评为先进企",
        "source": "workbench/ocr/raw/中/part01/page_0415.txt；源稿断行形态",
    },
    {
        "label": "物资管理市水泥厂",
        "old": "扩建了市水泥广，于1980年投产",
        "new": "扩建了市水泥厂，于1980年投产",
        "source": "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:19350；建筑材料分配语境",
    },
    {
        "label": "物资管理市水泥厂断行",
        "old": "扩建了市水泥广，于1980",
        "new": "扩建了市水泥厂，于1980",
        "source": "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:19350；源稿断行形态",
    },
    {
        "label": "小金库市绝缘材料厂",
        "old": "市绝缘材料广私设“小金库”问题",
        "new": "市绝缘材料厂私设“小金库”问题",
        "source": "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:21459；同书多处为市绝缘材料厂",
    },
    {
        "label": "尘毒治理市绝缘材料厂",
        "old": "市绝缘材料广采用风水相结合的防尘措施",
        "new": "市绝缘材料厂采用风水相结合的防尘措施",
        "source": "workbench/ocr/raw/下/part01/page_0278.txt；劳动保护尘毒治理企业名",
    },
    {
        "label": "噪声治理市电线厂",
        "old": "市电线广在编织车间采用超细玻璃纤维吸声",
        "new": "市电线厂在编织车间采用超细玻璃纤维吸声",
        "source": "workbench/ocr/raw/下/part01/page_0278.txt；同页噪声治理企业名",
    },
]

LEFT_UNTOUCHED = [
    "`1974年，该广24.45万米` 源页缺动词，本批不补写推断内容。",
    "电力章多处 `新海发电广` 留待单独核对，避免跨卷批量误修。",
    "`一一批/一一些` 继续不做全局替换。",
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
        "scope": "Raw/body context-backed enterprise-name residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with source-page or same-chapter evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 建材针织环保企业残留补修第一百零六批：raw/正文回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的建材、针织、环保、物资管理企业名残留。",
        "- 只处理源页或同章上下文能够闭合的精确短语。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百零六批：建材针织环保企业残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做回源修复，处理建材公司下辖企业、制瓦厂、水泥厂、玻璃纤维厂、耐火材料厂、东海县针织总厂、物资管理和劳动保护卷中的 `广 -> 厂` 企业名残留。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_raw_backed_enterprise_gaiguang_batch106_20260706.md`。
- 边界：`1974年，该广24.45万米` 源页缺动词未猜补；电力章 `新海发电广` 留待单独核对；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
