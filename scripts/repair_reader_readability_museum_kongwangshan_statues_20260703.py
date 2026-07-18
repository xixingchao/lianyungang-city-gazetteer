# -*- coding: utf-8 -*-
"""Restore Kongwangshan cliff statues passage from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_kongwangshan_statues_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_kongwangshan_statues_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷孔望山摩崖造像回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0101.txt:31-41; "
    "workbench/ocr/paddle_ocr/下/part02/page_0102.txt:3-18"
)
SCOPE_START = "<p>二、造像</p>\n<p>孔望山摩崖造像位于孔望山南麓西端。"
SCOPE_END = "<p>六神台佛教造像位于灌云县伊山镇东北22公里处的伊芦山顶，石窟内。"

NEW_HTML = """<p>二、造像</p>
<p>孔望山摩崖造像位于孔望山南麓西端。相传孔子曾登临此山以望东海，故名孔望山。依山岩的自然形势，共雕刻出105躯各种形态的造像。分成13个组体，刻在东西长17米、高8米的峭崖上。最大的图像高1.54米，最小的头像仅10厘米。</p>
<p>造像群的题材，历来说法不一。有人认为是“古圣贤遗像”，清《嘉庆海州直隶州志》认为是“诸贤摩崖像”，《汉代画像全集》认为是“人事起居”，还有人认为是“士大夫阶层的人物和武士”，或“供人作乐的被剥削者”。1980年中国历史博物馆研究员史树青首次指出有佛教内容。概括起来约有三方面内容：一曰佛教造像。像群中有高肉髻、顶光、莲花、施无畏印、结跏跌坐等，并有表现佛本生故事的萨陲那太子舍身饲虎图。有表现佛传故事的“说法”和“涅槃”。有单个立像、坐像、菩萨像、弟子像、力士像和胡人形像的供养人像等。</p>
<p>这些都是佛教造像的特征。二曰道教造像。三尊各自独立存在的正面像，分别于造像群的最高处，是摩崖中最大的造像，其衣冠同汉代常见的世俗服饰，有的像下有“莲座”、“香炉”和“灯碗”等设置。当是道教在造像中的具体反映。三曰世俗画。即汉画像石中常见的“进谒”、“宴饮”等。</p>
<p>造像群的雕刻技法，有两种形式。一是在山岩上直接刻图；二是在长方形的龛中刻画。用传统的汉画像雕刻技法来表现外来的佛教题材，是孔望山摩崖造像的时代特征。具体使用了单线阴刻、平面线刻、浅浮雕和高浮雕四种，基本以平面线刻为主，约占整个造像的80%。</p>
<p>对造像的时代，有的认为是东汉晚期。有的认为从造像的主体来看，可认为是东汉遗物。也有人据洪适《隶释》所收录的东汉灵帝熹平元年（172年）《东海庙碑》考证：东海君庙供奉的神像就有两处，一处在庙内礼堂，一处在庙外祭坛。孔望山摩崖造像时代，当于此前后。还有人提出，孔望山造像的年代应在“晋魏之后，元魏之前”的观点。此外，有人认为，造像时代有晚到南北朝刘宋时期，甚至唐代的可能。</p>
<p>关于佛教艺术传入连云港孔望山之路线，也有两种不同见解。一曰海上丝绸之路，二曰西域通往内地的陆地丝绸之路逐步向东延伸所至。</p>
<p>孔望山造像比人们认为最早的敦煌莫高窟佛教艺术（366年）还要早约200年。它是我国佛教艺术的早期雏形。</p>
"""

EXPECTED_TEXT = [
    "一曰佛教造像",
    "高肉髻、顶光、莲花",
    "结跏跌坐等",
    "萨陲那太子舍身饲虎图",
    "“说法”和“涅槃”",
    "弟子像、力士像",
    "二曰道教造像",
    "三曰世俗画",
    "“进谒”、“宴饮”",
    "长方形的龛中刻画",
]
RESIDUALS = [
    "一日佛教造像",
    "高肉馨",
    "结咖跌坐",
    "萨睡那太子",
    "涅檗",
    "力土像",
    "二日道教造像",
    "三日世俗画",
    "“进”、“宴饮”",
    "的中刻画",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = NEW_HTML
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

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
        "scope": "第五十三卷文物 / 第四章石刻石雕 / 第一节摩崖石刻 / 二、造像 / 孔望山摩崖造像",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建孔望山摩崖造像小节，停止在六神台佛教造像前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷孔望山摩崖造像回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第四章石刻石雕 / 第一节摩崖石刻 / 二、造像 / 孔望山摩崖造像`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建孔望山摩崖造像小节，停止在 `六神台佛教造像` 前。
- 修正 `一曰`、`高肉髻`、`结跏跌坐`、`萨陲那太子`、`涅槃`、`力士像`、`进谒`、`龛中刻画` 等明确错识。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `page_0101.txt` 确认小节开头和佛教造像题材段。
- `page_0102.txt` 确认跨页续文、雕刻技法、时代判断和六神台边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷孔望山摩崖造像回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第四章石刻石雕 / 第一节摩崖石刻 / 二、造像 / 孔望山摩崖造像` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `六神台佛教造像` 前，未触碰后续条目。
- 修正 `一曰`、`高肉髻`、`结跏跌坐`、`萨陲那太子`、`涅槃`、`力士像`、`进谒`、`龛中刻画` 等明确错识。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_kongwangshan_statues_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum kongwangshan statues repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
