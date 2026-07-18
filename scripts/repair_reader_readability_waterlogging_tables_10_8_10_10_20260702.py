# -*- coding: utf-8 -*-
"""Replace flattened table residue for tables 10-8 to 10-10 in 第十卷 水利."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_waterlogging_tables_10_8_10_10_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_waterlogging_tables_10_8_10_10_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第十卷水利沂北除涝表10-8至10-10残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:17990-18216"
START_MARKER = "<p>米/秒）</p>\n<p>（米）</p>\n<p>（米）</p>\n<p>（米）</p>\n<p>公里）</p>"
END_MARKER = '<h4 id="第十卷-第二章除涝-第二节沭南除涝">第二节沭南除涝</h4>'
SECTION_START = '<section class="verified-table-block reader-repair-table-block" id="reader-repair-table-10-8-10-10">\n'
SECTION_END = "</section>\n"
CAPTIONS = [
    "表10-8 1990年连云港市沂北引排干河基本情况表",
    "表10-9 1990年连云港市沂北梯级控制河道基本情况表",
    "表10-10 1990年连云港市沂北主要控制涵闸基本情况表",
]
RESIDUAL_MARKERS = [
    "叮当河叮鸣河涵洞一叮当河闸24.1175.2",
    "东门节制闸白蚬乡德兴庄1961.4-1.0五图闸",
    "<p>（平方米）</p>\n<p>（米）</p>\n<p>/秒）</p>\n<p>（米）</p>",
]


def table_html(caption: str, columns: list[str], rows: list[list[str]]) -> str:
    ths = "".join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = "".join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    return (
        '<table class="structured-table">'
        f"<caption>{html.escape(caption)}</caption>"
        f"<thead><tr>{ths}</tr></thead><tbody>{''.join(trs)}</tbody></table>"
    )


def replacement_html() -> str:
    table_10_8 = table_html(
        CAPTIONS[0],
        ["河名", "境内起讫位置", "长度（公里）", "可读数值序列", "备注"],
        [
            ["东门五图河", "盐河一五图闸、图西闸", "48.5", "30～65；-0.8～-2.0；1：3；6.5～3.7；1：3", "数值列按源文行序保留"],
            ["五灌河", "小南沟—燕尾闸", "16.0", "-1.8～-2.0；1：4.5；6.5～5.5", "部分数值列空缺"],
            ["牛墩界圩河", "叮当河一小南沟", "43.3", "8～90；-0.5～-2.8；1：3～1：3.5；5.5～5.0；1：3", "数值列按源文行序保留"],
            ["车轴河", "盐河大柴市一车轴河闸", "32.0", "94.5；21～48.5；-0.5～-2.0；1：3.5；6.0～5.5；1：3", "数值列按源文行序保留"],
            ["古泊善后河", "龙苴乡夹滩村一善后新闸", "50.1", "14～124；-1.0～-3.0；1：3～1：4.5；9.5～6.0；1：3", "数值列按源文行序保留"],
            ["盐河", "黑风口一烧香河北闸", "26.3", "8～40；0.0～-2.5；1：3.5；6.0～5.0；1：3", "数值列按源文行序保留"],
            ["烧香河", "盐河黑风口一烧香河南闸", "46.0", "8～50；0.0～-2.5；1：3.5；6.0～5.0；1：3", "数值列按源文行序保留"],
            ["东盐排淡河", "西盐河口一大板跳闸", "37.1", "8～25；-1.0；1：3", "部分数值列空缺"],
        ],
    )
    table_10_9 = table_html(
        CAPTIONS[1],
        ["河名", "境内起迄位置", "长度（公里）", "可读数值序列", "备注"],
        [
            ["叮当河", "叮鸣河涵洞一叮当河闸", "24.1", "175.2；13～30；-0.5～-1.0；1：2.5～1：3；2.8", "数值列按源文行序保留"],
            ["盐河", "盐河北套闸一新浦", "47.3", "137.0；6～8；0.5～-0.5；1：4；1.8～1.6", "数值列按源文行序保留"],
            ["官沟河", "新沂河北堤一界圩河", "16.0", "110.4；0.0；1：4", "部分数值列空缺"],
            ["大新河", "车轴河一善后河", "6.3", "45.3；-1.0；1：4", "部分数值列空缺"],
        ],
    )
    table_10_10 = table_html(
        CAPTIONS[2],
        ["名称", "闸址", "水系", "建成年月", "可读数值序列", "备注"],
        [
            ["东门节制闸", "白蚬乡德兴庄", "", "1961.4", "-1.0", "部分工程字段空缺"],
            ["五图闸", "洋桥五图河口", "东门五图河", "1953.7", "-2.0；1.2～1.4", "数值列按源文行序保留"],
            ["图西闸", "洋桥五图河口", "", "1958.8", "-2.0；1.2～1.4", "水系栏空缺"],
            ["燕尾闸", "燕尾镇南", "五灌河", "1972.8", "-2.0；1.2～1.4", "数值列按源文行序保留"],
            ["枯沟河闸", "小伊乡光明村", "牛墩界圩河", "", "-0.8", "建成年月空缺"],
            ["界圩闸", "同兴乡杨五庄东", "", "1974.6", "-1.2", "水系栏空缺"],
            ["大新闸", "大新河南端", "", "", "-1.4", "水系、建成年月空缺"],
            ["同兴节制闸", "同兴集西", "车轴河", "1966.7", "-1.4", "数值列按源文行序保留"],
            ["车轴河闸", "东陬山", "", "", "-2.0；1.2～1.4", "水系、建成年月空缺"],
            ["埃字河闸", "埃字河口", "", "1965.6", "-1.4", "水系栏空缺"],
            ["叮当河闸", "叮当河北端", "古泊善后河", "", "-1.0；2.2", "建成年月空缺"],
            ["善后新闸", "东陬山", "", "1957.10", "-3.0", "水系栏空缺"],
            ["烧香河闸", "东陬山", "烧香河", "1957.6", "-2.0", "数值列按源文行序保留"],
            ["烧香河北闸", "烧香河古道入海口", "", "1973.12", "-2.5；3×2", "水系栏空缺"],
            ["玉带河闸", "东盐河西端", "东盐排淡河", "1971.5", "-1.0；5×1；3×2", "数值列按源文行序保留"],
            ["猴嘴闸", "猴嘴镇", "东盐排淡河", "", "-1.0；6×1", "建成年月空缺"],
            ["大板桥闸", "排淡河口", "", "", "-2.5；1.5", "水系、建成年月空缺"],
            ["盐河北套闸", "新沂河北堤盐河口", "", "", "-1.0；1.6", "水系、建成年月空缺"],
            ["善南套闸", "板浦镇", "盐河", "1964.7", "一；-1.5", "数值列按源文行序保留"],
            ["盐河通航闸", "锦屏镇高庄东", "", "1972.6", "-1.0", "水系栏空缺"],
            ["叮当河涵洞", "叮当河南端", "叮当河", "1971.9", "0.0；2.2", "数值列按源文行序保留"],
            ["蔷薇河南堤", "", "", "", "电厂闸；玉带河；玉带河西端", "末行关系按源文可读序列保留"],
        ],
    )
    return (
        SECTION_START
        + '<div class="structured-table-meta">资料来源：第四卷至第十卷（part02），页锚 LYG-S-0591 至 LYG-S-0592</div>\n'
        + f"{table_10_8}\n{table_10_9}\n{table_10_10}\n"
        + SECTION_END
    )


def current_counts(text: str) -> dict[str, object]:
    return {
        "captions": {caption: text.count(caption) for caption in CAPTIONS},
        "residual_markers": {marker: text.count(marker) for marker in RESIDUAL_MARKERS},
        "start_marker_count": text.count(START_MARKER),
    }


def validate_after(text: str) -> dict[str, object]:
    after = current_counts(text)
    if any(after["residual_markers"].values()):
        raise RuntimeError(f"waterlogging residue remains: {after['residual_markers']}")
    if any(count != 1 for count in after["captions"].values()):
        raise RuntimeError(f"unexpected caption counts: {after['captions']}")
    return after


def patch_reader() -> dict[str, object]:
    text = HTML.read_text(encoding="utf-8")
    before = current_counts(text)
    new_block = replacement_html()

    existing_start = text.find(SECTION_START)
    if existing_start != -1:
        existing_end = text.find(SECTION_END, existing_start)
        if existing_end == -1:
            raise RuntimeError("existing waterlogging repair section is not closed")
        existing_end += len(SECTION_END)
        if text[existing_start:existing_end] == new_block:
            return {"changed": 0, "before": before, "after": validate_after(text), "mode": "idempotent"}
        fixed = text[:existing_start] + new_block + text[existing_end:]
        HTML.write_text(fixed, encoding="utf-8")
        return {"changed": 1, "before": before, "after": validate_after(fixed), "mode": "updated"}

    start = text.find(START_MARKER)
    end = text.find(END_MARKER, start)
    if start == -1 or end == -1:
        raise RuntimeError("waterlogging table residue boundary not found")
    if text.find(START_MARKER, start + 1) != -1:
        raise RuntimeError("start marker is not unique")
    fixed = text[:start] + new_block + text[end:]
    HTML.write_text(fixed, encoding="utf-8")
    return {"changed": 1, "before": before, "after": validate_after(fixed), "mode": "patched"}


def write_reports(result: dict[str, object]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第十卷水利 / 第二章除涝 / 第一节沂北除涝 / 表10-8至表10-10残文",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "principle": "以源文OCR为依据保守重建结构化表，宽表列位不可靠处在报告中记录，阅读版只保留可读表格。",
        "result": result,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    before = result["before"]
    after = result["after"]
    md = f"""# 第十卷水利沂北除涝表10-8至表10-10残文修复

