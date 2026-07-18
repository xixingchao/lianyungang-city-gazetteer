# -*- coding: utf-8 -*-
"""Restore cadre healthcare section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_cadre_care_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_cadre_care_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷干部保健回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0205.txt:12-29; "
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101473-101489; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8168-8184"
)
SCOPE_START = '<h4 id="第五十五卷-第五章保健疗养-第三节干部保健">第三节干部保健</h4>'
SCOPE_END = '<h4 id="第五十五卷-第五章保健疗养-第四节知识分子保健">第四节知识分子保健</h4>'

NEW_HTML = """<p>解放初期，新海连特区干部享受供给制待遇，医疗保健由特区医院负责，医疗费用由国家负担。1952年11月，开始实行干部公费医疗制度，享受公费医疗的行政干部2000人，至1962年为3225人。1990年，市区享受公费医疗人员共20960人。公费医疗管理委员会制定法规，规定参加公费医疗的人员范围，经营开支制度，就诊、住院、疗养、药品使用等项制度。公费医疗的经费由市财政部门按标准一次拨给卫生部门掌握使用。其标准1952年为每人每年24元，1954年为每人每年18元，1978年为每人每年30元，1985年以后为每人每年55元。1961年，市卫生局对在职干部和职工全面进行一次健康检查，42.7%的干部和职工患有疾病，患肺结核病的占患病总数的13.8%，肝炎和肝大者占患病者11.6%。此后，市卫生局和市总工会联合建立干部疗养院，设50张疗养床位；建立干部保健卡，凭卡供应细粮和副食品；对933名在职干部（占干部总数12.5%）实行医疗保健。</p>
<p>1982年3月，市委组织部、老干部局、市人事局、卫生局组织第一次老干部健康检查，检查的253人中，除2人未发现异常情况外，其余均患有各种疾病，患病率较高的为动脉硬化129人，占被检人数的50.98%；患高血压病87人，占被检人数的34.38%；患冠心病80人，占31.6%等。市第一人民医院内科1病区改建为干部病区。此后对老干部每年进行一次健康检查。1985年，由财政拨款在市第一人民医院建老干部病房楼。1987年后，老干部体检改为二年一次。</p>"""

EXPECTED_TEXT = [
    "其标准1952年为每人每年24元，1954年为每人每年18元，1978年为每人每年30元，1985年以后为每人每年55元",
    "动脉硬化129人，占被检人数的50.98%；患高血压病87人，占被检人数的34.38%；患冠心病80人，占31.6%等",
]
RESIDUALS = [
    "其标准后为每人每年55元",
    "动脉硬化占31.6%等",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = "\n" + NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"cadre care expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"cadre care residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第五章保健疗养 / 第三节干部保健",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本复原干部保健漏文；正文汇总保留同样漏损，相关处以页级 OCR 为准。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷干部保健回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第五章保健疗养 / 第三节干部保健`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 补回公费医疗经费标准：`1952年为每人每年24元，1954年为每人每年18元，1978年为每人每年30元，1985年以后为每人每年55元`。
- 补回老干部健康检查统计：`动脉硬化129人...高血压病87人...冠心病80人...`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第四节知识分子保健`。

## 核对说明

- PaddleOCR `page_0205.txt` 确认本节完整文字和 `第四节知识分子保健` 边界。
- 正文汇总文件保留 `其标准后为每人每年55元` 和 `动脉硬化占31.6%等` 漏损，本次以页级 OCR 为准。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷干部保健回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第五章第三节 `干部保健` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；补回公费医疗经费标准和 1982 年老干部健康检查疾病统计漏文。
- 本轮新增整段替换 {changed} 处；`第四节知识分子保健` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_cadre_care_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("cadre care section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
