# -*- coding: utf-8 -*-
"""Restore child health checkup subsection from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_child_care_checkup_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_child_care_checkup_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷儿童健康体检卫生保健回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0203.txt:29-42; "
    "workbench/ocr/paddle_ocr/下/part02/page_0204.txt:3-21; "
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101416-101443; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8111-8138"
)
SCOPE_START_OPTIONS = (
    '<p>一、儿童健康体检和卫生保健',
    '<p><strong>一、儿童健康体检和卫生保健</strong></p>',
)
SCOPE_END_OPTIONS = (
    '<p>二、儿童多发病矫治',
    '<p><strong>二、儿童多发病矫治</strong></p>',
)

NEW_HTML = """<p><strong>一、儿童健康体检和卫生保健</strong></p>
<p>1951年5月，市卫生部门对市建国路小学277名学生体格检查，符合健康标准的66人，占23.83%。其余的均患有各种疾病或缺陷，其中沙眼患者108人，占38.99%。1952年后，每年“六一”儿童节期间进行体检。1954年，市卫生部门、市妇联在云台区新县乡建起农忙季节托儿所12个。1955年6月，进行首次散居儿童体检，共查216人，其中完全健康的48人，34.7%患营养不良症，30%患有沙眼，16.7%有蛔虫。对患病儿童及时治疗，1956年8月，由市委组织部等15个部门组建新海连市保教事业管理委员会。1958年，市内幼儿园、托儿所1142所，共有入托儿童21125人，有保教人员1531人。1959年，市内幼托机构减至494所，入托儿童减少至8341人，保教人员减至1123人。1963年，市内有托儿所20处、幼儿园5处，共有受托儿童806人，保教人员64人。</p>
<p>1966年，儿童保健工作停顿，1970年恢复。1974年，市妇幼保健所对学龄前儿童的保育情况作一次调查。在被调查的26022名儿童中，入幼儿园或托儿所1094人，其余散居儿童由家中老人带的15352人，由大孩子带的5957人，老人照顾的3319人，其他带领方法的300人。1979年为国际儿童年，市妇幼保健所对全市幼托机构情况调查，全市共有7岁以下儿童34953人，其中3岁以下13154人；共有幼儿园、托儿所313所，3岁以下儿童入托为4094人，入托率为31.12%，3~7岁儿童入托7857人，入托率为36.04%；各托幼机构共有工作人员1005人，其中教师340人。1981年，市妇幼保健所设立儿童保健门诊，开始检查儿童智力。1983年5月，新浦区开展独生子女“健优美”评选活动。1984年，举办市首届幼儿体操比赛。1985年贯彻国家卫生部颁发的《托儿所、幼儿园卫生保健制度》，市妇幼保健所、市总工会、市妇联、市教育局对105个托幼机构进行儿童保健制度检查，为211名保教人员检查。1987年，市总工会、市妇联等部门颁发《托幼机构分类检查评比方法》。</p>
<p>1989年，全市8所县级以上医院开展出生缺陷监测工作。1990年，全市共有托幼机构1958个，入托儿童143001人，各类工作人员5753人。卫生部门为儿童健康检查385115人，共查出患病和缺陷儿童14271人，分别进行矫治。</p>"""

EXPECTED_TEXT = [
    '<p><strong>一、儿童健康体检和卫生保健</strong></p>',
    "16.7%有蛔虫。对患病儿童及时治疗",
    "共有入托儿童21125人",
    "入托儿童减少至8341人，保教人员减至1123人。1963年",
    "入幼儿园或托儿所1094人",
    "3岁以下儿童入托为4094人，入托率为31.12%",
    "颁发《托幼机构分类检查评比方法》。",
]
RESIDUALS = [
    "一、儿童健康体检和卫生保健1951年",
    "16.7%有虫",
    "共有人托儿童21125人",
    "人托儿童减少至8341人",
    "1123人。：1963年",
    "人幼儿园或托儿所1094人",
    "儿童人托为4094人",
    "人托率为31.12%",
    "颁发《托幼机构分类检查评比方法。",
]


def find_scope(text: str) -> tuple[int, int]:
    starts = [text.find(marker) for marker in SCOPE_START_OPTIONS]
    valid_starts = [start for start in starts if start != -1]
    if not valid_starts:
        raise RuntimeError("child care checkup scope start not found")
    start = min(valid_starts)
    ends = [text.find(marker, start) for marker in SCOPE_END_OPTIONS]
    valid_ends = [end for end in ends if end != -1]
    if not valid_ends:
        raise RuntimeError("child care checkup scope end not found")
    return start, min(valid_ends)


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"child care checkup expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"child care checkup residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第五章保健疗养 / 第二节儿童保健 / 一、儿童健康体检和卫生保健",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分标题并复原首小节；正文汇总有入托/书名号残损，相关处以页级 OCR 为准。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷儿童健康体检卫生保健回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第五章保健疗养 / 第二节儿童保健 / 一、儿童健康体检和卫生保健`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、儿童健康体检和卫生保健` 小节标题。
- 修正 `蛔虫`、`入托儿童`、`入幼儿园或托儿所`、`入托率` 等 OCR 明确错字。
- 修正 `1123人。：1963年` 标点残损。
- 复原 `《托幼机构分类检查评比方法》` 书名号。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `二、儿童多发病矫治`。

## 核对说明

- PaddleOCR `page_0203.txt` 确认本小节标题和首页文字。
- PaddleOCR `page_0204.txt` 确认跨页续文、`入托`、书名号和下一小节边界。
- 正文汇总文件保留 `人托`、`人幼儿园`、书名号缺尾等残损，本次以页级 OCR 为准。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷儿童健康体检卫生保健回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第五章第二节 `儿童保健` 的 `一、儿童健康体检和卫生保健` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分标题，修正 `蛔虫`、`入托` 系列错识和 `《托幼机构分类检查评比方法》` 书名号。
- 本轮新增整段替换 {changed} 处；`二、儿童多发病矫治` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_child_care_checkup_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("child care checkup section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
