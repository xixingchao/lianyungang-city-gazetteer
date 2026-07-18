# -*- coding: utf-8 -*-
"""Repair source-backed volume 44 trial chapter heading boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume44_trial_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume44_trial_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十四卷审判章标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

REPAIRS = [
    {
        "label": "第三章审判标题前移",
        "source": f"{SOURCE}:5730-5732",
        "old": "<p>审判清雍正二年（1724年）海州升为直隶州，州衙审理海州及赣榆县、沭阳县二审案件。</p>",
        "new": "<h3 id=\"第四十四卷-第三章审判\">第三章审判</h3>\n<p>清雍正二年（1724年）海州升为直隶州，州衙审理海州及赣榆县、沭阳县二审案件。</p>",
    },
    {
        "label": "第一节机构 / 一、清末、民国时期地方审判机构",
        "source": f"{SOURCE}:5759-5760",
        "old": "<p>第一节机•构一、清末、民国时期地方审判机构清末，江苏地方行政兼理司法，分为省、道、府、州县四级，",
        "new": "<h4 id=\"第四十四卷-第三章审判-第一节机构\">第一节机构</h4>\n<h5>一、清末、民国时期地方审判机构</h5>\n<p>清末，江苏地方行政兼理司法，分为省、道、府、州县四级，",
    },
    {
        "label": "二、人民审判机构",
        "source": f"{SOURCE}:5796",
        "old": "<p>二、人民审判机构新海连市人民法院1949年10月，在原司法科基础上组建新海连市人民法院，",
        "new": "<h5>二、人民审判机构</h5>\n<p>新海连市人民法院1949年10月，在原司法科基础上组建新海连市人民法院，",
    },
    {
        "label": "移除错位的第三章/第一节标题",
        "source": f"{SOURCE}:5730-5760",
        "old": "\n<h3 id=\"第四十四卷-第三章审判\">第三章审判</h3>\n<h4 id=\"第四十四卷-第三章审判-第一节机构\">第一节机构</h4>",
        "new": "",
    },
    {
        "label": "一、反革命案件",
        "source": f"{SOURCE}:5869",
        "old": "<p>一、反革命案件1950年10月，根据中共中央、政务院指示，",
        "new": "<h5>一、反革命案件</h5>\n<p>1950年10月，根据中共中央、政务院指示，",
    },
    {
        "label": "二、普通刑事犯罪案件",
        "source": f"{SOURCE}:5975",
        "old": "<p>二、普通刑事犯罪案件杀人案件第一、二次镇压反革命（以下简称镇反运动)运动期间，",
        "new": "<h5>二、普通刑事犯罪案件</h5>\n<p>杀人案件第一、二次镇压反革命（以下简称镇反运动)运动期间，",
    },
    {
        "label": "三、经济犯罪案件",
        "source": f"{SOURCE}:6445",
        "old": "<p>三、经济犯罪案件贪污案件1949~1951年，",
        "new": "<h5>三、经济犯罪案件</h5>\n<p>贪污案件1949~1951年，",
    },
    {
        "label": "四、减刑、假释、特赦",
        "source": f"{SOURCE}:6661",
        "old": "<p>四、减刑、假释、特赦减刑、假释从1983年10月连云港市实行市管县体制后，",
        "new": "<h5>四、减刑、假释、特赦</h5>\n<p>减刑、假释从1983年10月连云港市实行市管县体制后，",
    },
    {
        "label": "一、婚姻家庭案件",
        "source": f"{SOURCE}:6845",
        "old": "<p>一、婚姻家庭案件离婚建国初期，",
        "new": "<h5>一、婚姻家庭案件</h5>\n<p>离婚建国初期，",
    },
    {
        "label": "二、财产权益案件",
        "source": f"{SOURCE}:6978",
        "old": "<p>二、财产权益案件债务建国初期，",
        "new": "<h5>二、财产权益案件</h5>\n<p>债务建国初期，",
    },
    {
        "label": "三、民事案件的执行",
        "source": f"{SOURCE}:7110",
        "old": "<p>三、民事案件的执行1949～1979年，",
        "new": "<h5>三、民事案件的执行</h5>\n<p>1949～1979年，",
    },
    {
        "label": "一、经济合同纠纷案件",
        "source": f"{SOURCE}:7315",
        "old": "<p>一、经济合同纠纷案件1979年12月以前，",
        "new": "<h5>一、经济合同纠纷案件</h5>\n<p>1979年12月以前，",
    },
    {
        "label": "二、农村承包合同纠纷案件",
        "source": f"{SOURCE}:7359",
        "old": "<p>二、农村承包合同纠纷案件1980~1984年，",
        "new": "<h5>二、农村承包合同纠纷案件</h5>\n<p>1980~1984年，",
    },
    {
        "label": "三、涉外经济纠纷案件",
        "source": f"{SOURCE}:7385",
        "old": "<p>三、涉外经济纠纷案件1980~1981年，",
        "new": "<h5>三、涉外经济纠纷案件</h5>\n<p>1980~1981年，",
    },
    {
        "label": "四、经济纠纷案件执行",
        "source": f"{SOURCE}:7413",
        "old": "<p>四、经济纠纷案件执行1956～1957年，",
        "new": "<h5>四、经济纠纷案件执行</h5>\n<p>1956～1957年，",
    },
    {
        "label": "一、申诉",
        "source": f"{SOURCE}:7674",
        "old": "<p>一、申诉：1949年，",
        "new": "<h5>一、申诉</h5>\n<p>1949年，",
    },
    {
        "label": "二、复查",
        "source": f"{SOURCE}:7698-7699",
        "old": "<p>二、复查刑事案件根据全国二届司法会议和全省三次司法会议精神，",
        "new": "<h5>二、复查</h5>\n<p>刑事案件根据全国二届司法会议和全省三次司法会议精神，",
    },
    {
        "label": "三、再审",
        "source": f"{SOURCE}:7898",
        "old": "<p>三、再审建国后，人民法院对审判工作和案件质量的监督，",
        "new": "<h5>三、再审</h5>\n<p>建国后，人民法院对审判工作和案件质量的监督，",
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
        "scope": "第四十四卷第三章审判：章标题、节标题、小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": [
            "仅恢复源文独立行可证明的章、节、小标题边界。",
            "不重建审判章统计表，不改无源证据正文数字。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十四卷审判章标题边界补修

- 时间：{now}
- 范围：第四十四卷第三章审判。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['label']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 将 `第三章审判` 章标题移回章序前，补出 `第一节机构` 与源文小标题边界。\n- 拆出刑事、民事、经济、审判监督各节内源文独立成行的小标题。\n- 不重建审判章内统计表，不改缺少源证的 OCR 正文。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十四卷审判章标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十四卷第三章审判 18 处章/节/小标题边界，覆盖机构、刑事案件审判、民事案件审判、经济案件审判、审判监督。
- 将 `第三章审判` 章标题移回章序前，并将 `第一节机构` 从正文粘连段中拆出。
- 不重建审判章统计表，不改缺少源证的 OCR 正文数字。
- 报告：`output/reports/reader_readability_volume44_trial_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
