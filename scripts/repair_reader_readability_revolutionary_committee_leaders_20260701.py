# -*- coding: utf-8 -*-
"""Repair flattened revolutionary committee leader list in volume 42."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_revolutionary_committee_leaders_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_revolutionary_committee_leaders_20260701.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第四十二卷市革命委员会首长名单残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = """<h4 id="第四十二卷-第五章连云港市革命委员会-第二节市革命委员会首长">第二节市革命委员会首长</h4>
<p>主任元庆标(1969.9~1971.2)张国安（1971.2~1972.10)刘文龙（1972.10~1974.2)金逊(1974.2~1977.6)智(1977.6~1978.1)湘(1969.9~1970.1)副主任坤(1969.9 ~1970.2)李力(1969.9~1970.3)邸志勇（1969.9~1971.3)陈心文（1969.9~1975.7)祝斌(1969.9~1975.11)刘文龙（1970.8~1971.10)曹良友(1970.8~1971.10)高心意（1970.9~1980.2)杨玉生(1971.12~1975.11)姚远(1973.5~1977.9)徐河均(1973.8~1982.2)杨鸿儒（1974.2~1974.10）</p>
<p>耿志英（女）（1975.11~1980.2)李敬松(1975.11~1980.2)耿杰民（1977.5~1980.2)雷成堂（1977.7~1980.2）</p>
<p>王遐松(1977.11~1980.2)谢克东(1977.11~1978.4)第三节政务纪要连云港市经过经济调整，准备执行发展国民经济第三个五年计划时，1966年5月，中共中央发出《中共中央通知》（5.16通知）,8月，中共中央发布《关于无产阶级文化大革命的决定》，标志“文化大革命全面发动。7月6～22日，中共连云港市委、连云港市人委决定成立“文化大革命”领导小组。1967年1月25日，连云港市革命造反派夺权委员会夺取市委、市人委、市“文化大革命”领导小组及其各部门的权，政府工作瘫痪，群众组织武斗频繁。1968年7月19日，经毛泽东主席批准，中共中央在北京举办毛泽东思想学习班徐海班及连云港班，通过《连云港市革命三结合方案》，9月10日，周恩来总理亲临连云港班，促成实现革命大联合。9月18日，中央举办的毛泽东思想学习班连云港班结束。全市按系统、行业、部门实现群众大联合。9月26日，成立连云港市革命委员会。10月2～6日，市革命委员会举行第一次会议，号召全市人民巩固发展革命大联合，各区、局人民公社成立三结合领导小组。</p>
<h4 id="第四十二卷-第五章连云港市革命委员会-第三节政务纪要">第三节政务纪要</h4>"""

NEW = """<h4 id="第四十二卷-第五章连云港市革命委员会-第二节市革命委员会首长">第二节市革命委员会首长</h4>
<p>主任</p>
<ul class="leader-list">
<li>元庆标（1969.9~1971.2）</li>
<li>张国安（1971.2~1972.10）</li>
<li>刘文龙（1972.10~1974.2）</li>
<li>金逊（1974.2~1977.6）</li>
<li>智（1977.6~1978.1）</li>
</ul>
<p>副主任</p>
<ul class="leader-list">
<li>刘湘（1969.9~1970.1）</li>
<li>刘坤（1969.9~1970.2）</li>
<li>李力（1969.9~1970.3）</li>
<li>邸志勇（1969.9~1971.3）</li>
<li>陈心文（1969.9~1975.7）</li>
<li>祝斌（1969.9~1975.11）</li>
<li>刘文龙（1970.8~1971.10）</li>
<li>曹良友（1970.8~1971.10）</li>
<li>高心意（1970.9~1980.2）</li>
<li>杨玉生（1971.12~1975.11）</li>
<li>姚远（1973.5~1977.9）</li>
<li>徐河均（1973.8~1982.2）</li>
<li>杨鸿儒（1974.2~1974.10）</li>
<li>耿志英（女）（1975.11~1980.2）</li>
<li>李敬松（1975.11~1980.2）</li>
<li>耿杰民（1977.5~1980.2）</li>
<li>雷成堂（1977.7~1980.2）</li>
<li>王遐松（1977.11~1980.2）</li>
<li>谢克东（1977.11~1978.4）</li>
</ul>
<h4 id="第四十二卷-第五章连云港市革命委员会-第三节政务纪要">第三节政务纪要</h4>
<p>连云港市经过经济调整，准备执行发展国民经济第三个五年计划时，1966年5月，中共中央发出《中共中央通知》（5.16通知），8月，中共中央发布《关于无产阶级文化大革命的决定》，标志“文化大革命”全面发动。7月6～22日，中共连云港市委、连云港市人委决定成立“文化大革命”领导小组。1967年1月25日，连云港市革命造反派夺权委员会夺取市委、市人委、市“文化大革命”领导小组及其各部门的权，政府工作瘫痪，群众组织武斗频繁。1968年7月19日，经毛泽东主席批准，中共中央在北京举办毛泽东思想学习班徐海班及连云港班，通过《连云港市革命三结合方案》，9月10日，周恩来总理亲临连云港班，促成实现革命大联合。9月18日，中央举办的毛泽东思想学习班连云港班结束。全市按系统、行业、部门实现群众大联合。9月26日，成立连云港市革命委员会。10月2～6日，市革命委员会举行第一次会议，号召全市人民巩固发展革命大联合，各区、局人民公社成立三结合领导小组。</p>"""


def write_reports(replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十二卷政务 / 第五章连云港市革命委员会 / 第二节市革命委员会首长",
        "source_files": [
            "workbench/ocr/paddle_ocr/中/part02/page_0490.txt",
            "workbench/ocr/raw/中/part02/page_0490.txt",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32138",
        ],
        "reader_path": str(HTML),
        "flattened_blocks_replaced": replaced,
        "notes": "按页级 OCR 恢复主任/副主任逐行名单，并将误粘入正文段的第三节标题恢复到段前。刘湘、刘坤、李力、祝斌等以 page_0490 PaddleOCR 行文本校正；单字“智”源页 OCR 与正文汇总均未给出姓氏，本轮不臆补。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第四十二卷市革命委员会首长名单残文修复

- 时间：{now}
- 范围：`第四十二卷政务 / 第五章连云港市革命委员会 / 第二节市革命委员会首长`
- 源文依据：`workbench/ocr/paddle_ocr/中/part02/page_0490.txt`、`workbench/ocr/raw/中/part02/page_0490.txt`

## 修复动作

- 将 `主任元庆标...副主任...谢克东...第三节政务纪要...` 的压平段恢复为主任、副主任两组名单。
- 将误粘入正文段的 `第三节政务纪要` 标题移回段前，避免正文段与标题重复错位。
- 替换阅读版压平残文：{replaced} 组。

## 核对说明

- `page_0490` 页级 OCR 清楚列出主任、副主任逐行名单。
- `刘湘`、`刘坤`、`李力`、`祝斌` 等以 PaddleOCR 行文本校正正文汇总中的漏字/空格。
- 单字 `智（1977.6~1978.1）` 在页级 OCR 与正文汇总中均未提供姓氏，本轮不臆补。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(replaced: int) -> None:
    marker = "## 2026-07-01 第四十二卷市革命委员会首长名单残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第四十二卷政务 `主任元庆标...副主任...谢克东...第三节政务纪要...` 压平残文回源修复。
- 据 `workbench/ocr/paddle_ocr/中/part02/page_0490.txt` 和 `workbench/ocr/raw/中/part02/page_0490.txt` 恢复主任、副主任逐行名单；同时把误粘入正文段的 `第三节政务纪要` 标题恢复到段前。
- `刘湘`、`刘坤`、`李力`、`祝斌` 等按页级 OCR 校正；单字 `智` 源页 OCR 与正文汇总均未给出姓氏，本轮保守保留。
- 阅读版压平残文替换 {replaced} 组。
- 报告：`output/reports/reader_readability_revolutionary_committee_leaders_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected one revolutionary committee leader block, found {count}")
    text = text.replace(OLD, NEW, 1)
    HTML.write_text(text, encoding="utf-8")
    write_reports(1)
    update_memory(1)
    print("revolutionary committee leader list repaired")
    print("flattened_blocks_replaced=1")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
