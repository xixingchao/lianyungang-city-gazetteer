# -*- coding: utf-8 -*-
"""Restore museum painting/calligraphy items from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_painting_items_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_painting_items_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷馆藏书画回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0119.txt:24-38; workbench/ocr/paddle_ocr/下/part02/page_0120.txt:3-16"
SCOPE_START = '<h4 id="第五十三卷-第五章馆藏文物-第五节书画">第五节书画</h4>'
SCOPE_END = '<h4 id="第五十三卷-第五章馆藏文物-第六节漆木 毛笔 牙器 其它">第六节漆木 毛笔 牙器 其它</h4>'

NEW_HTML = """<h4 id="第五十三卷-第五章馆藏文物-第五节书画">第五节书画</h4>
<p>一、万历圣旨</p>
<p>原藏三元宫，现藏市博物馆。圣旨色黄，堂心高31.8厘米，宽77.2厘米。天、地各有3.6厘米宽的二龙戏珠的云龙图案，色黄褐。圣旨内容为“……朕发诚心，刊造佛大藏经颁施在京及天下名山寺院。供奉经首护敕，已谕其由。尔住持及僧众人等务要虔诚供安。朝夕礼诵，保安眇躬。康泰宫壶。肃清忏已，真性愆祈无疆寿福。民安国泰，天下太平。俾四海八方，同归仁慈善教。朕成恭已无为之道焉。今准钦差提督山东、徐州等处地方矿税，兼理盐法，清查沿江河道船料内承运库事，御马监太监陈增奏请，前去彼处供安。各宜仰体知悉。钦哉谕。大明万历三十年九月六日”。文后加盖“广运大宝”大印，小篆，印高11.4厘米，阔11.1厘米，文、款皆楷书，字径1.6～1.7厘米。</p>
<p>二、王文《江关烟雨图》</p>
<p>文曰：“江关烟雨图，乾隆庚寅秋月河西王文”。绢本，纵192厘米，横104厘米。1979年5月经南京博物院肖平鉴定为真品，同年送南京博物院重新装裱，1980年4月入藏。</p>
<p>三、杨晋《天香书屋图》</p>
<p>为4条屏之一，绢本，纵50厘米，横48厘米。清杨晋绘，1979年5月经南京肖平鉴定为真品，1980年市博物馆正式入藏。</p>
<p>四、马元驭花鸟图轴</p>
<p>为绢本花鸟立轴，右上方有诗两行，诗曰：“柳斗轻狂，一种清幽缀池塘。最是西吹叶败，晚装和影对斜阳。”款一行：“癸未秋日写于大树山房，栖霞马元驭。”诗款皆行书。下有小印两方。白文：“元驭之印”，朱文：“扶曦”。皆小篆。此画是马元驭没骨花鸟画的精品。1979年5月经南京博物院肖平鉴定为真品。</p>
<p>五、边寿民册页画</p>
<p>册页6幅纸本，长24厘米，宽19厘米。画面为芦笋、水仙花、蛤蜊。桔子、菊花和梅花，每幅上都有题句，据画题，六幅小品皆作于乾隆辛未（1751年）春二月。该册页，1979年经徐邦达、肖平鉴定为真品，并为册页题字。</p>
"""

EXPECTED_TEXT = [
    "一、万历圣旨",
    "圣旨内容为“……朕发诚心",
    "保安眇躬",
    "真性愆祈无疆寿福",
    "无为之道焉",
    "文、款皆楷书",
    "二、王文《江关烟雨图》",
    "1979年5月经南京博物院肖平鉴定为真品",
    "三、杨晋《天香书屋图》",
    "正式入藏",
    "诗曰：“柳斗轻狂",
    "蛤蜊",
]
RESIDUALS = [
    "圣旨内容为·朕发诚心",
    "保安吵",
    "肃清已",
    "真性惩祈",
    "无为之道為",
    "文日：“江关烟雨图",
    "1979三、杨晋",
    "正式人藏",
    "诗日：“柳斗轻狂",
    "画面为芦笋、水仙花、蛤。",
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
        "scope": "第五十三卷文物 / 第五章馆藏文物 / 第五节书画 / 一至五",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建书画全节，停止在第六节漆木毛笔牙器其它前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷馆藏书画回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第五章馆藏文物 / 第五节书画 / 一至五`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、万历圣旨` 至 `五、边寿民册页画`，停止在 `第六节漆木 毛笔 牙器 其它` 前。
- 修正圣旨正文引号与 `眇躬`、`忏已`、`愆祈`、`焉` 等错识，拆开 `王文《江关烟雨图》` 与 `杨晋《天香书屋图》` 粘连，修正 `文曰`、`入藏`、`诗曰`、`蛤蜊` 等。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `康泰宫壶`、`朕成恭已`、`西吹叶败` 为源页可见用字，本次保留不改。
- 后续 `第六节漆木 毛笔 牙器 其它` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷馆藏书画回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第五章馆藏文物 / 第五节书画 / 一至五` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第六节漆木 毛笔 牙器 其它` 前，未触碰漆木等条目。
- 修正圣旨正文引号与 `眇躬`、`忏已`、`愆祈`、`焉` 等错识，拆开 `王文《江关烟雨图》` 与 `杨晋《天香书屋图》` 粘连，修正 `文曰`、`入藏`、`诗曰`、`蛤蜊` 等；保留源页可见用字 `康泰宫壶`、`朕成恭已`、`西吹叶败`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_painting_items_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum painting items repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
