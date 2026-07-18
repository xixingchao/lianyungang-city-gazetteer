# -*- coding: utf-8 -*-
"""Restore Fifth十五卷公共卫生第五节环境卫生 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_environment_hygiene_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_environment_hygiene_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷公共卫生环境卫生回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0172.txt:4-36; page_0173.txt:3-11"
SCOPE_START = '<h4 id="第五十五卷-第一章公共卫生-第五节环境卫生">第五节环境卫生</h4>'
SCOPE_END = '<h3 id="第五十五卷-第二章常见病防治">第二章常见病防治</h3>'

NEW_HTML = """<h4 id="第五十五卷-第一章公共卫生-第五节环境卫生">第五节环境卫生</h4>
<p><strong>一、饮用水水质监督</strong></p>
<p>市境内居民一向饮用河水、塘水、井水。民国32年（1943年）开始用自来水，未见水质监测记载。</p>
<p>1953年，开始培训饮用水消毒员，对饮用水加氯消毒。到1956年，全市已培训163人。1955年，对扩建后的花果山水库进行水质监测。1957年，新海连市人民委员会颁发《集中式生活饮用水水源选择及水质评价暂行规则》。1962年，各水厂开始建立水质检验制度，市卫生防疫站开始定期对水质抽样检测。1963～1966年，进行全市性第一次水源调查，全市共有水井627眼，其中采取消毒措施的397眼，占63.31%；饮用水塘141个，供应人口3.21万人；饮用河沟水人口5821人；饮用山涧水人口8472人；全市分散饮水户中进行缸水消毒的占70%。</p>
<p>1985年，进行饮用水源调查。市区已有自来水厂4处，供应22.75万人的饮用水，占市区总人口（下同）53.14%；浅水井1407眼，供应11.39万人的饮用水，占26.6%；饮用河水的2.72万人，占6.34%；饮用山区水库水3.78万人，占8.34%；饮用水塘17口，饮用人口2.17万人，占5.05%。经对各处水质进行检验，发现集中式供水的水源卫生状况尚好。</p>
<p>1986～1990年，逐步建立镇以上自来水厂卫生档案，定期对水厂人员进行体检，对不宜在水厂工作的调换工作。市卫生局及市政公用局制定《关于连云港市生活饮用水水源选择的有关规定》、《关于高层楼二次供水的管理规定》等法规性文件。</p>
<p><strong>二、粪便及垃圾管理</strong></p>
<p>民国35年（1946年），东海县警察局在新浦定时定点管理垃圾和粪便。民国38年1月，新海连特区公安总局颁发以保持环境卫生为主要内容的10条通告，对粪便、垃圾、污水的处理，对街道卫生的管理均有明确规定。1950年以后，市区内布点设置垃圾池，垃圾由清洁工人运出。部分街道由清洁工人到居民区收集垃圾，然后运往指定地点。1955年，新浦区清洁管理所成立，统一管理区内粪便和垃圾，市卫生防疫站负责指导、监督。</p>
<p>1963年，连云港、墟沟、海州、猴嘴等地均建立清洁管理所。全市共有清洁工人341人。至1980年，市区厕所以干式为主。1980年以后，开始改建和增建水冲式厕所。1981年4月15日，江苏省卫生厅、城市建设局通知规定从4月20日起城市环境卫生由卫生部门移交城建部门管理。</p>
<p><strong>三、公共场所卫生管理</strong></p>
<p>1953年6月，市卫生部门对文化宫、人民舞台、工人俱乐部等公共场所进行卫生检查。同年，开始对旅馆、浴池、理发店等服务性行业卫生管理，要求理发使用的用具必须经常消毒。1957年9月，开始在电影院进行空气蒸熏消毒。1962年制订电影院卫生管理规定。1981年，对市区游泳池水质定期进行监测监督，对部分影剧院空气中细菌总数进行监测。1984年，在全市18家影剧院作卫生学调查，共采集样品2897份，获有效数据10735个。1985年4月，对连云港市第一百货公司作卫生学调查。1986年，对不符合卫生要求的大村天然游泳场禁止开放。1987年，对公共场所的图书进行卫生检查，共采集样品120份，结果显示街头售书摊污染情况严重，大肠菌群检出率为96.7%。1988年，颁发《连云港市公共场所卫生管理条例》。1989年，对海滨浴场的出租游泳衣裤检查，将不符合卫生要求的1000余件游泳衣裤焚毁。1989年，市卫生防疫部门对检测合格的旅馆、影剧院等公共场所发给卫生许可证，共13家。1990年，又有14家旅馆、3家商场、12家宾馆领到卫生许可证。</p>
"""

EXPECTED_TEXT = [
    "市境内居民一向饮用河水、塘水、井水",
    "饮用山区水库水3.78万人，占8.34%",
    "<p><strong>二、粪便及垃圾管理</strong></p>",
    "<p><strong>三、公共场所卫生管理</strong></p>",
    "大肠菌群检出率为96.7%",
    "1990年，又有14家旅馆、3家商场、12家宾馆领到卫生许可证",
]
RESIDUALS = [
    "一、饮用水水质监督市境内",
    "居民向饮用河水",
    "3.78方人",
    "二、粪便及垃圾管理民国35年",
    "三、公共场所卫生管理1953年",
    "9%.7%",
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
    return changed, {"rewrote_scope": changed, "subheads_restored": 3, "paragraphs_restored": 8}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第一章公共卫生 / 第五节环境卫生",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建环境卫生节，停止在第二章常见病防治前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷公共卫生环境卫生回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：恢复三个小标题，修正 `一向饮用`、`3.78万人`、`大肠菌群检出率为96.7%` 等 OCR 残留。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷公共卫生环境卫生回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第一章公共卫生 / 第五节环境卫生` 至 `第二章常见病防治` 前。
- 修复内容：恢复 `一、饮用水水质监督`、`二、粪便及垃圾管理`、`三、公共场所卫生管理` 小标题；修正 `居民向饮用`、`3.78方人`、`9%.7%` 等残留。
- 报告：`output/reports/reader_readability_health_environment_hygiene_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷公共卫生环境卫生回源修复

- 对第五十五卷卫生 `第一章公共卫生 / 第五节环境卫生` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第二章常见病防治` 前。
- 恢复三个小标题，修正 `居民向饮用`、`3.78方人`、`大肠菌群检出率为9%.7%` 等 OCR 残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_environment_hygiene_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷公共卫生环境卫生回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
