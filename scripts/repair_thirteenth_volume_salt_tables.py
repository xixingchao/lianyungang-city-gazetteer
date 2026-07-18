# -*- coding: utf-8 -*-
"""Repair table placeholders in 第十三卷 盐业."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第十三卷盐业_表格专项阶段一.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第十三卷-盐业">第十三卷盐业</h2>)(.*?)(?=<h2 id="第十四卷-轻-手-工业">)', re.S)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def make_table(caption: str, columns: list[str], rows: list[list[str]], note: str = "") -> str:
    ths = ''.join(f"<th>{html.escape(c)}</th>" for c in columns)
    trs = ['<tr>' + ''.join(f"<td>{html.escape(v)}</td>" for v in row) + '</tr>' for row in rows]
    table = f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    return table + (f"\n<p>{html.escape(note)}</p>" if note else "")


def table_13_2() -> str:
    rows = [
        ["初一、十六", "2:26", "14:26", "7:26", "19:26"],
        ["初二、十七", "3:19", "15:19", "8:19", "20:19"],
        ["初三、十八", "4:12", "16:12", "9:12", "21:12"],
        ["初四、十九", "5:00", "17:00", "10:00", "22:00"],
        ["初五、二十", "5:33", "17:33", "10:33", "22:33"],
        ["初六、二十一", "6:26", "18:26", "11:26", "23:26"],
        ["初七、二十二", "7:19", "19:19", "0:19", "12:19"],
        ["初八、二十三", "8:12", "20:12", "1:12", "13:12"],
        ["初九、二十四", "9:00", "21:00", "2:00", "14:00"],
        ["初十、二十五", "9:33", "21:33", "2:33", "14:33"],
        ["十一、二十六", "10:26", "22:26", "3:26", "15:26"],
        ["十二、二十七", "11:19", "23:19", "4:19", "16:19"],
        ["十三、二十八", "6:12", "12:12", "5:12", "17:12"],
        ["十四、二十九", "1:00", "13:00", "6:00", "18:00"],
        ["十五、三十", "1:33", "13:33", "6:33", "18:33"],
    ]
    return make_table(
        "表13-2 连云港市境内盐场沿海涨落潮时刻表",
        ["农历日期", "涨潮第一次", "涨潮第二次", "落潮第一次", "落潮第二次"],
        rows,
        "注：从开始涨潮到潮满用5个小时，从开始退潮到潮洼平用7个小时；苏北沿海潮汐每日涨落两次，为半日潮。",
    )


def table_13_3() -> str:
    rows = [
        ["前段", "1352.6/1043.6；1952.3/1080.8；1334.5/771.3；1855.9/1452.5；1487.9/1004.3；1663.6/1114.5；1813.2/1026.2；1311.1/1042.5；1482.2/875.0；1417.0/970.2；1778.6/1117.1；1744.5/1129.7；1794.1/1050.0；2148.3/639.1；1756.0/905.8；2063.1/779.6；1986.4/1122.0；2140.7/648.5"],
        ["续上表", "2000.6/879.9；1594.0/625.2；1967.1/1009.2；1834.3/742.9；2122.8/1473.3；1644.5/884.1；1977.2/1016.9；1610.2/810.6；1881.4/853.5；1429.8/861.9；1816.7/1044.1；1391.6/917.5；1711.4/1225.7；1881.8/789.9；1719.6/724.5；1599.0/971.7；1810.2/700.6；1818.3/579.1；2105.8/611.5；1633.4/869.1；1808.3/1243.6；1290.7/1271.0"],
    ]
    return make_table(
        "表13-3 1951～1990年连云港市境内徐圩盐场蒸发量、降水量统计表",
        ["分段", "源 OCR 可读序列（蒸发量/降水量，毫米）"],
        rows,
        "注：源 OCR 年份列缺失、跨页串行，本轮先保留可读数值序列替代表页占位，完整年份对应待对照原图补录。",
    )


def table_13_6() -> str:
    rows = [
        ["管式收盐机大型（台）", "79", "10；15；19；18", "分场列位待校正"],
        ["管式收盐机小型（台）", "32", "20", "分场列位待校正"],
        ["热合机（台）", "42", "20", "分场列位待校正"],
        ["浮卷收放机（台）", "122", "18", "分场列位待校正"],
        ["动力牵引收放机（台）", "19", "10；12", "分场列位待校正"],
        ["土绞关收放机（台）", "2415", "157；126；420；353；308；1020；31；23", "分场列位待校正"],
        ["压池机（台）", "266", "68；24；16；35；98；46", "分场列位待校正"],
        ["活格机具（台）", "12", "", "分场列位待校正"],
        ["破碴机（台）", "57", "21", "续表列位待校正"],
    ]
    return make_table(
        "表13-6 1990年连云港市境内盐场盐田主要设备情况表",
        ["设备", "合计", "源 OCR 可读分场序列", "备注"],
        rows,
        "注：源 OCR 表头跨页错位，保留设备名、合计及可读分场序列；青口、台北、台南、徐圩、灌西、研究所、县乡等列位待原图校正。",
    )


def table_13_14() -> str:
    rows = [
        ["1949-1963", "42.19；46.36；43.76；55.87；72.76；70.45；68.35；86.47；82.38；96.17；97.38；125.05；113.93；104.28；107.00", "食盐、工业盐等分项序列保留在原 OCR，待校正"],
        ["1964-1979", "54.59；68.64；86.76；65.63；68.57；73.88；128.43；118.31；127.13；72.31；99.70；118.38；127.40；146.77；162.63；148.88", "跨页列位待校正"],
        ["1980-1986", "162.34；166.08；164.30；182.62；183.33；193.53；209.78", "分项列位待校正"],
    ]
    return make_table(
        "表13-14 1949～1990年淮北盐区原盐销量统计表",
        ["年份段", "合计销量可读序列（万吨）", "备注"],
        rows,
        "注：表13-14为多页宽表，源 OCR 分项列顺序错位；本轮先结构化合计可读序列，完整食盐、工业盐、农用盐等分项待原图补录。",
    )


def table_13_17() -> str:
    rows = [
        ["1949-1966", "税收/利润序列：10883/90.60；10689/584.06；7603/64.60；7002/270.84；8990/680.12；11134/280.54；13352/499.89；11712/447.59；13362/990.67；11692/378.15；16934/844.00；15766/664.79；7635/575.88；8525/-720.44；10585/851.55；12660/1153.12；16302/1294.00", "年份列位待原图校正"],
        ["1967以后", "税收/利润序列：13460/795.94；12333/555.53；13592/718.29；11790/264.90；11720/436.43；14982/386.57；13196/516.10；16454/649.96；13357/-211.63；12246/1184.96；14891/894.42；14468/345.59；11448/1041.21；15070/1478.67；13640/585.59；10717/51.17；12229/751.92；11459/957.70；106.25/-575.70", "续表 OCR 行列错位"],
    ]
    return make_table(
        "表13-17 1949～1990年淮北盐场盐税收入利润统计表",
        ["分段", "源 OCR 可读序列（万元）", "备注"],
        rows,
        "注：源 OCR 为三组年份并列表，跨页后行列错位；本轮保留可读税收/利润序列，年份精确对应待原图校正。",
    )


def audit(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_13_2": section.count('表13-2 连云港市境内盐场沿海涨落潮时刻表'),
        "table_13_3": section.count('表13-3 1951～1990年连云港市境内徐圩盐场蒸发量、降水量统计表'),
        "table_13_6": section.count('表13-6 1990年连云港市境内盐场盐田主要设备情况表'),
        "table_13_14": section.count('表13-14 1949～1990年淮北盐区原盐销量统计表'),
        "table_13_17": section.count('表13-17 1949～1990年淮北盐场盐税收入利润统计表'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第十三卷 盐业 section")
    heading, section = match.groups()
    before = audit(section)
    actions: list[str] = []

    if '<caption>表13-2 连云港市境内盐场沿海涨落潮时刻表</caption>' not in section:
        pattern = re.compile(re.escape(PLACEHOLDER) + r'\n<p>连云港市境内盐场沿海涨落潮时刻表表13-2.*?</p>\n<p>2、苏北沿海潮汐每日涨落两次.*?</p>', re.S)
        section, count = pattern.subn(table_13_2(), section, count=1)
        if count:
            actions.append("结构化表13-2涨落潮时刻表。")

    if '<caption>表13-3 1951～1990年连云港市境内徐圩盐场蒸发量、降水量统计表</caption>' not in section:
        pattern = re.compile(r'<p>1951～1990年连云港市境内徐圩盐场蒸发量、降水量统计表表13-3.*?</p>\n' + re.escape(PLACEHOLDER) + r'\n(?:<table class="structured-table">.*?</table>\n)?<p>续上表年份蒸发量降水量年份蒸发量降水量.*?二、盐场', re.S)
        section, count = pattern.subn(table_13_3() + '\n<p>二、盐场', section, count=1)
        if count:
            actions.append("结构化表13-3为核对型表格，清理跨页占位和误插小表。")

    broken = '<p>包括大高、二高、三高，每级二块为蒸发池；卤塘：储存卤水塘子，用砖砌成圆形，如在制卤期或晒盐期，降雨时，就可将卤水放卤塘子贮存；加卤格：又称包头格，即调节池；晒格：即结晶池；官沟：每两份滩合用水沟一道，用于走水、排淡；胖头河：每圩公用胖头河一条，圩</p>\n' + PLACEHOLDER + '\n<p>盐驳坨、盐船均在此起装；廪基：分大廪基、小廪基，'
    if broken in section:
        section = section.replace(broken, '<p>包括大高、二高、三高，每级二块为蒸发池；卤塘：储存卤水塘子，用砖砌成圆形，如在制卤期或晒盐期，降雨时，就可将卤水放卤塘子贮存；加卤格：又称包头格，即调节池；晒格：即结晶池；官沟：每两份滩合用水沟一道，用于走水、排淡；胖头河：每圩公用胖头河一条，圩盐驳坨、盐船均在此起装；廪基：分大廪基、小廪基，', 1)
        actions.append("清理八卦滩正文分页误占位。")

    if '<caption>表13-6 1990年连云港市境内盐场盐田主要设备情况表</caption>' not in section:
        pattern = re.compile(r'<p>1990年连云港市境内盐场盐田主要设备情况表表13-6.*?</p>\n' + re.escape(PLACEHOLDER), re.S)
        section, count = pattern.subn(table_13_6(), section, count=1)
        if count:
            actions.append("结构化表13-6盐田主要设备情况表为核对型表格。")

    if '<caption>表13-14 1949～1990年淮北盐区原盐销量统计表</caption>' not in section:
        pattern = re.compile(r'<p>1949～1990年淮北盐区原盐销量统计表表13-14单位：万吨.*?</p>\n' + re.escape(PLACEHOLDER), re.S)
        section, count = pattern.subn(table_13_14(), section, count=1)
        if count:
            actions.append("结构化表13-14原盐销量统计表为核对型表格。")

    if '<caption>表13-17 1949～1990年淮北盐场盐税收入利润统计表</caption>' not in section:
        pattern = re.compile(r'<p>清朝部分年份淮盐与全国盐税课岁入比较表表13 - 16.*?1949～1990年淮北盐场盐税收入利润统计表表13-17单位：万元.*?</p>\n' + re.escape(PLACEHOLDER) + r'\n(?:<table class="structured-table">.*?</table>\n)?<p>续上表年份税收利润.*?私</p>', re.S)
        section, count = pattern.subn(lambda m: m.group(0).split('1949～1990年淮北盐场盐税收入利润统计表')[0] + table_13_17(), section, count=1)
        if count:
            actions.append("结构化表13-17盐税收入利润表为核对型表格，清理误插行业表。")

    fixed = html_text[: match.start()] + heading + section + html_text[match.end():]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(SECTION_RE.search(fixed).group(2))  # type: ignore[union-attr]
    return actions, before, after


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = '\n'.join(f"- {a}" for a in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第十三卷盐业 表格专项阶段一

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第十三卷 盐业。
- 目标：优先处理表13-2、表13-3、表13-6、表13-14、表13-17及一处正文分页误占位。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第十三卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第十三卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表13-2出现次数 | {before['table_13_2']} | {after['table_13_2']} |
| 表13-3出现次数 | {before['table_13_3']} | {after['table_13_3']} |
| 表13-6出现次数 | {before['table_13_6']} | {after['table_13_6']} |
| 表13-14出现次数 | {before['table_13_14']} | {after['table_13_14']} |
| 表13-17出现次数 | {before['table_13_17']} | {after['table_13_17']} |

## 当场验收
- 表13-2按源 OCR 完整结构化。
- 表13-3、表13-6、表13-14、表13-17因宽表/跨页 OCR 列位错乱，均以核对型表格保留可读序列。
- 未臆造无法确认的年份或分场列位。

## 下一步计划
- 继续清理第十三卷剩余盐业占位，随后推进第十二卷水产和第十卷水利的 P1 收尾。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第十三卷盐业表格专项阶段一完成

已完成第十三卷盐业表格专项第一阶段：

- 新增脚本：`scripts/repair_thirteenth_volume_salt_tables.py`。
- 结构化表13-2、表13-3、表13-6、表13-14、表13-17，其中表13-3/13-6/13-14/13-17按核对型保留源 OCR 可读序列。
- 清理八卦滩正文中一处分页误占位。
- 第十三卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第十三卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第十三卷盐业_表格专项阶段一.md`。

下一步：继续处理第十三卷剩余占位，或转入第十二卷水产表格专项。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第十三卷盐业表格专项阶段一完成"
    if marker in memory:
        start = memory.find(marker)
        next_entry = memory.find("\n## ", start + len(marker))
        memory = memory[:start].rstrip() + "\n" + entry.rstrip() + ("\n" + memory[next_entry:].lstrip() if next_entry != -1 else "")
    else:
        memory = memory.rstrip() + "\n\n" + entry.lstrip()
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    actions, before, after = repair_html()
    if actions or not PROGRESS_PATH.exists():
        write_progress(actions, before, after)
    if actions:
        update_memory(before, after)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    if not actions:
        print("- no html changes; idempotent rerun")
    print(f"before={before}")
    print(f"after={after}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
