# -*- coding: utf-8 -*-
"""Restore Fifth十五卷公共卫生第三节食品卫生 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_food_hygiene_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_food_hygiene_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷公共卫生食品卫生回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0169.txt:7-36; page_0170.txt:3-10"
SCOPE_START = '<h4 id="第五十五卷-第一章公共卫生-第三节食品卫生">第三节食品卫生</h4>'
SCOPE_END = '<h4 id="第五十五卷-第一章公共卫生-第四节学校卫生">第四节学校卫生</h4>'

NEW_HTML = """<h4 id="第五十五卷-第一章公共卫生-第三节食品卫生">第三节食品卫生</h4>
<p><strong>一、监督管理</strong></p>
<p>民国35年（1946年），东海县警察局对新浦、海州两地的摊贩进行卫生管理，要求不得出售变质腐烂食品，违章者予以取缔。</p>
<p>1952年，新海连市接受加工一批香肠任务，支援朝鲜前线。市政府卫生科派员监督香肠制作的全过程，使这批香肠按要求及时运往朝鲜。1963年，市卫生防疫站根据国家卫生部、商业部、全国总工会颁布的《食品卫生管理暂行办法》、《食品加工、销售、饮食业卫生“五四制”》和新海连市人民政府颁布的《食品企业、饮食行业卫生管理办法》，对全市食品卫生进行监督管理。1958年，根据《工业企业设计暂行卫生标准规定》，对市罐头食品厂、牛奶厂、糖果糕点厂和7家冰棒厂的新建、扩建工程进行卫生监督；对190家食品生产经营单位经检查符合卫生标准后发给经营单位卫生合格证书。1980年，按照《中华人民共和国食品卫生管理条例》，市人民政府任命60名食品卫生监督员。1983年11月，实行《中华人民共和国食品卫生法》，对全市2400家生产、经营食品单位和个体商贩经检查符合食品卫生法发给卫生许可证。1985～1990年，对生产、经营食品单位和个体摊贩监督检查4.28万户次，累计销毁变质食品8.27万公斤，罚款1422户次，金额14.29万元，警告或限期改进5224户次，责令停业整顿802户次，吊销卫生许可证10户次。对从业人员进行体检15.13万人次，检出病人3885人。</p>
<p><strong>二、质量监测</strong></p>
<p>1953年开始对食品抽样检验，1975年以后逐步正常化。市卫生防疫站坚持每年对糕点、糖果及各种冷饮、酒、奶、调味品等进行卫生质量抽验。1984年，市罐头食品厂和渔业公司联营生产的五香鱼罐头，抽样9批均不符合卫生标准。1985年，市罐头食品厂生产的午餐肉罐头“85515”等三个批号计10吨，均不合格全部销毁。8月，海州8家商店经销的胡椒粉、山楂片、桔子粉、菊花晶等，经检测不合格，被销毁。1986年3月，市区各商店经销的105种白酒经抽样检测有5种不符合卫生标准，被勒令停止出售。1987年3～7月，从上海粮油贸易部门购进的22.7万公斤豆油经检测不符合卫生标准，除已售出的12.39万公斤，其余的均被勒令停止出售。1980～1990年，共抽检食品1.47万件，其中合格为1.13万件，合格率为76.82%。</p>
<p><strong>三、食物中毒防治</strong></p>
<p>1959年5月，连云港港务局码头工人因误食桐油造成363人中毒，经抢救全部脱险。同年，海州巴狗庄食堂误将敌敌涕粉剂当作食碱使用，造成46人中毒。1979年，陇海饭店由于嗜盐菌污染造成46人食物中毒。1982年10月10日，参加全国女排二级队联赛的10支排球队，在连云港市第二招待所因食用被蜡样芽胞杆菌污染的银耳汤造成36人中毒。1983年，赣榆县朱堵乡农民刘某出售被沙门氏菌污染的牛肉，造成185人中毒，1人死亡。1985年10月，来连云港市参加江苏省老年乒乓球赛的19名运动员发生副溶血性弧菌污染引起的食物中毒，经市人民医院治愈。1990年，赣榆县赣马镇一户居民食用河豚鱼，4人中毒，其中3人死亡。据统计，1970～1990年，全市共发生食物中毒136起，中毒3510人次，其中死亡7人。</p>
"""

EXPECTED_TEXT = [
    "按照《中华人民共和国食品卫生管理条例》",
    "午餐肉罐头“85515”等三个批号计10吨",
    "1987年3～7月，从上海粮油贸易部门购进的22.7万公斤豆油",
    "除已售出的12.39万公斤，其余的均被勒令停止出售",
    "海州巴狗庄食堂误将敌敌涕粉剂当作食碱使用",
    "副溶血性弧菌污染引起的食物中毒",
]
RESIDUALS = [
    "一、监督管理民国35年",
    "按照<中华人民共和国食品卫生管理条例》",
    "午餐肉罐头85515”",
    "1987年3.~712.39万公斤",
    "三、食物中毒防治1959年",
    "·同年，海州巴",
    "副溶血性孤菌",
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
    return changed, {"rewrote_scope": changed, "subheads_restored": 3, "paragraphs_restored": 6}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第一章公共卫生 / 第三节食品卫生",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建食品卫生节，停止在第四节学校卫生前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷公共卫生食品卫生回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：恢复三个小标题，修正《中华人民共和国食品卫生管理条例》书名号、午餐肉罐头批号、1987年3～7月豆油检测句、巴狗庄食堂句和副溶血性弧菌。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷公共卫生食品卫生回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第一章公共卫生 / 第三节食品卫生` 至 `第四节学校卫生` 前。
- 修复内容：恢复 `一、监督管理`、`二、质量监测`、`三、食物中毒防治` 小标题；修正 `<中华人民共和国食品卫生管理条例》`、`午餐肉罐头85515”`、`1987年3.~712.39万公斤`、`副溶血性孤菌` 等残留。
- 报告：`output/reports/reader_readability_health_food_hygiene_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷公共卫生食品卫生回源修复

- 对第五十五卷卫生 `第一章公共卫生 / 第三节食品卫生` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第四节学校卫生` 前。
- 恢复三个小标题，修正书名号、午餐肉罐头批号、1987 年豆油检测句、巴狗庄食堂断句和 `副溶血性孤菌` 等 OCR 残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_food_hygiene_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷公共卫生食品卫生回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
