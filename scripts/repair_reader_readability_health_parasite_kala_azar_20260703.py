# -*- coding: utf-8 -*-
"""Restore Fifth十五卷寄生虫病防治黑热病小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_parasite_kala_azar_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_parasite_kala_azar_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷寄生虫病防治黑热病回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0180.txt:8-20"
SCOPE_START = '<p><strong>二、黑热病</strong></p>'
SCOPE_END = '<p><strong>三、丝虫病</strong></p>'

NEW_HTML = """<p><strong>二、黑热病</strong></p>
<p>民国9年（1920年）境内始见黑热病记载，开始用吐酒石、新斯锑波霜等治疗，每治一人需银元30块。民国19年，市境内黑热病流行。民国28年，日军侵入市境，曾派伪同仁会华北中央防疫处医员冈部浩洋、伪同仁会青岛防疫处医员驹野丈夫和伪同仁会华北中央防疫处技术员长谷川吉等人于7月末至10月中在市内调查黑热病流行情况。调查中共确认71名黑热病患者，其中新浦19人，海州21人，连云港1人，近郊区30人；发病年龄最小的3岁，最大的45岁，以6～10岁居多；男41人，女30人；患者农民占39例。在71例患者中共进行骨髓穿刺66例，其中63例查到杜氏利什曼原虫。</p>
<p>建国后市内仍有新发病人。1950年12月，新海县卫生院举办黑热病培训班，培训防治专业人员13人。后在海州、新浦、新县、墟沟等地建立黑热病防治站，免费为患者治疗。</p>
<p>1952年，防治站撤销，该病治疗由各区卫生所和联合诊所承担。1950～1956年，采用敌敌涕、“六六六”灭蛉面积81.18万平方米。1950～1962年，全市累计治愈黑热病患者793人，另有53人死亡。1962年后该病绝迹。</p>
"""

EXPECTED_TEXT = [
    "以6～10岁居多",
    "1950～1956年，采用敌敌涕、“六六六”灭蛉面积81.18万平方米",
    "1950～1962年，全市累计治愈黑热病患者793人",
]
RESIDUALS = ["1950~1956年"]


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
    return changed, {"rewrote_scope": changed, "items_restored": 1, "paragraphs_restored": 3}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治 / 黑热病",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建黑热病小项，停止在三、丝虫病前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷寄生虫病防治黑热病回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：统一 `1950～1956年` 连接号。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷寄生虫病防治黑热病回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治` 中 `二、黑热病` 至 `三、丝虫病` 前。
- 修复内容：统一 `1950～1956年` 连接号。
- 报告：`output/reports/reader_readability_health_parasite_kala_azar_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷寄生虫病防治黑热病回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第二节寄生虫病防治` 的 `二、黑热病` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `三、丝虫病` 前。
- 统一 `1950～1956年` 连接号残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_parasite_kala_azar_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷寄生虫病防治黑热病回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
