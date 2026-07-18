# -*- coding: utf-8 -*-
"""Restore broadcast award and program schedule tables from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_broadcast_awards_schedules_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_broadcast_awards_schedules_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷广播获奖表和节目时间表回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0151.txt:19-115; page_0152.txt; page_0153.txt; page_0154.txt; page_0155.txt:3-30"
OLD_SCOPE_START = '<p>频率1350千赫波长222.2米1987年9月13日起执行第一次播音：</p>'
NEW_SCOPE_START = '<table class="structured-table"><caption>表54-4 1983～1989年连云港市广播系统获省厅政府级奖主要作品一览表</caption>'
SCOPE_END = '<h3 id="第五十四卷-第四章电视">第四章电视</h3>'

AWARD_ROWS = [
    ["1983", "市台", "新闻", "农家装上了电话机", "1"],
    ["1983", "市台", "农村节目", "冰雹无情人有情", "1"],
    ["1983", "灌云县站", "短评", "扶贫先扶志", "1"],
    ["1984", "市台", "录音通讯", "海港的春天", "1"],
    ["1984", "灌云县站", "新闻", "农民王洪明建立家庭农业科技档案", "1"],
    ["1985", "市台", "新闻", "市塑料五厂不出国考察，照样选准引进设备", "1"],
    ["1985", "东海县站", "通讯", "东海农村的两件新事", "1"],
    ["1986", "市台", "新闻", "市外贸包装公司为港口腹地提供服务", "1"],
    ["1986", "灌云县站", "听众信箱", "姑娘，不要把自己当成商品", "1"],
    ["1986", "东海县站", "故事", "犟老汉两请“辣椒王”", "1"],
    ["1986", "东海县站", "新闻", "百名青年农民申请入党", "1"],
    ["1987", "市台", "新闻", "陇海饭店开展信息服务", "1"],
    ["1987", "市台", "农村节目", "根除封建陋习，反对转婚换婚", "1"],
    ["1987", "赣榆县站", "新闻", "宋庄乡千名渔家女受聘省内外传授对虾加工技术", "1"],
    ["1988", "市台", "新闻", "市化肥厂帮助农民降低农用成本", "2"],
    ["1988", "市台", "戏曲专题", "潇洒流畅，落落大方", "2"],
    ["1989", "市台", "评论", "管不好全社会要管好本单位", "2"],
    ["1989", "市台", "录音通讯", "访故事大王陈实", "2"],
]

SCHEDULE_54_1 = [
    ("section", "第一次播音"),
    ("5:25", "开始曲、预告节目"),
    ("5:30", "音乐（有线广播5:40开始曲、预告节目）"),
    ("5:45", "港城风貌（二、四、六），农村节目（三、五），音乐（日），戏曲（一）"),
    ("6:00", "新闻"),
    ("6:15", "每周一歌"),
    ("6:25", "港城快讯（一音乐）"),
    ("6:30", "转播中央人民广播电台《新闻和报纸摘要》"),
    ("7:00", "新闻"),
    ("7:15", "天气预报"),
    ("7:20", "广告"),
    ("7:25", "各地之声"),
    ("7:35", "青少年之友（三、日），文化与生活（二、四、六），法制园地（五），音乐（一）"),
    ("7:45", "音乐（二、四、六），戏曲（一、三、五），听众点播（日到8:25）"),
    ("8:15", "第一次播音结束（日除外）"),
    ("8:25", "艺林漫步（日）"),
    ("8:35", "曲艺（日）"),
    ("9:05", "影视欣赏或重播周末家庭晚会（日）"),
    ("10:05", "戏曲之友（日）"),
    ("10:35", "音乐（日）"),
    ("section", "第二次播音"),
    ("10:40", "开始曲、预告节目（日除外）（有线、无线同步）"),
    ("10:45", "音乐（一、三、五），戏曲（二、四、六）"),
    ("11:00", "文学（一、五），音乐（二、四），曲艺（三、六），戏曲（日）"),
    ("11:30", "各地之声"),
    ("11:40", "天气预报"),
    ("11:45", "广告"),
    ("11:50", "青少年之友（三、日），文化与生活（二、四、六），法制园地（五），艺林漫步（一）"),
    ("12:00", "新闻"),
    ("12:15", "港城风貌（二、四、六），农村节目（三、五），音乐（一、日）"),
    ("12:30", "长篇连续广播"),
    ("13:00", "英语广播讲座（一、三、五），日语广播讲座（二、四、六），文学（日）（有线广播：第二次播音结束，日第一次播音结束）"),
    ("13:30", "第二次播音结束（日第一次播音结束）"),
    ("section", "第三次播音"),
    ("16:55", "开始曲、预告节目"),
    ("17:00", "音乐（一、三），听众点播（五到17:40），戏曲（二、四、六），周末家庭晚会（日到18:00），有线广播17:25开始曲、预告节目"),
    ("17:30", "港城风貌（一、三、五），农村节目（二、四），音乐（六、日）"),
    ("17:45", "戏曲（二、四、六、日），音乐（一、三、五）"),
    ("17:30", "曲艺（一、三），文学（四、六），戏曲之友（二）"),
    ("17:40", "音乐（五）"),
    ("18:00", "天气预报"),
    ("18:10", "广告"),
    ("18:15", "新闻（有线广播转播江苏人民广播电台新闻）"),
    ("18:30", "转播中央人民广播电台《各地人民广播电台联播节目》"),
    ("19:00", "港城风貌（一、三、五），农村节目（二、四）音乐（六、日到19:25）（有线广播：新闻）"),
    ("19:15", "音乐（一至五）（六、日有线音乐）"),
    ("19:25", "每周一歌"),
    ("19:35", "青少年之友（二、六），文化与生活（一、三、五），法制园地（四），艺林漫步（日）"),
    ("19:45", "各地之声"),
    ("19:55", "港城短讯（日音乐）"),
    ("20:00", "长篇连续广播"),
    ("20:30", "转播中央人民广播电台《今晚八点半》（日），音乐（一），戏曲（二），听众点播（三到21:10），广播剧院（四），曲艺晚会（五），周末家庭晚会（六、日有线）"),
    ("21:10", "音乐（三）"),
    ("21:25", "音乐（日）"),
    ("21:30", "戏曲（一、三、日），戏曲之友（五），音乐（二、四、六）"),
    ("22:00", "新闻"),
    ("22:15", "日语广播讲座（一、三、五），英语广播讲座（二、四、六），戏曲（日）（有线广播：天气预报、全天播音结束）"),
    ("22:45", "天气预报、全天播音结束"),
]

SCHEDULE_54_2 = [
    ("section", "第一次播音"),
    ("5:25", "开始曲、预告节目（无线、有线广播同步）"),
    ("5:30", "音乐"),
    ("5:45", "港城风貌（二、四、六），农村节目（三、五），音乐（日），戏曲（一）"),
    ("6:00", "新闻"),
    ("6:15", "每周一歌"),
    ("6:20", "港城短讯（一音乐）"),
    ("6:25", "广告"),
    ("6:30", "转播中央人民广播电台《新闻报纸摘要》"),
    ("7:00", "新闻（一至六），星期半小时（日到7:30）"),
    ("7:15", "天气预报与广告（一至六）"),
    ("7:25", "各地之声（一至六）"),
    ("7:30", "天气预报（日）"),
    ("7:35", "企业之声"),
    ("7:40", "青少年之友（三、日），文化与生活（二、四、六），法制园地（五），音乐（一）"),
    ("7:50", "音乐（二、四、六），戏曲（一、三、五），听众点播（日到8:30）"),
    ("8:20", "第一次播音结束（日除外）"),
    ("8:30", "艺林漫步（日）"),
    ("8:40", "音乐（日）"),
    ("9:00", "文艺乐园（日）"),
    ("9:30", "戏曲（日）"),
    ("section", "第二次播音"),
    ("9:55", "开始曲、预告节目（日除外）（有线、无线同步）"),
    ("10:00", "新闻"),
    ("10:15", "戏曲（一、三、五），音乐（二、四、六），文学（日）"),
    ("10:45", "音乐（一、三、五），戏曲（二、四、六、日）"),
    ("11:00", "文学（一、五），音乐（二、四），曲艺（三、六、日）"),
    ("11:30", "各地之声"),
    ("11:40", "天气预报"),
    ("11:45", "广告"),
    ("11:50", "青少年之友（三、日），文化与生活（二、四、六），法制园地（五），艺林漫步（一）"),
    ("12:00", "新闻（一至六），星期半小时（日到12:30）"),
    ("12:15", "港城风貌（二、四、六），农村节目（三、五），音乐（一）"),
    ("12:30", "企业之声"),
    ("12:35", "长篇连续广播"),
    ("13:05", "英语广播讲座（一、三、五），日语广播讲座（二、四、六），文学（日）（有线广播：第二次播音结束，日第一次播音结束）"),
    ("13:35", "第二次播音结束（日第一次播音结束）"),
    ("section", "第三次播音"),
    ("16:55", "开始曲、预告节目"),
    ("17:00", "音乐（一、三），听众点播（五到17:40），戏曲（二、四），文艺乐园（六）影视欣赏（日到18:00），（有线广播：17:25开始曲、预告节目）"),
    ("17:30", "港城风貌（一、三、五），农村节目（二、四），音乐（六、日）"),
    ("17:45", "戏曲（二、四、六、日），音乐（一、三、五）"),
    ("17:30", "文学（一、三、六），曲艺（二、四）"),
    ("17:40", "音乐（五）"),
    ("18:00", "每周一歌"),
    ("18:05", "广告"),
    ("18:10", "音乐"),
    ("18:15", "新闻（有线广播转播江苏人民广播电台新闻）"),
    ("18:30", "转播中央人民广播电台《各地人民广播电台联播节目》"),
    ("19:00", "港城风貌（一、三、五），农村节目（二、四）音乐（六、日）（有线广播：新闻）"),
    ("19:15", "天气预报"),
    ("19:20", "青少年之友（二、六），文化与生活（一、三、五），法制园地（四），艺林漫步（日）"),
    ("19:30", "港城短讯（一至六），音乐（日）"),
    ("19:35", "各地之声"),
    ("19:45", "音乐"),
    ("20:00", "长篇连续广播"),
    ("20:30", "音乐（一），文艺乐园（二），听众点播（三到21:10），广播剧院（四），曲艺晚会（五），戏曲（六），文学（日）"),
    ("21:00", "文学（二）"),
    ("21:10", "音乐（三）"),
    ("21:30", "戏曲（一、三、五、日），音乐（二、四、六）"),
    ("22:00", "新闻（有线广播：天气预报、全天播音结束）"),
    ("22:15", "天气预报"),
    ("22:20", "日语广播讲座（一、三、五），英语广播讲座（二、四、六），戏曲（日）"),
    ("22:50", "音乐"),
    ("23:00", "全天播音结束"),
]

EXPECTED_TEXT = [
    "表54-4 1983～1989年连云港市广播系统获省厅政府级奖主要作品一览表",
    "农家装上了电话机",
    "犟老汉两请“辣椒王”",
    "附54-1 连云港人民广播电台节目时间表（有线）",
    "1987年9月13日起执行；频率1350千赫；波长222.2米。",
    "转播中央人民广播电台《新闻和报纸摘要》",
    "附54-2 连云港人民广播电台节目时间表（有线、无线同步）",
    "1990年9月16日起实行；频率1350千赫；波长222.2米。",
    "转播中央人民广播电台《新闻报纸摘要》",
    "调频立体声广播节目94.4兆赫12:00～13:30（一～日）",
]
RESIDUALS = [
    "频率1350千赫波长222.2米1987年9月13日起执行第一次播音",
    "附54一2",
    "第三章广．·播．，2437",
    "新闲报纸摘要",
    "10:4010:45",
    "17:3017:45",
    "20:0020 :30",
    "全天播音结束调频立体声广播节目",
    "(注·文中一、二、三日",
]


def e(value: str) -> str:
    return escape(value, quote=False)


def table_html(caption: str, headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{e(cell)}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<table class="structured-table"><caption>{e(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def schedule_html(caption: str, meta: str, rows: list[tuple[str, str]]) -> str:
    out = [f'<table class="structured-table"><caption>{e(caption)}</caption><thead><tr><th>时间</th><th>节目</th></tr></thead><tbody>']
    for time, program in rows:
        if time == "section":
            out.append(f'<tr><th colspan="2">{e(program)}</th></tr>')
        else:
            out.append(f'<tr><td>{e(time)}</td><td>{e(program)}</td></tr>')
    out.append("</tbody></table>")
    return f"<p>{e(meta)}</p>\n" + "".join(out)


def build_new_html() -> str:
    pieces = [
        table_html(
            "表54-4 1983～1989年连云港市广播系统获省厅政府级奖主要作品一览表",
            ["年份", "获奖单位", "类别", "作品题目", "等次"],
            AWARD_ROWS,
        ),
        schedule_html(
            "附54-1 连云港人民广播电台节目时间表（有线）",
            "1987年9月13日起执行；频率1350千赫；波长222.2米。",
            SCHEDULE_54_1,
        ),
        "<p>注：文中一、二、三……日，指星期一、二、三……日。</p>",
        schedule_html(
            "附54-2 连云港人民广播电台节目时间表（有线、无线同步）",
            "1990年9月16日起实行；频率1350千赫；波长222.2米。",
            SCHEDULE_54_2,
        ),
        "<p>调频立体声广播节目94.4兆赫12:00～13:30（一～日）</p>",
        "<p>注：文中一、二、三……日，系指星期一、二、三……日。</p>",
    ]
    return "\n".join(pieces) + "\n"


NEW_HTML = build_new_html()


def find_scope(text: str) -> tuple[int, int]:
    old = text.find(OLD_SCOPE_START)
    new = text.find(NEW_SCOPE_START)
    candidates = [pos for pos in (old, new) if pos != -1]
    if not candidates:
        raise RuntimeError("broadcast awards/schedules scope start not found")
    start = min(candidates)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    changed = int(text[start:end] != NEW_HTML)
    if changed:
        HTML.write_text(text[:start] + NEW_HTML + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return changed, {
        "rewrote_scope": changed,
        "award_rows_restored": len(AWARD_ROWS),
        "schedule_54_1_rows": sum(1 for time, _ in SCHEDULE_54_1 if time != "section"),
        "schedule_54_2_rows": sum(1 for time, _ in SCHEDULE_54_2 if time != "section"),
    }


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第三章广播 / 第三节广播节目设置 / 表54-4与附54-1、附54-2",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本恢复获奖作品表和节目时间表；未改动结构化表格交付站点。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十四卷广播获奖表和节目时间表回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            f"- 恢复表54-4获奖作品记录：{counts['award_rows_restored']}行",
            f"- 恢复附54-1节目时间记录：{counts['schedule_54_1_rows']}行",
            f"- 恢复附54-2节目时间记录：{counts['schedule_54_2_rows']}行",
            "- 说明：本轮只修复阅读版正文展示，未新增结构化表格站点交付条目。",
            "",
        ]),
        encoding="utf-8",
    )
    progress = f"""
