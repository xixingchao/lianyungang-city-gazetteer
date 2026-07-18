# -*- coding: utf-8 -*-
"""Restore Fifth十五卷传染病防治十二至十四小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_infectious_measles_polio_tb_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_infectious_measles_polio_tb_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷传染病防治麻疹脊灰结核回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0177.txt:4-38; page_0178.txt:3-5"
SCOPE_START = '<p><strong>十二、麻疹</strong></p>'
SCOPE_END = '<p><strong>十五、狂犬病</strong></p>'

NEW_HTML = """<p><strong>十二、麻疹</strong></p>
<p>麻疹在市境内流行由来已久，解放前每隔2～3年流行一次，并发肺炎者较多，死亡率较高。1953年，发病3718例，死6例，发病率1982.0/10万。1955年，发病3965例，死3例，发病率1966.4/10万。1957年，发病6392例，死5例，发病率2852.2/10万。1957年1～2月，连岛乡麻疹暴发流行，市人民政府卫生科派出3人抢救小组，除治疗发病者外，还采用紫草根煮汤口服预防。1959年，全市麻疹流行时，新浦、连云两地曾重点采用中药“雷击散”液滴鼻预防。1959年，发病5915例，死11例，发病率2617.1/10万。1962年，发病4164例，死3例，发病率1740.6/10万。1964年，发病5781例，死17例，发病率2052.2/10万。1965年，发病5788例，死7例，发病率1998.6/10万。1953～1967年，发病4.05万例，死亡84例。1970年以后，开始进行麻疹疫苗接种。1977年，云台区朝阳乡发生流行，发病年龄最小者1岁，最大者24岁，发病3635例，死亡22人，发病率1067.2/10万。1983年，开始将麻疹疫苗接种纳入计划免疫，规定儿童出生后10～12个月初种，2岁及6岁时各接种一次。1985年，全市麻疹疫苗接种覆盖率约达80%～90%，1990年达90%～95%。</p>
<p>1987～1990年，全市每年发病10例。</p>
<p><strong>十三、脊髓灰质炎</strong></p>
<p>建国前未见市内有此病记载。1955年和1960年，市内有散发性发生，无明确疫情统计，仅见有该病后遗症的儿童。1971年，发病29例，发病率18.5/10万。1973年，发病13例，发病率3.8/10万。1983年将脊髓灰质炎的预防纳入计划免疫，儿童出生后至2岁给脊髓灰质炎疫苗糖丸口服，进行基础免疫。待长到7岁时再口服一次进行加强免疫。</p>
<p>1983年，全市口服脊髓灰质炎疫苗糖丸共5万人次。1977～1988年无病例发生。1989年，出现暴发流行，病发23例，死1例，发病率为0.71/10万，分布于东海县19例。1989年8月，邳县发生脊髓灰质炎暴发后，市卫生局及卫生防疫站立即组成两个调查组到市内各地调查疫情及疫苗接种等情况，找出薄弱环节，采取补救措施，对东海县安峰、石湖、石埠、桃林、曲阳、洪庄、山左口和灌云县穆圩、南岗、龙苴等乡镇的4岁以下儿童全部加服糖丸疫苗一次，其他乡镇、街道均按免疫程序查漏补服。1990年，市人民政府召开会议并下发文件，部署防疫工作，各级政府均建立脊髓灰质炎防治领导小组。</p>
<p><strong>十四、结核病</strong></p>
<p>结核病，主要是肺结核病（“肺痨”）在市境内流行久远，历来认为是“不治之症”。民国19年（1930年）至民国37年有此病记载。建国后，历年有散在性发病，但无疫情统计。</p>
<p>1953年，市内进行结核菌素试验和卡介苗接种，当年接种卡介苗3419人。此后，每年均对15岁以下学龄儿童接种。1970年以后，采用乙胺丁醇、利福平等治疗，疗效较好。1974年，连云港市结核病防治院对结核病的发病情况进行社会调查，1979年普查结束。6年共检查12.49万人次，查出结核病人2733人，患病率为2.19%。1981年后接种卡介苗对象改为6个月内的婴儿、7周岁和12周岁的儿童。1983年后，卡介苗接种纳入计划免疫。</p>
<p>1985年抽样调查，结核病发病率为0.52%。1983～1990年，全市共接种卡介苗111.48万人次，进行结核菌素试验91.86万人次，其中阳性21.84万人次。1990年抽样调查，查得结核病发病率为0.24%。</p>
"""

EXPECTED_TEXT = [
    "发病率1067.2/10万",
    "开始将麻疹疫苗接种纳入计划免疫",
    "1987～1990年，全市每年发病10例",
    "1989年8月，邳县发生脊髓灰质炎暴发后",
    "肺结核病（“肺痨”）在市境内流行久远",
    "1983年后，卡介苗接种纳入计划免疫",
]
RESIDUALS = [
    "1067.2/10方",
    "纳人计划免疫",
    "1987~1990年",
    "1989年8月，县发生",
    "（\"肺痨”）",
    "·1983年后",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
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
    return changed, {"rewrote_scope": changed, "items_restored": 3, "paragraphs_restored": 7}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治 / 麻疹至结核病",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建传染病防治十二至十四小项，停止在十五、狂犬病前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷传染病防治麻疹脊灰结核回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：修正 `1067.2/10方`、`纳人计划免疫`、`邳县` 漏字、`肺痨` 引号和 `·1983年后` 残留。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷传染病防治麻疹脊灰结核回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治` 中 `十二、麻疹` 至 `十五、狂犬病` 前。
- 修复内容：修正 `1067.2/10方`、`纳人计划免疫`、`1989年8月，县发生`、`肺痨` 引号、`·1983年后` 等残留。
- 报告：`output/reports/reader_readability_health_infectious_measles_polio_tb_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷传染病防治麻疹脊灰结核回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第一节传染病防治` 的 `十二、麻疹`、`十三、脊髓灰质炎`、`十四、结核病` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `十五、狂犬病` 前。
- 修正 `1067.2/10方`、`纳人计划免疫`、`邳县` 漏字、`肺痨` 引号和 `·1983年后` 等 OCR 残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_infectious_measles_polio_tb_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷传染病防治麻疹脊灰结核回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
