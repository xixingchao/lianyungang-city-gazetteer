# -*- coding: utf-8 -*-
"""Repair obvious middle-reader money unit residues, batch 129."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "output" / "final_reader" / "连云港市志_中册.html"]
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_money_batch129_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_money_batch129_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册金额单位残字回源补修第一百二十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "直流伺服电机拨款 HTML 标签残留", "old": r"拨款6(<[^>]+>)*方(<[^>]+>)*元", "new": r"拨款6\1万\2元", "regex": True},
    {"label": "畜牧事业费 HTML 标签残留", "old": r"畜牧事业费613(<[^>]+>)*方(<[^>]+>)*元", "new": r"畜牧事业费613\1万\2元", "regex": True},
    {"label": "润滑油厂产值 HTML 标签残留", "old": r"产值1030(<[^>]+>)*方(<[^>]+>)*元", "new": r"产值1030\1万\2元", "regex": True},
    {"label": "首饰玩具销售收入", "old": "销售收入608.72方元", "new": "销售收入608.72万元"},
    {"label": "植物纤维墙纸专项贷款", "old": "专项贷款20方元", "new": "专项贷款20万元"},
    {"label": "猪肉屠宰冷库投资", "old": "投资40多方元", "new": "投资40多万元"},
    {"label": "果酒厂产值", "old": "产值2669方元", "new": "产值2669万元"},
    {"label": "食品厂固定资产", "old": "固定资产原值129方元", "new": "固定资产原值129万元"},
    {"label": "康乐食品厂投资", "old": "投资30方元", "new": "投资30万元"},
    {"label": "电话机利润", "old": "利润80.6方元", "new": "利润80.6万元"},
    {"label": "直流伺服电机试制经费", "old": "经费1方元", "new": "经费1万元"},
    {"label": "直流伺服电机省局拨款", "old": "拨款6方元", "new": "拨款6万元"},
    {"label": "铁氧体方块磁体改造投资", "old": "投资53方元", "new": "投资53万元"},
    {"label": "煤式推板窑投资", "old": "投资22方元", "new": "投资22万元"},
    {"label": "四机部工艺处拨款", "old": "拨款54方元", "new": "拨款54万元"},
    {"label": "灌云县水泥厂扩建投资", "old": "投资425方元", "new": "投资425万元"},
    {"label": "水泥制品厂工业总产值", "old": "工业总产值300方元", "new": "工业总产值300万元"},
    {"label": "耐火材料厂投资", "old": "投资42方元", "new": "投资42万元"},
    {"label": "塑料门窗工业总产值", "old": "工业总产值150方元", "new": "工业总产值150万元"},
    {"label": "塑料门窗利税", "old": "实现利税20方元", "new": "实现利税20万元"},
    {"label": "设计节省投资", "old": "节省投资20方元", "new": "节省投资20万元"},
    {"label": "北固新村总投资", "old": "总投资9000方元", "new": "总投资9000万元"},
    {"label": "新东电灯公司筹股", "old": "筹股7.4方元", "new": "筹股7.4万元"},
    {"label": "输变电工程总投资", "old": "总投资2166.12方元", "new": "总投资2166.12万元"},
    {"label": "乡镇企业以工补农", "old": "151方元用于以工补农", "new": "151万元用于以工补农"},
    {"label": "乡镇企业教育事业", "old": "95方元用于教育事业", "new": "95万元用于教育事业"},
    {"label": "乡镇企业集体福利", "old": "63方元用于农村集体福利事业", "new": "63万元用于农村集体福利事业"},
    {"label": "乡镇企业其它事业投入", "old": "投人366方元", "new": "投人366万元"},
    {"label": "首饰玩具销售收入 HTML 拆段", "old": "销售收入608.72方</p><p>元", "new": "销售收入608.72万</p><p>元"},
    {"label": "植物纤维墙纸专项贷款 HTML 拆段", "old": "专项贷款20方</p><p>元", "new": "专项贷款20万</p><p>元"},
    {"label": "猪肉屠宰冷库投资 HTML 拆段", "old": "投资40多方</p><p>元", "new": "投资40多万</p><p>元"},
    {"label": "果酒厂产值 HTML 拆段", "old": "产值2669方</p><p>元", "new": "产值2669万</p><p>元"},
    {"label": "食品厂固定资产 HTML 拆段", "old": "固定资产原值129方</p><p>元", "new": "固定资产原值129万</p><p>元"},
    {"label": "直流伺服电机省局拨款 HTML 拆段", "old": "拨款6方</p><p>元", "new": "拨款6万</p><p>元"},
    {"label": "塑料门窗工业总产值 HTML 拆段", "old": "工业总产值150方</p><p>元", "new": "工业总产值150万</p><p>元"},
    {"label": "乡镇企业集体福利 HTML 拆段", "old": "63方</p><p>元用于农村集体福利事业", "new": "63万</p><p>元用于农村集体福利事业"},
    {"label": "乡镇轻工年产值", "old": "年产值85266方元", "new": "年产值85266万元"},
    {"label": "乡镇企业投入资金", "old": "投入资金860方元", "new": "投入资金860万元"},
    {"label": "镇村企业固定资产", "old": "固定资产原值1095方元", "new": "固定资产原值1095万元"},
    {"label": "开发区基建总投资", "old": "基本建设总投资繁计23082方元", "new": "基本建设总投资累计23082万元"},
    {"label": "开发区电子公司产值", "old": "实现产值1867.8方元", "new": "实现产值1867.8万元"},
    {"label": "开发区电子公司税利", "old": "税利148方元", "new": "税利148万元"},
    {"label": "氨纶有限公司总投资", "old": "总投资9571方元", "new": "总投资9571万元"},
    {"label": "外供公司销售额", "old": "销售额2504方元", "new": "销售额2504万元"},
    {"label": "集邮业务收入", "old": "收入达48.5方元", "new": "收入达48.5万元"},
    {"label": "百货收购值", "old": "收购值由200万元增加到647方元", "new": "收购值由200万元增加到647万元"},
    {"label": "百货调给省外", "old": "调给省外321方元", "new": "调给省外321万元"},
    {"label": "百货调给市区供销社", "old": "调给市区供销社306方元", "new": "调给市区供销社306万元"},
    {"label": "百货调给邻县", "old": "调给邻县919方元", "new": "调给邻县919万元"},
    {"label": "蔬菜销售额", "old": "蔬菜销售额70多方元", "new": "蔬菜销售额70多万元"},
    {"label": "医用敷料收购值", "old": "收购值为1550.17方元", "new": "收购值为1550.17万元"},
    {"label": "进口粮接运开办费", "old": "商业部拨开办费60方元", "new": "商业部拨开办费60万元"},
    {"label": "物资借入资金", "old": "借入资金10029方元", "new": "借入资金10029万元"},
    {"label": "物资折旧资金", "old": "折旧资金1541方元", "new": "折旧资金1541万元"},
    {"label": "财政收入", "old": "财政收入39808方元", "new": "财政收入39808万元"},
    {"label": "财政支出", "old": "财政支出38583方元", "new": "财政支出38583万元"},
    {"label": "支出基数调整", "old": "调整为7898方元", "new": "调整为7898万元"},
    {"label": "契税牙税", "old": "牙税7.28方元", "new": "牙税7.28万元"},
    {"label": "财政支出 HTML 拆段", "old": "财政支出38583方</p><p>元", "new": "财政支出38583万</p><p>元"},
    {"label": "支出基数调整 HTML 拆段", "old": "调整为7898方</p><p>元", "new": "调整为7898万</p><p>元"},
    {"label": "工业部门预算", "old": "工业部门1885方元", "new": "工业部门1885万元"},
    {"label": "其它部门支出", "old": "其它部门支出2540方元", "new": "其它部门支出2540万元"},
    {"label": "全年支出", "old": "全年支出1506方元", "new": "全年支出1506万元"},
    {"label": "化工部门支出", "old": "化工1056方元", "new": "化工1056万元"},
    {"label": "科技三项费用1984支出", "old": "1984年支出274方元", "new": "1984年支出274万元"},
    {"label": "科技三项费用累计", "old": "费用支出3022方元", "new": "费用支出3022万元"},
    {"label": "流动资金工业部门", "old": "工业部门3061方元", "new": "工业部门3061万元"},
    {"label": "畜牧事业费", "old": "畜牧事业费613方元", "new": "畜牧事业费613万元"},
    {"label": "教育经费", "old": "教育经费46477方元", "new": "教育经费46477万元"},
    {"label": "专项支出", "old": "专项支出共9054方元", "new": "专项支出共9054万元"},
    {"label": "罚没款", "old": "罚没款150余方元", "new": "罚没款150余万元"},
    {"label": "技术改造免税", "old": "免税450方元", "new": "免税450万元"},
    {"label": "减免税款", "old": "减免税款4720方元", "new": "减免税款4720万元"},
    {"label": "税前还贷", "old": "税前还贷509方元", "new": "税前还贷509万元"},
    {"label": "出口退税", "old": "出口产品退税670.5方元", "new": "出口产品退税670.5万元"},
    {"label": "外贸企业出口退税", "old": "出口退税1347.9方元", "new": "出口退税1347.9万元"},
    {"label": "税收清查偷漏税", "old": "偷漏税241方元", "new": "偷漏税241万元"},
    {"label": "存款余额1976", "old": "存款余额为7579方元", "new": "存款余额为7579万元"},
    {"label": "润滑油厂产值", "old": "产值1030方元", "new": "产值1030万元"},
    {"label": "投资贷款", "old": "投资贷款200方元", "new": "投资贷款200万元"},
    {"label": "交通贷款", "old": "发放贷款176方元", "new": "发放贷款176万元"},
    {"label": "信用卡存款余额", "old": "存款余额为人民币35.45方元", "new": "存款余额为人民币35.45万元"},
    {"label": "贷款余额", "old": "贷款余额4862方元", "new": "贷款余额4862万元"},
    {"label": "现金投放量", "old": "现金投放量9523方元", "new": "现金投放量9523万元"},
    {"label": "节约建设资金", "old": "节约建设资金10841方元", "new": "节约建设资金10841万元"},
    {"label": "首饰玩具销售收入跨段尾", "old": "销售收入608.72方元", "new": "销售收入608.72万元"},
    {"label": "猪肉屠宰冷库投资跨段尾", "old": "投资40多方元", "new": "投资40多万元"},
    {"label": "直流伺服电机拨款跨段尾", "old": "拨款6方元", "new": "拨款6万元"},
    {"label": "塑料门窗产值跨段尾", "old": "工业总产值150方元", "new": "工业总产值150万元"},
    {"label": "农村集体福利跨段尾", "old": "63方元用于农村集体福利事业", "new": "63万元用于农村集体福利事业"},
    {"label": "集邮业务收入跨段尾", "old": "收入达48.5方元", "new": "收入达48.5万元"},
    {"label": "医用敷料收购值跨段尾", "old": "收购值为1550.17方元", "new": "收购值为1550.17万元"},
    {"label": "折旧资金跨段尾", "old": "折旧资金1541方元", "new": "折旧资金1541万元"},
    {"label": "财政支出跨段尾", "old": "财政支出38583方元", "new": "财政支出38583万元"},
    {"label": "工业部门预算跨段尾", "old": "工业部门1885方元", "new": "工业部门1885万元"},
    {"label": "畜牧事业费跨段尾", "old": "畜牧事业费613方元", "new": "畜牧事业费613万元"},
    {"label": "专项支出跨段尾", "old": "专项支出共9054方元", "new": "专项支出共9054万元"},
    {"label": "润滑油厂产值跨段尾", "old": "产值1030方元", "new": "产值1030万元"},
    {"label": "首饰玩具销售收入原始分行", "old": "入608.72方元", "new": "入608.72万元"},
    {"label": "猪肉屠宰冷库投资原始分行", "old": "资40多方元", "new": "资40多万元"},
    {"label": "塑料门窗产值原始分行", "old": "业总产值150方元", "new": "业总产值150万元"},
    {"label": "农村集体福利原始分行", "old": "63方元用</p><p>于农村集体福利事业", "new": "63万元用</p><p>于农村集体福利事业"},
    {"label": "集邮业务收入原始分行", "old": "48.5方</p><p>元", "new": "48.5万</p><p>元"},
    {"label": "医用敷料收购值原始分行", "old": "1550.17</p><p>方元", "new": "1550.17</p><p>万元"},
    {"label": "折旧资金原始分行", "old": "1541方元", "new": "1541万元"},
    {"label": "财政支出原始分行", "old": "支出38583方元", "new": "支出38583万元"},
    {"label": "工业部门预算原始分行", "old": "1885方</p><p>元", "new": "1885万</p><p>元"},
    {"label": "专项支出原始分行", "old": "项支出共9054方元", "new": "项支出共9054万元"},
    {"label": "直流伺服电机拨款最终残留", "old": "拨款6方元", "new": "拨款6万元"},
    {"label": "畜牧事业费最终残留", "old": "畜牧事业费613方元", "new": "畜牧事业费613万元"},
    {"label": "润滑油厂产值最终残留", "old": "产值1030方元", "new": "产值1030万元"},
    {"label": "直流伺服电机拨款段首数字", "old": "拨款</p><p>6方元", "new": "拨款</p><p>6万元"},
    {"label": "润滑油厂产值段首数字", "old": "产值</p><p>1030方元", "new": "产值</p><p>1030万元"},
]

LEFT_UNTOUCHED = [
    "本批只处理金额上下文中的 `方元`；`外方人员/私方人员/资方人员` 等合法词不处理。",
    "不处理仍未逐条核实的其他 `方元` 候选。",
    "本批没有打开、展示或嵌入图片。",
]
CUMULATIVE_FIXED = 72


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            if item.get("regex"):
                text, count = re.subn(item["old"], item["new"], text)
            else:
                count = text.count(item["old"])
                if count:
                    text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        applied.append({"target": str(target), "changed": sum(i["count"] for i in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = sum(t["changed"] for t in applied)
    payload = {
        "time": now,
        "scope": "middle reader obvious money unit residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "cumulative_fixed": CUMULATIVE_FIXED,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册金额单位残字补修第一百二十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 只处理金额上下文中的固定 `方元` 残字。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本批累计命中：{CUMULATIVE_FIXED} 处",
        f"- 本次复跑替换：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        if target["changed"]:
            lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百二十九批：中册金额单位残字"
    upsert_memory(marker, f"""
{marker}

- 补修当前中册阅读稿中金额上下文的 `方元` 固定短语，改为 `万元`；合法的 `外方人员/私方人员/资方人员` 不处理。
- 本批证据短语 {len(REPLACEMENTS)} 项，累计命中 {CUMULATIVE_FIXED} 处；报告：`output/reports/middle_reader_money_batch129_20260707.md`。
- 仍保留未逐条核实的其他 `方元` 候选；未打开、展示或嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "cumulative_fixed": CUMULATIVE_FIXED, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
