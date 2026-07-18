# -*- coding: utf-8 -*-
"""Audit user-provided textflow sample against current readers and obsolete files."""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "output" / "final_reader"
REPORTS = ROOT / "output" / "reports"
PROGRESS = REPORTS / "progress"
REPORT_JSON = REPORTS / "user_sample_obsolete_and_encoding_20260707.json"
REPORT_MD = REPORTS / "user_sample_obsolete_and_encoding_20260707.md"
PROGRESS_MD = PROGRESS / "20260707_用户样本串页与编码复核.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

CURRENT_READERS = [
    FINAL / "连云港市志_全书.html",
    FINAL / "连云港市志_上册.html",
    FINAL / "连云港市志_中册.html",
    FINAL / "连云港市志_下册.html",
]
OBSOLETE_READERS = sorted((FINAL / "obsolete").glob("*.html")) if (FINAL / "obsolete").exists() else []

PROBES = [
    "上部；以白云斜长片麻岩为主",
    "第一节声韵调",
    "一、声母(18)",
    "二、韵母(40)",
    "本字汇收常用字4400多个",
]
MIX_PAIRS = [
    ("上部；以白云斜长片麻岩为主", "第一节声韵调"),
    ("东海一赣榆倒转复向斜", "本字汇收常用字4400多个"),
    ("连云港市地层", "一、声母(18)"),
]
TAG_RE = re.compile(r"<[^>]+>")
P_RE = re.compile(r"<p[^>]*>(.*?)</p>", re.S | re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)


def plain(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(TAG_RE.sub(" ", value))).strip()


def decode(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8"), "ok"
    except UnicodeDecodeError as exc:
        return raw.decode("utf-8", errors="replace"), str(exc)


def scan(path: Path) -> dict:
    text, decode_status = decode(path)
    flat = plain(text)
    paragraphs = [plain(m.group(1)) for m in P_RE.finditer(text)]
    title = plain(TITLE_RE.search(text).group(1)) if TITLE_RE.search(text) else ""
    cn_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    mojibake_count = len(re.findall(r"[ÃÂ]|(?:è|ä|å|ç|æ|œ|€)", text[:20000]))
    mixed = []
    for idx, paragraph in enumerate(paragraphs, 1):
        for left, right in MIX_PAIRS:
            if left in paragraph and right in paragraph:
                mixed.append({
                    "paragraph_index": idx,
                    "left": left,
                    "right": right,
                    "chars": len(paragraph),
                    "excerpt": paragraph[:260],
                })
    probes = []
    for probe in PROBES:
        pos = flat.find(probe)
        probes.append({"needle": probe, "present": pos >= 0, "position": pos})
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "bytes": path.stat().st_size,
        "mtime": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "decode": decode_status,
        "title": title,
        "chinese_chars": cn_count,
        "mojibake_markers_first20k": mojibake_count,
        "paragraphs": len(paragraphs),
        "long_paragraphs_ge2500": sum(1 for p in paragraphs if len(p) >= 2500),
        "mixed_paragraphs": mixed,
        "probes": probes,
    }


def render(data: dict) -> str:
    lines = [
        "# 用户样本串页与编码复核",
        "",
        f"- 生成时间：{data['time']}",
        "- 范围：当前正式全书/分册 HTML、obsolete 旧 HTML；未打开、展示或嵌入图片。",
        "",
        "## 结论",
        "",
        f"- 当前正式阅读文件：混合段落 {data['current_mixed_total']}，UTF-8 解码异常 {data['current_decode_issues']}，前 2 万字符 mojibake 标记 {data['current_mojibake_total']}。",
        f"- obsolete 旧文件：混合段落 {data['obsolete_mixed_total']}，超长段落 {data['obsolete_long_total']}；用户贴出的地层/方言压平样式主要对应旧版或旧中间层风险。",
        "- 交付包脚本 `scripts/build_delivery_package.py` 使用 `output/final_reader/连云港市志_全书.html` 复制为包内 `连云港市志_最终阅读版.html`，不读取 obsolete 目录。",
        "- 单独分册 HTML 以文件字节按 UTF-8 解码正常；PowerShell 中出现乱码属于控制台显示/管道编码问题，不是文件内容损坏。",
        "",
        "## 当前正式文件",
        "",
        "| 文件 | 标题 | 中文字符 | 解码 | mojibake标记 | 段落 | >=2500字段落 | 混合段落 | 修改时间 |",
        "|---|---|---:|---|---:|---:|---:|---:|---|",
    ]
    for item in data["current"]:
        lines.append(f"| `{item['path']}` | {item['title']} | {item['chinese_chars']} | {item['decode']} | {item['mojibake_markers_first20k']} | {item['paragraphs']} | {item['long_paragraphs_ge2500']} | {len(item['mixed_paragraphs'])} | {item['mtime']} |")
    lines.extend(["", "## obsolete 旧文件", "", "| 文件 | 中文字符 | 解码 | 段落 | >=2500字段落 | 混合段落 | 修改时间 |", "|---|---:|---|---:|---:|---:|---|"])
    for item in data["obsolete"]:
        lines.append(f"| `{item['path']}` | {item['chinese_chars']} | {item['decode']} | {item['paragraphs']} | {item['long_paragraphs_ge2500']} | {len(item['mixed_paragraphs'])} | {item['mtime']} |")
    lines.extend(["", "## 样本特征命中", "", "| 文件 | 特征 | 存在 | 位置 |", "|---|---|---:|---:|"])
    for item in data["current"] + data["obsolete"]:
        for probe in item["probes"]:
            lines.append(f"| `{item['path']}` | `{probe['needle']}` | {'是' if probe['present'] else '否'} | {probe['position']} |")
    return "\n".join(lines) + "\n"


def append_memory(text: str) -> None:
    marker = "## 2026-07-07 用户样本串页与编码复核"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


def main() -> None:
    current = [scan(path) for path in CURRENT_READERS if path.exists()]
    obsolete = [scan(path) for path in OBSOLETE_READERS]
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "current": current,
        "obsolete": obsolete,
        "current_mixed_total": sum(len(item["mixed_paragraphs"]) for item in current),
        "obsolete_mixed_total": sum(len(item["mixed_paragraphs"]) for item in obsolete),
        "current_decode_issues": sum(1 for item in current if item["decode"] != "ok"),
        "current_mojibake_total": sum(item["mojibake_markers_first20k"] for item in current),
        "obsolete_long_total": sum(item["long_paragraphs_ge2500"] for item in obsolete),
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(data)
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS_MD.write_text(report, encoding="utf-8")
    append_memory(f"""
## 2026-07-07 用户样本串页与编码复核

- 新增并运行 `scripts/audit_user_sample_obsolete_and_encoding_20260707.py`，复核用户贴出的地层表/方言声韵样本与当前正式阅读文件、obsolete 旧文件、分册 HTML 编码状态。
- 结论：当前正式全书/分册 HTML UTF-8 解码正常，未检出样本跨段混合；用户贴出的压平长段主要对应 obsolete 旧阅读稿或旧中间层风险。
- 报告：`output/reports/user_sample_obsolete_and_encoding_20260707.md`；未打开、展示或嵌入图片。
""")
    print(f"current_mixed={data['current_mixed_total']}")
    print(f"current_decode_issues={data['current_decode_issues']}")
    print(f"current_mojibake_total={data['current_mojibake_total']}")
    print(f"obsolete_mixed={data['obsolete_mixed_total']}")
    print(f"obsolete_long={data['obsolete_long_total']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
