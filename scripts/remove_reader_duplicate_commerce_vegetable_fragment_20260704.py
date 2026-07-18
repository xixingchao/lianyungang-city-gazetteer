# -*- coding: utf-8 -*-
"""Remove duplicated raw-line vegetable sales fragment from the main reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_duplicate_commerce_vegetable_fragment_removed_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_duplicate_commerce_vegetable_fragment_removed_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_商业蔬菜销售重复断行残片撤出.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COMPLETE = """<p>蔬菜销售建国初期，菜摊菜挑自由卖菜，每年春秋，附近赣榆县的沙河、墩尚、殷庄，东海县的白塔埠、富安等地农民到新浦卖菜，菜挑多沿街叫卖。1955年，市商业科和市工商联联合加强市场管理，建立蔬菜交易市场，规定菜贩进场销售明码标价，不得随意抬价，掺假使杂，短斤少两。新浦当时3万多人口，每天销售蔬菜几千公斤，最多不超过5000公斤。</p>
<p>1956年，新浦一部分菜摊菜贩成立合作小组，在国营公司领导下卖菜，全年销售200多万公斤。国营蔬菜公司以经营咸、干菜、调味品为主，计有木耳、黄花菜、笋干、花椒、八角等20多个品种，向供销社、合作组、个体户批发。鲜菜只供应驻军，节日向居民供应。</p>
<p>全年蔬菜销售额70多万元，其中咸干菜、调味品50多万元。销售鲜菜200多万公斤，外调13.5万公斤，计20多万元。经营大宗鲜菜损耗大，当年亏损12700元，经省市同意，在国营商业利润中抵减，称为“亏损补贴”。</p>"""

FRAGMENT = """<p>蔬菜销售建国初期，菜摊菜挑自由卖菜，每年春秋，附近赣榆县的沙河、墩尚、殷庄，</p>
<p>东海县的白塔埠、富安等地农民到新浦卖菜，菜挑多沿街叫卖。1955年，市商业科和市工</p>
<p>商联联合加强市场管理，建立蔬菜交易市场，规定菜贩进场销售明码标价，不得随意抬价，</p>
<p>掺假使杂，短斤少两。新浦当时3万多人口，每天销售蔬菜几千公斤，最多不超过5000公</p>
<p>斤。</p>
<p>1956年，新浦一部分菜摊菜贩成立合作小组，在国营公司领导下卖菜，全年销售200</p>
<p>多万公斤。国营蔬菜公司以经营咸、干菜、调味品为主，计有木耳、黄花菜、笋干、花椒、八</p>
<p>角等20多个品种，向供销社、合作组、个体户批发。鲜菜只供应驻军，节日向居民供应。</p>
<p>全年蔬菜销售额70多万元，其中咸干菜、调味品50多万元。销售鲜菜200多万公斤，外</p>
<p>调13.5万公斤，计20多万元。经营大宗鲜菜损耗大，当年亏损12700元，经省市同意，在</p>
<p>国营商业利润中抵减，称为“亏损补贴”。</p>"""


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    if COMPLETE not in text:
        raise RuntimeError("complete polished vegetable-sales block is missing; refusing to remove fragment")
    count = text.count(FRAGMENT)
    if count:
        text = text.replace(FRAGMENT, "")
        HTML.write_text(text, encoding="utf-8")
    verify = HTML.read_text(encoding="utf-8")
    if COMPLETE not in verify or FRAGMENT in verify:
        raise RuntimeError("duplicate fragment removal verification failed")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第三十三卷商业蔬菜销售重复断行残片撤出",
        "reader_path": str(HTML),
        "removed_fragments": count,
        "principle": "主阅读版已有完整精修段，仅撤出同段原始断行重复残片；正文源不改。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = f"""# 商业蔬菜销售重复断行残片撤出

- 时间：{now}
- 阅读器：`{HTML}`
- 撤出重复残片：{count} 组。
- 原则：主阅读版已有完整精修段，仅撤出同段原始断行重复残片；正文源不改。
- 相关源证据：`workbench/ocr/paddle_ocr/中/part02/page_0149.txt:19`；金额单位已在第五十批修复为 `70多万元`。
"""
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-04 商业蔬菜销售重复断行残片撤出"
    memory = f"""
{marker}
- 主阅读版 `output/final_reader/连云港市志_全书.html` 同时存在商业蔬菜销售完整精修段和同段原始断行残片；已撤出重复断行残片 {count} 组。
- 正文源 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 和分卷源不改，避免破坏回源材料。
- 报告：`output/reports/reader_duplicate_commerce_vegetable_fragment_removed_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"removed_fragments": count, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
