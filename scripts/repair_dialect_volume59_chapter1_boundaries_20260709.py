# -*- coding: utf-8 -*-
"""Repair small heading/number boundaries in Volume 59 chapter 1."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "dialect_volume59_chapter1_boundaries_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "dialect_volume59_chapter1_boundaries_20260709.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言第一章小标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

START = '<h3 id="第五十九卷-第一章方言差别">第一章方言差别</h3>'
END = '<h3 id="第五十九卷-第二章语音系统">第二章语音系统</h3>'
REPLACEMENTS = [
    (
        '<p>一、声母1.f、xu的分混。在青泉小片和牛山、房山、张湾等乡镇f、xu不混。海伊小片的大部分地区是 xu混入f,但灌云东南一线是f混入xu。例如：</p>',
        '<h5>一、声母</h5>\n<p>1.f、xu的分混。在青泉小片和牛山、房山、张湾等乡镇f、xu不混。海伊小片的大部分地区是 xu混入f,但灌云东南一线是f混入xu。例如：</p>',
        '一、声母',
    ),
    (
        '<p>二、韵母1. 果摄一等见系开口、合口字的今韵母，在青泉小片及方言的过渡带一般不混，开合分明，“饿”字例外；在海伊小片则是开口字混入合口字中。例如：</p>',
        '<h5>二、韵母</h5>\n<p>1. 果摄一等见系开口、合口字的今韵母，在青泉小片及方言的过渡带一般不混，开合分明，“饿”字例外；在海伊小片则是开口字混入合口字中。例如：</p>',
        '二、韵母',
    ),
    (
        '<p>三、声调1. 阴平。图河、燕尾一线是低降调；市内其他地方则是降升调，除靠近山东省的少数村庄之外，人们念阴平字时喉头有发紧的感觉，特别是海伊小片的方音。阴平字在赣榆北部的调值是214,在赣榆南部及东海县的西北部一般是213,在海伊小片多数是313。</p>',
        '<h5>三、声调</h5>\n<p>1. 阴平。图河、燕尾一线是低降调；市内其他地方则是降升调，除靠近山东省的少数村庄之外，人们念阴平字时喉头有发紧的感觉，特别是海伊小片的方音。阴平字在赣榆北部的调值是214,在赣榆南部及东海县的西北部一般是213,在海伊小片多数是313。</p>',
        '三、声调',
    ),
]


def patch() -> dict[str, object]:
    html = HTML.read_text(encoding="utf-8")
    start = html.index(START)
    end = html.index(END, start)
    section = html[start:end]
    changed_labels = []
    missing_labels = []
    new_section = section
    for old, new, label in REPLACEMENTS:
        if old in new_section:
            new_section = new_section.replace(old, new, 1)
            changed_labels.append(label)
        elif new in new_section:
            continue
        else:
            missing_labels.append(label)
    if missing_labels:
        raise RuntimeError(f"Cannot locate boundary paragraphs: {missing_labels}")
    changed = new_section != section
    if changed:
        HTML.write_text(html[:start] + new_section + html[end:], encoding="utf-8")
    return {"changed": changed, "changed_labels": changed_labels, "missing_labels": missing_labels}


def write_reports(result: dict[str, object]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十九卷方言 / 第一章方言差别 / 第一节语音差别",
        "reader_path": str(HTML),
        "principle": "仅拆分小标题与首个编号的边界，不改写正文内容。",
        "result": result,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第五十九卷方言第一章小标题边界修复

- 时间：{now}
- 范围：`第五十九卷方言 / 第一章方言差别 / 第一节语音差别`

## 修复动作

- 将 `一、声母1.` 拆为 `<h5>一、声母</h5>` 与 `1.` 正文段。
- 将 `二、韵母1.` 拆为 `<h5>二、韵母</h5>` 与 `1.` 正文段。
- 将 `三、声调1.` 拆为 `<h5>三、声调</h5>` 与 `1.` 正文段。
- 不改写原文字词、音标和例字内容。

## 结果

- 阅读版发生改写：{result['changed']}
- 已处理：{', '.join(result['changed_labels']) if result['changed_labels'] else '此前已处理'}
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(result: dict[str, object]) -> None:
    marker = "## 2026-07-09 第五十九卷方言第一章小标题边界修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 修复第五十九卷方言第一章第一节 3 处小标题与编号粘连：`一、声母1.`、`二、韵母1.`、`三、声调1.`。
- 只恢复标题边界，不改写正文、音标和例字。
- 报告：`output/reports/dialect_volume59_chapter1_boundaries_20260709.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = patch()
    write_reports(result)
    update_memory(result)
    print("dialect chapter1 boundaries repaired")
    print(f"changed={int(result['changed'])}")
    print(f"labels={','.join(result['changed_labels'])}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
