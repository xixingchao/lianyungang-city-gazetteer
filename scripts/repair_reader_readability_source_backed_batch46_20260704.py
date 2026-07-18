# -*- coding: utf-8 -*-
"""Forty-sixth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch46_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch46_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十六批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "肉类加工冷库投资", "old": "资40多方元，建成1000吨冷库", "new": "资40多万元，建成1000吨冷库", "source": "workbench/ocr/paddle_ocr/中/part01/page_0071.txt:6"},
    {"label": "异维生素C钠出资", "old": "出资5方元与安徽省生物研究所", "new": "出资5万元与安徽省生物研究所", "source": "workbench/ocr/paddle_ocr/中/part01/page_0100.txt:36"},
    {"label": "豆浆晶生产投资", "old": "投资30方元，在灌云县伊山镇筹建", "new": "投资30万元，在灌云县伊山镇筹建", "source": "workbench/ocr/paddle_ocr/中/part01/page_0105.txt:26"},
    {"label": "红旗化工厂启动资金", "old": "以5方元党费作启动资金", "new": "以5万元党费作启动资金", "source": "workbench/ocr/paddle_ocr/中/part01/page_0141.txt:18"},
    {"label": "锦屏化工厂固定资产", "old": "固定资产原值764方元", "new": "固定资产原值764万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0162.txt:17"},
    {"label": "化工企业产值", "old": "完成产值1524方元", "new": "完成产值1524万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0164.txt:15"},
    {"label": "农药厂搬迁投资", "old": "该厂投资256方元将厂址", "new": "该厂投资256万元将厂址", "source": "workbench/ocr/paddle_ocr/中/part01/page_0171.txt:13"},
    {"label": "橡胶厂利税", "old": "利税106方元", "new": "利税106万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0188.txt:20"},
    {"label": "车辆厂亏损", "old": "亏损241方元", "new": "亏损241万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0206.txt:8"},
    {"label": "传真机利润", "old": "实现利润80.6方元", "new": "实现利润80.6万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0236.txt:30"},
    {"label": "直流伺服电机试制经费", "old": "试制经费1方元", "new": "试制经费1万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0256.txt:9"},
    {"label": "直流伺服电机拨款", "old": "拨款\n6方元", "new": "拨款\n6万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0256.txt:9-10"},
    {"label": "人造水晶技改投资", "old": "该厂投资200方元", "new": "该厂投资200万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0259.txt:25"},
    {"label": "铁氧方块磁体改造投资", "old": "该厂投资53方元", "new": "该厂投资53万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0260.txt:11"},
    {"label": "煤式推板窑投资", "old": "该厂投资22方元", "new": "该厂投资22万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0260.txt:14"},
    {"label": "四机部工艺处拨款", "old": "工艺处又拨款54方元", "new": "工艺处又拨款54万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0264.txt:22"},
    {"label": "建材企业工业总产值", "old": "工业总产值300方元", "new": "工业总产值300万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0284.txt:30"},
    {"label": "耐火材料厂投资", "old": "耐火材料广投资42方元", "new": "耐火材料厂投资42万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0290.txt:36"},
    {"label": "塑料门窗产值", "old": "业总产值150方元", "new": "业总产值150万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0292.txt:21"},
    {"label": "塑料门窗利税", "old": "利税20方元", "new": "利税20万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0292.txt:21"},
    {"label": "勘察节省投资", "old": "节省投资20方元", "new": "节省投资20万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0297.txt:24"},
    {"label": "输电工程总投资", "old": "总投资2166.12方元", "new": "总投资2166.12万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0349.txt:26"},
    {"label": "以工补农支出", "old": "出151方元用于以工补农", "new": "出151万元用于以工补农", "source": "workbench/ocr/paddle_ocr/中/part01/page_0395.txt:35"},
    {"label": "教育事业支出", "old": "95方元用于教育事业", "new": "95万元用于教育事业", "source": "workbench/ocr/paddle_ocr/中/part01/page_0395.txt:35"},
    {"label": "农村集体福利支出", "old": "63方元用\n于农村集体福利事业", "new": "63万元用\n于农村集体福利事业", "source": "workbench/ocr/paddle_ocr/中/part01/page_0395.txt:35-36"},
    {"label": "其它事业投入", "old": "投人366方元", "new": "投入366万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0395.txt:36"},
    {"label": "乡镇轻工业年产值", "old": "年产值85266方元", "new": "年产值85266万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0401.txt:21"},
    {"label": "企业投入资金", "old": "投入资金860方元", "new": "投入资金860万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0411.txt:100"},
    {"label": "镇村工业固定资产", "old": "固定资产原值1095方元", "new": "固定资产原值1095万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0413.txt:4"},
    {"label": "乡镇企业产值", "old": "创产值500方元", "new": "创产值500万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0417.txt:26"},
    {"label": "开发区基建总投资", "old": "基本建设总投资繁计23082方元", "new": "基本建设总投资累计23082万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0424.txt:17"},
    {"label": "青连微电机产值", "old": "产值1867.8方元", "new": "产值1867.8万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0432.txt:28"},
    {"label": "青连微电机税利", "old": "税利148方元", "new": "税利148万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0432.txt:28"},
    {"label": "氨纶公司总投资", "old": "总投资9571方元", "new": "总投资9571万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0433.txt:7"},
    {"label": "外供公司销售额", "old": "销售额2504方元", "new": "销售额2504万元", "source": "workbench/ocr/paddle_ocr/中/part01/page_0485.txt:18"},
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(target["changed"] for target in targets)
    payload = {
        "time": now,
        "scope": "第四十六批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "依据中册 part01 PaddleOCR 分页文本修复化工、电子、建材、电力、乡镇企业和外贸金额单位残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十六批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：依据中册 part01 PaddleOCR 分页文本修复化工、电子、建材、电力、乡镇企业和外贸金额单位残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                lines.append(f"- {item['label']}：依据 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。")
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 第四十六批正文残留回源修复"
    memory = f"""
{marker}
- 依据中册 part01 PaddleOCR 分页文本，修复化工、电子、建材、电力、乡镇企业和外贸段 `方元` 金额单位残留，共 {total} 处。
- 同步目标：`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`；最终阅读版未命中这些旧串。
- 保留旧币/银元、单位表头以及未有完整源证据闭合的残留，继续待核。
- 报告：`output/reports/reader_readability_source_backed_batch46_20260704.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
