# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed 文曰/诗曰 and nearby relic-volume OCR residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_relic_wenyue_shiyue_batch_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_relic_wenyue_shiyue_batch_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十六批_文物文曰诗曰.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("西郭宝墓木俑", "木器中有8件雕工精美，造型生动的木角", "木器中有8件雕工精美，造型生动的木俑", "workbench/ocr/paddle_ocr/下/part02/page_0085.txt"),
    ("西郭宝墓侍俑", "武士佩2件", "武士俑2件", "workbench/ocr/paddle_ocr/下/part02/page_0085.txt"),
    ("西郭宝墓侍俑2", "侍佣2件", "侍俑2件", "workbench/ocr/paddle_ocr/下/part02/page_0085.txt"),
    ("西郭宝墓女性俑", "是素面女性痛", "是素面女性俑", "workbench/ocr/paddle_ocr/下/part02/page_0085.txt"),
    ("西郭宝墓12字", "3行12学的隶体墨书", "3行12字的隶体墨书", "workbench/ocr/paddle_ocr/下/part02/page_0085.txt"),
    ("西郭宝墓文曰1", "隶书体墨书，文日：“东海", "隶书体墨书，文曰：“东海", "workbench/ocr/paddle_ocr/下/part02/page_0085.txt"),
    ("西郭宝墓文曰2", "隶体墨书，文日：“东海太守宝再拜谒", "隶体墨书，文曰：“东海太守宝再拜谒", "workbench/ocr/paddle_ocr/下/part02/page_0085.txt"),
    ("黄谭庙文曰", "石刻楹联，文日“二圣灵", "石刻楹联，文曰“二圣灵", "workbench/ocr/paddle_ocr/下/part02/page_0093.txt"),
    ("生庆公文曰", "漆雕楹联，文日：“言不二价，童叟", "漆雕楹联，文曰：“言不二价，童叟", "workbench/ocr/paddle_ocr/下/part02/page_0099.txt"),
    ("六神台文曰", "造像铭一处，文日“仙山方士”", "造像铭一处，文曰“仙山方士”", "workbench/ocr/paddle_ocr/下/part02/page_0102.txt"),
    ("王谟诗曰", "记文后代其诗日因巡来至此瞩海", "记文后代其诗曰因巡来至此瞩海", "workbench/ocr/paddle_ocr/下/part02/page_0103.txt"),
    ("王谟北宋", "最早收录于北来阮阅", "最早收录于北宋阮阅", "workbench/ocr/paddle_ocr/下/part02/page_0103.txt"),
    ("归云飞鸟文曰", "崖壁。文日：“归云", "崖壁。文曰：“归云", "workbench/ocr/paddle_ocr/下/part02/page_0103.txt"),
    ("安钝文曰", "【安钝题名】刻在龙洞外西侧石壁。文日：大明", "【安钝题名】刻在龙洞外西侧石壁。文曰：大明", "workbench/ocr/paddle_ocr/下/part02/page_0103.txt"),
    ("林廷玉跋文曰", "诗后跋文日：“弘治十二年余", "诗后跋文曰：“弘治十二年余", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("钱泳文曰", "隶书。文白：“吕星垣", "隶书。文曰：“吕星垣", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("卢绍文曰", "楷书。文日：“海州刺史赐排鱼袋", "楷书。文曰：“海州刺史赐绯鱼袋", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("卢绍判官", "军事判宫前左领侍卫", "军事判官前左领侍卫", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("卢绍仝登", "正月十七日全登", "正月十七日仝登", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("张叔夜文曰", "正楷。文日：徽献阁待制知", "正楷。文曰：徽猷阁待制知", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("鳌头山龛", "高120厘米、深10厘米的内。“整头山”三字", "高120厘米、深10厘米的龛内。“鏊头山”三字", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("鳌头山文曰", "皆楷书。文日：“整头山，海州城西", "皆楷书。文曰：“鏊头山，海州城西", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("鳌头山鏊首", "实类鑫首，因取", "实类鏊首，因取", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("鳌头山更名", "更其名日整头山", "更其名日鏊头山", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("王梦龄文曰", "字径4厘米。文日：“太子", "字径4厘米。文曰：“太子", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("王梦龄躬游", "梦龄权牧是州，游其盛", "梦龄权牧是州，躬游其盛", "workbench/ocr/paddle_ocr/下/part02/page_0104.txt"),
    ("廖世昭文曰", "字径18厘米。文日：“大明嘉靖葵未岁四月仲夏玉申", "字径18厘米。文曰：“大明嘉靖癸未岁四月仲夏壬申", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("高行清风文曰", "行楷，文日：“高行清风”，款日：“中泉王同为", "行楷，文曰：“高行清风”，款曰：“中泉王同为", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("戴南枝诗曰", "七绝二首，隶书。诗日：“一片寒云复石", "七绝二首，隶书。诗曰：“一片寒云复石", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("戴南枝孰知名", "空岩草木熟知名", "空岩草木孰知名", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("戴南枝堕泪碑", "谁共题君泪碑", "谁共题君堕泪碑", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("五言诗文曰", "7字,隶书。文日：“稳坐石棚上", "7字,隶书。文曰：“稳坐石棚上", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("石棚山海鳌", "“石曼卿读书处”、“夫容洞”、“海整”", "“石曼卿读书处”、“夫容洞”、“海鳌”", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("石棚山可奕枰", "“东皋”、“可奕秤”、“辟烟垒”", "“东皋”、“可奕枰”、“辟烟垒”", "workbench/ocr/paddle_ocr/下/part02/page_0105.txt"),
    ("钱泳款曰", "米。款日：“钱泳题”", "米。款曰：“钱泳题”", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("管干珍文曰", "楷书。文日“俯瞰东滇”", "楷书。文曰“俯瞰东溟”", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("管干珍款曰", "款日：“阳湖管翰珍”", "款曰：“阳湖管幹珍”", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("武同举文曰", "文日：“海上山，云漠漠，西南，飞一角", "文曰：“海上山，云漠漠，迤西南，飞一角", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("武同举款曰", "款白：“乐掌，西山麓，葵丑年，山筑", "款曰：“挹乐亭，西山麓，癸丑年，笏山筑", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("徒然洞曰", "洞之上方，日：“徒然洞”三字", "洞之上方，曰：“徒然洞”三字", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("徒然洞文曰1", "右上首，文日：“观徒然洞偶感", "右上首，文曰：“观徒然洞偶感", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("徒然洞倭寇", "扶桑楼寇兮扰我邦", "扶桑倭寇兮扰我邦", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("徒然洞文曰2", "左上首，文日：“题徒然洞", "左上首，文曰：“题徒然洞", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("徒然洞文曰3", "洞口直上，文日：“题徒然洞", "洞口直上，文曰：“题徒然洞", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("黄窝诗刻文曰1", "文日：“民国十年夏咏龙潭飞雪", "文曰：“民国十年夏咏龙潭飞雪", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("黄窝诗刻文曰2", "张学瀚诗刻侧。文日：“民国辛酉", "张学瀚诗刻侧。文曰：“民国辛酉", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("黄窝陟游泉石", "忠等游泉石，观龙泉飞瀑", "忠等陟游泉石，观龙泉飞瀑", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("黄窝一经枕漱", "时值盛暑，经枕漱，凉澈心脾牌", "时值盛暑，一经枕漱，凉澈心脾", "workbench/ocr/paddle_ocr/下/part02/page_0106.txt"),
    ("东晋纪年砖文曰", "铭文模印在砖的一侧，文日“义熙九年", "铭文模印在砖的一侧，文曰“义熙九年", "workbench/ocr/paddle_ocr/下/part02/page_0117.txt"),
    ("米芾残碑文曰", "字径1.5厘米。文日：“使准安乡太称绍圣于", "字径1.5厘米。文曰：“使淮安乡太称绍圣于", "workbench/ocr/paddle_ocr/下/part02/page_0117.txt"),
    ("江关烟雨文曰", "文日：“江关烟雨图，乾隆庚寅秋月河西王文”", "文曰：“江关烟雨图，乾隆庚寅秋月河西王文”", "workbench/ocr/paddle_ocr/下/part02/page_0119.txt"),
    ("马元驭诗曰", "右上方有诗两行，诗日：“柳斗轻狂", "右上方有诗两行，诗曰：“柳斗轻狂", "workbench/ocr/paddle_ocr/下/part02/page_0120.txt"),
    ("名谒文曰1", "一件3行14字。隶体墨书。文日：“东海", "一件3行14字。隶体墨书。文曰：“东海", "workbench/ocr/paddle_ocr/下/part02/page_0120.txt"),
    ("名谒文曰2", "另件3行12字，隶体墨书。文日：“东海", "另件3行12字，隶体墨书。文曰：“东海", "workbench/ocr/paddle_ocr/下/part02/page_0120.txt"),
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:5]}")
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "PaddleOCR-backed relic-volume 文曰/诗曰 and adjacent OCR residue repair",
        "targets": applied,
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "principle": "Only exact long-context replacements backed by the cited PaddleOCR page are changed.",
        "skipped": "Appendix 顾乾《云台山三十六景》 `诗日` cluster and uncertain names remain unmodified until page evidence closes.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七十六批：文物卷文曰诗曰",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、下册 part02 源稿、全书正文汇总中的文物卷短片段。",
        "- 只处理 PaddleOCR 同页明确支撑的 `文日/诗日/款日` 及同句邻近错字。",
        "- 不处理附录顾乾《云台山三十六景》成片 `诗日`，也不处理 Paddle 读数仍可能牵涉版本差异的人名。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次实际替换：{payload['changed_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第七十六批：文物卷文曰诗曰

- 依据下册 part02 文物卷 PaddleOCR 页 `page_0085`、`page_0093`、`page_0099`、`page_0102`、`page_0103`、`page_0104`、`page_0105`、`page_0106`、`page_0117`、`page_0119`、`page_0120`，修复主阅读版、下册源稿、全书正文汇总中的 `文日/诗日/款日` 及邻近 OCR 残留。
- 典型修复：`文日/诗日/款日` 改为 `文曰/诗曰/款曰`，`木角/女性痛/12学` 改为 `木俑/女性俑/12字`，`整头山/鑫首` 改为 `鏊头山/鏊首`，`俯瞰东滇` 改为 `俯瞰东溟`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_relic_wenyue_shiyue_batch_20260706.md`。
- 暂缓：附录顾乾《云台山三十六景》成片 `诗日` 和个别未闭合人名，继续按页核对，不做全局替换。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第七十六批：文物卷文曰诗曰", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
