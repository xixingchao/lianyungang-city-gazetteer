# -*- coding: utf-8 -*-
"""Batch 47: verified factory/unit OCR fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch47_units_factories_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch47_units_factories_20260706.json"

CHANGES = [
    {
        "old": "连云港绝缘材料厂该广为市属全民企业。",
        "new": "连云港绝缘材料厂该厂为市属全民企业。",
        "section": "绝缘材料厂厂况段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0225.txt:4-5 作连云港绝缘材料厂、该厂为市属全民企业"],
    },
    {
        "old": "一、连云港市水泥厂该厂是生产建筑用水泥的专业工广，",
        "new": "一、连云港市水泥厂该厂是生产建筑用水泥的专业工厂，",
        "section": "连云港市水泥厂简介段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0284.txt:9 作专业工厂"],
    },
    {
        "old": "加工广，生产各种大理石、花岗石及其它石材制品。",
        "new": "加工厂，生产各种大理石、花岗石及其它石材制品。",
        "section": "大理石板材加工厂段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0392.txt:17 作大理石板材专业工厂"],
    },
    {
        "old": "两组35方于瓦的热电站",
        "new": "两组35万千瓦的热电站",
        "section": "华能南京热电站安装段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0321.txt:10 作两组35万千瓦的热电站"],
    },
    {
        "old": "海州发电所1600于瓦发电机组建成投运",
        "new": "海州发电所1600千瓦发电机组建成投运",
        "section": "电力用电发展民国段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0365.txt:12 作1600千瓦发电机组"],
    },
    {
        "old": "年用电475万于瓦时，最高负荷750干瓦。",
        "new": "年用电475万千瓦时，最高负荷750千瓦。",
        "section": "电力用电发展民国负荷段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0365.txt:13-14 作475万千瓦时、750千瓦"],
    },
    {
        "old": "全省用电量15711万于瓦时",
        "new": "全省用电量15711万千瓦时",
        "section": "电力用电发展1949年段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0365.txt:18 附近同段单位为万千瓦时"],
    },
    {
        "old": "用电720方千瓦时",
        "new": "用电720万千瓦时",
        "section": "电力用电发展1957年段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0365.txt:22 作用电720万千瓦时"],
    },
    {
        "old": "人均用电212于瓦时",
        "new": "人均用电212千瓦时",
        "section": "电力用电发展1980年段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0365.txt:36 作人均用电212千瓦时"],
    },
    {
        "old": "年平均负荷为13.9方千瓦",
        "new": "年平均负荷为13.9万千瓦",
        "section": "电力用电发展1990年段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0366.txt:7 作年平均负荷为13.9万千瓦"],
    },
    {
        "old": "每于瓦线路工程贴费",
        "new": "每千瓦线路工程贴费",
        "section": "供电业务扩充贴费段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0375.txt:22-23 作每千瓦线路工程贴费"],
    },
    {
        "old": "每于瓦时0.14元",
        "new": "每千瓦时0.14元",
        "section": "电价1953年段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0377.txt:15 作每千瓦时0.14元"],
    },
    {
        "old": "每月每于瓦7.63元",
        "new": "每月每千瓦7.63元",
        "section": "电价两部制基本电价段",
        "evidence": ["workbench/body_chapters/连云港市志_全书_正文汇总.md:141625 同段电价上下文；单位应为千瓦"],
    },
    {
        "old": "每干瓦时0.105元",
        "new": "每千瓦时0.105元",
        "section": "电价灌溉用电段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0377.txt:15 及同页电价段单位体系为千瓦时"],
    },
    {
        "old": "1.6干瓦高频",
        "new": "1.6千瓦高频",
        "section": "海岸电台发信台设备段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0448.txt:15 作1.6千瓦高频"],
    },
    {
        "old": "供电系统总能力1800干瓦",
        "new": "供电系统总能力1800千瓦",
        "section": "港口机械设备供电能力段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0449.txt:19 作供电系统总能力1800千瓦"],
    },
    {
        "old": "7.5干瓦电动警报器",
        "new": "7.5千瓦电动警报器",
        "section": "人防音响警报器段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part01/page_0189.txt:27 作7.5千瓦电动警报器"],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}: {change['old'][:80]}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修源页闭合且旧串唯一命中的工厂/千瓦单位 OCR 残留；石灰厂 raw OCR 仍错的片段暂缓。未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四十七批：工厂与千瓦单位短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- {item['section']}：`{item['old']}` -> `{item['new']}`（命中 {item['count']} 处）")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版，不改 OCR 原文。",
        "- 每项旧串均要求唯一命中。",
        "- 暂不处理仅 raw OCR 可见且 raw 本身仍错的石灰厂段 `市石灰广/烟简/第建筑公司/进行商`。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
