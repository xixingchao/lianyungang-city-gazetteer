# -*- coding: utf-8 -*-
"""Restore source-backed boundaries where a title is followed by same lead word."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_same_title_lead_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_same_title_lead_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_同名正文首词条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/连云港市志_全书_正文汇总.md"

ITEMS = json.loads(r'''
[
  {"title":"一、海州湾渔场","lead":"海州湾渔场","source_line":45428},
  {"title":"三、赣榆县工艺美术公司","lead":"赣榆县工艺美术公司","source_line":121873},
  {"title":"一、连云港市绣品厂","lead":"连云港市绣品厂","source_line":122373},
  {"title":"二、连云港市地毯厂","lead":"连云港市地毯厂","source_line":122384},
  {"title":"一、连云港印铁制罐厂","lead":"连云港印铁制罐厂","source_line":123180},
  {"title":"三、检修","lead":"检修","source_line":139463},
  {"title":"一、新浦热电厂","lead":"新浦热电厂","source_line":140032},
  {"title":"一、海连线","lead":"海连线","source_line":140343},
  {"title":"二、刘灌线","lead":"刘灌线","source_line":140366},
  {"title":"六、平茅线","lead":"平茅线","source_line":140406},
  {"title":"一、平山变电所","lead":"平山变电所","source_line":140430},
  {"title":"三、刘顶变电所","lead":"刘顶变电所","source_line":140483},
  {"title":"一、锦屏磷矿","lead":"锦屏磷矿","source_line":141892},
  {"title":"二、新浦磷矿","lead":"新浦磷矿","source_line":141914},
  {"title":"一、蓝晶石矿","lead":"蓝晶石矿","source_line":142164},
  {"title":"二、砂岩","lead":"砂岩","source_line":142169},
  {"title":"三、蛭石","lead":"蛭石","source_line":142173},
  {"title":"四、玄武岩矿","lead":"玄武岩矿","source_line":142178},
  {"title":"四、集装箱运输","lead":"集装箱运输","source_line":146520},
  {"title":"四、监督管理","lead":"监督管理","source_line":150164},
  {"title":"二、蔷薇河","lead":"蔷薇河","source_line":60011},
  {"title":"三、东门五图河","lead":"东门五图河","source_line":60025},
  {"title":"四、古泊善后河","lead":"古泊善后河","source_line":60037},
  {"title":"十、藏军洞","lead":"藏军洞","source_line":63469},
  {"title":"二十、海天洞","lead":"海天洞","source_line":63547},
  {"title":"二十三、玉女峰","lead":"玉女峰","source_line":63572},
  {"title":"一、渔湾","lead":"渔湾","source_line":63616},
  {"title":"六、仙人屋","lead":"仙人屋","source_line":63771},
  {"title":"九、悟正庵","lead":"悟正庵","source_line":63790},
  {"title":"一、连云港码头","lead":"连云港码头","source_line":63801},
  {"title":"三、东西连岛","lead":"东西连岛","source_line":63819},
  {"title":"八、西墅村","lead":"西墅村","source_line":63853},
  {"title":"一、锦屏山","lead":"锦屏山","source_line":63885},
  {"title":"二、白虎山","lead":"白虎山","source_line":63893},
  {"title":"四、青龙涧","lead":"青龙涧","source_line":63915},
  {"title":"五、双龙井","lead":"双龙井","source_line":63923},
  {"title":"六、桃花涧","lead":"桃花涧","source_line":63930},
  {"title":"八、石棚山","lead":"石棚山","source_line":63947},
  {"title":"十、孔望山","lead":"孔望山","source_line":63965},
  {"title":"十四、孔望山摩崖造像","lead":"孔望山摩崖造像","source_line":64004},
  {"title":"一、东海温泉","lead":"东海温泉","source_line":64032},
  {"title":"二、羽山","lead":"羽山","source_line":64038},
  {"title":"四、徐福村","lead":"徐福村","source_line":64052},
  {"title":"五、夹谷山","lead":"夹谷山","source_line":64059},
  {"title":"二、典税","lead":"典税","source_line":79890},
  {"title":"二、固定工","lead":"固定工","source_line":163523},
  {"title":"一、计时工资","lead":"计时工资","source_line":164353},
  {"title":"三、奖励工资","lead":"奖励工资","source_line":164380},
  {"title":"四、津贴","lead":"津贴","source_line":164469},
  {"title":"二、京剧","lead":"京剧","source_line":93744},
  {"title":"三、童子戏","lead":"童子戏","source_line":93770},
  {"title":"四、吕剧","lead":"吕剧","source_line":93814},
  {"title":"五、柳琴戏","lead":"柳琴戏","source_line":93822},
  {"title":"六、淮北盐场淮海剧团","lead":"淮北盐场淮海剧团","source_line":94038},
  {"title":"七、赣榆县京剧团","lead":"赣榆县京剧团","source_line":94052},
  {"title":"八、东海县京剧团","lead":"东海县京剧团","source_line":94064},
  {"title":"九、灌云县淮海剧团","lead":"灌云县淮海剧团","source_line":94073},
  {"title":"十、东海县淮海剧团","lead":"东海县淮海剧团","source_line":94086},
  {"title":"十三、云台区文化馆","lead":"云台区文化馆","source_line":94441},
  {"title":"一、云台山封土石室","lead":"云台山封土石室","source_line":96441},
  {"title":"一、铁匠","lead":"铁匠","source_line":106292},
  {"title":"四、裁缝","lead":"裁缝","source_line":106307},
  {"title":"六、屠夫","lead":"屠夫","source_line":106323},
  {"title":"七、染坊","lead":"染坊","source_line":106328},
  {"title":"九、槽坊","lead":"槽坊","source_line":106336},
  {"title":"一、主食","lead":"主食","source_line":106409},
  {"title":"三、地方风味菜","lead":"地方风味菜","source_line":106421},
  {"title":"三、清明节","lead":"清明节","source_line":106588},
  {"title":"十三、植树节","lead":"植树节","source_line":106641},
  {"title":"四、玩旱船","lead":"玩旱船","source_line":106684}
]
''')

SKIPPED = ["三、其它收入", "一、淮海戏（文化卷）", "一、淮海戏（民俗卷）"]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for item in ITEMS:
        title = item["title"]
        lead = item["lead"]
        old = f"<p>{title}{lead}"
        new = f"<h5>{title}</h5>\n<p>{lead}"
        old_count = html.count(old)
        if old_count == 1:
            html = html.replace(old, new, 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and html.count(new) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {title!r} once, got {old_count}")
        changes.append({**item, "status": status, "changed": changed})

    HTML.write_text(html, encoding="utf-8")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed_total = sum(item["changed"] for item in changes)
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "source": SOURCE, "changes": changes, "skipped": SKIPPED}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 同名正文首词条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        f"- 处理：按 `{SOURCE}` 中独立标题行恢复 70 处 `标题+同名正文首词` 的段落边界；只拆标题，不改正文文字。",
        f"- 状态：本次变更 {changed_total} 处；目标清理 {len(changes)}/70 处。",
        "- 跳过：`三、其它收入` 源定位未唯一；两个 `一、淮海戏` 同名标题需按上下文单独处理。",
        "",
        "## 明细",
        "",
    ]
    for item in changes:
        lines.append(f"- {item['title']}：{item['status']}，源证据 `{SOURCE}:{item['source_line']}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 同名正文首词条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_same_title_lead_boundaries_20260705.py`，按 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 中独立标题行恢复 70 处 `标题+同名正文首词` 边界。
- 本批只拆标题为 `<h5>`，不改正文文字；跳过 `三、其它收入` 与两个 `一、淮海戏`，因源定位不唯一或需上下文单独判断。
- 报告：`output/reports/reader_same_title_lead_boundaries_20260705.md`。
""",
    )

    print("reader_same_title_lead_boundaries_repaired")
    print(f"changed={changed_total}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
