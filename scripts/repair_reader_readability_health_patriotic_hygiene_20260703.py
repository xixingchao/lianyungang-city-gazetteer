# -*- coding: utf-8 -*-
"""Restore Fifth十五卷公共卫生第一节爱国卫生 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_patriotic_hygiene_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_patriotic_hygiene_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷公共卫生爱国卫生回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0166.txt:4-34; page_0167.txt:3-19"
SCOPE_START = '<h4 id="第五十五卷-第一章公共卫生-第一节爱国卫生">第一节爱国卫生</h4>'
SCOPE_END = '<h4 id="第五十五卷-第一章公共卫生-第二节劳动卫生">第二节劳动卫生</h4>'

NEW_HTML = """<h4 id="第五十五卷-第一章公共卫生-第一节爱国卫生">第一节爱国卫生</h4>
<p><strong>一、机构</strong></p>
<p>民国38年（1949年）1月，新海连特区卫生建设委员会成立。1950年6月，新海县防疫委员会成立，翌年1月，改称新海连市防疫委员会，市长周子虹兼任主任。1952年4月，新海连市防疫委员会改为新海连市爱国卫生运动委员会（简称“市爱卫会”），周子虹兼任主任。市爱国卫生运动委员会设5个区分会、22个直属分会，各分会共设2093个卫生小组。</p>
<p>1956年6月，新海连市爱国卫生运动委员会调整，副市长刘一麟担任主任。1961年，新海连市爱国卫生运动委员会更名为连云港市爱国卫生运动委员会，“文化大革命”开始后，停止工作。1970年，市爱卫会恢复。1975年，市爱卫会解体。1976年10月，市爱卫会重新组建，由市政府负责人担任主任。1990年创建卫生城市，市长王稳卿任领导小组组长。</p>
<p><strong>二、活动</strong></p>
<p>解放初，中共新海连特委书记谷牧在干部会上提出要把改善城市医疗卫生状况，作为今后工作要点之一。发动新浦区军民8796人参加卫生义务劳动，疏通水沟58条，计15782米；清除臭淤9000吨、垃圾528吨，新挖明沟12条，计3083米；新建公共厕所、垃圾池158处，初步改变新浦城市卫生面貌。为保持环境卫生，新海连特区公安局制订《公共卫生规则》。1952年，全市掀起爱国卫生运动，动员全市人民，讲究卫生，粉碎美国的细菌战。为防止美国散布带菌昆虫侵入，连云区组织10个防疫灭虫大队、3个灭虫突击队，共3750人，在划定的海岸责任地段昼夜设岗了望和巡逻。1952年4月8日下午，墟沟镇、海头乡、海头湾村沿海岸边漂来许多带菌昆虫；4月10日，高公岛柳河海湾等地发现长约20米、宽1米面积的带菌昆虫；黄窝村发现许多黄色大蝇。以上发现的带菌虫类都被当地军民捕灭。1953年3月4日，连云港海岸沿线25公里范围内发现带菌昆虫，被当地军民捕灭。当年全市共开展全民大扫除15次，清除垃圾3412吨，疏通明暗沟2万米，填平臭水塘369个。运用黑板报、有线广播、幻灯、卫生知识展览对群众进行卫生宣传教育，教育面达全市人口的80%。</p>
<p>1955年，全市爱国卫生运动以除“四害”、讲卫生、消灭疾病为主要内容。发动群众捕灭蚊子、苍蝇、臭虫、虱子、老鼠等。坚持周六爱国卫生日，每周三、六两天卫生检查、地段保洁、轮流卫生值日等制度。1957年开展评选“清洁人家”、“卫生模范户”活动，共评出900余户。1958年，爱国卫生运动兴起除“四害”、讲卫生运动，全市每天有4万人次参加除“四害”和打扫卫生活动。1961～1962年，继续搞好除害灭病，还以防治浮肿、营养不良、闭经、子宫脱垂四病为中心，两年间全市治愈浮肿病人13639人次。1962～1965年，开展“两管五灭”（管水、管粪；灭蝇、灭鼠、灭蚊、灭臭虫、灭虱子）活动。1964年，全市有100个农村生产队建立粪场，设置专职粪管员。1966～1970年，爱国卫生运动各项活动停止。虽有部分街道乡镇仍按习惯坚持做好清洁卫生工作，但全市总体卫生水平下降，蚊蝇密度回升。</p>
<p>1976年，爱国卫生运动仍以除害灭病为主要内容，在全市推广连云港镇卫生工作经常化、制度化和锦屏公社刘顶大队粪便、饮水统一管理的经验。1978～1979年，开展全市性卫生扫除、卫生突击周活动和卫生大检查。1980年，爱国卫生运动的主要内容是治理城市卫生环境的脏、乱、差。1984年，开展争创文明卫生单位活动。新浦区出动1万人次填平区内最大的臭水塘—西天池。连云港港务局开展创建“无鼠害港”活动，使港区内鼠密度为0.08%，达到标准，通过中共中央爱国卫生委员会验收。1985年，国家卫生部、交通部授予连云港港为“无鼠害港”称号。1987年，全市开展灭鼠活动，使鼠密度从11.35%下降到4.53%，以鼠为传播媒介的流行性出血热的发病率比1986年下降43%。</p>
<p>1989年3月，全市开展第一个爱国卫生月活动。1990年，爱国卫生运动以创建国家卫生城市、提高人民生产、生活和环境质量水平为中心，市政府投资35万元，市区各单位资助158.49万元，共新建水冲式厕所46座、垃圾池43个，维修、改造老厕所312座，添置公共场所果皮箱435个、垃圾桶700只。共出动35万人次、机动车5110辆次、人力车5770辆次，清理垃圾13万吨。</p>
"""

EXPECTED_TEXT = [
    "副市长刘一麟担任主任",
    "疏通明暗沟2万米",
    "1962～1965年，开展“两管五灭”",
    "虽有部分街道乡镇仍按习惯坚持做好清洁卫生工作",
    "填平区内最大的臭水塘—西天池",
]
RESIDUALS = [
    "一、机•构",
    "刘一一麟",
    "疏通明暗沟2方米",
    "1962~～1965年",
    "虽有1976年",
    "一一西天池",
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
    return changed, {"rewrote_scope": changed, "subheads_restored": 2, "paragraphs_restored": 6}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第一章公共卫生 / 第一节爱国卫生",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建爱国卫生节，停止在第二节劳动卫生前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷公共卫生爱国卫生回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：恢复 `一、机构`、`二、活动` 小标题，修正刘一麟、明暗沟2万米、1962～1965年等错字，补回 1966～1970 年后漏失的清洁卫生工作句。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷公共卫生爱国卫生回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第一章公共卫生 / 第一节爱国卫生` 至 `第二节劳动卫生` 前。
- 修复内容：修正 `一、机•构`、`刘一一麟`、`疏通明暗沟2方米`、`1962~～1965年`、`一一西天池` 等 OCR 残留；补回 `虽有部分街道乡镇仍按习惯坚持做好清洁卫生工作...` 漏句。
- 报告：`output/reports/reader_readability_health_patriotic_hygiene_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷公共卫生爱国卫生回源修复

- 对第五十五卷卫生 `第一章公共卫生 / 第一节爱国卫生` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第二节劳动卫生` 前。
- 修正 `一、机•构`、`刘一一麟`、`疏通明暗沟2方米`、`1962~～1965年`、`一一西天池` 等 OCR 残留，并补回 1966～1970 年后漏句。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_patriotic_hygiene_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷公共卫生爱国卫生回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
