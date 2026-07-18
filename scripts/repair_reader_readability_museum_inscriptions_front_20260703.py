# -*- coding: utf-8 -*-
"""Restore museum inscription front items from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_inscriptions_front_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_inscriptions_front_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷馆藏碑刻前段回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0117.txt:8-38; workbench/ocr/paddle_ocr/下/part02/page_0118.txt:3-39"
SCOPE_START = '<h4 id="第五十三卷-第五章馆藏文物-第四节碑刻">第四节碑刻</h4>'
SCOPE_END = '<p>十一、海州乡贡进士题名记碑'

NEW_HTML = """<h4 id="第五十三卷-第五章馆藏文物-第四节碑刻">第四节碑刻</h4>
<p>一、东海庙碑</p>
<p>碑为东汉熹平元年（172年）东海相满君所立。《天下碑录》、《太平寰宇记》、《金石录》、《隶释》等都收录。据《隶释》所录，碑的内容主要是记述东海相桓君于东汉永寿元年（155年）修缮东海庙的缘起、经过及“尊灵祗、敬鬼神”之宗旨，碑背有一行17字：“阙者，秦始皇所立，名之秦东门阙，事在史记”。字体略扁，挑捺明显。按《隶释》引《天下碑录》，此乃东海相任公在满君之后修庙时书刻。在孔望山摩崖造像东南约100米处，屹立着一块高4米，直径3米的天然大石，作石碣形，顶部有碑槽。据考证，此即东海庙碑之座。碑阴拓片有关资料保存于市博物馆。</p>
<p>二、糜竺墓碑</p>
<p>位于海州区石棚山北麓糜竺墓前。碑文为“安汉将军糜公之墓”。“文化大革命”中被毁坏。</p>
<p>三、东晋纪年砖</p>
<p>1986年3月，灌云县陡沟乡张薛村东晋墓出土。纪年砖皆长32厘米，宽15.5厘米，厚4.5厘米。菱纹模印在砖的一端和一侧，纪年砖铭文模印在砖的一侧，文曰“义熙九年为卞证君作。”已藏灌云县博物馆。</p>
<p>四、宁海门碑</p>
<p>1981年冬文物普查中发现，碑已残，唯“宁海”二字依稀可辨，魏体，字径50厘米。据张百川《云台导游诗钞》载，碑出土于咸丰十一年（1861年），上有“字径五尺”的“宁海门”三大字，并有“贞观十三年春魏征题”的刻题款。宁海门即古东海县城的南门，因此碑面有“宁海门”的名称。据考证，该碑并不是魏征所题，它是《西游记》“魏征梦斩泾河龙”故事影响下产生的海祭镇物。藏连云港市博物馆。</p>
<p>五、米芾书墓志残碑</p>
<p>1976年出土于海州朐山宋墓。墓志残碑为4块，最大宽26.5厘米，高18厘米，左起竖书10行，44字。4块残碑尚有65字可读，字径1.5厘米。文曰：“使淮安乡太称绍圣于京师年以是岁十月朐山县凤凰山长乡县君逢氏马尚书礼部侍郎涟水军使米芾”。藏连云港市博物馆。</p>
<p>六、王氏墓志碑</p>
<p>1956年12月出土于海州东门外玉带河五代砖室墓中。碑为石质，长宽各48厘米，厚19厘米，真书。结体严谨。根据墓志记载，该墓建于吴太和五年农历八至九月间，葬于同年九月二十九日，墓主为海州刺史赵思虔夫人太原县君王氏，享年41岁。该墓志的出土不仅是一件难得的五代书法艺术品，也为研究五代十国13年中墓葬的断代提供了重要的依据。藏南京博物院。</p>
<p>七、重修镇远楼碑</p>
<p>碑在海州钟鼓楼城下，为明嘉靖年间海州知州王同所立。碑体尚完好，额作弧形，高2.5米，宽1.03米，厚0.28米。碑阴面刻明正德年间《新建海道碑记》。两面碑文均因风化而模糊不清。</p>
<p>八、明神宗续颁藏经敕谕碑</p>
<p>此碑又称“圣旨碑”，高2.68米、宽1.04米，碑额高0.68米。明万历三十年（1602年）十月据御赐藏经护持刊立，坐落于三元宫藏经阁内。碑文楷书，满行26字，计316字，字径5厘米。碑额镌“圣旨”两个篆书大字。碑阴有《明神宗御制颁降藏经敕谕》，碑文记载颁赐藏经始末。云台山作为佛教名山，两次所赐藏经达678函，皆保存于三元宫藏经阁。</p>
<p>民国37年（1948年）三元宫毁于兵火，大藏经后辗转保存于宿城法起寺。1952年被山东省文管会借走，后被保存于山东省图书馆。其颁赐藏经的护持保存于连云港市博物馆。</p>
<p>九、院道明文碑和圣谕碑</p>
<p>二碑原在海州师范（明清时为海州州衙所在地）院内。“院道明文”碑高180厘米、宽80厘米、厚18厘米。碑文横书“院道明文”四字，竖书“佐贰首领不许擅受民词如违究被告不许赴理”的内容。楷书，字径13厘米。“圣谕”碑高160厘米、宽70厘米、厚22厘米。额勒“圣谕”二字，竖刻“圣谕”六条。字迹漫漶，尚有部分文字可读。此碑是明永乐年间巡按淮安等处御史刘（佚名）刊立。他来海州考核吏治时，发现海州官吏腐败，贪污横行，因立是碑以警告，同时布告州民，对海州地方官吏予以监察。此二碑藏于连云港市博物馆。</p>
<p>十、重修云台山香火田地碑</p>
<p>此碑原座落于花果山三元宫正殿西侧碑庐。民国27年（1938年）日机轰炸云台山，该碑脱落。碑碣、碑身和碑座基本完整。1985年重修碑亭，复安原位，现列为市级文物保护单位。</p>
<p>田地碑始立于清康熙十四年（1676年），为砚石雕成，三节。碑碣宽118厘米、高60厘米、厚46厘米。两面浮雕二龙戏珠，形态生动。碑座和碑碣形制一样，两面浮雕二龙戏珠。在高70厘米、宽90厘米的碑座下尚有高40厘米狭肩的二层台埋入地下。座上正中有一正方形榫眼，和碑身下一长30厘米的石榫接合成一整体，碑身高157厘米、宽89厘米、厚29厘米。正文14行，行42字，字径2厘米。书体取法欧阳询。由奉直大夫知江南淮安府海州事赵之鼎撰文，杨书屏书丹。碑文记三元宫官修建缘起，清初裁复海的始未，明以来免赋的香火田三处，是研究云台山成陆，裁复海史及封建社会寺院经济的重要实证。</p>
"""

EXPECTED_TEXT = [
    "一、东海庙碑",
    "修缮东海庙",
    "挑捺明显",
    "石棚山北麓",
    "文曰“义熙九年为卞证君作。",
    "米芾书墓志残碑",
    "使淮安乡太称绍圣",
    "明神宗续颁藏经敕谕碑",
    "碑额镌“圣旨”两个篆书大字",
    "御制颁降藏经敕谕",
    "字迹漫漶",
    "正方形榫眼",
    "石榫接合成一整体",
]
RESIDUALS = [
    "修东海庙的缘起",
    "挑擦明显",
    "石榭山北麓",
    "文日“义熙九年",
    "为下证君作",
    "米蒂书墓志残碑",
    "使准安乡太称",
    "米蒂”。藏",
    "藏经谕",
    "碑额镌圣旨”",
    "字迹漫，",
    "正方形样眼",
    "石样接合",
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
        "scope": "第五十三卷文物 / 第五章馆藏文物 / 第四节碑刻 / 一至十",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建碑刻前段，停止在十一、海州乡贡进士题名记碑前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷馆藏碑刻前段回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第五章馆藏文物 / 第四节碑刻 / 一至十`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、东海庙碑` 至 `十、重修云台山香火田地碑`，停止在 `十一、海州乡贡进士题名记碑` 前。
- 修正 `修缮东海庙`、`挑捺`、`石棚山`、`文曰`、`卞证君`、`米芾`、`淮安`、`敕谕`、`圣旨` 引号、`漫漶`、`榫眼`、`石榫` 等明确错识。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `东海相满君`、`东海相桓君`、`尊灵祗`、`卞证君`、`裁复海` 为源页 OCR 可见用字，本次保留不改。
- 后续 `十一、海州乡贡进士题名记碑` 及以后条目不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷馆藏碑刻前段回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第五章馆藏文物 / 第四节碑刻 / 一至十` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `十一、海州乡贡进士题名记碑` 前，未触碰碑刻后段。
- 修正 `修缮东海庙`、`挑捺`、`石棚山`、`文曰`、`卞证君`、`米芾`、`淮安`、`敕谕`、`圣旨` 引号、`漫漶`、`榫眼`、`石榫` 等明确错识；保留源页可见用字 `东海相满君`、`东海相桓君`、`尊灵祗`、`卞证君`、`裁复海`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_inscriptions_front_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum inscriptions front repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
