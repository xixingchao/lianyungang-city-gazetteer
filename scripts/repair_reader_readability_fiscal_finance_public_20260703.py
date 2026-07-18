# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in fiscal, finance, civil affairs, and public security chapters."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_fiscal_finance_public_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_fiscal_finance_public_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_财政金融民政治安高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

GROUPS = [
    {
        "name": "第三十八卷财政 / 第三章财政支出 / 第一节经济建设支出",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0294.txt:25-28; page_0295.txt:5-6",
        "start": '<h4 id="第三十八卷-第三章财政支出-第一节经济建设支出">第一节经济建设支出</h4>',
        "end": '<h4 id="第三十八卷-第三章财政支出-第二节城市维护及建设支出">第二节城市维护及建设支出</h4>',
        "replacements": [
            ("新建厂房", "新建了-批广房", "新建了一批厂房"),
            ("纳入地方预算", "纳人地方预算", "纳入地方预算"),
            ("纳入市财政预算", "纳人市财政预算", "纳入市财政预算"),
            ("工业部门1885万元", "工业部门1885方元", "工业部门1885万元"),
            ("基建寥寥无几", "基建寒寒无几", "基建寥寥无几"),
            ("其它部门2540万元", "其它部门支出2540方元", "其它部门支出2540万元"),
            ("全年支出1506万元", "全年支出1506方元", "全年支出1506万元"),
        ],
    },
    {
        "name": "第四十卷金融 / 第四章贷款 / 第一节本位币贷款",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0361.txt:22-27; page_0366.txt:20-22",
        "start": '<h4 id="第四十卷-第四章贷款-第一节本位币贷款">第一节本位币贷款</h4>',
        "end": '<h4 id="第四十卷-第四章贷款-第二节外汇贷款">第二节外汇贷款</h4>',
        "replacements": [
            ("敞口供应", "资金需要口供应", "资金需要敞口供应"),
            ("626万元", "贷款余额626万，元", "贷款余额626万元"),
            ("赊销预付", "除销预付", "赊销预付"),
            ("银行六条书名号", "认真贯彻银行六条》规定", "认真贯彻《银行六条》规定"),
            ("徘徊不前", "产值连续五年排不前", "产值连续五年徘徊不前"),
            ("进一步提高", "进步提高了生产能力", "进一步提高了生产能力"),
            ("新坝锦屏", "对新项、锦屏、朝阳", "对新坝、锦屏、朝阳"),
        ],
    },
    {
        "name": "第四十三卷民政信访 / 第三章救灾救济扶贫 / 第一节救灾",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0028.txt:22-28; page_0029.txt:4",
        "start": '<h4 id="第四十三卷-第三章救灾救济扶贫-第一节救灾">第一节救灾</h4>',
        "end": '<h4 id="第四十三卷-第三章救灾救济扶贫-第二节救济">第二节救济</h4>',
        "replacements": [
            ("50万人", "50方人", "50万人"),
            ("20万人", "20方人", "20万人"),
            ("5千万元", "5千方元", "5千万元"),
            ("家畜几死尽", "家畜儿死尽", "家畜几死尽"),
            ("人口47.5%", "人口.47.5%", "人口47.5%"),
            ("深入灾区", "深人灾区", "深入灾区"),
            ("风力7~12级", "风力712级", "风力7~12级"),
        ],
    },
    {
        "name": "第四十四卷治安司法 / 第一章治安 / 第二节政治保卫",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0068.txt:4-11",
        "start": '<h4 id="第四十四卷-第一章治安-第二节政治保卫">第二节政治保卫</h4>',
        "end": '<h4 id="第四十四卷-第一章治安-第三节经济、文化保卫">第三节经济、文化保卫</h4>',
        "replacements": [
            ("第一阶段", "第－阶段", "第一阶段"),
            ("阶段分号", "1951年10月31日1951年11月1日", "1951年10月31日；1951年11月1日"),
            (
                "二次镇反结束后",
                "第二次镇压反革命运动结束击处理特务、土匪、恶霸、反动党团骨干、反动会道门头子5个方面的反革命分子3082人。",
                "第二次镇压反革命运动结束后，根据中共中央指示精神，开展扫清残余反革命分子斗争。两次镇压反革命运动，共打击处理特务、土匪、恶霸、反动党团骨干、反动会道门头子5个方面的反革命分子3082人。",
            ),
        ],
    },
    {
        "name": "第四十四卷治安司法 / 第一章治安 / 第五节治安管理 / 防火检查",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0092.txt:18-41; page_0093.txt:3-6",
        "start": '<h4 id="第四十四卷-第一章治安-第五节治安管理">第五节治安管理</h4>',
        "end": '<h4 id="第四十四卷-第一章治安-第六节预审监所">第六节预审监所</h4>',
        "replacements": [
            (
                "1962防火检查开头",
                "1962年12月，市政府从市公安、劳动、工会、商业、粮食、物资、供销等期整顿。1975年9月26~28日",
                "1962年12月，市政府从市公安、劳动、工会、商业、粮食、物资、供销等11个部门抽调21名干部组成4个检查组，对市属和区属16个较大粮、棉、油、百货仓库和粮、油、棉加工厂进行防火检查，查出不安全仓库11个，有8个仓库及时整改，3个仓库限期整顿。1975年9月26~28日",
            ),
            ("1060厂次", "检查1060厂（次）", "检查1060厂(次)"),
            ("隐患1916处", "隐惠1916处", "隐患1916处"),
            (
                "1985防火检查",
                "市消防大队组织人员到厂余处，对80余处较大隐患，下发整改通知书限期整改。",
                "市消防大队组织人员到厂矿、企事业单位检查400余人次，查出隐患500余处，当场督促整改312处，限期整改100余处，对80余处较大隐患，下发整改通知书限期整改。",
            ),
            ("2800人次", "检查2800人（次）", "检查2800人(次)"),
            ("深入单位", "深人单位检查", "深入单位检查"),
        ],
    },
]


