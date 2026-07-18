# -*- coding: utf-8 -*-
"""Restore religion volume overview from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_religion_overview_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_religion_overview_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十七卷宗教概述回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0257.txt:5-30; "
    "workbench/ocr/paddle_ocr/下/part02/page_0258.txt:3-17"
)
SCOPE_START = '<h3 id="第五十七卷-概述">概述</h3>'
SCOPE_END = '<h3 id="第五十七卷-第一章佛教">第一章佛教</h3>'

NEW_HTML = """<p>东汉时佛教从西域传入市境。据专家考证，孔望山摩崖石刻为汉代佛像群雕。宿城法起寺僧人与古康居国（今苏联撒马尔罕一带）僧人有交往，寺内鹫峰石塔、罗汉墓就是康居国高僧的墓塔。</p>
<p>魏晋南北朝时期，佛教在境内不断发展。唐宋以后，统治阶级提倡、士大夫喜谈禅学、百姓也随之信奉，法起寺成为境内及附近地区研究、传播大乘教义的主要寺院之一。明清时为佛教鼎盛时期，由于三元宫转为佛教寺院并多次扩建，形成云台山区的佛教寺院群。</p>
<p>明万历十五年（1587年），神宗皇帝朱翊钧颁降经敕谕，由钦差大臣专程护送到云台山，随赐《大藏经》、佛像等佛物。时三元宫香火逾两万家，后一度衰颓。清康熙三十一年（1692年），皇帝玄烨亲书“遥镇洪流”匾额赐三元宫，康熙三十八年又派太监上云台山进香。康熙五十二年，大规模修建法起寺，境内佛教事业步上顶峰，直至民国初期长盛不衰。</p>
<p>道教在元明两代兴盛起来，境内道教庙观较多，仅云台山区就有云门寺、上真观、三元宫、延福观、祥云观、紫阳观、无梁殿、白龙王庙、北老君堂、碧霞宫、三元庙等。但自乾隆以后，每况愈下。</p>
<p>清末天主教和基督教传入境内，清光绪三十二年（1906年）美国基督教派牧师米德安夫妇等来海州，边行医边传教，此为境内基督教传布的发端。天主教是通过徐州教区沭阳教会传入境内的，光绪三十三年海州设立本堂，法籍董师中为本堂第一任神父。</p>
<p>此后，由于社会不安定以及战争原因，佛教道教寺庙大多毁坏，僧尼、道士大多数还俗；伊斯兰教活动分散，规模不大；天主教徒集中在海州、新浦两地活动；基督教教徒在新浦、海州两处教堂尚有宗教活动。解放后，中国共产党和人民政府实行宗教信仰自由的政策，1953年成立新海连市人民政府宗教事务处。“文化大革命”期间，宗教活动中断。中国共产党十一届三中全会以后，党的宗教政策得到落实，修复寺院和教堂，恢复正常的宗教活动。</p>
<p>1989年，连云港市将宗教事务处改名为民族宗教事务局，随后灌云县、东海县民族宗教事务科改名为民族宗教事务局，均列为政府序列。赣榆县民族宗教事务科仍隶属于中共赣榆县委统战部。新浦、海州、云台、连云4个区均在各区中共统战部增设民族宗教事务局。市、县（区）民族宗教事务管理部门，认真落实党的宗教政策，加强对宗教教职人员和信教群众的教育，提高其爱国主义、社会主义和坚持独立自主、自办教会原则的觉悟，引导宗教界人士为改革开放和社会主义“两个文明”建设服务。</p>
<p>1990年，连云港市有佛教、伊斯兰教、天主教和基督教，信教群众5.5万多人，经批准开放宗教活动场所75处，宗教教职人员75人。宗教界人士选为全国人大代表1人、市人大代表3人、市政协委员7人、县人大代表1人、县区政协委员11人。爱国宗教组织有市基督教“三自”爱国运动委员会、市基督教协会、市天主教爱国会（筹备）、市佛教协会（筹备）、市伊斯兰教协会筹委会。</p>"""

EXPECTED_TEXT = [
    "寺内鹫峰石塔、罗汉墓就是康居国高僧的墓塔",
    "神宗皇帝朱翊钧颁降经敕谕",
    "随赐《大藏经》、佛像等佛物",
    "教会传入境内的",
    "尚有宗教活动",
    "市、县（区）民族宗教事务管理部门",
    "市基督教“三自”爱国运动委员会",
]
RESIDUALS = [
    "鹫蜂石塔",
    "朱翊钩",
    "随赐大藏经》",
    "传人境内的",
    "尚有崇教活动",
    "（区)民族宗教事务",
    "。，“：",
    "基督教三自”爱国运动委员会",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = "\n" + NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"religion overview expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"religion overview residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十七卷宗教 / 概述",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建宗教卷概述，修复明确错识和段尾噪声。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十七卷宗教概述回源修复

- 时间：{now}
- 范围：`第五十七卷宗教 / 概述`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第五十七卷宗教 / 概述`，停止在 `第一章佛教` 前。
- 修正 `鹫峰石塔`、`朱翊钧`、`《大藏经》`、`传入境内`、`尚有宗教活动`、`基督教“三自”爱国运动委员会` 等明确错识。
- 清理概述段尾 `。，“：` 噪声。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。

## 核对说明

- PaddleOCR `page_0257.txt` 确认概述起始至跨页段。
- PaddleOCR `page_0258.txt` 确认概述尾段和 `第一章佛教` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十七卷宗教概述回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十七卷宗教 `概述` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第一章佛教` 前，未触碰后续章节。
- 修正 `鹫峰石塔`、`朱翊钧`、`《大藏经》`、`传入境内`、`尚有宗教活动`、`基督教“三自”爱国运动委员会` 等明确错识，并清理段尾噪声。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_religion_overview_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("religion overview repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
