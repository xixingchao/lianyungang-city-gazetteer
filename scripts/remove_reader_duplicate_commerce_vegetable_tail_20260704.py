# -*- coding: utf-8 -*-
"""Remove remaining duplicated raw-line vegetable sales tail from the main reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_duplicate_commerce_vegetable_tail_removed_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_duplicate_commerce_vegetable_tail_removed_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_商业蔬菜销售尾段重复断行残片撤出.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COMPLETE_MARKER = "<p>1987年，市蔬菜公司主要任务为：管淡放旺，管大放小，保证春缺伏缺和国庆、中秋、元旦、春节四大节日，搞好冬储大白菜。全年购进本地菜2000多万公斤，外地菜500多万公斤。1988年，从山东寿光县购进青椒10多万公斤。此后大部分蔬菜实行了市场调节。</p>"

FRAGMENT = """<p>1987年，市蔬菜公司主要任务为：管淡放旺，管大放小，保证春缺伏缺和国庆、中秋、</p>
<p>元旦、春节四大节日，搞好冬储大白菜。全年购进本地菜2000多万公斤，外地菜500多万</p>
<p>公斤。1988年，从山东寿光县购进青椒10多万公斤。此后大部分蔬菜实行了市场调节。</p>

<p>1958年下半年开始，城乡掀起“大跃进”热潮，蔬菜供求矛盾突出。蔬菜公司以经营</p>
<p>鲜菜为主，成立蔬菜商店，对蔬菜包销。1959年销售量达到620.5万公斤。</p>
<p>1960年，因国民经济困难，蔬菜公司为适应市政府“以菜代粮”的口号，统一安排郊区</p>
<p>人民公社和城区对口供应，由海州郊区负责海州城和新浦地区，墟沟负责连云地区，朝阳、</p>
<p>中云、云台负责盐区，新坝产菜由市公司统一调剂。城市人口发票定量定点供应，每人每</p>
<p>天不少于1斤，各单位不得自行到农村买菜。全年销售1131万公斤。1961年销售2265</p>
<p>万公斤，国家给予亏损补贴54万元。1962年，粮食供应好转，销售545万公斤，亏损补贴</p>
<p>33.5万元。</p>
<p>1963年，市蔬菜公司对市场供应“管淡不管旺”，只管春缺、伏缺，全年销214万公斤。</p>
<p>1964~1965年改为管秋冬供应，销售量又上升到2063万公斤，亏损补贴1~3万元。调味</p>
<p>品经营移交烟酒公司。1966～1970年文化大革命”中，蔬菜公司职工坚守岗位，每年供应</p>
<p>市场蔬菜1500万公斤左右，多数为计划调节与市场调节相结合。1970年，开始调出大白</p>
<p>菜，每年50～100万公斤。</p>
<p>1972年蔬菜社会总销量1300多万公斤，蔬菜公司销售656万公斤，占总销量的50%，</p>
<p>其余为农户销售。考虑到大白菜起菜时间集中，必须采取特殊的供应方法。经多次研究</p>
<p>与实践，采取把计划分配到各机关、工厂、学校、街道，由各单位自已组织运输力量到田头</p>
<p>运菜，蔬菜公司派驻员到田头过磅。各单位把菜运回后下放各户储藏备用。市政府给予</p>
<p>每公斤1.4~2分钱补贴。当年分销400万公斤，补贴15万元。1973年，蔬菜公司恢复调</p>
<p>味品经营，品种30多个，年销售额90多万元。并兼营食盐批发，直到1983年，移交省盐</p>
<p>业公司。</p>
<p>1975年，市区关闭自由市场。1976年，连云港港口建设扩大，城市人口增加到25万，</p>
<p>由蔬菜公司承担蔬菜供应任务，全年销售蔬菜3184万公斤，亏损补贴59万元。1977~</p>
<p>1978年，蔬菜公司销售量占社会总销量的80%。</p>
<p>中共十一届三中全会以后，城乡农贸市场发展，个体卖菜户增加，蔬菜公司销售2877</p>
<p>万公斤，农贸市场成交624.5万公斤。</p>
<p>1983年1月，市政府为发挥国营商业主导作用，解决长期存在的产销矛盾，成立直属</p>
<p>市政府由农委代管的市蔬菜产销联合公司，对协调产销关系起了一定作用，但是亏损补贴</p>
<p>无法解决，当年撤销，恢复由市商业局领导的蔬菜公司。全年销售蔬菜3968.5万公斤，调</p>
<p>出5000公斤，亏损补贴122万元。农贸市场成交1642.5万公斤。</p>
<p>1985年后，蔬菜市场全部放开，蔬菜公司对市场“管淡放旺”，发挥主渠道作用，销售</p>
<p>量逐渐减小。1985年销售蔬菜1534.5万公斤，占社会总销量的20%~30%，调出57.5万</p>
<p>公斤，亏损补贴138万元，农贸市场成交1632.5万公斤。1988年停止蔬菜亏损补贴。</p>
<p>1990年，市区蔬菜总销售8823万公斤，其中蔬菜公司销售3742万公斤，农贸市场成</p>
<p>交5081万公斤，蔬菜市场逐渐以集市贸易为主。</p>"""


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    if COMPLETE_MARKER not in text:
        raise RuntimeError("complete polished vegetable tail marker is missing; refusing to remove fragment")
    count = text.count(FRAGMENT)
    if count:
        text = text.replace(FRAGMENT, "")
        HTML.write_text(text, encoding="utf-8")
    verify = HTML.read_text(encoding="utf-8")
    if COMPLETE_MARKER not in verify or FRAGMENT in verify:
        raise RuntimeError("vegetable tail duplicate removal verification failed")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第三十三卷商业蔬菜销售尾段重复断行残片撤出",
        "reader_path": str(HTML),
        "removed_fragments": count,
        "principle": "主阅读版已有完整精修段，仅撤出同段原始断行重复尾段；正文源不改。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = f"""# 商业蔬菜销售尾段重复断行残片撤出

- 时间：{now}
- 阅读器：`{HTML}`
- 撤出重复残片：{count} 组。
- 原则：主阅读版已有完整精修段，仅撤出同段原始断行重复尾段；正文源不改。
- 相关修复：`output/reports/reader_readability_commerce_vegetable_page_20260704.md`。
"""
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-04 商业蔬菜销售尾段重复断行残片撤出"
    memory = f"""
{marker}
- 主阅读版商业蔬菜销售段仍有从 `1987年` 至 `1990年` 的原始断行重复尾段；已撤出 {count} 组。
- 正文源不改，保留完整精修段作为读者入口。
- 报告：`output/reports/reader_duplicate_commerce_vegetable_tail_removed_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"removed_fragments": count, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
