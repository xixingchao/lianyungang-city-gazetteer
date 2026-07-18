# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern residues, batch 109."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch109_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch109_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_包干与乒乓球残留回源补修第一百零九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "新海区财政支出指标包干",
        "old": "市财政对新海区财政试行支出按分配指标包于，节馀留用",
        "new": "市财政对新海区财政试行支出按分配指标包干，节馀留用",
        "source": "workbench/ocr/raw/上/part01/page_0235.txt:35；Paddle 同页误作包于",
    },
    {
        "label": "云台地区财政递增包干",
        "old": "随后实行递增包于、收支挂钩，广开财源等办法",
        "new": "随后实行递增包干、收支挂钩，广开财源等办法",
        "source": "workbench/ocr/raw/上/part01/page_0246.txt:28；Paddle 同页误作包于",
    },
    {
        "label": "财政收入包干范围",
        "old": "按划定的收入包于范围调整核实收入包干基数",
        "new": "按划定的收入包干范围调整核实收入包干基数",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0283.txt:33；raw 同页误作包于",
    },
    {
        "label": "区级财政比例包干",
        "old": "改按“收支挂钩，比例包于”的财政管理体制",
        "new": "改按“收支挂钩，比例包干”的财政管理体制",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0284.txt:16；raw 同页误作包于",
    },
    {
        "label": "财政经营情况递增包干",
        "old": "对经营情况较好的企业，实行“递增包于，超收分成”的办法",
        "new": "对经营情况较好的企业，实行“递增包干，超收分成”的办法",
        "source": "workbench/ocr/raw/中/part02/page_0305.txt:24；Paddle 同页误作包于",
    },
    {
        "label": "预算包干办法",
        "old": "位实行预算包于办法；对基本没有收入",
        "new": "位实行预算包干办法；对基本没有收入",
        "source": "workbench/ocr/raw/中/part02/page_0305.txt:30；Paddle 同页误作包于",
    },
    {
        "label": "农业行政经费包干",
        "old": "按照行政经费包于办法进行包干",
        "new": "按照行政经费包干办法进行包干",
        "source": "workbench/ocr/raw/中/part02/page_0305.txt:33 与上下文包干术语互证",
    },
    {
        "label": "专项经费不列入包干范围",
        "old": "专项结报，不列人包于范围",
        "new": "专项结报，不列入包干范围",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0305.txt:32；raw 同页误作列人包于范围",
    },
    {
        "label": "信贷计划包干",
        "old": "改为“存贷下放、计划包于、差额管理、统一调度”的办法，并在差额包于的基础上改为上、下半年的两次包干",
        "new": "改为“存贷下放、计划包干、差额管理、统一调度”的办法，并在差额包干的基础上改为上、下半年的两次包干",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0389.txt:14-15；raw 同页误作包于",
    },
    {
        "label": "机关工作人员包干费",
        "old": "机关工作人员工资、包于费级别进行调整",
        "new": "机关工作人员工资、包干费级别进行调整",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0206.txt:19；raw 同页误作包于",
    },
    {
        "label": "残疾人李扬乒乓球国际比赛",
        "old": "残疾人李扬3次参加乒丘球国际比赛",
        "new": "残疾人李扬3次参加乒乓球国际比赛",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0218.txt:12；raw 同页误作乒丘球",
    },
    {
        "label": "汉城伤残人运动会乒乓球赛",
        "old": "淮海大学教师李杨在汉城第八届伤残人运动会上乒丘球赛取得第四名",
        "new": "淮海大学教师李杨在汉城第八届伤残人运动会上乒乓球赛取得第四名",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0039.txt:34；raw 同页误作准海大学/乒丘球赛",
    },
    {
        "label": "汉城伤残人运动会乒乓球赛源稿准海残留",
        "old": "准海大学教师李杨在汉城第八届伤残人运动会上乒丘球赛取得第四名",
        "new": "淮海大学教师李杨在汉城第八届伤残人运动会上乒乓球赛取得第四名",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0039.txt:34；源稿断行/旧 OCR 残留",
    },
]

LEFT_UNTOUCHED = [
    "未对 `包于` 做全局替换，只处理财政、信贷、工资段中页级证据闭合的精确短语。",
    "`中西合壁` 与 `并人徐州第四监狱` 仍因 raw/Paddle 未给出更强证据而保留。",
    "道路表等疑似表格压平段不在本批 OCR 短句修复范围内。",
    "本批未使用或展示页图。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        for item in items:
            item["verified"] = verify.count(item["new"])
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Source-backed modern residue repair for 包干 and 乒乓球",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with raw/Paddle page evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 包干与乒乓球残留补修第一百零九批：回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的 `包于/包干` OCR 混淆残留。",
        "- 下册体育段 `乒丘球` 残留。",
        "- 仅处理 raw/Paddle 页级文本可互证的精确短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次运行新增替换：{payload['changed_this_run']} 处",
        f"- 当前核验覆盖：{payload['verified_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百零九批：包干与乒乓球残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 raw/Paddle 页级回源，修复财政、信贷、工资段 `包于 -> 包干` 混淆，专项经费 `列人包于范围`，以及体育段 `乒丘球 -> 乒乓球`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch109_20260706.md`。
- 边界：未对 `包于` 全局替换；`中西合壁`、`并人徐州第四监狱` 和表格压平疑点继续等待更强证据；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