# 第五十四卷广播获奖表和节目时间表回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第三章广播 / 第三节广播节目设置` 后的 `表54-4`、`附54-1`、`附54-2`，停止在 `第四章电视` 前。
- 修复内容：补回阅读版缺失的 `表54-4 1983～1989年连云港市广播系统获省厅政府级奖主要作品一览表` 18行；将原来黏连成段的 `附54-1`、`附54-2` 节目时间表按 OCR 时间行重排。
- 边界：未改动结构化表格交付站点，后续如需将表54-4纳入交付表，应另走 table_entries 流程。
- 报告：`output/reports/reader_readability_broadcast_awards_schedules_20260703.md`。
"""
    PROGRESS.write_text(progress.strip() + "\n", encoding="utf-8")
    memory = f"""
## 2026-07-03 第五十四卷广播获奖表和节目时间表回源修复

- 对第五十四卷报刊广播电视 `第三章广播 / 第三节广播节目设置` 后续表格化内容进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；恢复 `表54-4`、`附54-1`、`附54-2` 至 `第四章电视` 前。
- 修正阅读版缺失 `表54-4`、节目时间表大段黏连、页眉误入 `第三章广．·播．，2437`、`附54一2`、`新闲报纸摘要` 等问题；本轮未新增结构化表格站点条目。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_broadcast_awards_schedules_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十四卷广播获奖表和节目时间表回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
