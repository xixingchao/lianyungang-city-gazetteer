# -*- coding: utf-8 -*-
"""
连云港市志 上册跨页回接检测脚本

检测所有分页边界处可能的断句问题：
1. 上一页末尾不以句号/问号/感叹号/分号结尾 → 可能是断句
2. 下一页开头以小写/逗号开头 → 可能是上一页句子的延续
3. 提取上下文供人工复核

输出：workbench/qa/上册跨页回接检测报告.md
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "workbench" / "body_chapters" / "上"
OUT_REPORT = ROOT / "workbench" / "qa" / "上册跨页回接检测报告.md"

SENTENCE_END = re.compile(r'[。！？；」』）\)\""\'》\.]$')
SENTENCE_START_BAD = re.compile(r'^[，、。，；：""''）\)\]\}\)\u2026\u2014\u2015]')

# 需要跳过的页（封面、版权页等）
SKIP_PAGES = {1, 2, 301, 606}  # 分册封面/版权


def extract_last_sentence(text: str, max_chars: int = 80) -> str:
    """提取一段文本的最后一句（用于判断是否完整）"""
    text = text.strip()
    if not text:
        return ""
    # 取最后 max_chars 个字符
    return text[-max_chars:].replace("\n", " ")


def extract_first_sentence(text: str, max_chars: int = 80) -> str:
    """提取一段文本的第一句"""
    text = text.strip()
    if not text:
        return ""
    return text[:max_chars].replace("\n", " ")


def detect_page_breaks(filepath: Path) -> list[dict]:
    """检测单个精修文件中的所有跨页断点"""
    text = filepath.read_text(encoding="utf-8")
    issues = []

    # 匹配每个 page-anchor 及其后的文本块
    # 格式: <!-- page-anchor: LYG-S-XXXX -->\n\n{text}\n\n<!-- page-anchor
    pattern = re.compile(
        r'<!-- page-anchor: LYG-S-(\d+) -->\s*\n(.*?)(?=\n<!-- page-anchor:|\Z)',
        re.DOTALL
    )
    pages = pattern.findall(text)

    for i in range(len(pages) - 1):
        curr_page_num = int(pages[i][0])
        next_page_num = int(pages[i + 1][0])
        curr_text = pages[i][1].strip()
        next_text = pages[i + 1][1].strip()

        # 跳过标记页
        if curr_page_num in SKIP_PAGES or next_page_num in SKIP_PAGES:
            continue

        # 跳过空页
        if not curr_text or not next_text:
            continue

        # 跳过表格页
        if "续上表" in curr_text or "续表" in curr_text:
            continue

        # 检查：上一页末尾不是句子结尾
        curr_last = extract_last_sentence(curr_text)
        curr_ends_well = bool(SENTENCE_END.search(curr_last[-3:])) if len(curr_last) >= 3 else True

        # 检查：下一页开头不是大写/数字/标题
        next_first = extract_first_sentence(next_text)
        next_starts_bad = bool(SENTENCE_START_BAD.match(next_first)) if next_first else False

        # 检查：下一页开头是中文小写（可能是上一页句子的延续）
        next_first_char = next_first[0] if next_first else ""
        next_starts_lower = bool(re.match(r'[\u4e00-\u9fff]', next_first_char))

        # 判定
        severity = "OK"
        if not curr_ends_well and next_starts_lower:
            severity = "SUSPICIOUS"  # 高可疑：上页末不断句 + 下页开头是汉字
        elif not curr_ends_well:
            severity = "CHECK"  # 需检查：上页末不断句
        elif next_starts_bad:
            severity = "CHECK"  # 需检查：下页开头是标点

        if severity != "OK":
            issues.append({
                "curr_page": curr_page_num,
                "next_page": next_page_num,
                "severity": severity,
                "curr_end": curr_last[-60:],
                "next_start": next_first[:60],
            })

    return issues


def main():
    files = sorted(CHAPTER_DIR.glob("*.md"))
    all_issues = []

    for fpath in files:
        if fpath.name.startswith("连云港市志_上册_正文汇总"):
            continue
        issues = detect_page_breaks(fpath)
        if issues:
            all_issues.append((fpath.name, issues))

    # 生成报告
    lines = []
    lines.append("# 上册跨页回接检测报告")
    lines.append("")
    lines.append(f"检测文件数：{len(files)}")
    lines.append("")

    total_sus = 0
    total_check = 0
    for fname, issues in all_issues:
        sus = [i for i in issues if i["severity"] == "SUSPICIOUS"]
        chk = [i for i in issues if i["severity"] == "CHECK"]
        total_sus += len(sus)
        total_check += len(chk)

    lines.append(f"高可疑断句（SUSPICIOUS）：{total_sus} 处")
    lines.append(f"需检查断句（CHECK）：{total_check} 处")
    lines.append("")

    if total_sus > 0:
        lines.append("## 高可疑断句（优先人工复核）")
        lines.append("")
        lines.append("| 文件 | pN→pN+1 | 上页末尾 | 下页开头 |")
        lines.append("| --- | --- | --- | --- |")
        for fname, issues in all_issues:
            for iss in issues:
                if iss["severity"] == "SUSPICIOUS":
                    lines.append(
                        f"| {fname} | p{iss['curr_page']}→p{iss['next_page']} | "
                        f"{iss['curr_end']} | {iss['next_start']} |"
                    )

    if total_check > 0:
        lines.append("")
        lines.append("## 需检查断句")
        lines.append("")
        lines.append("| 文件 | pN→pN+1 | 上页末尾 | 下页开头 | 类型 |")
        lines.append("| --- | --- | --- | --- | --- |")
        for fname, issues in all_issues:
            for iss in issues:
                if iss["severity"] == "CHECK":
                    reason = "上页不断句" if not SENTENCE_END.search(iss["curr_end"][-3:]) else "下页开头是标点"
                    lines.append(
                        f"| {fname} | p{iss['curr_page']}→p{iss['next_page']} | "
                        f"{iss['curr_end']} | {iss['next_start']} | {reason} |"
                    )

    if total_sus == 0 and total_check == 0:
        lines.append("未检测到可疑跨页断句。")
    else:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("**说明**：")
        lines.append("- SUSPICIOUS：上页末尾不是句子结尾 + 下页开头是汉字 → 很可能是跨页断句")
        lines.append("- CHECK：上页末尾不是句子结尾 或 下页开头是标点 → 需人工判断")
        lines.append("- 表格页、封面页、空白页已自动跳过")
        lines.append("- 地方志中跨页段落是正常现象，大部分不需要修复")

    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"检测完成：高可疑 {total_sus} 处，需检查 {total_check} 处")
    print(f"报告：{OUT_REPORT}")


if __name__ == "__main__":
    main()
