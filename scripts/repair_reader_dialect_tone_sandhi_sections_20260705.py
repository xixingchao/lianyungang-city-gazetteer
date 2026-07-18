# -*- coding: utf-8 -*-
"""Restore missing dialect tone-sandhi and sound-rime sections."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_dialect_tone_sandhi_sections_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_dialect_tone_sandhi_sections_20260705.md"

START = '<h4 id="第五十九卷-第二章语音系统-第二节连续变调">第二节连续变调</h4>'
MID = '<h4 id="第五十九卷-第二章语音系统-第三节声韵配合关系">第三节声韵配合关系</h4>'
END = '<h3 id="第五十九卷-第三章同音字汇">第三章同音字汇</h3>'

TONE_ROWS = [
    ("11", "[313/21 313]", "知音 ig；阴天 i tiē；花生 xua sa；丁香 tin sian"),
    ("12", "[313/21 35]", "知名 min；猪皮 tu pi；汪塘 uag taq；推头 t‘ei tə"),
    ("15", "[313/2113]", "知足 tsuə；生铁 sap t‘iə；钢笔 ka pi；锅屋 ko uə"),
    ("41", "[51/21 313]", "自卑 pei；汽车 ti ei；认生 zə sə；是非 fei"),
    ("42", "[55/21 35]", "自由 iə；泡茶 p α；算盘 sō pō；树皮 u pi"),
    ("45", "[55/21 13]", "自杀 s；罪恶 tsei ə；大雪 ta cyə；树叶 su iə"),
    ("43", "[55/313 41]", "自满 mō；上火 sa xo；豆饼 təu pi；报纸 po"),
    ("44", "[55/313 55]", "自爱 ε；犯罪 f ei；菜地 ε ti；地蛋 ti t"),
    ("51", "[13/21 313]", "职工 ə kog；竹杆 tuə k；读书 tuə su；蜜蜂 mi fən"),
    ("52", "[13/21 35]", "职权 tyǒ；出头 uə t；学堂 yə ta；屋梁 uə lia"),
    ("55", "[13/21 13]", "职业 t iə；积木 teil mə；蜡烛 l tu；月食 yə"),
    ("53", "[13/21 41]", "职守 u；滴水 tir suei；石板 p；节省 tçiə sa"),
    ("54", "[13/55 55]", "职位 ə uei；出汗 uə x ē；国庆 kuə t i；立夏 liī cia"),
    ("21", "[35/55 313]", "辞书 1 şu；塘灰 tan xuei；茴香 xuei eian；镰刀 liē t"),
    ("22", "[35/55 35]", "辞行 t1 sin；围棋 uei ti；喉咙 xə loq；煤油 mei iəu"),
    ("25", "[35/55 13]", "辞职 1；劳力 l li；墙壁 tia pi；陪客 pei kə"),
    ("23", "[35/55 41]", "辞典 t1 t‘ie；年底 liě ti；沿海 iě xe；床板 ua p"),
    ("24", "[35/55 55]", "辞令 ι lin；城市 a l；麻袋 ma tε；停电 ti tie"),
    ("31", "[41/55 313]", "子孙 sa；火车 xo ei；剪刀 tciē to；顶针 tin təan"),
    ("32", "[41/55 35]", "子时；酒瓶 tçiəu pin；小娘 ci liag；买油 mε iəu"),
    ("35", "[41/55 13]", "子目 tl muə；打发 ta fe；解渴 tçie kp；火药 xo yə"),
    ("33", "[41/55 41]", "子女 ly；井水 tein şuei；老酒 lo tçiəu；土产 tu ‘"),
    ("34", "[41/55 55]", "子弟 tl ti；冷静 lag tcin；马路 ma lu；老树 l su"),
]

RIME_ROWS = [
    ("Pp m", "包盘梦", "标皮面", "布普目", ""),
    ("f", "翻", "", "富", ""),
    ("t t", "多同", "低田", "度脱", ""),
    ("1", "男", "娘", "路", "女"),
    ("ts ts", "在愁婶软", "", "祖锤霜如", ""),
    ("tc tc c", "", "鸡桥信", "", "举渠选"),
    ("k k x", "哥口汉", "", "姑葵荒", ""),
    ("0", "文", "羊", "伟", "玉"),
]


def table(headers: list[str], rows: list[tuple[str, ...]], caption: str) -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<table class="dialect-phonology-table"><caption>{caption}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def build_tone_section() -> str:
    return "\n".join([
        START,
        '<p>这里描写的连读变调，不包括含轻声字的两字组、三字组。为了行文方便，下文用代码表示调类，1、2、3、4、5分别表示阴平、阳平、上声、去声、入声。两字组的连读变调规律见表59-1。</p>',
        '<p>表左标明前字调类，表端标明后字调类。表中同一横行组合的前字调类相同，同一竖行组合的后字调类相同。变调相同的，不再用线条分开。两字组连调共有25种组合，前字变调，后字一律不变调，但阴平加上声和阴平加去声的组合前字不变调。举例排在表下。</p>',
        table(["组合", "变调", "例词"], TONE_ROWS, "表59-1 新浦话两字组连读变调表"),
    ])


def build_rime_section() -> str:
    return "\n".join([
        MID,
        '<p>新浦话声母、韵母的配合关系见表59-2。表里把韵母分成开齐合摄四类，声母分成八类。空格表示声韵不相拼合。</p>',
        table(["声母类", "开口呼", "齐齿呼", "合口呼", "撮口呼"], RIME_ROWS, "表59-2 新浦话声韵配合关系表"),
    ])


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    start = html.index(START)
    end = html.index(END, start)
    old = html[start:end]
    new = build_tone_section() + "\n\n" + build_rime_section() + "\n\n"
    changed = old != new
    if changed:
        html = html[:start] + new + html[end:]
        HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "changed": changed,
        "scope": "第五十九卷方言 第二章语音系统 第二节连续变调、第三节声韵配合关系",
        "source": [
            "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:13784-13873",
            "workbench/ocr/paddle_ocr/下/part02/page_0301.txt",
            "workbench/ocr/paddle_ocr/下/part02/page_0302.txt",
        ],
        "tone_rows": len(TONE_ROWS),
        "rime_rows": len(RIME_ROWS),
        "principle": "恢复漏掉的源文和表格版式；保留现有标题锚点，不改同音字汇。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text("\n".join([
        "# 第五十九卷方言连续变调与声韵配合关系补修",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复对象",
        "",
        "主阅读版 `第五十九卷方言 / 第二章语音系统` 中 `第二节连续变调`、`第三节声韵配合关系` 只有标题、正文和表格缺失。",
        "",
        "## 处理方式",
        "",
        "- 依据正文汇总和页级 OCR 补回两节说明文字。",
        "- 将表59-1、表59-2 恢复为 `dialect-phonology-table`。",
        "- 沿用现有标题锚点，不改动后续 `第三章同音字汇`。",
        "",
        "## 结果",
        "",
        f"- 文件发生改写：{changed}",
        f"- 表59-1 行数：{len(TONE_ROWS)}",
        f"- 表59-2 行数：{len(RIME_ROWS)}",
        "",
        "## 源证据",
        "",
        "- `workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:13784-13873`",
        "- `workbench/ocr/paddle_ocr/下/part02/page_0301.txt`",
        "- `workbench/ocr/paddle_ocr/下/part02/page_0302.txt`",
        "",
    ]) + "\n", encoding="utf-8")
    print(f"changed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
