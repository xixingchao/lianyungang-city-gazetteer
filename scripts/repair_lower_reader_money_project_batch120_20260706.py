# -*- coding: utf-8 -*-
"""Repair remaining lower-reader money/project OCR residues backed by full reader/Paddle."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_money_project_batch120_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_money_project_batch120_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_下册万元与跨段项目残留回源补修第一百二十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "东辛奶牛项目跨段",
        "old": "东辛奶牛项</p><p>自协调会",
        "new": "东辛奶牛项</p><p>目协调会",
        "source": "全书版同段为 `东辛奶牛项目协调会`；HTML 分段导致 batch119 未命中",
    },
    {
        "label": "技术改造项目跨段",
        "old": "技术改造项</p><p>自需五亿元",
        "new": "技术改造项</p><p>目需五亿元",
        "source": "全书版同段为 `技术改造项目需五亿元`；HTML 分段导致 batch119 未命中",
    },
    {
        "label": "体育活动项目",
        "old": "体育活动开展的项自和参加活动的人数都不多",
        "new": "体育活动开展的项目和参加活动的人数都不多",
        "source": "同章体育上下文均为活动/比赛项目，raw/Paddle 多处证 `项目`",
    },
    {
        "label": "电力系统推广",
        "old": "在全省电力系</p><p>统推厂",
        "new": "在全省电力系</p><p>统推广",
        "source": "全书版同段为 `在全省电力系统推广`；HTML 分段导致 batch119 未命中",
    },
    {
        "label": "连云市赈灾款",
        "old": "连云市5千方元",
        "new": "连云市5千万元",
        "source": "全书版同段为 `连云市5千万元`；raw 下 part01/page_0028.txt 为方元残留",
    },
    {
        "label": "扶贫救灾款",
        "old": "救灾款33.66方元",
        "new": "救灾款33.66万元",
        "source": "全书版同段为 `救灾款33.66万元`；raw 下 part01/page_0034.txt 为方元残留",
    },
    {
        "label": "扶贫救济款跨段",
        "old": "救济款13.21</p><p>方元",
        "new": "救济款13.21</p><p>万元",
        "source": "全书版同段为 `救济款13.21万元`",
    },
    {
        "label": "扶贫低息农贷款",
        "old": "低息农贷款121.77方元",
        "new": "低息农贷款121.77万元",
        "source": "全书版同段为 `低息农贷款121.77万元`",
    },
    {
        "label": "福利募捐留用",
        "old": "留用96方元",
        "new": "留用96万元",
        "source": "全书版同段为 `留用96万元`；raw 下 part01/page_0040.txt 为方元残留",
    },
    {
        "label": "殡仪馆造价",
        "old": "总造价3方元",
        "new": "总造价3万元",
        "source": "全书版同段为 `总造价3万元`；raw 下 part01/page_0053.txt 为方元残留",
    },
    {
        "label": "劳动服务无息贷款",
        "old": "无息贷款424方元",
        "new": "无息贷款424万元",
        "source": "全书版同段为 `无息贷款424万元`；raw 下 part01/page_0242.txt 为方元残留",
    },
    {
        "label": "锦屏化工厂投资跨段",
        "old": "锦屏化工厂投资70多方</p><p>元",
        "new": "锦屏化工厂投资70多万</p><p>元",
        "source": "全书版同段为 `锦屏化工厂投资70多万元`；raw 下 part01/page_0278.txt 为方元残留",
    },
    {
        "label": "尘毒治理投资",
        "old": "投资153.9方元",
        "new": "投资153.9万元",
        "source": "全书版同段为 `投资153.9万元`；raw 下 part01/page_0278.txt 为方元残留",
    },
    {
        "label": "侨务捐赠总额",
        "old": "接受捐赠折合人民币400多方元",
        "new": "接受捐赠折合人民币400多万元",
        "source": "全书版同段为 `接受捐赠折合人民币400多万元`；raw 下 part01/page_0302.txt 为方元残留",
    },
    {
        "label": "侨务港币捐款跨段",
        "old": "费培捐款10方</p><p>港市",
        "new": "费培捐款10万</p><p>港币",
        "source": "全书版同段为 `费培捐款10万港币`",
    },
    {
        "label": "侨务人民币",
        "old": "3万元人民市",
        "new": "3万元人民币",
        "source": "全书版同段为 `3万元人民币`",
    },
    {
        "label": "工会福利设施资金",
        "old": "资金达7219方元",
        "new": "资金达7219万元",
        "source": "全书版同段为 `资金达7219万元`；raw 下 part01/page_0315.txt 为方元残留",
    },
    {
        "label": "科技三项经费单位",
        "old": "单位：方元",
        "new": "单位：万元",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0427.txt:29 明确为 `单位:万元`",
    },
    {
        "label": "文化馆收入",
        "old": "年均收入约3.5方元",
        "new": "年均收入约3.5万元",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0048.txt:5 明确为 `年均收入约3.5万元`",
    },
    {
        "label": "小品万元户",
        "old": "《方元户的追求》",
        "new": "《万元户的追求》",
        "source": "全书版同段为 `《万元户的追求》`；raw 下 part02/page_0050.txt 为方元户残留",
    },
    {
        "label": "文化训练经费旧人民币",
        "old": "经费200方元（旧人民市）",
        "new": "经费200万元（旧人民币）",
        "source": "全书版同段为 `经费200万元（旧人民币）`；raw 下 part02/page_0051.txt 为方元/人民市残留",
    },
    {
        "label": "盐补贴款",
        "old": "49方元盐补贴款",
        "new": "49万元盐补贴款",
        "source": "全书版同段为 `49万元盐补贴款`；raw 下 part02/page_0353.txt 为方元残留",
    },
]

LEFT_UNTOUCHED = [
    "本批仍不处理未充分核定的 `方人`、其它数字异常和 `准海/准阴/并人/输人`。",
    "只改当前下册分册读者；全书版同段多已正确。",
    "未展示、未嵌入图片。",
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
    text = TARGET.read_text(encoding="utf-8")
    items = []
    for item in REPLACEMENTS:
        count = text.count(item["old"])
        if count:
            text = text.replace(item["old"], item["new"])
        items.append({**item, "count": count})
    TARGET.write_text(text, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = sum(i["count"] for i in items)
    payload = {"time": now, "target": str(TARGET), "changed_this_run": changed, "items": items, "left_untouched": LEFT_UNTOUCHED}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 下册万元与跨段项目残留补修第一百二十批：全书版/Paddle 回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 当前下册阅读版 `output/final_reader/连云港市志_下册.html`。",
        "- 处理全书版同段或 Paddle 页级 OCR 明确支持的跨段项目、推广和万元/币种残留。",
        "",
        "## 统计",
        "",
        f"- 本次替换：{changed} 处",
        "",
        "## 修复项",
        "",
    ]
    for item in items:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`，{item['count']} 处；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百二十批：下册万元与跨段项目残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 按全书版同段和 Paddle 页级 OCR，补修当前下册分册读者中跨段 `项自/推厂` 以及 `方元/人民市/港市` 残留，覆盖扶贫、福利、殡葬、劳动服务、尘毒治理、侨务、工会、科技经费、文化馆、小品、旧人民币和盐补贴款等明确项。
- 本批只改 `output/final_reader/连云港市志_下册.html`，共 {changed} 处；报告：`output/reports/lower_reader_money_project_batch120_20260706.md`。
- 边界：未充分核定的其它数字异常及 `准海/准阴/并人/输人` 不做全局替换；未展示、未嵌入图片。
""")
    print(json.dumps({"changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
