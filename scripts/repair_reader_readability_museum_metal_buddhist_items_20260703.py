# -*- coding: utf-8 -*-
"""Restore museum metal Buddhist items from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_metal_buddhist_items_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_metal_buddhist_items_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷馆藏金属佛教器物回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0116.txt:6-38; workbench/ocr/paddle_ocr/下/part02/page_0117.txt:3-7"
SCOPE_START = "<p>十六、银匣</p>"
SCOPE_END = "<h4 id=\"第五十三卷-第五章馆藏文物-第四节碑刻\">第四节碑刻</h4>"

NEW_HTML = """<p>十六、银匣</p>
<p>1975年维修宋海清寺塔时发现。匣高6.8厘米，宽5.4厘米，重95克。银匣盖呈弧顶形，匣下有座，座下有四腿。匣内有琉璃葫芦瓶一个。内装舍利子。座上并放火烧过的人骨（佛骨）。盖铭文曰：“佛真身舍利两颗永同供养，进士傅县一家发心共施”。匣文曰：“阖家等施，傅县男女安仁傅氏大娘傅氏二娘傅氏三娘施同达妻子孟氏四娘与女儿同施”。匣后文曰：“大宋国海州西市界进士傅县天圣四年四月八日安”。</p>
<p>十七、铜权</p>
<p>1990年12月，灌云县龙苴镇一农民打井至地表下1.5米深处发现。铜权上窄下宽，六棱八面，权上部有高2厘米、宽3.5～4.3厘米的梯形钮，中有一扁圆孔。束腰，2.5厘米高的台阶状底座。权通高10.7厘米，重450克。权正面铸“大德十年”（1306年）四字，阳文；背面有“益都路”三字，阴文。</p>
<p>十八、大定通宝钱文镜</p>
<p>1981年5月在哑吧山征集。镜直径11.8厘米，浅卷边、鼻钮，连铢纹钮座。分内外区，内区围绕钮座有五枚不同方向的“大定通宝”钱文图饰，每两枚钱的中间有柿蒂形纹饰间隔。外区一周连珠纹，窄缘。该镜为典型的金代大定年间铜镜，较少见。</p>
<p>十九、铜造像</p>
<p>原藏三元宫，1976年5月入藏市博物馆。铜造像为观音、普贤、文殊。三尊像均高47厘米，像下有座。座高41厘米，座宽42厘米。三尊铜像造型端庄，比例匀称，装饰华美，均为明代佛教造像中的精品。</p>
<p>观音造像座为吼，吼头上扬，口张开，似怒吼，背上托上莲花，观音结跏跌坐于其上，手持经卷。</p>
<p>普贤造像座为象，身披缨络，象匍伏于地，象背上托起一朵莲花，普贤结跏跌坐于莲花上，双手持如意，双目下垂，面目安祥，似在入定。</p>
<p>文殊造像座为狮子，狮子头微扬，一副慵懒状，狮背莲花座上，文殊一手指天，一手指地，身披缨络，结跏跌坐，虔诚安祥。</p>
<p>二十、琉球炉</p>
<p>清嘉庆二十一年（1816年）夏，琉球国（今日本冲绳）八品巡见官毛朝玉，因海舶遇风飘至海州鹰游门。海州知州师亮采“日给廪纥”。为表感恩之情以炉相贻。师亮采为此题辞飧刻于上。腹部有“琉球炉”三个篆字并隶书落款20字，另有记述此炉来源的隶书71字。字体清秀，结体古拙，镌刻精美。</p>
<p>琉球炉，质地为紫铜，呈圆形，鼓腹。重5.1公斤，通高20.5厘米，口径7.5厘米，腹最大径为31厘米，底微鼓，等腰三角形分布于代足，足高2.3厘米，平底足径4厘米，在口沿部铸有一缺口长11.5厘米。</p>
<p>此炉原供奉宿城法起寺，1952年11月27日被山东省古代文物管理委员会借走，1976年由连云港市博物馆索还收藏。</p>
"""

EXPECTED_TEXT = [
    "<p>十六、银匣</p>",
    "盖铭文曰：“佛真身舍利两颗永同供养，进士傅县一家发心共施”",
    "匣后文曰",
    "龙苴镇",
    "益都路”三字",
    "普贤结跏跌坐于莲花上",
    "似在入定",
    "身披缨络，结跏跌坐",
    "日给廪纥",
    "以炉相贻",
    "重5.1公斤",
]
RESIDUALS = [
    "十六、银　厘",
    "厘高6.8厘米",
    "盖铭文日",
    "进土傅县",
    "便文日",
    "厘后文日",
    "龙直镇",
    "益都路”三学",
    "结咖跌坐",
    "似在人定",
    "身披缕络",
    "结跌坐",
    "日给原",
    "以炉相始",
    "71学",
    "5.1公厅",
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
        "scope": "第五十三卷文物 / 第五章馆藏文物 / 第三节金属器 / 十六至二十",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建金属器尾段，停止在第四节碑刻前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷馆藏金属佛教器物回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第五章馆藏文物 / 第三节金属器 / 十六至二十`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `十六、银匣` 至 `二十、琉球炉`，停止在 `第四节碑刻` 前。
- 修正 `银匣`、`进士傅县`、`匣文曰`、`匣后文曰`、`龙苴镇`、`三字`、`结跏跌坐`、`缨络`、`入定`、`廪纥`、`相贻`、`公斤` 等明确错识。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `面目安祥` 为源页用字，本次保留不改。
- 后续 `第四节碑刻` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷馆藏金属佛教器物回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第五章馆藏文物 / 第三节金属器 / 十六至二十` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第四节碑刻` 前，未触碰碑刻条目。
- 修正 `银匣`、`进士傅县`、`匣文曰`、`匣后文曰`、`龙苴镇`、`三字`、`结跏跌坐`、`缨络`、`入定`、`廪纥`、`相贻`、`公斤` 等明确错识；保留源页用字 `面目安祥`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_metal_buddhist_items_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum metal Buddhist items repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
