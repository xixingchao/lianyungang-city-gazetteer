# -*- coding: utf-8 -*-
"""Restore broadcast program setting sections 4-5 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_broadcast_programs_04_05_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_broadcast_programs_04_05_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷广播节目设置四至五回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0151.txt:5-18"
SCOPE_START = '<p>四、服务性节目'
SCOPE_END = '<p>频率1350千赫波长222.2米1987年9月13日起执行第一次播音：</p>'

NEW_HTML = """<p>四、服务性节目</p>
<p>1983年，服务性节目有“节目预告”、“天气预报”、“影剧之窗”、“广播体操”、“广告”等。1990年，服务性节目共4个。每年的广告费净收入，从1983年的1.5万元增至1990年的11万元。</p>
<p>五、三县有线广播节目设置</p>
<p>1978年后，赣榆人民广播站每天播出时间7小时15分，自办节目时间3小时30分，其中文字节目1小时30分。1990年自办节目有“新闻”、“今日赣榆”、“农村”、“科技”、“赣榆是个好地方”、“青少年之友”、“为您服务”、“文艺”等栏目。</p>
<p>东海人民广播站成立时，自办节目有“东海新闻”、“贫下中农、工人阶级上广播”、“文艺”等。1987年以后，自办节目有“东海新闻”、“简明新闻”、“农村”、“文海艺林”、“科技与生活”、“青年之友”、“广告与信息”、“文艺信箱”、“每周一歌”等。</p>
<p>灌云人民广播站成立时，办有“新闻”、“文艺”、“天气预报”等节目。1985年自办节目有“灌云新闻”、“灌云生活”、“学习”、“为您服务”、“科普讲座”、“简明新闻”、“卫生与健康”、“音乐”、“地方戏曲”、“报刊集锦”、“文艺”、“天气预报”等。</p>

"""

EXPECTED_TEXT = [
    "<p>四、服务性节目</p>",
    "服务性节目有“节目预告”、“天气预报”、“影剧之窗”、“广播体操”、“广告”等",
    "<p>五、三县有线广播节目设置</p>",
    "“新闻”、“今日赣榆”、“农村”、“科技”、“赣榆是个好地方”",
    "“文海艺林”、“科技与生活”",
    "“新闻”、“文艺”、“天气预报”等节目",
    "“科普讲座”、“简明新闻”、“卫生与健康”",
]
RESIDUALS = [
    "四、服务性节目1983年",
    "五、三县有线广播节目设置1978年后",
    "有“新闻”“今日赣榆”",
    "“文海艺林”“科技与生活”",
    "“文艺”“天气预报”",
    "“科普讲座”“简明新闻”",
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
    return changed, {"rewrote_scope": changed, "program_sections_restored": 2}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第三章广播 / 第三节广播节目设置 / 四至五",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建广播节目设置四至五，停止在附54-1节目时间表前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十四卷广播节目设置四至五回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：拆出 `四、服务性节目`、`五、三县有线广播节目设置` 标题，补正赣榆、东海、灌云栏目之间缺失的顿号和引号分隔。",
            "- 边界：未处理后续 `附54-1` 节目时间表；该段需按节目时间表另行重排。",
            "",
        ]),
        encoding="utf-8",
    )
    progress = f"""
# 第五十四卷广播节目设置四至五回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第三章广播 / 第三节广播节目设置 / 四至五`，停止在 `附54-1` 节目时间表前。
- 修复内容：拆分服务性节目和三县节目设置标题；按源文补正“新闻”、“今日赣榆”等栏目顿号，补正“文海艺林”、“科技与生活”以及灌云“文艺”、“天气预报”、“科普讲座”、“简明新闻”等黏连。
- 报告：`output/reports/reader_readability_broadcast_programs_04_05_20260703.md`。
"""
    PROGRESS.write_text(progress.strip() + "\n", encoding="utf-8")
    memory = f"""
## 2026-07-03 第五十四卷广播节目设置四至五回源修复

- 对第五十四卷报刊广播电视 `第三章广播 / 第三节广播节目设置 / 四至五` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `附54-1` 节目时间表前。
- 修正 `四、服务性节目1983年`、`五、三县有线广播节目设置1978年后` 标题正文黏连，以及赣榆、东海、灌云栏目名之间顿号和引号缺失。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_broadcast_programs_04_05_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十四卷广播节目设置四至五回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
