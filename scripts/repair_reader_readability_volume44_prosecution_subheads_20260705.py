# -*- coding: utf-8 -*-
"""Repair source-backed volume 44 prosecution chapter boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume44_prosecution_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume44_prosecution_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十四卷检察章标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

CHAPTER_OLD = """<p>直检察民国2（1913年）～民国3年，东海、赣榆、灌云设审检所，后由县知事管理司法、检察。</p>
<p>民国16年至34年8月，实行审检合署。此后，废除兼理司法制度，东海县地方法院设检察处，赣榆、灌云设县司法处，由县长兼理检察、行政事务。</p>
<h3 id="第四十四卷-第二章检察">第二章检察</h3>"""

CHAPTER_NEW = """<h3 id="第四十四卷-第二章检察">第二章检察</h3>
<p>民国2（1913年）～民国3年，东海、赣榆、灌云设审检所，后由县知事管理司法、检察。</p>
<p>民国16年至34年8月，实行审检合署。此后，废除兼理司法制度，东海县地方法院设检察处，赣榆、灌云设县司法处，由县长兼理检察、行政事务。</p>"""

REPAIRS = [
    {
        "label": "第二章检察标题前移",
        "source": f"{SOURCE}:5039-5047",
        "old": CHAPTER_OLD,
        "new": CHAPTER_NEW,
    },
    {
        "label": "一、民国时期地方检察机构",
        "source": f"{SOURCE}:5049",
        "old": "<p>一、民国时期地方检察机构民国2年（1913年）6月，东海县地方检查厅成立，",
        "new": "<h5>一、民国时期地方检察机构</h5>\n<p>民国2年（1913年）6月，东海县地方检查厅成立，",
    },
    {
        "label": "二、人民检察机关",
        "source": f"{SOURCE}:5062",
        "old": "<p>二、人民检察机关1951年7月，灌云县人民检察署成立，隶属苏北人民检察署淮阴分署，",
        "new": "<h5>二、人民检察机关</h5>\n<p>1951年7月，灌云县人民检察署成立，隶属苏北人民检察署淮阴分署，",
    },
    {
        "label": "一、审查批捕",
        "source": f"{SOURCE}:5115",
        "old": "<p>一、审查批捕1955年，市、县检察院根据1954年颁布的《中华人民共和国宪法》、《人民检察院组织法》的规定，",
        "new": "<h5>一、审查批捕</h5>\n<p>1955年，市、县检察院根据1954年颁布的《中华人民共和国宪法》、《人民检察院组织法》的规定，",
    },
    {
        "label": "二、审查起诉（刑事检察）",
        "source": f"{SOURCE}:5301-5325",
        "old": "<p>均作了有罪判决，复查一、二、三季度办的127件起诉案件，起诉正确率98%。",
        "new": "<h5>二、审查起诉</h5>\n<p>1955年10月至1956年4月，审查起诉主要审查犯罪性质与认定的犯罪事实是否符合，审查起诉意见书、送核表和供词是否一致，审查认定的犯罪事实是否完整，证据是否确实、充分，阅卷时作好笔录。</p>\n<p>1956~1957年，审查起诉注意犯罪事实，特别是主要犯罪事实和情节是否清楚，证据是否充分，证据来源是否可靠，各项证据之间和被告供词之间有无矛盾，被告申诉和反证是否经过查证核实等。全面分析案情，弄清犯罪时间、地点、动机、目的、手段等，根据政策标准和法律规定，分析被告是否犯罪，决定起诉或不起诉。</p>\n<p>1958年，公检法联合办案，对起诉案件由“三员”（侦查员、检察员、审判员）汇报，“三长”（公安局长、检察长、法院院长）研究决定，党委批准。检察机关主要是全面阅卷、重点审查，发现问题与预审人员联系，并有重点地提讯被告。对案情复杂可诉可不诉的案件，则采取携卷下乡与群众见面的方法，防止错漏，保证案件质量。当年抽查145个案件，发现有问题的9件，起诉准确率为94%。1959年，市检察院全年审查起诉人犯137人，法院均作了有罪判决，复查一、二、三季度办的127件起诉案件，起诉正确率98%。",
    },
    {
        "label": "三、出庭公诉",
        "source": f"{SOURCE}:5481",
        "old": "<p>三、出庭公诉1956年，全市检察机关担负出庭支持公诉，凡法院召开预备庭，",
        "new": "<h5>三、出庭公诉</h5>\n<p>1956年，全市检察机关担负出庭支持公诉，凡法院召开预备庭，",
    },
    {
        "label": "四、侦查监督",
        "source": f"{SOURCE}:5500",
        "old": "<p>四、侦查监督1955~1957年，检察机关参与公安机关逮捕、预审、搜查、拘留、现场勘验及事故鉴定等工作，",
        "new": "<h5>四、侦查监督</h5>\n<p>1955~1957年，检察机关参与公安机关逮捕、预审、搜查、拘留、现场勘验及事故鉴定等工作，",
    },
    {
        "label": "五、审判监督",
        "source": f"{SOURCE}:5516",
        "old": "<p>五、审判监督1955~1957年，检察机关开始审判监督，主要审查判决书，",
        "new": "<h5>五、审判监督</h5>\n<p>1955~1957年，检察机关开始审判监督，主要审查判决书，",
    },
    {
        "label": "经济检察 一、立案侦查",
        "source": f"{SOURCE}:5535",
        "old": "<p>一、立案侦查1955年，根据最高人民检察院规定，经济检察主要是立案侦查国家机关、工厂、企业、事业和合作社职工贪污盗窃国家和集体财产的犯罪案件",
        "new": "<h5>一、立案侦查</h5>\n<p>1955年，根据最高人民检察院规定，经济检察主要是立案侦查国家机关、工厂、企业、事业和合作社职工贪污盗窃国家和集体财产的犯罪案件",
    },
    {
        "label": "经济检察 二、审查起诉",
        "source": f"{SOURCE}:5579",
        "old": "<p>二、审查起诉1955~1959年，经济检察由审判监督科负责，专人审查。",
        "new": "<h5>二、审查起诉</h5>\n<p>1955~1959年，经济检察由审判监督科负责，专人审查。",
    },
    {
        "label": "法纪检察 一、立案侦查",
        "source": f"{SOURCE}:5594",
        "old": "<p>一、立案侦查1956年，根据《江苏省公安厅、人民检察院、人民法院受理刑事案件试行办法》规定，",
        "new": "<h5>一、立案侦查</h5>\n<p>1956年，根据《江苏省公安厅、人民检察院、人民法院受理刑事案件试行办法》规定，",
    },
    {
        "label": "法纪检察 二、审查起诉",
        "source": f"{SOURCE}:5613",
        "old": "<p>二、审查起诉1955~1966年，法纪检察起诉由审判监督科负责，审查程序同经济检察，",
        "new": "<h5>二、审查起诉</h5>\n<p>1955~1966年，法纪检察起诉由审判监督科负责，审查程序同经济检察，",
    },
    {
        "label": "三、一般监督",
        "source": f"{SOURCE}:5627",
        "old": "<p>三、一般监督1956年，根据最高人民检察院要求，开展一般监督工作，",
        "new": "<h5>三、一般监督</h5>\n<p>1956年，根据最高人民检察院要求，开展一般监督工作，",
    },
    {
        "label": "四、检察通讯员",
        "source": f"{SOURCE}:5637",
        "old": "<p>四、检察通讯员1956年，检察通讯员的设置，是根据最高人民检察院“慎重稳进”方针",
        "new": "<h5>四、检察通讯员</h5>\n<p>1956年，检察通讯员的设置，是根据最高人民检察院“慎重稳进”方针",
    },
    {
        "label": "一、判决、裁定执行监督",
        "source": f"{SOURCE}:5655",
        "old": "<p>一、判决、裁定执行监督1957年，监所检察对判决、裁定执行实行监督，",
        "new": "<h5>一、判决、裁定执行监督</h5>\n<p>1957年，监所检察对判决、裁定执行实行监督，",
    },
    {
        "label": "二、监所监督",
        "source": f"{SOURCE}:5667",
        "old": "<p>二、监所监督1956年起，监所对犯人思想改造工作抓得较紧。",
        "new": "<h5>二、监所监督</h5>\n<p>1956年起，监所对犯人思想改造工作抓得较紧。",
    },
    {
        "label": "一、来信、来访",
        "source": f"{SOURCE}:5693",
        "old": "<p>一、来信、来访1956年，共受理人民来信203件，",
        "new": "<h5>一、来信、来访</h5>\n<p>1956年，共受理人民来信203件，",
    },
    {
        "label": "二、办理申诉案件",
        "source": f"{SOURCE}:5718",
        "old": "<p>二、办理申诉案件1956~1966年，处理来信来访，也对一些申诉案件复查，",
        "new": "<h5>二、办理申诉案件</h5>\n<p>1956~1966年，处理来信来访，也对一些申诉案件复查，",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed: list[dict[str, str]] = []
    for item in REPAIRS:
        count = text.count(item["old"])
        if count != 1:
            raise RuntimeError(f"expected one match for {item['label']}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"label": item["label"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十四卷第二章检察：章标题位置、小标题边界、审查起诉缺段",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": [
            "仅恢复源文独立行可证明的标题边界。",
            "补回刑事检察二、审查起诉分页前半段；不重建表格数字。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十四卷检察章标题边界补修

- 时间：{now}
- 范围：第四十四卷第二章检察。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['label']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 将 `第二章检察` 章标题移回章序前。\n- 补回刑事检察 `二、审查起诉` 分页前半段；不重建批捕、起诉等统计表。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十四卷检察章标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十四卷第二章检察 18 处章/小标题边界，覆盖机构、刑事检察、经济检察、法纪检察、监所检察、控告申诉检察。
- 将 `第二章检察` 章标题移回章序前，并依据 `{SOURCE}:5301-5325` 补回刑事检察 `二、审查起诉` 分页前半段。
- 不重建批捕、起诉等统计表，不改无源证据正文。
- 报告：`output/reports/reader_readability_volume44_prosecution_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
