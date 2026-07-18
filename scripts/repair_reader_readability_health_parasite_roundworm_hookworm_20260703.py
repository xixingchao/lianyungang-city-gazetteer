# -*- coding: utf-8 -*-
"""Restore Fifth十五卷寄生虫病防治蛔虫病、钩虫病小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_parasite_roundworm_hookworm_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_parasite_roundworm_hookworm_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷寄生虫病防治蛔虫钩虫回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0180.txt:33-38; workbench/ocr/paddle_ocr/下/part02/page_0181.txt:3-16"
SCOPE_START = '<p><strong>四、蛔虫病</strong></p>'
SCOPE_END = '<h4 id="第五十五卷-第二章常见病防治-第三节地方病防治">第三节地方病防治</h4>'

NEW_HTML = """<p><strong>四、蛔虫病</strong></p>
<p>蛔虫病自古即有，市境未见疫情记载，民间常用山道年等驱蛔虫。1953年，在锦屏乡刘顶村和新海电厂进行蛔虫病感染情况调查，刘顶村民感染率为71.1%，电厂工人感染率为24%。1960～1970年在小范围调查5次，发现市内感染率在50%以上。1979年，按“国际儿童年”要求，市卫生防疫部门对1360名儿童进行粪便检验，发现蛔虫阳性者758名，阳性率为55.7%；集体生活儿童阳性率为54.9%，散居儿童阳性率为58.6%；城镇儿童阳性率为45.6%，农村儿童阳性率为76.3%。1988年，在落实国家卫生部“全国人体寄生虫分布调查”任务时，连云港市查出市内10个调查点的蛔虫总阳性率为60.31%。同年，海州区对7所小学进行蛔虫调查，发现感染率平均为20.87%。采用驱蛔灵、驱虫净治疗效果良好。</p>
<p><strong>五、钩虫病</strong></p>
<p>1955年对钩虫病在市内小范围调查，发现郊区农民感染率为19.93%。1958年全市普查，发现平均感染率为13.8%。1960年第二次全市普查，共查12.11万人，查出钩虫病患者1.02万人，感染率为8.39%。1960年采用四氯乙烯治疗，当年服药7982人。1978年冬到1979年春，抽样调查云台区朝阳乡9个村、中云乡西诸曹村、连云区连岛乡5个村、高公岛乡3个村、海州区白虎山村、锦屏区刘顶村等20个村，粪检1.15万人，确诊钩虫感染979人，平均感染率8.2%。1988年抽样调查中，共粪检5501人，查出钩虫感染者1003人，感染率20%。1988年，采用丙硫咪唑治疗，阳转率为86.4%。该病预防主要是注意个人卫生和治理好环境卫生。</p>
"""

EXPECTED_TEXT = [
    "1960～1970年在小范围调查5次",
    "1978年冬到1979年春，抽样调查云台区朝阳乡9个村",
    "共粪检5501人，查出钩虫感染者1003人",
]
RESIDUALS = ["1960~1970年", "5501人,"]


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
    return changed, {"rewrote_scope": changed, "items_restored": 2, "paragraphs_restored": 2}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治 / 蛔虫病、钩虫病",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建蛔虫病、钩虫病小项，停止在第三节地方病防治前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷寄生虫病防治蛔虫钩虫回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：统一 `1960～1970年` 连接号，并核定 `5501人，查出钩虫感染者1003人` 标点。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷寄生虫病防治蛔虫钩虫回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治` 中 `四、蛔虫病` 至 `第三节地方病防治` 前。
- 修复内容：统一 `1960～1970年` 连接号；核定钩虫病 `5501人，查出钩虫感染者1003人`。
- 报告：`output/reports/reader_readability_health_parasite_roundworm_hookworm_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷寄生虫病防治蛔虫钩虫回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第二节寄生虫病防治` 的 `四、蛔虫病`、`五、钩虫病` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第三节地方病防治` 前。
- 统一 `1960～1970年` 连接号，核定 `共粪检5501人，查出钩虫感染者1003人`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_parasite_roundworm_hookworm_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷寄生虫病防治蛔虫钩虫回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
