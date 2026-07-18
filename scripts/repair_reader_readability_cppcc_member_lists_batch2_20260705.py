# -*- coding: utf-8 -*-
"""Restore compressed CPPCC member list appendices 42-11 to 42-14."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SOURCE = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_cppcc_member_lists_batch2_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_cppcc_member_lists_batch2_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_市政协委员名单附录第二批版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

BLOCKS = [
    {"title": "附42-11：市政协第四届委员会组成人员名单", "end": "会议号召全市各界人民在党的领导下", "marker": "会议号召全市各界人民在党的领导下"},
    {"title": "附42－12：市政协第五届委员会组成人员名单", "end": "会议决议指出，为把连云港市建设成为工业海港城市", "marker": "会议决议指出，为把连云港市建设成为工业海港城市"},
    {"title": "附42－13：市政协第六届委员会组成人员名单", "end": "会议决议指出，三年来全市政治、经济形势发生显著变化", "marker": "会议决议指出，三年来全市政治、经济形势发生显著变化"},
    {"title": "附42-14：市政协第七届委员会组成人员名单", "end": "会议决议指出，在社会主义初级阶段，人民政协肩负着重要任务", "marker": "会议决议指出，在社会主义初级阶段，人民政协肩负着重要任务"},
]

SPLITS = {
    "<p>二、主要工作组织委员学习。": "<h5>二、主要工作</h5>\n<p>组织委员学习。",
    "<p>二、主要工作市五届政协对": "<h5>二、主要工作</h5>\n<p>市五届政协对",
    "<p>二、主要工作组织学习。": "<h5>二、主要工作</h5>\n<p>组织学习。",
    "<p>二、主要工作学中把": "<h5>二、主要工作</h5>\n<p>学中把",
}

ROLE_PREFIXES = ("主席", "副主席", "秘书长", "常务委员")
RESIDUALS = [
    "附42-11：市政协第四届委员会组成人员名单主席",
    "戴崇松会议号召全市各界人民",
    "附42－12：市政协第五届委员会组成人员名单主席",
    "魏伯衡会议决议指出，为把连云港市建设",
    "附42－13：市政协第六届委员会组成人员名单主席",
    "熊正文会议决议指出，三年来全市政治",
    "附42-14：市政协第七届委员会组成人员名单主席",
    "魏宗荣会议决议指出，在社会主义初级阶段",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def source_list(title: str, end_text: str) -> list[str]:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    start = lines.index(title)
    out: list[str] = []
    for raw in lines[start:]:
        line = raw.strip()
        if not line or line.startswith("<!--"):
            continue
        if line.startswith(end_text):
            break
        out.append(line)
    return out


def render(lines: list[str]) -> str:
    out = [f"<h4>{html.escape(lines[0])}</h4>"]
    in_list = False
    for line in lines[1:]:
        if "：" in line and line.split("：", 1)[0] in ROLE_PREFIXES:
            if in_list:
                out.append("</ul>")
                in_list = False
            role, rest = line.split("：", 1)
            out.append(f"<p><strong>{html.escape(role + '：' + rest)}</strong></p>")
            continue
        if not in_list:
            out.append('<ul class="reader-restored-list">')
            in_list = True
        out.append(f"<li>{html.escape(line)}</li>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def replace_appendix(text: str, title: str, end_text: str, marker: str) -> tuple[str, int]:
    needle = f"<p>{title}"
    if needle not in text:
        return text, 0
    start = text.index(needle)
    marker_pos = text.index(marker, start)
    para_end = text.index("</p>", marker_pos) + len("</p>")
    suffix = text[marker_pos:para_end - len("</p>")]
    new_block = render(source_list(title, end_text)) + "\n" + f"<p>{html.escape(suffix)}</p>"
    return text[:start] + new_block + text[para_end:], 1


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for block in BLOCKS:
        text, count = replace_appendix(text, block["title"], block["end"], block["marker"])
        changed += count
    for old, new in SPLITS.items():
        if old in text:
            text = text.replace(old, new, 1)
            changed += 1
    empty_list = '<ul class="reader-restored-list">\n</ul>\n'
    empty_count = text.count(empty_list)
    if empty_count:
        text = text.replace(empty_list, "")
        changed += empty_count
    for residue in RESIDUALS:
        if residue in text:
            raise RuntimeError(f"compressed CPPCC residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十二卷政务：市政协第四至第七届委员会组成人员名单",
        "replacement_count": changed,
        "source_evidence": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33882-33894",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33958-33986",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:34035-34071",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:34197-34229",
        ],
        "notes": ["名单按源 Markdown 行边界恢复；会议正文保留最终阅读版现有文字；复跑时清理空列表。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 市政协委员名单附录第二批版式修复

- 时间：{now}
- 范围：第四十二卷政务，第十二章第四至第七节。
- 本次替换或清理压缩块：{changed} 处。

## 修复

- 将 `附42-11`、`附42-12`、`附42-13`、`附42-14` 的政协委员名单恢复为附录标题、职务行和名单列表。
- 将名单后被粘连的会议决议正文恢复为独立段落。
- 将第四、第五、第六、第七届中的 `二、主要工作` 恢复为独立小节标题。
- 清理首次复原产生的空 `reader-restored-list`。
- 正文段保留最终阅读版现有文字，不用源 OCR 整段覆盖。

## 暂缓

- 源文中 `魏伯衡）`、`张名丽（女）张荣山张`、`七届-次`、`深人` 等疑似 OCR 问题，本批不猜修。

## 依据

- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33882-33894`
- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33958-33986`
- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:34035-34071`
- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:34197-34229`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 市政协委员名单附录第二批版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十二卷政务第十二章 `附42-11` 至 `附42-14` 市政协委员名单在最终阅读版中被压入会议决议正文的问题。
- 按源 Markdown 行边界恢复附录标题、职务行和 `reader-restored-list` 名单，并恢复 `二、主要工作` 小节标题。
- 正文段保留最终阅读版现有文字；源文疑似 OCR 错字不猜修。
- 报告：`output/reports/reader_readability_cppcc_member_lists_batch2_20260705.md`。
""",
    )
    print(f"replacement_count={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
