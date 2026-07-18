# -*- coding: utf-8 -*-
"""Restore Fifth十五卷寄生虫病防治疟疾小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_parasite_malaria_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_parasite_malaria_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷寄生虫病防治疟疾回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0179.txt:24-37; page_0180.txt:3-7"
SCOPE_START = '<p><strong>一、疟疾</strong></p>'
SCOPE_END = '<p><strong>二、黑热病</strong></p>'

NEW_HTML = """<p><strong>一、疟疾</strong></p>
<p>市内疟疾流行已久，民国23年（1934年）有记载以来，历年有发病。</p>
<p>1951年，市内发病154人。1952年发病1778人。1953～1958年，发病率在80.92/万～7.14/万之间波动。1959年后，发病率明显升高，当年全市发病1.2万例，发病率为489.4/万。50年代，着重于治疗现症病人。1960年以后，开始以环氯胍为主进行疟疾病抗复发治疗。1960年，发病7.15万人，发病率2709.6/万。1961年，发病5.14万人，发病率为2009.6/万。1961年，全市分片进行3次应用环氯胍抗复发治疗，共治疗13.43万人次，此后，又对进行过抗复发治疗的患者进行复查。1962～1965年，应用乙胺嘧啶和氯奎进行抗疟治疗。1966年，发病1.24万例，发病率为416.7/万。1971年，发病4.63万人，发病率1404.2/万。1971～1973年，根据国家卫生部防疫司制订的“两根治，一预防，大力灭蚊”的北方地区疟疾防治技术方案，全市共进行疟疾休止期根治68.93万人，复治2.43万人，治疗现症病人34.91万人及疑似病人8.44万人。同时在60个乡镇采用乙胺嘧啶进行半月一次的预防服药共107.81万人。1974年，连云港市纳入苏鲁皖豫鄂五省疟疾联防范围，各种防治措施统一安排。1975年发病5444例，发病率152.9/万。1978年发病5121例，发病率135.2/万。1983年全市发病171人，发病率4/万。1985年，赣榆县已达消灭疟疾病标准。1986年，东海县、灌云县及市区疟疾发病率均达1/万以下。1990年，全市116个乡、镇、场中，已有109个全年未发生疟疾，其余7个乡、镇、场的发病率均在1/万以下。</p>
"""

EXPECTED_TEXT = [
    "1953～1958年，发病率在80.92/万～7.14/万之间波动",
    "50年代，着重于治疗现症病人",
    "1971～1973年，根据国家卫生部防疫司制订的“两根治，一预防，大力灭蚊”",
    "1990年，全市116个乡、镇、场中，已有109个全年未发生疟疾",
]
RESIDUALS = [
    "1953~1958年",
    "80.92/万~7.14/万",
    "50年代,着重",
    "1971~1973年",
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
    return changed, {"rewrote_scope": changed, "items_restored": 1, "paragraphs_restored": 2}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治 / 疟疾",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建疟疾小项，停止在二、黑热病前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷寄生虫病防治疟疾回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：统一疟疾小项年份连接号，修正 `50年代,` 标点残留。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷寄生虫病防治疟疾回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治` 中 `一、疟疾` 至 `二、黑热病` 前。
- 修复内容：统一 `1953～1958年`、`1971～1973年` 等连接号，修正 `50年代,着重` 标点残留。
- 报告：`output/reports/reader_readability_health_parasite_malaria_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷寄生虫病防治疟疾回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第二节寄生虫病防治` 的 `一、疟疾` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `二、黑热病` 前。
- 统一年份连接号，并修正 `50年代,着重` 标点残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_parasite_malaria_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷寄生虫病防治疟疾回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
