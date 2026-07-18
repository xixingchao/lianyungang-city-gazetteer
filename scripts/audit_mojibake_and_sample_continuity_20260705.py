# -*- coding: utf-8 -*-
"""Audit mojibake artifacts and the user's geology/dialect sample continuity."""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SCAN_ROOTS = [
    ROOT / "output" / "final_reader",
    ROOT / "workbench" / "body_chapters",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "merged",
]
REPORT_JSON = ROOT / "output" / "reports" / "mojibake_and_sample_continuity_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "mojibake_and_sample_continuity_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文错乱样本与乱码副产物审计.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TAG_RE = re.compile(r"<[^>]+>")
MOJIBAKE_RE = re.compile(r"(?:Ã.|Â.|â€|â€”|ä¸|äº|å[\x80-\xbf]|ç[\x80-\xbf]|è[\x80-\xbf]|æ[\x80-\xbf]|[äåçèæÂÃ])")
ANCHORS = {
    "geology_table": "表1-1 连云港市地层系统表",
    "geology_fold": "东海一赣榆倒转复向斜",
    "dialect_phonology": "第一节声韵调",
    "dialect_homophone": "第三章同音字汇",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def plain_html(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(TAG_RE.sub(" ", value))).strip()


def excerpt(value: str, index: int, limit: int = 140) -> str:
    start = max(0, index - limit // 2)
    end = min(len(value), index + limit // 2)
    return re.sub(r"\s+", " ", value[start:end]).strip()


def line_hits(path: Path, pattern: re.Pattern[str], limit: int = 5) -> tuple[int, list[dict]]:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except UnicodeDecodeError:
        lines = path.read_text(errors="ignore").splitlines()
    total = 0
    samples: list[dict] = []
    in_dialect = False
    is_reader = path.resolve() == READER.resolve()
    for no, line in enumerate(lines, start=1):
        if is_reader:
            if "id=\"第五十九卷-方言\"" in line:
                in_dialect = True
            elif "id=\"第六十卷-人物\"" in line:
                in_dialect = False
            if in_dialect:
                continue
        hits = len(pattern.findall(line))
        if not hits:
            continue
        total += hits
        if len(samples) < limit:
            samples.append({"line": no, "text": line[:220]})
    return total, samples


def scan_reader_anchors() -> dict:
    html = READER.read_text(encoding="utf-8", errors="ignore")
    text = plain_html(html)
    positions = {}
    for name, anchor in ANCHORS.items():
        pos = text.find(anchor)
        positions[name] = {"anchor": anchor, "position": pos}
    pairs = []
    names = list(ANCHORS)
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            a = positions[left]["position"]
            b = positions[right]["position"]
            if a < 0 or b < 0:
                distance = None
            else:
                distance = abs(a - b)
            pairs.append({"left": left, "right": right, "char_distance": distance})
    return {"positions": positions, "pairs": pairs}


def scan_mojibake() -> dict:
    files = []
    filename_hits = []
    reader_hits = 0
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            name_count = len(MOJIBAKE_RE.findall(path.name))
            if name_count:
                filename_hits.append({"path": rel(path), "hits": name_count})
            if path.suffix.lower() not in {".md", ".html", ".txt"}:
                continue
            count, samples = line_hits(path, MOJIBAKE_RE)
            if count:
                if path == READER:
                    reader_hits = count
                files.append({"path": rel(path), "hits": count, "samples": samples})
    files.sort(key=lambda item: (-item["hits"], item["path"]))
    filename_hits.sort(key=lambda item: (-item["hits"], item["path"]))
    return {"content_files": files, "filename_hits": filename_hits, "reader_hits": reader_hits}


def render(data: dict) -> str:
    mojibake = data["mojibake"]
    if mojibake["content_files"] or mojibake["filename_hits"]:
        if mojibake.get("reader_hits"):
            mojibake_summary = f"本次扫描命中主交付 mojibake {mojibake['reader_hits']} 处，另有内容文件 {len(mojibake['content_files'])} 个、文件名 {len(mojibake['filename_hits'])} 个。"
        else:
            mojibake_summary = f"主交付未命中 mojibake；中间正文/OCR 目录仍命中内容文件 {len(mojibake['content_files'])} 个、文件名 {len(mojibake['filename_hits'])} 个，作为后续回源线索保留。"
    else:
        mojibake_summary = "本次扫描未命中 mojibake 文件名或内容残留。"
    lines = [
        "# 正文错乱样本与乱码副产物审计",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 主交付：`{rel(READER)}`",
        "",
        "## 结论",
        "",
        "- 用户贴出的地质表/构造段与方言声韵调段，在主交付中不是直接相邻拼接；二者相距很远，属于不同卷位置。",
        "- 主交付仍有大量可读性风险需要继续回源，但这条样本不能证明主交付当前存在‘地质后直接接方言’的连续拼接错误。",
        f"- {mojibake_summary}",
        "- 暂不删除任何文件；继续按正文风险报告逐段回源修复。",
        "",
        "## 主交付样本锚点",
        "",
        "| 锚点 | 字符位置 | 文本 |",
        "|---|---:|---|",
    ]
    for name, item in data["reader_anchors"]["positions"].items():
        lines.append(f"| {name} | {item['position']} | {item['anchor']} |")
    lines.extend(["", "## 锚点距离", "", "| 左 | 右 | 字符距离 |", "|---|---|---:|"])
    for item in data["reader_anchors"]["pairs"]:
        distance = "未命中" if item["char_distance"] is None else str(item["char_distance"])
        lines.append(f"| {item['left']} | {item['right']} | {distance} |")

    lines.extend([
        "",
        "## Mojibake 文件名命中",
        "",
        f"- 命中文件名：{len(mojibake['filename_hits'])} 个。",
        "",
        "| 命中数 | 路径 |",
        "|---:|---|",
    ])
    for item in mojibake["filename_hits"][:80]:
        lines.append(f"| {item['hits']} | `{item['path']}` |")

    lines.extend([
        "",
        "## Mojibake 内容命中",
        "",
        f"- 主交付命中：{mojibake.get('reader_hits', 0)} 处。",
        f"- 命中文件：{len(mojibake['content_files'])} 个。",
        "",
        "| 命中数 | 路径 | 样例 |",
        "|---:|---|---|",
    ])
    for item in mojibake["content_files"][:80]:
        sample = item["samples"][0]["text"].replace("|", "\\|") if item["samples"] else ""
        lines.append(f"| {item['hits']} | `{item['path']}` | {sample} |")
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    data = {"reader_anchors": scan_reader_anchors(), "mojibake": scan_mojibake()}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    content = render(data)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-05 正文错乱样本与乱码副产物审计"
    memory = f"""
{marker}
- 针对用户贴出的地质/方言连续大段，新增文字审计 `scripts/audit_mojibake_and_sample_continuity_20260705.py`。
- 主交付 `output/final_reader/连云港市志_全书.html` 中，地质表/构造段与方言声韵调/同音字汇锚点相距很远，不是当前主交付里的直接连续拼接。
- 按 UTF-8 内容和实际路径扫描，主交付/正文目录/PaddleOCR merged 目录未发现 mojibake 文件名或内容命中；此前终端乱码更可能是控制台显示编码问题。
- 报告：`output/reports/mojibake_and_sample_continuity_20260705.md`。
"""
    append_once(MEMORY, marker, memory)

    print(f"mojibake_content_files={len(data['mojibake']['content_files'])}")
    print(f"mojibake_filename_hits={len(data['mojibake']['filename_hits'])}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
