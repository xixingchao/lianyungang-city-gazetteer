# -*- coding: utf-8 -*-
"""Restore Fifth十五卷传染病防治六至八小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_infectious_hepatitis_dysentery_hemorrhagic_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_infectious_hepatitis_dysentery_hemorrhagic_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷传染病防治肝炎菌痢出血热回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0175.txt:7-38; page_0176.txt:3-8"
SCOPE_START = '<p><strong>六、病毒性肝炎</strong></p>'
SCOPE_END = '<p><strong>九、流行性感冒</strong></p>'

NEW_HTML = """<p><strong>六、病毒性肝炎</strong></p>
<p>1950年，新浦、海州有零星病毒性肝炎发生。1955年，新海连市立医院设立肝炎病房，隔离治疗肝炎病人。1966年8月，中云乡局部流行肝炎病，共发病106例，其中仅东巷村即达53例，无死亡。1970～1980年，全市共发病743例，发病率211.6/10万。1980年，海州区新坝乡小荡村肝炎流行，市卫生防疫站即派专人到村指导防治。以病家为单位隔离治疗，采取消毒措施，并进行预防注射。1986年，对市内饮食业人员进行乙型肝炎病毒感染的血清学调查，共调查接触食品的工作人员1527人，感染率为30.49%，乙型肝炎表面抗原携带率6.2%。1987年起，对新生儿和重点人群接种乙肝疫苗，市卫生防疫站制订《阻断母婴乙型肝炎传播工作方案》，要求各医疗卫生单位对孕妇全部进行乙型肝炎表面抗原检测，对检测结果阳性孕妇所生的新生儿全部进行乙肝疫苗接种。1988年春，上海市发生甲型肝炎流行，市人民政府办公室发出《关于加强防治肝炎工作的通知》，市、县（区）卫生局和卫生防疫站层层召开会议，研究制订防治措施，使肝炎控制在散发状态，未形成流行。1983～1990年，全市发病1.45万人，平均每年1800例，发病率61.9/10万，死亡11例，病死率6.05%。其中1989年为发病率高峰年份，发病4.23万例，死亡4例，发病率129.87/10万，主要分布于赣榆（1596例）、东海（1456例）两县。</p>
<p><strong>七、细菌性痢疾</strong></p>
<p>1952年，发动群众消灭苍蝇，管好水源、粪便、饮食卫生，预防疾病。1953年，发病2052例，死亡2例，发病率为1093.9/10万。1954年，采用赤痢噬菌口服预防，6～7月，全市共分3次完成7113人次。1955年7月，对市内饮食行业职工、清洁工以及环境卫生欠差地区的居民共口服4015人次。1957年，发病1696例，无死亡，发病率756.8/10万。</p>
<p>1960年，各医院开始建立肠道门诊，将菌痢作为监测的重点之一，凡腹泻病人均留粪便检验。1961年，改为痢疾菌苗注射接种。1970～1990年，全市发病5.89万例，死亡2例。其中发病率高峰年为1974年和1983年。1974年发病4102人，发病率为1265.1/10万；1983年发病7996人，发病率为1847.1/10万。</p>
<p><strong>八、流行性出血热</strong></p>
<p>1972年12月，市内首次发现流行性出血热2例。1974年和1975年发病皆17例，为高峰年份，发病率分别为5.24/10万、5.02/10万。至1982年，市区共发病96例，死亡1例。1983年，对东海、赣榆两县进行流行病学调查和监测，确定黑线姬鼠为连云港市境内流行性出血热的主要传染源，随即对境内鼠密度监测，开展灭鼠运动。1984年，市政府、东海县政府、赣榆县政府相继召开灭鼠防病保粮的专题会议，研究部署灭鼠工作。市、县（区）各级卫生防疫部门组织人力分赴农村进行灭鼠防病技术指导。赣榆县组织灭鼠专业队1803个，参加人数1.59万人次，共灭鼠259.17万只，堵、灌、挖鼠洞72.37万个，使鼠密度下降到7.27%。1984年为发病率高峰年份，共发病1626例，死亡60例，发病率55.6/10万。流行范围波及77个乡、镇、场，占全市乡、镇、场总数68.1%。以东海、赣榆两县为多，从11月开始到翌年2月下降。以30～39岁患者为多；男女患者之比为2.7：1，东海县发病1048例，死亡50例，发病率122.2/10万，占全市发病总数64.45%。1983～1990年，全市发病6899例，死亡77例。1990年全市发病374例，死亡6例，发病率为10.89/10万。</p>
"""

EXPECTED_TEXT = [
    "其中仅东巷村即达53例",
    "1983～1990年，全市发病1.45万人",
    "采用赤痢噬菌口服预防，6～7月",
    "将菌痢作为监测的重点之一",
    "改为痢疾菌苗注射接种",
    "发病率分别为5.24/10万、5.02/10万",
    "以30～39岁患者为多；男女患者之比为2.7：1",
]
RESIDUALS = [
    "东巷：村",
    "1983~1990年",
    "赤痫噬菌",
    "6~7月",
    "菌痫作为",
    "痫疾菌苗",
    "5.24/10方",
    "2.7:1,东海县",
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
    return changed, {"rewrote_scope": changed, "items_restored": 3, "paragraphs_restored": 4}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治 / 病毒性肝炎至流行性出血热",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建传染病防治六至八小项，停止在九、流行性感冒前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷传染病防治肝炎菌痢出血热回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：修正 `东巷：村`、`赤痫/菌痫/痫疾`、`5.24/10方`、出血热男女比标点等 OCR 残留。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷传染病防治肝炎菌痢出血热回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治` 中 `六、病毒性肝炎` 至 `九、流行性感冒` 前。
- 修复内容：修正 `东巷：村`、`赤痫噬菌`、`菌痫作为`、`痫疾菌苗`、`5.24/10方`、`2.7:1,东海县` 等残留。
- 报告：`output/reports/reader_readability_health_infectious_hepatitis_dysentery_hemorrhagic_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷传染病防治肝炎菌痢出血热回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第一节传染病防治` 的 `六、病毒性肝炎`、`七、细菌性痢疾`、`八、流行性出血热` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `九、流行性感冒` 前。
- 修正 `东巷：村`、`赤痫/菌痫/痫疾`、`5.24/10方`、`2.7:1,东海县` 等 OCR 残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_infectious_hepatitis_dysentery_hemorrhagic_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷传染病防治肝炎菌痢出血热回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
