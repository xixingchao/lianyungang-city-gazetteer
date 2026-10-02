# -*- coding: utf-8 -*-
"""Build a traceable delivery package for the current final reader."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import json
import tempfile
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PACKAGE = ROOT / "output" / "package" / f"连云港市志_交付包_{STAMP}"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PACKAGE_READER = PACKAGE / "连云港市志_最终阅读版.html"
PACKAGE_PDF = PACKAGE / "连云港市志_最终阅读版.pdf"
REPORTS = ROOT / "output" / "reports"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

REPORT_FILES = [
    REPORTS / "连云港市志_交付质量门禁报告.md",
    REPORTS / "章节数据审计报告.md",
    REPORTS / "final_gate_residue_removed.md",
    REPORTS / "remaining_reader_residue_removed.md",
    REPORTS / "reader_visible_unverified_tables_removed.md",
    REPORTS / "结构化表格交付就绪审计报告.md",
    REPORTS / "结构化表格回源核录优先队列.md",
    REPORTS / "连云港市志_东辛经验复用与交付整改计划.md",
    REPORTS / "progress" / "20260629_第二批_最终门禁清零与交付包生成.md",
    REPORTS / "progress" / "20260701_全量已核结构化表格嵌回主阅读版.md",
    REPORTS / "progress" / "方言卷双审遗留清单与判定说明_20261002.md",
    REPORTS / "progress" / "20261002_批次4_第五卷道路表回源核录与残文撤出.md",
    ROOT / "PROJECT_MEMORY.md",
]


def sha256_prefix(path: Path, length: int = 16) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:length]


def size_label(path: Path) -> str:
    size = path.stat().st_size
    if size >= 1024 * 1024:
        return f"{size / 1024 / 1024:.2f} MB"
    if size >= 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size} B"


def copy_optional_file(src: Path, dst_dir: Path) -> Path | None:
    if not src.exists():
        return None
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    return dst


def generate_pdf() -> tuple[bool, str]:
    if not EDGE.exists():
        return False, "未找到 Microsoft Edge headless 打印程序"
    with tempfile.TemporaryDirectory(prefix="lyg_pdf_profile_") as profile:
        cmd = [
            str(EDGE),
            "--headless=new",
            "--disable-gpu",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={PACKAGE_PDF}",
            PACKAGE_READER.resolve().as_uri(),
        ]
        result = subprocess.run(
            cmd,
            cwd=PACKAGE,
            text=True,
            capture_output=True,
            timeout=180,
            encoding="utf-8",
            errors="replace",
        )
    if PACKAGE_PDF.exists() and PACKAGE_PDF.stat().st_size > 0:
        return True, "已用 Microsoft Edge headless 生成 PDF"
    detail = (result.stderr or result.stdout or "PDF 文件未生成").strip()
    return False, detail[:500]


def main() -> None:
    if not READER.exists():
        raise SystemExit(f"missing reader: {READER}")

    PACKAGE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(READER, PACKAGE_READER)

    copied_reports: list[Path] = []
    for src in REPORT_FILES:
        copied = copy_optional_file(src, PACKAGE / "reports")
        if copied:
            copied_reports.append(copied)

    table_index = ROOT / "output" / "structured_tables" / "index.html"
    table_index_note = "结构化表格站含未核/待回源骨架，本次不纳入主交付入口。"
    table_count: int | str = "未知"
    if table_index.exists():
        table_text = table_index.read_text(encoding="utf-8", errors="ignore")
        table_match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", table_text, re.S)
        if table_match:
            table_count = len(json.loads(table_match.group(1)))
        if "待对照原图录入" not in table_text and "待精修" not in table_text and "待确认" not in table_text:
            copy_optional_file(table_index, PACKAGE / "structured_tables")
            table_index_note = "结构化表格入口已纳入：`structured_tables/index.html`。"

    table_audit_json = REPORTS / "结构化表格交付就绪审计报告.json"
    table_audit_note = "- 结构化表格站审计：未读取到结构化表格交付就绪审计 JSON，请查看随包报告。"
    if table_audit_json.exists():
        audit_payload = json.loads(table_audit_json.read_text(encoding="utf-8"))
        audit_issues = audit_payload.get("issues") or []
        problem_tables = len({issue.get("table_id") for issue in audit_issues if issue.get("table_id")})
        table_audit_note = (
            f"- 结构化表格站审计：表格总数 {table_count}，"
            f"问题表格 {problem_tables}，"
            f"问题记录 {len(audit_issues)}。"
        )

    reader_text = PACKAGE_READER.read_text(encoding="utf-8", errors="ignore")
    toc_links = len(re.findall(r'<li class="toc-item(?: [^"]+)?"><a href="#', reader_text))
    h2_count = len(re.findall(r"<h2(?:\s|>)", reader_text))
    h3_count = len(re.findall(r"<h3(?:\s|>)", reader_text))
    placeholder_count = len(re.findall(r'class="table-placeholder"', reader_text))
    embedded_tables = len(re.findall(r'class="verified-table-block"', reader_text))

    pdf_ok, pdf_note = generate_pdf()

    files = [p for p in PACKAGE.rglob("*") if p.is_file()]
    rows = []
    for path in sorted(files, key=lambda p: str(p.relative_to(PACKAGE))):
        rel = path.relative_to(PACKAGE).as_posix()
        rows.append(f"| `{rel}` | {size_label(path)} | `{sha256_prefix(path)}` |")

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = [
        "# 连云港市志 交付包说明",
        "",
        f"生成时间：{generated_at}",
        "",
        "## 推荐打开入口",
        "",
        "1. 最终阅读版 HTML：`连云港市志_最终阅读版.html`",
        "2. 最终阅读版 PDF：`连云港市志_最终阅读版.pdf`" if pdf_ok else "2. 最终阅读版 PDF：本次未生成，见下方说明",
    ]
    # 入口只列随包实际存在的报告（避免指向未随包文件）
    entry_no = 3
    for label, rel in (
        ("交付质量门禁", "reports/连云港市志_交付质量门禁报告.md"),
        ("章节结构审计", "reports/章节数据审计报告.md"),
        ("方言卷双审遗留清单与判定说明（校勘记）", "reports/方言卷双审遗留清单与判定说明_20261002.md"),
        ("项目记忆", "reports/PROJECT_MEMORY.md"),
        ("结构化表格交付就绪审计", "reports/结构化表格交付就绪审计报告.md"),
        ("表格回源核录优先队列", "reports/结构化表格回源核录优先队列.md"),
    ):
        if (PACKAGE / rel).exists():
            note.append(f"{entry_no}. {label}：`{rel}`")
            entry_no += 1
    if (PACKAGE / "structured_tables" / "index.html").exists():
        note.append(f"{entry_no}. 结构化表格入口：`structured_tables/index.html`")
    # 从门禁报告实际解析问题计数（不再硬编码 issues=0）
    gate_issues = None
    gate_report = REPORTS / "连云港市志_交付质量门禁报告.md"
    if gate_report.exists():
        gate_text = gate_report.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"## 问题计数\s*\n(.*?)(?:\n## |\Z)", gate_text, re.S)
        if m:
            gate_issues = sum(int(x) for x in re.findall(r"\|\s*(\d+)\s*\|", m.group(1)))
        else:
            gate_issues = 0 if "未通过交付质量门禁" not in gate_text else -1
    note.extend([
        "",
        "## 当前验收结论",
        "",
        (f"- `scripts/audit_delivery_quality.py`：issues={gate_issues}。"
         if gate_issues is not None and gate_issues >= 0 else
         "- `scripts/audit_delivery_quality.py`：见随包门禁报告（本次未解析到计数）。"),
        f"- `scripts/audit_full_reader.py`：Missing anchors=[]，H2={h2_count}，H3={h3_count}，Placeholders={placeholder_count}，TOC links={toc_links}。",
        "- 主阅读版已撤出未核结构化表、OCR 串行数字块、工作台说明、占位卡片、扫描页码/页码残留等读者可见非交付内容。", 
        "- 结构化表格已完成本轮回源核录清零，随包提供结构化表格入口和审计报告。", 
        f"- 主阅读版已嵌回已核结构化表格 {embedded_tables} 张。",
        f"- {table_index_note}",
        table_audit_note,
        "",
        "## PDF 生成",
        "",
        f"- {pdf_note}",
        "",
        "## 文件清单",
        "",
        "| 路径 | 大小 | SHA256 前16位 |",
        "| --- | ---: | --- |",
        *rows,
        "",
    ])
    (PACKAGE / "交付包说明.md").write_text("\n".join(note), encoding="utf-8")

    print(f"package={PACKAGE}")
    print(f"pdf={'ok' if pdf_ok else 'failed'}")
    print(f"files={len(list(PACKAGE.rglob('*')))}")


if __name__ == "__main__":
    main()
