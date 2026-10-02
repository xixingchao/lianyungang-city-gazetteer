# -*- coding: utf-8 -*-
"""Audit final-reader delivery quality from the reader-facing acceptance standard."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_PATH = ROOT / "output" / "reports" / "连云港市志_交付质量门禁报告.md"


@dataclass(frozen=True)
class Issue:
    kind: str
    line_no: int
    section: str
    text: str


def strip_tags(value: str) -> str:
    value = re.sub(r"<script.*?</script>", "", value, flags=re.S | re.I)
    value = re.sub(r"<style.*?</style>", "", value, flags=re.S | re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def strip_structured_tables(value: str) -> str:
    value = re.sub(r'<section class="verified-table-block".*?</section>', ' ', value, flags=re.S | re.I)
    return re.sub(r'<table class="(?:structured-table|dialect-phonology-table)".*?</table>', ' ', value, flags=re.S | re.I)


def excerpt(value: str, limit: int = 180) -> str:
    text = strip_tags(value)
    return text if len(text) <= limit else text[: limit - 1] + "..."


def audit() -> list[Issue]:
    lines = HTML_PATH.read_text(encoding="utf-8").splitlines()
    issues: list[Issue] = []
    current_h2 = "未进入正文"

    for line_no, line in enumerate(lines, start=1):
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", line, re.S)
        if h2:
            current_h2 = strip_tags(h2.group(1)) or current_h2

        text = strip_tags(line)
        if not text:
            continue
        non_table_text = strip_tags(strip_structured_tables(line))
        if not non_table_text:
            continue

        checks: list[tuple[str, bool]] = [
            ("可见待核图说明", "待对照原图" in non_table_text or "待核图" in non_table_text or "待补录" in non_table_text),
            ("pending-check核对表", 'pending-check' in line),
            ("空表/待录入单元格", "待对照原图录入" in non_table_text),
            ("长数字串/表格残文", bool(re.search(r"[0-9][0-9.]{25,}", non_table_text))),
            ("可见处理说明", any(token in non_table_text for token in ("源 OCR", "核对型", "处理说明", "原阅读版裸占位"))),
            ("HTML转义残留", "&lt;" in strip_structured_tables(line) or "&gt;" in strip_structured_tables(line) or "&quot;" in strip_structured_tables(line)),
            ("英文总述粘连/页码残留", bool(re.search(r"GENERALSUMMARY|General Summary[:：.]?\s*\d|Histroy of LianYunGang|yearsago|trans-portation", non_table_text))),
            # 表格残文串成正文时长行内几乎没有句末标点；正常正文提到"表 X-Y"时句号成串，据此排除误报。
            ("疑似表格正文串行",
             bool(re.search(r"表\s*\d+\s*-\s*\d+", non_table_text))
             and len(non_table_text) >= 160
             and non_table_text.count("。") <= 2),
        ]
        for kind, matched in checks:
            if matched:
                issues.append(Issue(kind=kind, line_no=line_no, section=current_h2, text=excerpt(line)))
    return issues


def render_report(issues: list[Issue]) -> str:
    by_kind = Counter(issue.kind for issue in issues)
    by_section: dict[str, Counter[str]] = defaultdict(Counter)
    for issue in issues:
        by_section[issue.section][issue.kind] += 1
    passed = not issues

    lines = [
        "# 连云港市志 交付质量门禁报告",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 基于：`{HTML_PATH.relative_to(ROOT)}`",
        "",
        "## 交付标准复核",
        "",
        "从项目记忆与参考交付包复核到的口径：",
        "",
        "- OCR 初稿只作为检索和校对底稿，正文和表格仍需原图核读。",
        "- 从全书 HTML 和结构化表格基线开始，按章节从头修复核对；未经记录和验收的章节不视为完成。",
        "- 参考交付包要求：主交付版本为正文含表版，正文中直接嵌入已核对结构化表格。",
        "- 参考交付包要求：最终阅读版不显示扫描页码、原书页码、导出说明、校对说明或表格占位卡片。",
        "",
        "## 当前结论",
        "",
        "- 当前最终阅读版通过交付质量门禁。" if passed else "- 当前最终阅读版未通过交付质量门禁。",
        f"- 本轮检出门禁问题 {len(issues)} 项。" if passed else "- 读者可见的待核图说明、pending-check 核对表、空表、串行 OCR 数字块或英文总述粘连仍需处理。",
        "- `正文表格占位符=0` 只说明旧占位卡片被移除；表格是否核对以结构化表格审计为准。",
        "",
        "## 问题计数",
        "",
        "| 问题类型 | 数量 |",
        "|---|---:|",
    ]
    for kind, count in by_kind.most_common():
        lines.append(f"| {kind} | {count} |")

    lines.extend([
        "",
        "## 章节分布（前 30）",
        "",
        "| 章节 | 总数 | 主要类型 |",
        "|---|---:|---|",
    ])
    section_rows = sorted(by_section.items(), key=lambda item: sum(item[1].values()), reverse=True)
    for section, counts in section_rows[:30]:
        total = sum(counts.values())
        top = "；".join(f"{k} {v}" for k, v in counts.most_common(4))
        lines.append(f"| {section} | {total} | {top} |")

    lines.extend([
        "",
        "## 代表样例（前 80）",
        "",
        "| 行号 | 章节 | 类型 | 摘录 |",
        "|---:|---|---|---|",
    ])
    for issue in issues[:80]:
        text = issue.text.replace("|", "\\|")
        lines.append(f"| {issue.line_no} | {issue.section} | {issue.kind} | {text} |")

    lines.extend([
        "",
        "## 下一步修复口径",
        "",
        "1. 先处理读者可见的非交付内容：`待对照原图`、`pending-check`、`处理说明`、HTML 转义残留。",
        "2. 对长数字串和表格正文串行区域按卷建立回源 PDF/页图核对任务，能结构化的录成表，不能确认的不得伪装为成品表。",
        "3. 对英文总述和附录做文字专项，清除页码、断词和粘连后再纳入最终阅读版。",
        "4. 每一批修复后复跑本门禁报告；只有高优先级读者可见问题清零，才可进入交付打包。",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    issues = audit()
    REPORT_PATH.write_text(render_report(issues), encoding="utf-8")
    print(f"issues={len(issues)}")
    for kind, count in Counter(issue.kind for issue in issues).most_common():
        print(f"{kind}: {count}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()

