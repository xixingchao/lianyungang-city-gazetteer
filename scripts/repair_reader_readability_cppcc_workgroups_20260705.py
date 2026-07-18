# -*- coding: utf-8 -*-
"""Restore compressed CPPCC workgroup appendix 42-15."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SOURCE = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_cppcc_workgroups_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_cppcc_workgroups_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_市政协工作组名单附录版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TITLE = "附42-15：政协第五至七届委员会经济科技委员会及各工作组领导成员名单"
END = "四、文史资料委员会"
HTML_START = f"<p>{TITLE}"
HTML_END = "<p>四、文史资料委员会"
GROUP_HEADS = (
    "第五届",
    "第六届一次全会后",
    "第六届二次全会后",
    "第六届三次全会后",
    "第六届四次全会后",
    "第七届一次全会后",
    "第七届二次全会后至1990年底",
)
RESIDUALS = [
    "附42-15：政协第五至七届委员会经济科技委员会及各工作组领导成员名单第五届",
    "李云汉王子俊第六届二次全会后",
    "第六届四次全会后经济工作组委员会主任",
    "委员：王玉本王福启四、文史资料委员会",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def source_lines() -> list[str]:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    start = lines.index(TITLE)
    end = lines.index(END, start)
    return [line.strip() for line in lines[start:end] if line.strip() and not line.startswith("<!--")]


def render(lines: list[str]) -> str:
    out = [f"<h4>{html.escape(lines[0])}</h4>"]
    in_list = False
    for line in lines[1:]:
        if line in GROUP_HEADS:
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h5>{html.escape(line)}</h5>")
            continue
        if not in_list:
            out.append('<ul class="reader-restored-list">')
            in_list = True
        out.append(f"<li>{html.escape(line)}</li>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(HTML_START)
    if HTML_END in text[start:]:
        end = text.index(HTML_END, start)
        tail_prefix = ""
    else:
        end = text.index(END, start)
        tail_prefix = "<p>"
    replacement = render(source_lines()) + "\n" + tail_prefix
    changed = int(text[start:end] != replacement)
    if changed:
        text = text[:start] + replacement + text[end:]
    for residue in RESIDUALS:
        if residue in text:
            raise RuntimeError(f"compressed workgroup residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十二卷政务：附42-15 市政协经济科技委员会及各工作组领导成员名单",
        "html_scope_rewritten": changed,
        "source_evidence": ["workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:34328-34480"],
        "notes": ["按源 Markdown 行边界恢复分组和列表；未解析为表格，疑似 OCR 字词不猜修。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 市政协工作组名单附录版式修复

- 时间：{now}
- 范围：第四十二卷政务，第十二章第八节，附42-15。
- 本次重写 HTML 范围：{changed} 处。

## 修复

- 将 `附42-15` 从压缩长段恢复为附录标题、届次/全会分组标题和名单列表。
- 将被粘入名单末尾的 `四、文史资料委员会` 恢复为后续正文入口。
- 按源 Markdown 行边界恢复，不解析为复杂表格，不猜切姓名。

## 暂缓

- 源文中的 `邮华民`、`袁塗史善五`、`民族宗教工作组组长：刘 / 逸`、`李 / 王福元` 等疑似 OCR 问题，本批照录。
- `附42-16` 也存在压缩，将另批处理。

## 依据

- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:34328-34480`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 市政协工作组名单附录版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十二卷政务第十二章第八节 `附42-15` 市政协经济科技委员会及各工作组领导成员名单在最终阅读版中被压成长段的问题。
- 按源 Markdown 行边界恢复附录标题、届次/全会分组标题和 `reader-restored-list` 名单。
- 源文疑似 OCR 错字照录；`附42-16` 另批处理。
- 报告：`output/reports/reader_readability_cppcc_workgroups_20260705.md`。
""",
    )
    print(f"html_scope_rewritten={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
