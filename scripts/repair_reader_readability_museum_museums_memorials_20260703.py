# -*- coding: utf-8 -*-
"""Restore museums and memorials section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_museums_memorials_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_museums_memorials_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷博物馆纪念馆回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0124.txt:11-38"
SCOPE_START = '<h4 id="第五十三卷-第六章文物管理与保护-第四节博物馆 纪念馆">第四节博物馆 纪念馆</h4>'
SCOPE_END = '<h2 id="第五十四卷-报刊广播-电视">第五十四卷报刊广播电视</h2>'

NEW_HTML = """<h4 id="第五十三卷-第六章文物管理与保护-第四节博物馆 纪念馆">第四节博物馆 纪念馆</h4>
<p>一、博物馆</p>
<p>连云港市博物馆位于连云港市新浦区苍梧路，占地47亩，建筑面积2200平方米，其中陈列面积1500平方米，库房400平方米，讲演厅300平方米，建筑风格为仿古园林式。</p>
<p>市博物馆的前身是建于1958年的市地志文物陈列室，原在海州大慈寺，1973年5月8日经市革命委员会批准改建而成。几经搬迁，于1983年迁到现址。后投资10万元，于1987年建成新馆，定编30人，在编人员中大专以上文化程度18人，负责挖掘、考古、保管、修复、陈列、巡展、学术研究等工作。</p>
<p>馆内藏品总数有1万多件，其中以汉代墓葬出土文物较多。</p>
<p>灌云县博物馆建于1985年6月25日，属县文化局领导，馆址在灌云县大伊山镇。有办公室18平方米，陈列室120平方米，馆藏文物3500多件，工作人员4人，其中大专文化程度3人，有馆员职称2人，分考古征集、保管、陈列三组。</p>
<p>东海县博物馆始建于1987年12月31日，属县文化局领导，和县图书馆合署办公。有馆藏文物1273件。</p>
<p>赣榆县博物馆1987年12月30日成立，属县文化局领导，编制3人，馆藏文物500多件，馆址设于县影剧院内。平时主要开展文物的调查、征集、保管和研究工作，陈列、展览工作尚未正式开展。</p>
<p>二、纪念馆</p>
<p>连云港市革命纪念馆位于市新浦区民主中路201号，原名陇海公寓，为民国14年（1925年）建造的宾馆。民国27年上半年，中共中央长江局巡视员张文海、谷牧曾住于此，开展友军工作，在国民革命军第五十七军第一一二师内建立了中共地下工作委员会，并在陇海公寓发展第六六七团团长万毅为中共特别党员。1987年6月6日，中共连云港市委、市人民政府决定将陇海公寓改建为市革命纪念馆，作为陈列、收藏革命斗争史和建设成就史资料的纪念设施。1990年有工作人员6人，隶属于市委党史工作委员会领导。该馆已被列为市文物保护单位。</p>
<p>该馆建筑为前亭后井，前亭为两层小楼，后井为生活用房，占地250平方米，建筑面积为420平方米。馆内设“全国党史”、“地方革命史”、“建国后成就”、“海州建党”、“保卫连云港”、“盐场春秋”、“港口风云”等展览室及碑廊，展出照片、图片528幅，实物127件、各种模型40个、碑刻32块。</p>
"""

EXPECTED_TEXT = [
    "一、博物馆</p>",
    "馆内藏品总数有1万多件",
    "灌云县博物馆建于1985年6月25日",
    "二、纪念馆</p>",
    "民国14年（1925年）建造的宾馆",
    "实物127件、各种模型40个、碑刻32块",
]
RESIDUALS = [
    "一、博物馆连云港市博物馆",
    "1方多件",
    "建于.1985年",
    "二、纪念馆连云港市革命纪念馆",
    "民国14年（1925年)建造",
    "曾住于此,开展友军工作",
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
        "scope": "第五十三卷文物 / 第六章文物管理与保护 / 第四节博物馆 纪念馆",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建博物馆、纪念馆小节，停止在第五十四卷前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷博物馆纪念馆回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第六章文物管理与保护 / 第四节博物馆 纪念馆`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第四节博物馆 纪念馆`，停止在 `第五十四卷报刊广播电视` 前。
- 拆开 `一、博物馆`、`二、纪念馆` 与正文粘连。
- 修正 `馆内藏品总数有1方多件` 为 `馆内藏品总数有1万多件`，修正 `灌云县博物馆建于.1985年6月25日` 为 `灌云县博物馆建于1985年6月25日`。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `前亭后井` 为源页可见用字，本次保留不改。
- 后续 `第五十四卷报刊广播电视` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷博物馆纪念馆回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第六章文物管理与保护 / 第四节博物馆 纪念馆` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第五十四卷报刊广播电视` 前，未触碰后续报刊广播电视卷正文。
- 拆开 `一、博物馆`、`二、纪念馆` 与正文粘连，修正 `馆内藏品总数有1万多件`、`灌云县博物馆建于1985年6月25日` 等源页明确内容；保留源页用字 `前亭后井`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_museums_memorials_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
