# -*- coding: utf-8 -*-
"""Restore museum lacquer/wood/misc items from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_lacquer_wood_items_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_lacquer_wood_items_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷馆藏漆木毛笔牙器其它回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0120.txt:17-38; workbench/ocr/paddle_ocr/下/part02/page_0121.txt"
SCOPE_START = '<h4 id="第五十三卷-第五章馆藏文物-第六节漆木 毛笔 牙器 其它">第六节漆木 毛笔 牙器 其它</h4>'
SCOPE_END = '<h4 id="第五十三卷-第五章馆藏文物-第七节版本文献">第七节版本文献</h4>'

NEW_HTML = """<h4 id="第五十三卷-第五章馆藏文物-第六节漆木 毛笔 牙器 其它">第六节漆木 毛笔 牙器 其它</h4>
<p>一、骨针</p>
<p>采集于海州二涧水库新石器时代遗址。骨针断二节已复修。长12.7厘米，直径0.4厘米，上端有一小圆孔，为针眼，针眼较小并乾圆，可见当时钻孔技术先进。从整体来看，骨针比较光滑，上端粗，下端尖。骨针的发现，说明6000年前人类即开始初期的服饰制作。</p>
<p>二、名谒</p>
<p>1985年4月23日，海州锦屏山黄石崖西汉东海太守西郭宝墓中出土。名谒一套五件，首尾素片。中夹名谒2器疏1，皆木质，大小一样，长21.5厘米，宽6.5厘米，厚0.8厘米。出土时，名谒在墓主人头侧。一件3行14字。隶体墨书。文曰：“东海太守宝再拜请足下西郭子笔”。另件3行12字，隶体墨书。文曰：“东海太守宝再拜谒西郭子笔”。名谒，即名刺，西汉谓之谒，东汉谓之刺。</p>
<p>三、木牍</p>
<p>1985年4月23日西郭宝墓中出土。木牍2件，均长21.5厘米，宽6.5厘米，厚0.8厘米。上记随葬物品的名称和数量，字迹清秀。隶体墨书。</p>
<p>四、木俑</p>
<p>1979年5月出土于云台乡高高顶西汉晚期墓的边箱。共计11件，皆属侍俑。抄手俑3件，最高者52厘米。1件长袍广袖，束高髻，体态丰盈。另2件亦长袍广袖，无高髻，平顶，抄手而肃立。持盾俑2件，高46厘米，发髻挽于脑后，袍长过膝，双腿并拢，威然挺立，裤管角肥大，垂掩拖地，双手将盾紧握胸前。盾面朱绘云气纹。俑的面部表情庄严，两眼直视，如威武卫士。拱手俑4件，两件耸高髻，两件髻挽于脑后，均长袍，似为供人驱使而忙碌不停。举臂俑1件，高髻长袍、窄袖，左臂曲举、右臂后垂。</p>
<p>另无臂细腰屈膝女俑1件，髻垂后颈，着长袍，身材纤秀，其动态、神情、姿态优美。</p>
<p>五、七子漆奁盒</p>
<p>西汉墓出土，盒高12.5厘米，腹径19.5厘米。盒圆形，内有7个小盒。母盒盖边缘饰以朱红色复线纹，其间绘有奔放的流云和劲健的斗兽，盖正中贴饰柿芾形银片，上有鸟兽图案。整个盒体绘画线条圆润而流利，子盒小巧玲珑，有圆形、长方形、马蹄形、椭圆形等，因形状不同而作用各异。马蹄形盒放梳篦，长方形盒内放耳环，有的盒里还有作脂粉用的辰砂。漆奁是以夹泞为胎，端庄不拙，在汉代漆器工艺品中，是难得的珍品。</p>
<p>六、漆砚盖</p>
<p>海州西汉墓出土。砚盖长19厘米，宽5.5厘米，砚盖断裂，变形，已修复。砚盖表面绘熊、虎相斗、形像生动，这是本地区发现的第一件汉代绘画作品。</p>
<p>七、毛笔</p>
<p>1985年4月出土于西郭宝墓。笔残长为21.2厘米，通体插入在竹制的并绘有朱色横条纹的笔套内。此笔的笔套是从尾部套入抹至毫端的。笔杆略长于笔套约2厘米。故整笔长约23.2厘米。笔杆木质，前端打一洞并垂直锯开，四分其木，作栽插笔头用。其孔长为1.8厘米。杆端0.3厘米，向后达1.5厘米，为紧固笔头用。并用大漆粘固成黑色。笔毫选料制成后总长3.2厘米，栽入笔内为0.7厘米，露出笔杆的毛锋长2.3厘米。毛出土时的色泽似用旧了的狼毫，但较细软，经鉴定为全兔毫。形制的独特和工艺之精，乃为国内首次发现。</p>
<p>八、骑马俑</p>
<p>1979年春出土于海州晚唐墓。俑一组4件，皆木质。其中骑马俑1件，侍俑3件。骑马女俑，高40厘米，头挽高髻，身披风衣。鞋尖点镫，双手挽缰。牵马俑1件，高26.5厘米。载朴俑头，衣短袍，腰束带，右手握拳于胸前，左手搭右肩作牵马状。侍女俑2件。一挽高髻，一挽平髻。整组木俑造型生动，颇具艺术感染力。在艺术造型上，已从盛唐以胖为美的风韵中脱出，丰满而不臃肿，纤巧多于朴实。</p>
<p>九、“佛牙”</p>
<p>1975年修海清寺塔时发现。“佛牙”长8厘米，宽25厘米，厚2.3厘米。出土时置于鎏金银棺内。“佛牙”根残缺，石化程度甚高，呈青绿色，经鉴定是马牙上颚第三齿。</p>
"""

EXPECTED_TEXT = [
    "二、名谒",
    "名谒一套五件",
    "文曰：“东海太守宝再拜请足下西郭子笔”",
    "西汉谓之谒，东汉谓之刺",
    "三、木牍",
    "木牍2件",
    "四、木俑",
    "皆属侍俑",
    "抄手俑3件",
    "持盾俑2件",
    "拱手俑4件",
    "女俑1件",
    "七子漆奁盒",
    "马蹄形、椭圆形等",
    "漆奁是以夹泞为胎",
    "出土于西郭宝墓",
    "栽入笔内",
    "八、骑马俑",
    "骑马女俑",
    "鞋尖点镫",
    "九、“佛牙”",
    "鎏金银棺内",
    "马牙上颚第三齿",
]
RESIDUALS = [
    "名　谒",
    "名谒套五件",
    "文日：“东海太守宝",
    "西汉谓之谌",
    "木、牍",
    "木膜2件",
    "四、木1979",
    "皆属侍。",
    "抄手角3件",
    "束高馨",
    "持盾角2件",
    "盾面朱绘云气纹。的面部",
    "拱手佣4件",
    "笃高髻",
    "女佣1件",
    "七子漆盒",
    "马蹄形、圆形等",
    "漆是以夹为胎",
    "出上于西郭宝墓",
    "通体插人在",
    "栽人笔内",
    "骑马補",
    "佣一组4件",
    "骑马诵1件",
    "侍角3件",
    "骑马女，高40厘米",
    "鞋尖点，",
    "牵马角1件",
    "侍女佣2件",
    "平馨",
    "木痛造型",
    "出土时置于</p>",
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
        "scope": "第五十三卷文物 / 第五章馆藏文物 / 第六节漆木 毛笔 牙器 其它 / 一至九",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建漆木毛笔牙器其它全节，停止在第七节版本文献前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷馆藏漆木毛笔牙器其它回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第五章馆藏文物 / 第六节漆木 毛笔 牙器 其它 / 一至九`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、骨针` 至 `九、“佛牙”`，停止在 `第七节版本文献` 前。
- 修正 `名谒`、`文曰`、`木牍`、`木俑`、`侍俑`、`抄手俑`、`持盾俑`、`拱手俑`、`七子漆奁盒`、`漆奁`、`出土于`、`栽入`、`骑马俑`、`鞋尖点镫` 等明确错识，并补回 `佛牙` 条目的 `鎏金银棺内` 与 `马牙上颚第三齿` 尾句。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `乾圆`、`2器疏1`、`柿芾形银片`、`夹泞为胎`、`载朴俑头` 为源页可见用字，本次保留不改。
- 后续 `第七节版本文献` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷馆藏漆木毛笔牙器其它回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第五章馆藏文物 / 第六节漆木 毛笔 牙器 其它 / 一至九` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第七节版本文献` 前，未触碰版本文献条目。
- 修正 `名谒`、`文曰`、`木牍`、`木俑`、`侍俑`、`抄手俑`、`持盾俑`、`拱手俑`、`七子漆奁盒`、`漆奁`、`出土于`、`栽入`、`骑马俑`、`鞋尖点镫` 等明确错识，并补回 `佛牙` 条目的 `鎏金银棺内` 与 `马牙上颚第三齿` 尾句；保留源页可见用字 `乾圆`、`2器疏1`、`柿芾形银片`、`夹泞为胎`、`载朴俑头`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_lacquer_wood_items_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum lacquer/wood items repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
