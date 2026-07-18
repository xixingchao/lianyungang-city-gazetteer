# -*- coding: utf-8 -*-
"""Restore Fifth十五卷传染病防治九至十一小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_infectious_flu_diphtheria_pertussis_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_infectious_flu_diphtheria_pertussis_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷传染病防治流感白喉百日咳回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0176.txt:9-38"
SCOPE_START = '<p><strong>九、流行性感冒</strong></p>'
SCOPE_END = '<p><strong>十二、麻疹</strong></p>'

NEW_HTML = """<p><strong>九、流行性感冒</strong></p>
<p>1954年春，市区流行流行性感冒，患者儿童为多，据当时盐河区卫生所统计，2月4日，即发生230人，全市死亡3人。1956年夏，新浦、海州流行流行性感冒，7月下半月，患者2628人，未见死亡。1957年春，全市发病2.1万人，未见死亡，发病率为10700/10万。</p>
<p>新海连市人民委员会于4月3日发出预防流行性感冒的通知，组织7个防治组分赴各地各单位指导防治技术，委托缝纫社赶制口罩2万只分发各单位。1974年3月，发病5464人，经血清学检验确定为亚甲型。1977年8月、1979年冬至1980年春、1980年冬至1981年春，市内皆有小范围流行，发病人数较少。</p>
<p><strong>十、白喉</strong></p>
<p>民国28年至29年（1939～1940年），市境内白喉发病人数较多，有死亡，未见统计数字。</p>
<p>自1951年开始，每年冬春进行白喉类毒素接种，接种对象为8个月以上至8岁以下儿童。1953年开始进行锡克氏试验，监测人群对白喉的免疫力。1957年分3次对新浦、海州接种白喉类毒素。第一次接种9468人，第二次接种7440人，第三次接种6754人，平均全程接种者7887人。1959年，接种2.09万人。1960～1965年接种7.65万人。1953～1966年，全市发生白喉病人973人，死45人。1967年全市发病11例，无死亡，发病率5/10万。1971年发病160例。1972～1979年，每年接种白喉类毒素5000人。1972～1980年，全市发病19例，无死亡。1982～1990年，每年接种白喉类毒素3.13～16万人。</p>
<p><strong>十一、百日咳</strong></p>
<p>自1949年有疫情记载以来，每年均有不同程度的散发和流行。1954年进行百日咳菌苗预防接种，对象一般为3个月到6岁儿童。1962年，采用百白二联菌苗（即百日咳、白喉）进行预防接种。1963年后改为百白破三联菌苗（即百日咳、白喉、破伤风）接种。1954～1990年全市共发病4565例。其中，1954～1966年，全市发病2427例；1967～1969年无统计资料；1970～1982年，全市发病1259例；1983～1990年，全市发病855例。发病率超过100/10万的年份有1957年、1958年、1959年、1963年、1965年、1972年等，其中1959年最高，发病率为204.4/10万，发病总数为462例，历年病例均无死亡。</p>
<p>1990年3～7月，东海县驼峰乡上林村发生暴发流行，共发病95人，年龄最小者3个月，最大者13岁，家庭续发率46.1%。市卫生防疫站会同东海县卫生防疫站赶赴现场，对全村和周围村庄12岁以下儿童进行应急接种，对12岁以下的密切接触者口服红霉素预防，很快控制了疫情。</p>
"""

EXPECTED_TEXT = [
    "7月下半月，患者2628人",
    "发病率为10700/10万",
    "民国28年至29年（1939～1940年）",
    "1960～1965年接种7.65万人",
    "1982～1990年，每年接种白喉类毒素3.13～16万人",
    "1954～1990年全市共发病4565例",
]
RESIDUALS = [
    "7月下平月",
    "10700/10方",
    "1939~1940年",
    "1960~1965年",
    "1982~1990年",
    "1954~1990年全市共发病4565例",
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
    return changed, {"rewrote_scope": changed, "items_restored": 3, "paragraphs_restored": 6}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治 / 流行性感冒至百日咳",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建传染病防治九至十一小项，停止在十二、麻疹前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷传染病防治流感白喉百日咳回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：修正 `7月下平月`、`10700/10方`，并统一本组年份连接号。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷传染病防治流感白喉百日咳回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治` 中 `九、流行性感冒` 至 `十二、麻疹` 前。
- 修复内容：修正 `7月下平月`、`10700/10方`、年份连接号等残留。
- 报告：`output/reports/reader_readability_health_infectious_flu_diphtheria_pertussis_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷传染病防治流感白喉百日咳回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第一节传染病防治` 的 `九、流行性感冒`、`十、白喉`、`十一、百日咳` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `十二、麻疹` 前。
- 修正 `7月下平月`、`10700/10方` 和本组年份连接号残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_infectious_flu_diphtheria_pertussis_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷传染病防治流感白喉百日咳回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
