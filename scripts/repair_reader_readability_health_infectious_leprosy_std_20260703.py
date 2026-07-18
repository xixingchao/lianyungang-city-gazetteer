# -*- coding: utf-8 -*-
"""Restore Fifth十五卷传染病防治十九至二十小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_infectious_leprosy_std_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_infectious_leprosy_std_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷传染病防治麻风性病回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0178.txt:32-36; page_0179.txt:3-23"
SCOPE_START = '<p><strong>十九、麻风</strong></p>'
SCOPE_END = '<h4 id="第五十五卷-第二章常见病防治-第二节寄生虫病防治">第二节寄生虫病防治</h4>'

NEW_HTML = """<p><strong>十九、麻风</strong></p>
<p>麻风病在市境内流行已久，未见发病情况记载。</p>
<p>1953年4月，对市内麻风病发病情况调查，查出患者76人，其中35人为1949年以前发病。由于民间一直存在对该病的恐惧心理，故患者皆着意隐瞒，少有自动就医者，该病的流行情况主要依靠社会普查获取。1957年进行普查。1966年以前，对查出的患者由卫生部门专人送医送药到其住处，免费治疗。1966年9月，连云港市麻风病防治所在云台区板桥镇建立，免费收治患者78名。1972～1973年进行普查，其余年份主要依靠线索调查掌握发病情况。1973年查出连云区宿城乡患者10人，占该乡总人口2500人的4%；查出海州区新坝乡樊庄村5名患者，占该村总人口2000人的2.5%。截至1989年，连云港市皮肤病防治所累计收治患者413人，其中治愈355人，外迁及死亡42人，现症患者16人。全市累计发病328人，占全市总人口的0.65‰，为中等度流行区域。1985～1989年，全市发病率被控制在2/10万以下。</p>
<p><strong>二十、性病</strong></p>
<p>市内性病流行年代已很久，民国36年（1947年）就有文字记载，但无疫情统计。民国35年至37年，海属公立医院每周为妓女检查一次，对被查出的性病患者留其住院，经采用砷制剂“九一四”、“六零六”治愈后方可出院。1950年，新海连市人民政府取缔妓院，禁止嫖娼卖淫，对妓女安排劳动就业，同时救治性病患者，到1953年性病绝迹。1986年，市内新发现3名淋病患者。1987年，发现性病29例。同年6月，市皮肤病防治所被指定为性病监测单位负责全市性病防治人员培训、技术指导等各项工作。1988年，发现性病306例。1989年，发现性病505例。发病年龄在20～35岁的占77%。1989年12月，市皮肤病防治所内成立市性病监测中心，设立性病检验室，专设性病咨询门诊部。1989年12月16～20日，举办市首期性病培训班，培训技术人员60余人。1988～1990年，市皮肤病防治所组织3次性病普查，检查对象主要是宾馆、招待所服务人员。其中，1988年共检查196人次，查出性病患者9例。1989年8月，对东海县劳改农场劳改人员检查中，共查27人次，查出性病患者10人。性病治疗采用菌必治、淋必治，效果较好。</p>
"""

EXPECTED_TEXT = [
    "1972～1973年进行普查",
    "全市累计发病328人，占全市总人口的0.65‰",
    "1985～1989年，全市发病率被控制在2/10万以下",
    "禁止嫖娼卖淫",
    "发病年龄在20～35岁的占77%",
    "1989年12月16～20日，举办市首期性病培训班",
    "性病治疗采用菌必治、淋必治，效果较好",
]
RESIDUALS = [
    "1972~1973年",
    "0.65%0",
    "1985~1989年",
    "禁止娟卖淫",
    "20~35岁",
    "16~20日",
    "淋必治,效果较好",
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
    return changed, {"rewrote_scope": changed, "items_restored": 2, "paragraphs_restored": 4}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治 / 麻风、性病",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建传染病防治尾段，停止在第二节寄生虫病防治前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷传染病防治麻风性病回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：修正麻风发病率千分号、`禁止嫖娼卖淫`、年份连接号和末尾逗号残留。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷传染病防治麻风性病回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治` 中 `十九、麻风` 至 `第二节寄生虫病防治` 前。
- 修复内容：修正 `0.65%0`、`禁止娟卖淫`、年份连接号、`淋必治,效果较好` 等残留。
- 报告：`output/reports/reader_readability_health_infectious_leprosy_std_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷传染病防治麻风性病回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第一节传染病防治` 的 `十九、麻风`、`二十、性病` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第二节寄生虫病防治` 前。
- 修正 `0.65%0`、`禁止娟卖淫`、年份连接号和 `淋必治,效果较好` 等 OCR 残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_infectious_leprosy_std_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷传染病防治麻风性病回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
