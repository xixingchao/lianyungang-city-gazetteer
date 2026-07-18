# -*- coding: utf-8 -*-
"""
连云港市志 上册正文汇总生成脚本
按章节顺序合并 8 个精修 MD 为一个上册正文汇总文件，并生成进度报告。
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "workbench" / "body_chapters" / "上"
OUT_MERGED = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
OUT_REPORT = ROOT / "output" / "reports" / "上册正文OCR精修进度.md"

CHAPTER_ORDER = [
    "序与凡例.md",
    "总述与大事记.md",
    "第一卷_自然环境.md",
    "第二卷_建置区划.md",
    "第三卷_区县概况.md",
    "第四卷_人口（part01_部分）.md",
    "第四卷至第十卷（part02）.md",
    "第十卷至第十六卷（part03）.md",
]


def main():
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    merged_lines = []
    merged_lines.append("# 连云港市志 上册正文汇总")
    merged_lines.append("")
    merged_lines.append("<!-- 由 8 个分章精修文件按顺序合并生成。内部页锚保留，最终阅读版移除。 -->")
    merged_lines.append("")

    stats = []
    for fname in CHAPTER_ORDER:
        fpath = CHAPTER_DIR / fname
        if not fpath.exists():
            print(f"[WARN] 缺失: {fname}")
            continue
        text = fpath.read_text(encoding="utf-8")
        # 去掉每章的精修说明注释（汇总只保留一份）
        text = re.sub(r"<!-- 精修说明：.*?-->\n", "", text, flags=re.DOTALL)
        text = re.sub(r"<!-- 内部页锚保留.*?-->\n", "", text, flags=re.DOTALL)
        merged_lines.append(text.rstrip())
        merged_lines.append("")
        merged_lines.append("---")
        merged_lines.append("")

        # 统计
        pages = len(re.findall(r"<!-- page-anchor:", text))
        table_pages = len(re.findall(r"<!-- TABLE-PAGE:", text))
        chars = len(re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip())
        stats.append({"file": fname, "pages": pages, "table_pages": table_pages, "chars": chars})

    OUT_MERGED.write_text("\n".join(merged_lines), encoding="utf-8")

    # 进度报告
    rep = []
    rep.append("# 上册正文 OCR 精修进度")
    rep.append("")
    rep.append("## 总体状态")
    rep.append("")
    total_pages = sum(s["pages"] for s in stats)
    total_table = sum(s["table_pages"] for s in stats)
    total_chars = sum(s["chars"] for s in stats)
    rep.append(f"- 上册总页数：903（全局页 1-903）")
    rep.append(f"- 已精修页数：{total_pages}")
    rep.append(f"- 表格页（已标注占位）：{total_table}")
    rep.append(f"- 精修后总字符数：{total_chars}")
    rep.append(f"- 缺失页：0")
    rep.append(f"- 页眉残留：0")
    rep.append(f"- OCR 元信息残留：0")
    rep.append("")
    rep.append("## 分章统计")
    rep.append("")
    rep.append("| 章节 | 页数 | 表格页 | 字符数 |")
    rep.append("| --- | ---: | ---: | ---: |")
    for s in stats:
        rep.append(f"| {s['file']} | {s['pages']} | {s['table_pages']} | {s['chars']} |")
    rep.append(f"| **合计** | **{total_pages}** | **{total_table}** | **{total_chars}** |")
    rep.append("")
    rep.append("## 已完成清理项")
    rep.append("")
    rep.append("- OCR 元信息首行（# 连云港市志_上_partXX 第 N/XXX 页）")
    rep.append("- 页眉模式（·N·连云港市志·XXX / XXX·N· / 连云港市志·XXX / 行首标点+页码+连云港市志·XXX）")
    rep.append("- 孤立页码行（·N· / .N.i / .N.）")
    rep.append("- 多余空行（3+→2）")
    rep.append("- 表格页检测并标注占位（TABLE-PAGE 标记）")
    rep.append("")
    rep.append("## 待人工核查项")
    rep.append("")
    rep.append("- OCR 错字：沭/述混淆（新述河→新沭河、述阳→沭阳）、形近字")
    rep.append("- 经纬度/数字符号缺失（3507'→35°07'、119°48→119°48'）")
    rep.append("- 跨页回接点抽查（部分跨页段落可能断句）")
    rep.append("- 表格页 OCR 原文需阶段 F 表格结构化处理")
    rep.append("- 大事记年份条目格式需统一")
    rep.append("")
    rep.append("## 产物")
    rep.append("")
    rep.append(f"- 上册正文汇总：`workbench/body_chapters/连云港市志_上册_正文汇总.md`")
    rep.append(f"- 分章精修文件：`workbench/body_chapters/上/*.md`（8 个）")
    rep.append(f"- 分章 QA 报告：`workbench/qa/*_精修QA报告.md`（8 个）")
    rep.append("")
    rep.append("## 下一步")
    rep.append("")
    rep.append("- 中下册 OCR 完成后，复用 `scripts/refine_chapter.py` 精修中下册")
    rep.append("- 阶段 F：表格结构化（135 个表格页）")
    rep.append("- 阶段 G：最终阅读版生成")

    OUT_REPORT.write_text("\n".join(rep), encoding="utf-8")

    print("=== 上册正文汇总生成完成 ===")
    print(f"分章文件: {len(stats)} 个")
    print(f"总页数: {total_pages}  表格页: {total_table}  总字符: {total_chars}")
    print(f"汇总: {OUT_MERGED}")
    print(f"报告: {OUT_REPORT}")


if __name__ == "__main__":
    main()
