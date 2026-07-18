# -*- coding: utf-8 -*-
"""Restore museum inscription tail items from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_inscriptions_tail_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_inscriptions_tail_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷馆藏碑刻后段回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0119.txt:5-24"
SCOPE_START = '<p>十一、海州乡贡进士题名记碑'
SCOPE_END = '<h4 id="第五十三卷-第五章馆藏文物-第五节书画">第五节书画</h4>'

NEW_HTML = """<p>十一、海州乡贡进士题名记碑</p>
<p>此碑明成化十一年（1475年）立于海州儒学（今连云港市海州中大街小学院内）。碑高1.77米，宽0.81米；座高0.56米、宽1.20米，圆首。额及边沿饰卷云纹，右下部剥蚀较严重。碑为王概撰文唐震书丹，程洛篆额。</p>
<p>十二、环境保护碑</p>
<p>环境保护碑光绪三十年（1904年）三月立于南城石桥上，是连云港市发现并保存下来的一块具有近代环境保护意义的碑刻。刻碑为花岗片麻岩。高100厘米、宽39厘米、厚9厘米。文竖刻3行，计31字。字径6厘米。正文三行：“公议桥下水道毋准委弃污秽泥士，违者每担罚洋壹元。光绪三十年三月毂旦”。此碑藏于连云港市博物馆。</p>
<p>十三、新浦天后宫记碑</p>
<p>新浦天后宫记碑原立于新浦天后宫（今新浦区政府），现移立于新浦公园湖边。碑为青色石灰岩，连碑座高220厘米、宽90厘米、厚16厘米。文14行，行22字，计583字，楷书，字径3厘米。碑立于民国6年（1917年）10月，新浦商会会长刘振殿撰文，刘允生书。</p>
<p>十四、王得胜“记功”碑</p>
<p>碑在东海县南辰乡西朱范村。碑系用石灰岩加工，有两通，大小同，均高186厘米、宽77厘米、厚30厘米。碑额刻一大圆。</p>
"""

EXPECTED_TEXT = [
    "十一、海州乡贡进士题名记碑",
    "十二、环境保护碑",
    "水道毋准委弃污秽泥士",
    "十三、新浦天后宫记碑",
    "楷书，字径3厘米",
    "民国6年（1917年）10月",
    "刘振殿撰文，刘允生书",
    "十四、王得胜“记功”碑",
]
RESIDUALS = [
    "十一、海州乡贡进士题名记碑此碑",
    "水道准委弃污移泥士",
    "十三、新浦天后宫记碑新浦天后宫记碑",
    "计583字，楷十四、王得胜",
    "碑额刻一大圆。</p>\n<h4 id=\"第五十三卷-第五章馆藏文物-第五节书画\"",
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
        "scope": "第五十三卷文物 / 第五章馆藏文物 / 第四节碑刻 / 十一至十四",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建碑刻后段，停止在第五节书画前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷馆藏碑刻后段回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第五章馆藏文物 / 第四节碑刻 / 十一至十四`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `十一、海州乡贡进士题名记碑` 至 `十四、王得胜“记功”碑`，停止在 `第五节书画` 前。
- 修正 `环境保护碑` 正文中 `毋准委弃污秽泥士`，补回 `新浦天后宫记碑` 的 `楷书`、`字径3厘米`、`民国6年（1917年）10月`、`刘振殿撰文，刘允生书`，拆开 `十三/十四` 粘连。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- `毂旦` 为源页可见用字，本次保留不改。
- 后续 `第五节书画` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷馆藏碑刻后段回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第五章馆藏文物 / 第四节碑刻 / 十一至十四` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第五节书画` 前，未触碰书画条目。
- 修正 `环境保护碑` 正文中 `毋准委弃污秽泥士`，补回 `新浦天后宫记碑` 的 `楷书`、`字径3厘米`、`民国6年（1917年）10月`、`刘振殿撰文，刘允生书`，拆开 `十三/十四` 粘连；保留源页可见用字 `毂旦`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_inscriptions_tail_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum inscriptions tail repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
