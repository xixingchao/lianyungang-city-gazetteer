# -*- coding: utf-8 -*-
"""Restore museum jade/stone items from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_jade_stone_items_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_jade_stone_items_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷馆藏玉石器中段回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0110.txt:22-38; workbench/ocr/paddle_ocr/下/part02/page_0111.txt:3-35"
SCOPE_START = "<p>十、石函</p>"
SCOPE_END = "<h4 id=\"第五十三卷-第五章馆藏文物-第二节陶瓷器\">第二节陶瓷器</h4>"

NEW_HTML = """<p>十、石函</p>
<p>1975年维修宋海清寺塔时出土，发现于塔第一层踏步下的一个方形砖室内。</p>
<p>石函系砚石雕成，长90厘米，宽40厘米，高60厘米。函盖折为3节，系旧断痕。盖四周浮雕四神，按左青龙、右白虎、前朱雀、后玄武顺序，函头端有阴线刻门扇一，上有锁，并有按五行排列的阴线刻门钉，门两侧还有阴线刻窗棂。石函两侧有浮雕，是内容相同的送葬行列。前半部是诸天降12部乐来迎佛人涅槃境，前导者四人，第一人执伞，第二人击钹，第三人掌幡，第四人吹法螺。后半为帝释、梵天扶一戴冠著袍的长者，再后是十大弟子哭泣像。石函下连须弥座，又浮雕四力士，肩负舍利石函，平托函底。座上部阴线刻缠枝花草如意纹。束腰及下部刻云气纹，函内前槽转浅为13厘米，后部转深为20.5厘米。整个石函造型凝重，雕刻细腻。石函虽出于宋塔中，盖有旧断痕，且盖上龙为三爪，门锁有唐风。故断定石函年代早于宋，可能是晚唐至五代时的作品。</p>
<p>十一、青玉蟠螭璧</p>
<p>1978年12月由白鸽涧生产队捐赠。此件为宋仿汉蟠螭形璧，质地为玉，直径为21厘米，璧眼4.5厘米，质地较好，形状完整，在器面上浮雕两蟠螭戏珠，形象生动。是研究宋代玉器的代表性的作品。</p>
<p>十二、白玉四环蟠螭</p>
<p>是以白玉雕成，直径4.5厘米，形状为四蟠螭盘围一起呈圆形，头向四个方向伸展。蟠螭头额宽阔，且很高。肩、鼻、口都集中在整个面部的下方，所占面积只有面部的三分之一。竖耳，“臣”字形眼。蟠螭为圆身，呈爬行状。尾特别长，作旋滑形。整个蟠螭神态栩栩如生，姿态非常美观。该四环蟠螭为元代作品。</p>
<p>十三、白玉佛造像</p>
<p>1966年从三元宫交来。该造像高48.5厘米，宽25厘米。为明代造像。人物造型，神态自然，眼睛有神，线条流畅，面貌安祥。雕刻手法古拙淳朴，此像据传由缅甸输入，当时是三元宫和尚背来做为镇庙之宝。建国后，供奉于龙洞庵，后交市博物馆。</p>
<p>十四、玉带版</p>
<p>以白玉浮雕而成，共12节，有长方形、桃形和长方形一端圆角三种，计大小36块，最大尺寸为16.4×6.5厘米，最小尺寸为5.4×1.4厘米。带版分首和尾两部分。明万历二十二年（1594年）由贞肃文献皇太后随同《大藏经》一部及三品紫衣一袭（附玉带）颁赐云台山三元宫。历明、清、民国作为重要庙产一直妥为保藏。民国27年9月（1938年），日军侵占连云港，这批文物由主持埋入地下。建国后紫衣、袈裟等文物流散，玉带版、佛像等转交海州地志文物陈列室，1973年入藏于市博物馆。</p>
<p>带版玉质细腻，刻工精致，首由7块长方形带版组成，它和尾方形一端带圆角，浮雕的纹饰相同。中间是五爪龙，盘绕于如意云之间，两侧各雕一异鸟，对午呈祥。龙的整个造型纤秀细长，以浮雕刻出龙身，再经阴刻去突出眼、爪和鳞片，体现了飞龙的浮沉起落和威严气势。尾及其它长方形和桃形带版皆镂雕出花鸟、流云和万字图案。整个带版成左右对称排列，大小长短相同。结构严谨，工艺精湛，实为一件难得的明代宫廷匠师制作的玉雕佳品。</p>
<p>十五、石祖</p>
<p>又名始祖石或石笋。出土于赣榆县秦方士徐福故里村南的新石器时代遗址上，通长146厘米，直径5厘米，顶端约28厘米，长的一段呈馒头形，表示为“龟头”，其下有一道槽沟。以下略呈方形，角、棱不太明显，“龟头”部分稍显凸出。从表面看石柱粗糙，似为用一块天然石料经简单打制而成，但“龟头”部分却极为光滑，该物长期以来被当地人崇拜为能使妇人生育的神物，有些不育妇人常来此抚摸或磕头祈求生子。此雕为清代遗物，已移入徐福祠保存。</p>
"""

EXPECTED_TEXT = [
    "<p>十、石函</p>",
    "砚石雕成",
    "阴线刻窗棂",
    "涅槃境",
    "第三人掌幡",
    "年代早于宋",
    "青玉蟠螭璧",
    "白玉四环蟠螭",
    "栩栩如生",
    "雕刻手法古拙淳朴",
    "缅甸输入",
    "紫衣、袈裟等文物流散",
    "万字图案",
    "十五、石祖",
    "移入徐福祠保存",
]
RESIDUALS = [
    "十、石1975",
    "砚右雕成",
    "阴线刻窗。",
    "涅境",
    "掌蟠",
    "年代卓于宋",
    "青玉蟠蝎璧",
    "蟠螨形璧",
    "白玉四环蟠蝎",
    "蟠螨神态",
    "古淳朴",
    "缅甸输人",
    "紫衣裴裂",
    "方字图案",
    "十五、石又名",
    "天然石的神物",
    "移人徐福祠",
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
        "scope": "第五十三卷文物 / 第五章馆藏文物 / 第一节玉石器 / 十至十五",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建玉石器中段，停止在第二节陶瓷器前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷馆藏玉石器中段回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第五章馆藏文物 / 第一节玉石器 / 十至十五`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `十、石函` 至 `十五、石祖`，停止在 `第二节陶瓷器` 前。
- 修正 `石函`、`砚石`、`窗棂`、`涅槃境`、`掌幡`、`早于宋`、`蟠螭`、`栩栩如生`、`古拙淳朴`、`输入`、`紫衣、袈裟`、`万字图案`、`石祖`、`移入徐福祠` 等明确错识。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `面貌安祥`、`对午呈祥` 为源页用字，本次保留不改。
- 后续 `第二节陶瓷器` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷馆藏玉石器中段回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第五章馆藏文物 / 第一节玉石器 / 十至十五` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第二节陶瓷器` 前，未触碰陶瓷器条目。
- 修正 `石函`、`砚石`、`窗棂`、`涅槃境`、`掌幡`、`早于宋`、`蟠螭`、`栩栩如生`、`古拙淳朴`、`输入`、`紫衣、袈裟`、`万字图案`、`石祖`、`移入徐福祠` 等明确错识；保留源页用字 `面貌安祥`、`对午呈祥`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_jade_stone_items_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum jade/stone items repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