def find_scope(text: str, group: dict[str, object]) -> tuple[int, int]:
    start = text.index(str(group["start"]))
    end = text.index(str(group["end"]), start)
    return start, end


def patch_reader() -> tuple[int, list[dict[str, object]]]:
    text = HTML.read_text(encoding="utf-8")
    results: list[dict[str, object]] = []
    changed_total = 0

    for group in GROUPS:
        start, end = find_scope(text, group)
        original = text[start:end]
        segment = original
        counts: dict[str, int] = {}

        for label, old, new in group["replacements"]:  # type: ignore[index]
            count = segment.count(old)
            if count:
                segment = segment.replace(old, new)
            elif new not in segment:
                raise RuntimeError(f"neither old nor new text found for {group['name']} / {label}")
            counts[label] = count

        if segment != original:
            text = text[:start] + segment + text[end:]
            changed_total += 1

        results.append({
            "name": group["name"],
            "source": group["source"],
            "counts": counts,
            "changed": int(segment != original),
        })

    HTML.write_text(text, encoding="utf-8")
    verify_reader()
    return changed_total, results


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    for group in GROUPS:
        start, end = find_scope(text, group)
        segment = text[start:end]
        missing = []
        residuals = []
        for _label, old, new in group["replacements"]:  # type: ignore[index]
            if new not in segment:
                missing.append(new)
            if old in segment:
                residuals.append(old)
        if missing or residuals:
            raise RuntimeError(f"verification failed for {group['name']}: missing={missing}, residuals={residuals}")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed_total: int, results: list[dict[str, object]]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_replacements = sum(sum(item["counts"].values()) for item in results)  # type: ignore[union-attr]
    payload = {
        "time": now,
        "reader_path": str(HTML),
        "changed_scopes": changed_total,
        "total_replacements": total_replacements,
        "groups": results,
        "principle": "仅修复页级 OCR 已确认、且最终阅读版存在明确坏串的错识；保留未核定疑点。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 财政金融民政治安高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 阅读器：`{HTML}`",
        f"- 本次改写章节范围：{changed_total}",
        f"- 本次替换总数：{total_replacements}",
        "- 原则：只修复页级 OCR 已确认、且最终阅读版存在明确坏串的错识。",
        "",
        "## 修复范围",
    ]
    for item in results:
        changed = item["changed"]
        count = sum(item["counts"].values())  # type: ignore[union-attr]
        lines.extend([
            "",
            f"- {item['name']}",
            f"  - 源文：`{item['source']}`",
            f"  - 改写：{changed}；替换：{count}",
        ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    progress = f"""# 财政金融民政治安高置信错识回源修复

- 时间：{now}
- 阅读器：`output/final_reader/连云港市志_全书.html`。
- 修复范围：第三十八卷财政、第四十卷金融、第四十三卷民政信访、第四十四卷治安司法。
- 本次替换：{total_replacements} 处；改写章节范围：{changed_total} 个。
- 依据：页级 OCR 明确给出 `敞口供应`、`赊销预付`、`徘徊不前`、`新坝`、`50万人`、`5千万元`、`第一阶段`、`防火检查` 等源文。
- 保留：未能在本批源文中直接核定的其它 `方元`、连接号和数字密集段落。
- 报告：`output/reports/reader_readability_fiscal_finance_public_20260703.md`。
"""
    PROGRESS.write_text(progress, encoding="utf-8")

    marker = "## 2026-07-03 财政金融民政治安高置信错识回源修复"
    memory = f"""
{marker}

- 按页级 OCR 对第三十八卷财政、第四十卷金融、第四十三卷民政信访、第四十四卷治安司法做一批高置信错识修复。
- 源文依据：`workbench/ocr/paddle_ocr/中/part02/page_0294.txt`、`page_0295.txt`、`page_0361.txt`、`page_0366.txt`，以及 `workbench/ocr/paddle_ocr/下/part01/page_0028.txt`、`page_0029.txt`、`page_0068.txt`、`page_0092.txt`、`page_0093.txt`。
- 修复示例：`新建了-批广房`→`新建了一批厂房`，`资金需要口供应`→`资金需要敞口供应`，`50方人`→`50万人`，`第－阶段`→`第一阶段`，补回防火检查开头缺失句。
- 本次替换 {total_replacements} 处；改写章节范围 {changed_total} 个。
- 报告：`output/reports/reader_readability_fiscal_finance_public_20260703.md`。
"""
    append_once(MEMORY, marker, memory)


def main() -> None:
    changed_total, results = patch_reader()
    write_reports(changed_total, results)
    total_replacements = sum(sum(item["counts"].values()) for item in results)  # type: ignore[union-attr]
    print(json.dumps({
        "changed_scopes": changed_total,
        "total_replacements": total_replacements,
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
