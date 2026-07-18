# -*- coding: utf-8 -*-
"""Restore appendix representative lists from line-preserved source."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SOURCE = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
SOURCE_ALL = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_people_congress_representative_lists_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_people_congress_representative_lists_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_人大代表名单附录版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

START_TITLE = "附42-6：连云港市出席全国人民代表大会代表名单"
NEXT_HEADING = '<h3 id="第四十二卷-第十一章区、县各界人民代表会议、人民代表大会">'
RESIDUALS = [
    "名单一、连云港市出席第六届全国人大会议代表",
    "代表徐守盛金叶汝春甘黎明（女）赵金香(女)：1820：",
    "名单一、连云港市出席江苏省六届人大会议代表万玉绪刘士花",
    "张连珍</p>",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def source_block() -> list[str]:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    start = lines.index(START_TITLE)
    end = next(i for i, line in enumerate(lines[start:], start) if line.startswith("区、县各界人民代表会议"))
    return lines[start:end]


def parse_appendices(lines: list[str]) -> list[dict[str, object]]:
    appendices: list[dict[str, object]] = []
    current_app: dict[str, object] | None = None
    current_section: dict[str, object] | None = None
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("<!--") or line == "：1820：":
            continue
        if line.startswith("附42"):
            current_app = {"title": line, "sections": []}
            appendices.append(current_app)
            current_section = None
            continue
        if line[:2] in {"一、", "二、", "三、"}:
            if current_app is None:
                raise RuntimeError(f"section without appendix: {line}")
            current_section = {"title": line, "items": []}
            current_app["sections"].append(current_section)  # type: ignore[index, union-attr]
            continue
        if current_section is None:
            raise RuntimeError(f"item without section: {line}")
        current_section["items"].append(line)  # type: ignore[index]
    return appendices


def render(appendices: list[dict[str, object]]) -> list[str]:
    out: list[str] = []
    for appendix in appendices:
        out.append(f"<h4>{html.escape(str(appendix['title']))}</h4>")
        for section in appendix["sections"]:  # type: ignore[index]
            out.append(f"<h5>{html.escape(str(section['title']))}</h5>")
            out.append('<ul class="reader-restored-list">')
            for item in section["items"]:  # type: ignore[index]
                out.append(f"<li>{html.escape(str(item))}</li>")
            out.append("</ul>")
    return out


def patch_html(new_lines: list[str]) -> int:
    lines = HTML.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(f"<p>{START_TITLE}"))
    end = next(i for i, line in enumerate(lines[start:], start) if line.startswith(NEXT_HEADING))
    changed = int(lines[start:end] != new_lines)
    if changed:
        HTML.write_text("\n".join(lines[:start] + new_lines + lines[end:]) + "\n", encoding="utf-8")
    scope = "\n".join(HTML.read_text(encoding="utf-8").splitlines()[start : start + len(new_lines) + 2])
    for residue in RESIDUALS:
        if residue in scope:
            raise RuntimeError(f"linearized appendix residue remains: {residue}")
    return changed


def main() -> None:
    appendices = parse_appendices(source_block())
    new_lines = render(appendices)
    changed = patch_html(new_lines)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    counts = {str(app["title"]): sum(len(sec["items"]) for sec in app["sections"]) for app in appendices}  # type: ignore[index]
    payload = {
        "time": now,
        "scope": "第四十二卷政务：附42-6、附42-7 人大代表名单",
        "html_scope_rewritten": changed,
        "appendix_item_counts": counts,
        "source_evidence": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33296-33492",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md:91521-91717",
        ],
        "notes": [
            "按源 Markdown 行边界恢复标题、届次和名单；源行中多人连写者照录为一个列表项，不猜切姓名。",
            "移除夹在两附录之间的页码残留 `：1820：`。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 人大代表名单附录版式修复

- 时间：{now}
- 范围：第四十二卷政务，附42-6、附42-7。
- 本次重写 HTML 范围：{changed} 处。

## 修复

- 将两个被压成超长段落的人大代表名单附录恢复为附录标题、届次标题和名单列表。
- 按源 Markdown 行边界处理名单；源行中多人连写者照录为一个列表项，不猜切姓名。
- 移除两附录之间误入正文的页码残留 `：1820：`。

## 统计

- 附42-6 列表项：{counts.get(START_TITLE, 0)}
- 附42-7 列表项：{counts.get('附42－7：连云港市出席江苏省人民代表大会名单', 0)}

## 依据

- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33296-33492`
- `workbench/body_chapters/连云港市志_全书_正文汇总.md:91521-91717`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 人大代表名单附录版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十二卷政务 `附42-6`、`附42-7` 在最终阅读版中被压成长段的问题，恢复为附录标题、届次标题和 `reader-restored-list` 名单。
- 名单边界以 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33296-33492` 为准；源行多人连写处照录，不猜切姓名。
- 移除两附录之间误入正文的页码残留 `：1820：`。
- 报告：`output/reports/reader_readability_people_congress_representative_lists_20260705.md`。
""",
    )
    print(f"html_scope_rewritten={changed}")
    print(f"appendix_item_counts={counts}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