- 时间：{now}
- 范围：`第十卷水利 / 第二章除涝 / 第一节沂北除涝`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 将第一节末尾、`第二节沭南除涝` 前的表格单位残行和压平残文替换为 3 张结构化表。
- 表10-8、表10-9按河名、起讫位置和源 OCR 可读数值序列保守重建。
- 表10-10按闸名、闸址、水系、建成年月和源 OCR 可读序列保守重建；末行断裂处不强行推断。
- 阅读版只保留读者可见表格，过程性说明留在本报告，不进入正文页面。
- 不触碰 `第二节沭南除涝` 及后续正文。

## 结果

- 本轮改动：{result['changed']}
- 模式：{result['mode']}
- 表题计数：{json.dumps(after['captions'], ensure_ascii=False)}
- 残文标记：{json.dumps(after['residual_markers'], ensure_ascii=False)}
- 残块起始标记：{before['start_marker_count']} -> {after['start_marker_count']}

## 核对说明

- 源 OCR 宽表列位存在错位，尤其表10-10末尾 `蔷薇河南堤 / 电厂闸 / 玉带河 / 玉带河西端` 行关系断裂，本轮只在表内保留可读序列。
- 后续若对照原图，可以将 `可读数值序列` 拆入完整工程字段。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(result: dict[str, object]) -> None:
    marker = "## 2026-07-02 第十卷水利沂北除涝表10-8至表10-10残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第十卷水利 `叮当河叮鸣河涵洞一叮当河闸24.1175.2...`、`东门节制闸白蚬乡德兴庄1961.4-1.0...` 等表格压平残文进行回源修复。
- 源文依据：`{SOURCE_NOTE}`，覆盖表10-8《1990年连云港市沂北引排干河基本情况表》、表10-9《1990年连云港市沂北梯级控制河道基本情况表》、表10-10《1990年连云港市沂北主要控制涵闸基本情况表》。
- 阅读版中第一节沂北除涝末尾的单位残行和压平残文已替换为 3 张结构化表；宽表列位不可靠处保留可读数值序列，未臆造字段归属。
- 表10-10末行 `蔷薇河南堤 / 电厂闸 / 玉带河 / 玉带河西端` 源 OCR 关系断裂，本轮保守记录在报告中。
- 报告：`output/reports/reader_readability_waterlogging_tables_10_8_10_10_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = patch_reader()
    write_reports(result)
    if result["changed"]:
        update_memory(result)
    print("waterlogging table residue repaired")
    print(f"changed={result['changed']}")
    print(f"mode={result['mode']}")
    print(f"after={result['after']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
