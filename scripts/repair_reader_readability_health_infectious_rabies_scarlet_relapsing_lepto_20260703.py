# -*- coding: utf-8 -*-
"""Restore Fifth十五卷传染病防治十五至十八小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_infectious_rabies_scarlet_relapsing_lepto_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_infectious_rabies_scarlet_relapsing_lepto_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷传染病防治狂犬猩红回归钩体回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0178.txt:6-31"
SCOPE_START = '<p><strong>十五、狂犬病</strong></p>'
SCOPE_END = '<p><strong>十九、麻风</strong></p>'

NEW_HTML = """<p><strong>十五、狂犬病</strong></p>
<p>民国期间市内有狂犬病记载，无疫情统计。1979年后方有疫情资料，1979年有1例。1980年有1例。1981年开始使用狂犬疫苗预防，注射对象主要为被犬咬伤的人或犬。</p>
<p>1981年，鉴于市内出现多起疯犬咬伤人畜事件，市政府下发灭犬通知，当年全市灭犬1550条，捕杀率为62%。对允许饲养的家犬普遍注射狂犬疫苗，当年注射1350条。1985年，狂犬伤人事件频繁。当年6～7月，新浦有11名居民被疯犬咬伤，灌云县有一条疯犬连续咬伤4人，到花果山游览的两名日本游客也被咬伤，因此，市人民政府决定再次开展灭犬活动，并成立专门灭犬队。1988年发病14例，发病率0.5/10万。1981～1990年，卫生部门供应狂犬疫苗1.55万人份。1979～1990年，全市共发生99例，狂犬病人全部死亡。</p>
<p><strong>十六、猩红热</strong></p>
<p>从民国11年（1922年）起，猩红热每年春夏都有范围不等的流行。1973年，发病570例，发病率180.1/10万。1974年，发病294例，发病率90.7/10万。1978年，发病222例，发病率63.2/10万。1989年，发病189例，发病率37.2/10万。1973～1990年，全市累计散发2549例，无死亡。猩红热无特殊方法预防，一般采用隔离法，治疗上应用抗菌素效果较好。</p>
<p><strong>十七、回归热</strong></p>
<p>民国23年（1934年）始见回归热在市内流行的记载。1949～1952年，市内呈散在性发生，年发病率约为258/10万。1952年后未见有病例发生。预防方法主要是讲究个人卫生，消灭体虱，治疗一般用砷制剂“九一四”、“六零六”等。</p>
<p><strong>十八、钩端螺旋体病</strong></p>
<p>1970年以前连云港市未见有钩端螺旋体病记载。1971年1月，市卫生局会同市兽医站，在新浦区向阳大队调查。该大队共157户802人，当时有发热症状者138人，其中112人做了血清学检查，查出阳性3人。1972年，再次对向阳大队钩体病感染及流行情况调查，343人中有14人为阳性，阳性率4.1%。此后数年中，除1976年全市见有51例该病的报告外，其余年份均未见有发病。对发现的患者皆及时给以青霉素注射治疗，效果较佳。注意水源清洁和畜圈卫生是预防的重要措施。</p>
"""

EXPECTED_TEXT = [
    "1979～1990年，全市共发生99例",
    "1973～1990年，全市累计散发2549例",
    "发病570例，发病率180.1/10万",
    "1970年以前连云港市未见有钩端螺旋体病记载",
    "注意水源清洁和畜圈卫生是预防的重要措施",
]
RESIDUALS = [
    "1979~1990年",
    "1973~1990年",
    "发病570例,发病率",
    "1978年,发病222例",
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
    return changed, {"rewrote_scope": changed, "items_restored": 4, "paragraphs_restored": 5}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治 / 狂犬病至钩端螺旋体病",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建传染病防治十五至十八小项，停止在十九、麻风前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷传染病防治狂犬猩红回归钩体回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：统一 `1979～1990年`、`1973～1990年` 等连接号并清理局部标点残留。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷传染病防治狂犬猩红回归钩体回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治` 中 `十五、狂犬病` 至 `十九、麻风` 前。
- 修复内容：统一年份连接号，修正 `发病570例,发病率`、`1978年,发病222例` 等局部标点残留。
- 报告：`output/reports/reader_readability_health_infectious_rabies_scarlet_relapsing_lepto_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷传染病防治狂犬猩红回归钩体回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第一节传染病防治` 的 `十五、狂犬病`、`十六、猩红热`、`十七、回归热`、`十八、钩端螺旋体病` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `十九、麻风` 前。
- 统一年份连接号，并清理 `发病570例,发病率`、`1978年,发病222例` 等局部标点残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_infectious_rabies_scarlet_relapsing_lepto_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷传染病防治狂犬猩红回归钩体回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
