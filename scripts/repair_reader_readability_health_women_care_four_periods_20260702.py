# -*- coding: utf-8 -*-
"""Restore women's four-period protection subsection from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_women_care_four_periods_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_women_care_four_periods_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷妇女四期保护回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0203.txt:4-29; "
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101391-101410; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8086-8110"
)
SCOPE_START_OPTIONS = (
    '<p>三、妇女“四期”保护',
    '<p><strong>三、妇女“四期”保护</strong></p>',
)
SCOPE_END = '<h4 id="第五十五卷-第五章保健疗养-第二节儿童保健">第二节儿童保健</h4>'

NEW_HTML = """<p><strong>三、妇女“四期”保护</strong></p>
<p>民国38年（1949年）9月，新海连特区妇婴保健委员会成立后，加强对妇女特别是劳动妇女的月经期、怀孕期、产褥期、哺乳期的卫生保护工作。1953年，开始在城区各厂矿向女工进行月经期和怀孕期基本卫生知识教育。1953~1954年，全市通过图片展览、放幻灯、召开女工会或母亲会等形式进行女工卫生保健知识宣传教育活动241场次，受教育人数2.8万人次。1956年，在陇东火柴厂、新海印刷厂等厂进行女工新式月经带推广和建立月经卡制度试点。年底，全市有70%的青壮年妇女使用新式月经带。1958年，在农村和厂矿推行女工月经期、怀孕期、哺乳期挂片制度照顾女工、农妇在月经期调干不调湿，怀孕期调轻不调重，哺乳期调近不调远。产妇由政府发给2元营养费，享受30天产假。1960年，全市已有10家工厂、2个镇、33个生产队、4条城镇街道、2所学校、2个园艺场及盐场的31个工区成立女工保护委员会。75%的劳动妇女实行“三期挂牌制”。1961年，市妇女联合会、市卫生局发出《关于妇女劳动保护工作的意见》，要求城镇工厂、农村人民公社建立妇女劳动保护委员会，工厂车间、农村生产队建立妇女劳动保护小组；对16岁以下女青年不得作为整劳力使用；要贯彻执行“三调三不调”制度，切实做好妇女“四期”保护；妇女分娩给56天产假。1966年后，妇女“四期”保护的规定仍执行。1977年5月，在锦屏公社李圩大队召开市幼托工作现场会，推广其“四期”保护工作经验。1979年，贯彻《江苏省妇幼卫生条例》，开始注意妇女更年期的劳动保护。1981年5月，市政府规定自6月1日起，凡晚婚晚育领取独生子女证的妇女，其产假从法定的56天增加到96天，假期工资照发，工分照记。</p>
<p>1984年后，在全市开展“围产期保健”工作，即从妇女怀孕直到分娩后的45天内，进行一系列的卫生保健工作，在东海县驼峰乡试点。1987年，市总工会颁发《女职工卫生室检查验收标准》。1990年2月，市卫生局制订《女职工保健评比标准》，7月在市锦屏化工厂等10个厂试建女工系列保健模式工厂，使城区厂矿女工卫生保健工作规范化。在全市农村中开展孕产妇系统保健管理的乡已达73个、镇19个、村935个；全年早孕建卡20775人，产前检查3次以上者16259人次，产后访视16533人次，系统保健管理建卡8579人。</p>"""

EXPECTED_TEXT = [
    '<p><strong>三、妇女“四期”保护</strong></p>',
    "推行女工月经期、怀孕期、哺乳期挂片制度",
    "在全市农村中开展孕产妇系统保健管理的乡已达73个、镇19个、村935个",
    "全年早孕建卡20775人，产前检查3次以上者16259人次",
]
RESIDUALS = [
    "三、妇女“四期”保护民国38年",
    "坏孕期",
    "在全市农人，产前检查",
]


def find_scope(text: str) -> tuple[int, int]:
    starts = [text.find(marker) for marker in SCOPE_START_OPTIONS]
    valid_starts = [start for start in starts if start != -1]
    if not valid_starts:
        raise RuntimeError("women care four-periods scope start not found")
    start = min(valid_starts)
    end = text.index(SCOPE_END, start)
    return start, end


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
        raise RuntimeError(f"women care four-periods expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"women care four-periods residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第五章保健疗养 / 第一节妇女保健 / 三、妇女“四期”保护",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分标题并复原本小节尾句；正文汇总本句有残损，尾句以页级 OCR 为准。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷妇女四期保护回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第五章保健疗养 / 第一节妇女保健 / 三、妇女“四期”保护`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `三、妇女“四期”保护` 小节标题。
- 修正 `坏孕期` 为 `怀孕期`。
- 依据页级 OCR 复原尾句：`在全市农村中开展孕产妇系统保健管理的乡已达73个、镇19个、村935个；全年早孕建卡20775人...`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第二节儿童保健`。

## 核对说明

- PaddleOCR `page_0203.txt` 确认本小节标题、`怀孕期`、尾句与 `第二节儿童保健` 边界。
- 正文汇总文件在尾句处保留 `在全市农人` 残损，本次以页级 OCR 为准。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷妇女四期保护回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第五章第一节 `妇女保健` 的 `三、妇女“四期”保护` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分标题，修正 `坏孕期`，并按页级 OCR 复原 `在全市农村中开展孕产妇系统保健管理...` 尾句。
- 本轮新增整段替换 {changed} 处；`第二节儿童保健` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_women_care_four_periods_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("women care four-periods section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
