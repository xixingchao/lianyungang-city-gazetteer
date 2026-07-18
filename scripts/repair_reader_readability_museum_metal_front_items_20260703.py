# -*- coding: utf-8 -*-
"""Restore museum metal front items from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_metal_front_items_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_metal_front_items_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷馆藏金属器前段回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0113.txt:20-37; workbench/ocr/paddle_ocr/下/part02/page_0114.txt; workbench/ocr/paddle_ocr/下/part02/page_0115.txt"
SCOPE_START = '<h4 id="第五十三卷-第五章馆藏文物-第三节金属器">第三节金属器</h4>'
SCOPE_END = '<p>十六、银匣</p>'

NEW_HTML = """<h4 id="第五十三卷-第五章馆藏文物-第三节金属器">第三节金属器</h4>
<p>一、铜甄</p>
<p>1960年出土于云台公社大村西周墓中，该器高52.3厘米，口径31.5厘米，颈部有弦纹两道，中缺算，三足空，上下为一整体。此为西周早期器物，曾被郭沫若选入《中国史稿》一书中，该器物器形完整，为研究西周伐夷提供重要史证。</p>
<p>二、铜鼎</p>
<p>1960年出土于云台公社大村。铜鼎高32.3厘米，口径29.15厘米。器形厚重，两耳直立沿上，颈部有雷纹一道，腹与腿有飞子。一足内撇，铜鼎系西周早期青铜重器，被郭沫若编入《中国史稿》一书中。</p>
<p>三、青铜匜</p>
<p>1982年1月1日，东海县青湖镇厂旺村春秋墓出土。该器长35.5厘米，高17.5厘米，瓢形，有柄，柄为一动物造型，腹下三足，亦作兽形，腹部饰一圈云雷纹、柄部有一裂纹。此器藏于东海县博物馆。</p>
<p>四、铜罍</p>
<p>1982年1月10日，东海县青湖镇厂旺村春秋墓出土。该青铜器完整无缺，高36厘米，口径14.5厘米，底径16厘米，壁厚0.6厘米。有两耳，小口，鼓腹，平底。腹上饰云雷纹图案，小腹上各有一道阴刻弦纹。</p>
<p>五、襄城楚境尹戈</p>
<p>1990年7月，市博物馆于海州区锦屏镇陶湾村附近采集。铜戈在距地表1.5米处出土，同时伴出的还有残陶器及零星残骨。戈竖向排列，推测戈应为军伍用于陪葬的器物。三戈中，最小的一件在内部有镌刻铭文两行，右起竖读为“都寿之岁，襄城楚尹所造”。“都寿之岁”当言楚国在寿建都三年。证明了公元前241年楚国虽迁城寿春，但并未失去襄城之地，这一实物出土，弥补了文献记载的不足。</p>
<p>六、秦父子诏量</p>
<p>1982年出土于东海县双店乡竹墩村，该量铜质，口近圆形，靠柄部弧曲。柄中空，圆底，量壁和口沿有磨损。据铭文中“相”、“皆”、“黔”、“并”等字的残缺程度，磨损0.6厘米。铜量通长18.2厘米，高7厘米，底径9.65厘米。口长13.4厘米，宽11.8厘米。柄长6.3厘米，宽3.9厘米。容量630毫升。铜量外腹部一侧竖刻秦始皇二十六年的法度量诏书，阴文篆刻，文7行，行6字，共40字，字径0.6～1厘米。文曰：“廿六年，皇帝尽并兼天下诸侯，黔首大安，立号为皇帝。乃诏丞相状、绾。法度量则不一歉疑之，皆明一之”。另一侧竖刻秦二世法度量的诏书，亦篆体阴文，文12行，行4～6字，计60字，字径0.4～1厘米。文曰：“元年制诏丞相斯、去疾，法度量尽始皇为之，皆有刻辞焉。今袭号而刻辞不称始皇帝，其于久远也。如后嗣为之者，不称成功盛德。刻此诏故刻左，使毋疑”。</p>
<p>秦始皇、二世“父子诏”铜量的发现，为研究秦代度量衡、文字等提供了一份重要的实物。</p>
<p>七、铜洗</p>
<p>1980年出土于东海县双店乡竹墩村汉遗址中。该铜洗完整无缺，高13厘米，口径26厘米，底径16.6厘米。作今脸盆形，微鼓腹，喇叭形口。斜口，平底外表光滑无纹，内部盆底有阴刻鱼一尾，其旁有“陈氏器”三字铭文，小篆。</p>
<p>八、“军假司马”印</p>
<p>1988年12月出土于东海县曲阳古城内，铜质，通高2.2厘米。印呈长方形，边长2.3厘米，坛钮，钮座高1.2厘米，长1.6厘米，主体呈梯形，上部边长2.1厘米，印阴刻篆书“军假司马”四字。经考证，为汉代铜印。</p>
<p>九、朐臣铜锅</p>
<p>1981年出土于赣榆县朱堵乡寺后村汉墓中。器型奇特，通高21.2厘米，10厘米高的三蹄形足支撑着腹孟形器身，腹径21.5厘米，腹深12厘米，壁厚0.2厘米，圆口微敛，矮沿，直唇，口径14.1厘米，口外有一圈阴线弦纹。折耳方穿，耳高6.2厘米，腹底圆弧略平，尚有烟炱，11个阴线篆体铭文横镌上腹部，字为缘腹睡书，字形由大而小，笔势遒劲，笔迹清晰，文为：“朐臣铜锅容斗四升重廿斤”。</p>
<p>铜锅为一次性模铸而成，现自身重为4050克，口微残，能容大米400克。铜锅出土地点附近，曾出土秦代铁权、铁剑、铜壶等物。考为汉代器物。</p>
<p>十、铜灯</p>
<p>铜灯两件。一高35厘米，豆形。顶端有一圆盘，口径14.5厘米，深2.6厘米，壁厚0.5厘米，盘内分大扇形格三个，每格内有一烛。盘下连三根圆形灯柱，高20厘米，直径2厘米。灯座喇叭形，饰有三周阶梯状旋纹。</p>
<p>另一灯龟形，长13厘米，宽11厘米，高8厘米。龟腹中空，侧有半月形双耳。灯盖一分为二，一半与座连为一体，另半盖用铰链与之相连。用时将此半盖翻于龟背之上，作灯碗用。碗内有灯芯，前有流。龟背、双耳和灯碗内皆刻有龙凤神兽及云纹图案。两铜灯造型别致，构思巧妙，寓装饰与实用于一体。为汉代器形。</p>
<p>十一、带鞘铁剑</p>
<p>1985年4月海州西汉西郭宝墓出土。该器剑身长98厘米，宽3厘米，剑格宽4.8厘米，剑把12厘米。鞘长87.8厘米，宽3厘米，剑身已有所锈蚀，但仍可见寒光，剑口锋利，鞘为夹胎。剑与鞘保存完好，这在全国也少见。墓主西郭宝为西汉中晚期时的东海太守。</p>
<p>十二、铜镳斗</p>
<p>1978年9月，在中云乡隔村废品收购站征集到。器口径18.5厘米，把长19厘米，流长2.8厘米，流宽3.8厘米，高26.5厘米。该器兽足，三足外撇，腹部有二道弦纹，龙把，有流。器物口沿延伸部分有残，上有一立耳，耳高2.3厘米，器物造型甚佳，器形较完整。为连云港市西晋遗物中的精品。</p>
<p>十三、银棺</p>
<p>1975年修海清寺塔时发现。棺长20.5厘米，宽8.8～5.6厘米，高10.5～9厘米，重375克。银棺内放一金棺，棺首有执剑、执斧天王力士像各一。四周绕以莲花纹，盖上为佛涅槃像，前后左右各有三个佛的三宝之一“金钢叉”图像。两侧为佛十八弟子哭泣像，另三人为梵天来降守护圣灵之像。画面生动，形象逼真。底部为模压的缠枝如意纹，下连须弥座四周镂空云纹。棺的铭文7行94字。</p>
<p>十四、鎏金银棺</p>
<p>1975年维修海清寺塔时发现。棺长10.3厘米，宽5.7厘米，高7.5厘米，重160克。棺盖呈弧形，上有佛的涅槃像，四周绕以缠枝如意纹，棺前、两侧各有一跌坐莲台的菩萨像。底部为一朵模压而成的大莲花，棺后有铭文，文曰：“施主弟子沈忠怒与眷孟氏二娘于天圣四年丙寅四月八日安葬舍利功德记”。</p>
<p>十五、银精舍</p>
<p>1975年维修宋海清寺塔时发现。银精舍长10厘米，宽6厘米，高6.5厘米，重95克。其下为长方形木莲座。上置一枚木刻马牙模型。前后各辟一门，两侧有护法天王像各一。四周环以波浪纹，两侧每边各开三个3×1.7厘米长方形窗扇，顶呈弧形，盖和四周全饰缠枝如意纹。</p>
"""

EXPECTED_TEXT = [
    "一、铜甄",
    "选入《中国史稿》",
    "三、青铜匜",
    "瓢形，有柄",
    "四、铜罍",
    "文曰：“廿六年",
    "丞相状、绾",
    "刻辞焉",
    "“陈氏器”三字铭文",
    "九、朐臣铜锅",
    "圆口微敛",
    "尚有烟炱",
    "笔势遒劲",
    "十二、铜镳斗",
    "佛涅槃像",
    "文曰：“施主弟子沈忠怒与眷孟氏二娘",
    "顶呈弧形",
]
RESIDUALS = [
    "一、铜1960",
    "选人《中国史稿》",
    "青铜匾",
    "高17.5厘米，形，有柄",
    "为一一动物造型",
    "四、铜1982",
    "文日：“廿六年",
    "丞相状、。",
    "刻辞為",
    "文日：“元年制诏",
    "“陈氏器三字铭文",
    "九、臣铜锅",
    "圆口微敏",
    "尚有烟，",
    "笔势道劲",
    "胸臣铜锅",
    "十二、铜斗",
    "佛涅像",
    "文日：“施主弟子",
    "与着孟氏二娘",
    "顶皇弧形",
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
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十三卷文物 / 第五章馆藏文物 / 第三节金属器 / 一至十五",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建金属器前段，停止在十六、银匣前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷馆藏金属器前段回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第五章馆藏文物 / 第三节金属器 / 一至十五`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、铜甄` 至 `十五、银精舍`，停止在 `十六、银匣` 前。
- 修正 `铜甄`、`选入`、`青铜匜`、`铜罍`、`文曰`、`丞相状、绾`、`刻辞焉`、`陈氏器`、`朐臣铜锅`、`微敛`、`烟炱`、`遒劲`、`铜镳斗`、`佛涅槃像`、`文曰`、`眷孟氏二娘`、`顶呈弧形` 等明确错识。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `中缺算`、`腹孟形器身`、`缘腹睡书`、`金钢叉`、`沈忠怒` 为源页 OCR 可见用字，本次保留不改。
- 后续 `十六、银匣` 至 `二十、琉球炉` 已由既有脚本维护，不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷馆藏金属器前段回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第五章馆藏文物 / 第三节金属器 / 一至十五` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `十六、银匣` 前，未触碰已修复的金属器尾段。
- 修正 `铜甄`、`选入`、`青铜匜`、`铜罍`、`文曰`、`丞相状、绾`、`刻辞焉`、`陈氏器`、`朐臣铜锅`、`微敛`、`烟炱`、`遒劲`、`铜镳斗`、`佛涅槃像`、`眷孟氏二娘`、`顶呈弧形` 等明确错识；保留源页可见用字 `中缺算`、`腹孟形器身`、`缘腹睡书`、`金钢叉`、`沈忠怒`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_metal_front_items_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum metal front items repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
