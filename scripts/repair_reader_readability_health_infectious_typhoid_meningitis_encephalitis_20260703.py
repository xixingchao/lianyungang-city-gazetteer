# -*- coding: utf-8 -*-
"""Restore Fifth十五卷传染病防治三至五小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_infectious_typhoid_meningitis_encephalitis_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_infectious_typhoid_meningitis_encephalitis_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷传染病防治伤寒流脑乙脑回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0174.txt:9-38; page_0175.txt:3-6"
SCOPE_START = '<p><strong>三、伤寒、副伤寒</strong></p>'
SCOPE_END = '<p><strong>六、病毒性肝炎</strong></p>'

NEW_HTML = """<p><strong>三、伤寒、副伤寒</strong></p>
<p>解放前，市内伤寒病时有发生，死亡人数无统计，但为数不少，仅连云港港口民国33年（1944年）伤寒病流行，码头工人死亡35人。当时，新浦、海州受到波及，出现部分散在性病例。民国38年夏，新海连特区所属浦西区朱圈村发生伤寒30例，死亡1例。自1951年开始，每年均进行伤寒、副伤寒混合菌苗或伤寒菌苗预防接种，重点对象为饮食服务行业职工，在发病区则普遍接种。1951年，全市发病127例，死亡1例，发病率67.6/10万。</p>
<p>1952年发生36例。1953～1958年，每年5例。1959年29例。1960年30例。1961年56例。1962年84例。1963年38例。1964年31例。1965～1974年，平均每年10例。1976年，全市发病127人，发病率37.7/10万，其中，连云区墟沟镇院前村有120人，占97%。</p>
<p>1979～1982年，每年发病人数多者29例，少者3例。1983～1987年，全市平均每年发病数在83～101例之间。1988年全市发病445例，发病率为14/10万。1989年171例。1990年93例。1952～1990年，伤寒病人除1955年和1966年共死亡4人外，余皆治愈。</p>
<p><strong>四、流行性脑脊髓膜炎</strong></p>
<p>1957年，全市流行性脑脊髓膜炎67例，死亡9例，发病率27.9/10万。1961年160例，死亡9例，发病率62.5/10万。流脑发病高峰期，市卫生局及各医疗卫生单位组成巡回组，深入各区各单位检查指导防治工作，在市级各医院专设流脑隔离病床150张，配备专职医护人员。通过宣传工具宣传流脑防治知识，对在公共场所的活动人群进行呋喃西林口腔喷雾。开展清洁卫生运动，保持环境空气清新，对疫点周围人群及中小学生进行口腔药物喷雾和磺胺噻唑口服。加强疫情报告制度，查治“苗头病人”。1962年1241例，死亡80例，发病率480.1/10万。1963年558例，死亡33例，发病率205.07/10万。1965年950例，死亡35例，发病率328.04/10万。1967年613例，死亡35例，发病率201.78/10万。1970年，开始流脑菌苗预防接种。1976年394例，死亡46例，发病率107.92/10万。</p>
<p>1977年282例，死亡4例，发病率75.64/10万。1981年后，每年仅发生一些散在性病例，1985年后，流脑菌苗预防接种普及，接种时间多在冬季，疫情得到控制。</p>
<p><strong>五、流行性乙型脑炎</strong></p>
<p>1954年，全市共发生流行性乙型脑炎66例，死亡14例，发病率33.4/10万。1955年开始接种乙脑疫苗3240人。1956年全市共发生乙型脑炎104例，死亡14例，发病率48.5/10万。1957年接种乙脑疫苗8500人，以后每年接种2000～8000人。1962年，发病91例，死亡7例，发病率38/10万。1963年，发病89例，死亡4例，发病率35.3/10万。</p>
<p>1966年，发病106例，死亡8例，发病率38.6/10万。1970年发病率为39.6/10万。1971年发病率为35.6/10万。1972年发病率为27.5/10万。1982年接种乙脑疫苗31349人。至1989年发病率均在10/10万以下。1990年市区发病率为3.7/10万，全市接种乙型脑炎疫苗占婴儿总数95%。在病家50米周边及蚊虫孳生场所喷洒药物灭蚊虫。</p>
"""

EXPECTED_TEXT = [
    "1979～1982年，每年发病人数多者29例，少者3例",
    "1983～1987年，全市平均每年发病数在83～101例之间",
    "发病率62.5/10万",
    "1967年613例，死亡35例",
    "1990年市区发病率为3.7/10万",
    "蚊虫孳生场所喷洒药物灭蚊虫",
]
RESIDUALS = [
    "1979~1982年,每年",
    "1983~1987年",
    "62.5/10方",
    "1967年.613例",
    "3.7/10方",
    "蚊虫擎生",
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
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治 / 伤寒副伤寒至流行性乙型脑炎",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建传染病防治三至五小项，停止在六、病毒性肝炎前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷传染病防治伤寒流脑乙脑回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：修正伤寒年份连接号、流脑 `10方` 和 `1967年.613例`、乙脑 `3.7/10方` 和 `蚊虫擎生` 等 OCR 残留。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷传染病防治伤寒流脑乙脑回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治` 中 `三、伤寒、副伤寒` 至 `六、病毒性肝炎` 前。
- 修复内容：修正 `1979~1982年,每年`、`62.5/10方`、`1967年.613例`、`3.7/10方`、`蚊虫擎生` 等残留。
- 报告：`output/reports/reader_readability_health_infectious_typhoid_meningitis_encephalitis_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷传染病防治伤寒流脑乙脑回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第一节传染病防治` 的 `三、伤寒、副伤寒`、`四、流行性脑脊髓膜炎`、`五、流行性乙型脑炎` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `六、病毒性肝炎` 前。
- 修正年份连接号、`10方`、`1967年.613例`、`3.7/10方`、`蚊虫擎生` 等 OCR 残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_infectious_typhoid_meningitis_encephalitis_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷传染病防治伤寒流脑乙脑回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
