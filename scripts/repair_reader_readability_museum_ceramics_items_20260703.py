# -*- coding: utf-8 -*-
"""Restore museum ceramics items from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_ceramics_items_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_ceramics_items_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷馆藏陶瓷器回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0111.txt:34-38; workbench/ocr/paddle_ocr/下/part02/page_0112.txt; workbench/ocr/paddle_ocr/下/part02/page_0113.txt:3-19"
SCOPE_START = '<h4 id="第五十三卷-第五章馆藏文物-第二节陶瓷器">第二节陶瓷器</h4>'
SCOPE_END = '<h4 id="第五十三卷-第五章馆藏文物-第三节金属器">第三节金属器</h4>'

NEW_HTML = """<h4 id="第五十三卷-第五章馆藏文物-第二节陶瓷器">第二节陶瓷器</h4>
<p>一、髹漆陶匜</p>
<p>灌云县东辛乡莱园村西汉墓出土，陶胎，髹黑漆。飘状，长槽流平口沿，垂直壁，腹部圈收，小平底。流长6.2厘米，口径长17厘米，宽14厘米，通高6厘米。与该器伴出有髹漆陶钫（残）、半两钱等。</p>
<p>二、东汉陶俑</p>
<p>1983～1984年，灌云县大伊山砖瓦厂、夹山口西东汉墓出土，陶俑共6件，皆侍女俑。四俑高矮服饰、表情完全一样，如出一模。均高35厘米。袖手而立、长裙束腰，腰略前倾，面部表情如有所思。</p>
<p>三、青瓷罐</p>
<p>通高27厘米，口径12厘米，直口微敛，平底微内凹，椭圆形腹，肩附四系，穿孔横贴，并有凸棱弦纹一周；腹有三道隐于釉下弦纹。罐身胎上细密坠致，布纹拍制，罐身中上部施青色釉，釉料厚实均匀，釉色明晰阳刻曲线图纹；底部露胎，通体晶莹细腻，浑朴温润，表现了精美制瓷工艺，时代当为西晋。</p>
<p>四、青釉绿彩水盂</p>
<p>1979年7月，由海州西门大队王庄生产队王冕献交。口径为3厘米，底径4.6厘米，腹径8.7厘米，高6.6厘米，产地长沙窑。釉下绿彩。器形完整，绿彩飘逸潇洒。为唐代外销瓷中的精品。</p>
<p>五、船形茶盏</p>
<p>1965年10月18日，海州园林寺大队果园生产队挖地时发现。盏为船形，高5.4厘米，宽7.5厘米，口径长12厘米，底径长6.1厘米。施青釉，胎厚重，敛口，圈足并有支烧点。为五代越州瓷窑的产品。</p>
<p>六、耀州窑瓷盏</p>
<p>1981年6月采集于大村砖厂。该瓷盏为宋代耀州窑产品。青釉压花。口径9厘米，底径4厘米，腹深2厘米，卷口宽边。胎上划印菊花图案。青色釉中泛黄釉，纹饰清晰，布局严谨，丰满，现状完整，光泽很强，手感较好。</p>
<p>七、葵瓣白瓷盏</p>
<p>1979年2月出土于海州大成砖厂。该器为葵瓣形，口径12.3厘米，底径6厘米，腹深3厘米。圈足、外撇。露灰白胎，并隐见开片纹。足底有墨书“米宅”二字。此盏是宋代安徽繁昌窑出品。</p>
<p>八、青白釉瓷钵</p>
<p>1972年采集于海州南门大队。瓷器为北宋产品，产地为湖田窑。口径21.7厘米，底径7.5厘米，高10厘米，腹围6.5厘米，青白釉折腰钵。形状完整，釉色偏黄。</p>
<p>九、青白釉菊瓣形瓷盒</p>
<p>瓷盒为南宋景德镇产品。直径5.6厘米，高3.3厘米，形状完整，为青白釉。盒底部有“许家合子记”铭款。口有伤缺，但因有制造家款识颇为少见。</p>
<p>十、黄釉碗</p>
<p>1986年10月7日，连云港市博物馆用馆藏汉代鹅形玉带钩与故宫博物院交换得来。该碗高6厘米，口径18.1厘米，线条柔和，釉质细腻。肥厚滋润，给人美感。碗深腹撇口，口沿很整齐。高圈足，足径7.3厘米。碗内外施黄釉，其中底部为白釉。底部口沿露胎，有桔红色窑红。碗底有用兰色画的双环纹，环内有用正楷字书写的“大明正德年制”年款。整个碗为一色釉，表面颜色鲜艳，光泽度强。从碗为素面单色釉并有窑红来看，它是明早期官窑烧制的瓷器。</p>
<p>十一、青白釉缠枝莲高足瓷碗</p>
<p>1986年10月与故宫博物院交换所得。该器为清乾隆年御窑产品。产地为景德镇。青白釉。器物高9.8厘米，口径14.4厘米，底径4.4厘米，器形完整，胎质坚致细腻，釉色晶莹透澈，工艺精湛，碗内底心有双圈六字两行“大清乾隆年制”官窑楷书刻款。</p>
"""

EXPECTED_TEXT = [
    "一、髹漆陶匜",
    "髹黑漆",
    "飘状",
    "髹漆陶钫（残）",
    "二、东汉陶俑",
    "陶俑共6件，皆侍女俑",
    "四俑高矮服饰、表情完全一样",
    "平底微内凹",
    "时代当为西晋",
    "青釉绿彩水盂",
    "圈足并有支烧点",
    "圈足、外撇",
    "墨书“米宅”二字",
    "十一、青白釉缠枝莲高足瓷碗",
]
RESIDUALS = [
    "漆陶匝",
    "黑漆。熟状",
    "漆陶（残）",
    "陶佣",
    "陶角共6件",
    "侍女佣",
    "四高矮服饰",
    "平底徽内凹",
    "西普",
    "水孟",
    "，足并有支烧点",
    "来宅",
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
        "scope": "第五十三卷文物 / 第五章馆藏文物 / 第二节陶瓷器 / 一至十一",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建陶瓷器全节，停止在第三节金属器前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷馆藏陶瓷器回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第五章馆藏文物 / 第二节陶瓷器 / 一至十一`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、髹漆陶匜` 至 `十一、青白釉缠枝莲高足瓷碗`，停止在 `第三节金属器` 前。
- 修正 `漆陶匝`、`黑漆/熟状`、`陶佣/陶角/侍女佣`、`四高矮服饰`、`平底徽内凹`、`西普`、`水孟`、`足并有支烧点`、`来宅` 等明确错识。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `坠致`、`兰色` 为源页 OCR 可见用字，本次保留不改。
- 后续 `第三节金属器` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷馆藏陶瓷器回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第五章馆藏文物 / 第二节陶瓷器 / 一至十一` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第三节金属器` 前，未触碰金属器条目。
- 修正 `漆陶匝`、`黑漆/熟状`、`陶佣/陶角/侍女佣`、`四高矮服饰`、`平底徽内凹`、`西普`、`水孟`、`足并有支烧点`、`来宅` 等明确错识；保留源页可见用字 `坠致`、`兰色`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_ceramics_items_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum ceramics items repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
