# -*- coding: utf-8 -*-
"""Repair conservative source-body residues already clean in the final reader, batch 112."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第一卷_自然环境.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "body_chapter_source_residues_batch112_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "body_chapter_source_residues_batch112_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_正文源稿残留回补第一百一十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("体育运动项目", "运动项自一直", "运动项目一直"),
    ("水文测报项目", "测报项自", "测报项目"),
    ("人口普查项目指标", "各个项自指标", "各个项目指标"),
    ("环境监测项目", "部分项自超过", "部分项目超过"),
    ("废水治理项目", "治理项自107个", "治理项目107个"),
    ("环保建设项目", "建设项自和技术改造项自", "建设项目和技术改造项目"),
    ("计划技术改造项目", "技术改造项自计划", "技术改造项目计划"),
    ("统计项目年报", "《大中型（限额以上）项自一", "《大中型（限额以上）项目一"),
    ("世行贷款项目审计", "世界银行贷款项自审计", "世界银行贷款项目审计"),
    ("外债洽谈项目", "与外商洽谈项自时", "与外商洽谈项目时"),
    ("外债项目领导", "6任项自领导", "6任项目领导"),
    ("农作物推广品种", "引进推厂鲁三", "引进推广鲁三"),
    ("旱地机械化推广", "赣榆县推厂旱地", "赣榆县推广旱地"),
    ("农技推广站", "农技推厂站", "农技推广站"),
    ("农技推广中心", "农技推厂中心", "农技推广中心"),
    ("纺麻技术推广", "在全国推厂", "在全国推广"),
    ("皮革星火项目", "开发项自获国家", "开发项目获国家"),
    ("进口报批项目批件", "项自批件", "项目批件"),
    ("批准外资项目", "批准项自：113个", "批准项目：113个"),
    ("体育比赛项目", "比赛项自有", "比赛项目有"),
    ("传统体育项目", "传统项自", "传统项目"),
    ("安全技术措施项目", "安全技术措施项自范围", "安全技术措施项目范围"),
    ("安全技术措施表题", "主要项自统计表", "主要项目统计表"),
    ("星火计划项目", "“星火计划”项自", "“星火计划”项目"),
    ("卫生监测项目", "两个项自", "两个项目"),
    ("贝雕生产线项目", "画框条生产线项自", "画框条生产线项目"),
    ("淀粉项目由扬州设计", "项自由扬州", "项目由扬州"),
    ("溴素项目在交流会", "溴素等项自在", "溴素等项目在"),
    ("人造水晶技改项目", "人造水晶技改项自", "人造水晶技改项目"),
    ("粉煤灰优秀项目奖", "国家优秀项自奖", "国家优秀项目奖"),
    ("大修项目审批", "项目审批制度，一般项自", "项目审批制度，一般项目"),
    ("三资项目", "“三资”项自", "“三资”项目"),
    ("开发区项目门槛", "万美元的项自", "万美元的项目"),
    ("开发区项目引进", "开发区项自引进", "开发区项目引进"),
    ("港口重点建设项目", "重点建设项自之一", "重点建设项目之一"),
    ("水利工程项目", "水利工程项自", "水利工程项目"),
    ("幼儿运动会项目", "项自有小皮球", "项目有小皮球"),
    ("体育活动项目", "活动开展的项自", "活动开展的项目"),
    ("中学生运动会项目", "竞赛项自有", "竞赛项目有"),
    ("引进项目投产", "这批项自投产", "这批项目投产"),
    ("共保招标承包", "推厂招标承包", "推行招标承包"),
    ("计算机系统推广", "系统推厂", "系统推广"),
    ("计算机系统推广断行", "统推厂", "统推广"),
    ("县农业技术推广中心", "县农业技术推厂中心", "县农业技术推广中心"),
    ("省运会项目比赛", "8个项自比赛", "8个项目比赛"),
    ("新海电厂", "新海电广", "新海电厂"),
    ("啤酒厂安装项目", "啤酒广安装项自", "啤酒厂安装项目"),
    ("千伏单位", "干伏", "千伏"),
    ("万美元单位", "方美元", "万美元"),
    ("万千瓦时单位", "方千瓦时", "万千瓦时"),
    ("万千瓦单位", "方千瓦", "万千瓦"),
    ("溴素化工", "漠素", "溴素"),
    ("工业溴乙烷", "工业漠乙烷", "工业溴乙烷"),
]

LEFT_UNTOUCHED = [
    "`准海`/`淮海` 类历史地名和机构名未处理，需逐页回源，不能批量改。",
    "海关统计段 `对项自进行解除`/主阅读版 `对项目进行解除` 尚未定位源页，疑似仍需回源，不在本批猜改。",
    "`这是一项自动控制多` 是正常 `一项`，不是 `项自` 残留。",
    "本批不使用、不展示页图。",
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
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        items = []
        for label, old, new in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        for item in items:
            item["verified_new"] = verify.count(item["new"])
        applied.append({"target": str(target), "changed": sum(i["count"] for i in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Conservative repair of residual OCR forms in body_chapter source files; final reader was already clean for these contexts.",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": sum(t["changed"] for t in applied),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文源稿残留回补第一百一十二批：主阅读版反校",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前主阅读版 `output/final_reader/连云港市志_全书.html` 对应语境已为正形，本批同步修复正文源稿和汇总中的保守残留。",
        "- 只处理 `项目`、`推广`、`千伏`、`万美元`、`万千瓦时`、`溴素`、`电厂` 等上下文确定的 OCR 字形。",
        "",
        "## 统计",
        "",
        f"- 规则：{len(REPLACEMENTS)} 条",
        f"- 本次替换：{payload['changed_this_run']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        if target["changed"]:
            lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text("\n".join(lines) + "\n", encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 源稿残留补修第一百一十二批：正文源稿反校"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 五项交付审计先行通过后，确认用户粘贴的地层/方言混排风险没有以失控形态进入当前主阅读版；主阅读版地层表和方言声母表均已结构化。
- 本批仅同步修正文源稿/汇总中仍残留的高置信 OCR 字形：`项自 -> 项目`、`推厂 -> 推广`、`新海电广 -> 新海电厂`、`干伏 -> 千伏`、`方美元 -> 万美元`、`方千瓦时 -> 万千瓦时`、`漠素 -> 溴素` 等限定上下文。
- 报告：`output/reports/body_chapter_source_residues_batch112_20260706.md`；边界：`准海/淮海` 等历史地名继续不批量改；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
