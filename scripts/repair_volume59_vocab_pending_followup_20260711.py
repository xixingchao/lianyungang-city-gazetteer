from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "volume59_vocab_pending_followup_20260711.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_vocab_pending_followup_20260711.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260711_第五十九卷方言词汇挂起项续修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_REPLACEMENTS = [
    {
        "name": "嫌好识歹音值碎片并行",
        "old": "嫌好识歹 cie35\nx41\nS13\ntε41过份挑剔",
        "new": "嫌好识歹 cie35 x41 S13 tε41过份挑剔",
        "evidence": "书页2613 OCR、源稿、HTML 均显示 `嫌好识歹` 后的 `x41/S13/tε41` 被拆成孤行；合并后只恢复词条行界，不改音值。",
    },
    {
        "name": "嫌废与甜不拉叽释义归位",
        "old": "嫌废 ciē35 fei55 嫌弃：不~饭，孬好都\n甜不拉叽 t‘iě35 pə13 la313 tci313 ①\n行\n甜味不正②盐少味淡：这烫~的",
        "new": "嫌废 ciē35 fei55 嫌弃：不~饭，孬好都行\n甜不拉叽 t‘iě35 pə13 la313 tci313 ①甜味不正②盐少味淡：这烫~的",
        "evidence": "书页2613 `行` 位于 `不~饭，孬好都` 与 `甜不拉叽` 之间，按释义闭合为 `孬好都行`；`①甜味不正②盐少味淡` 为同一词条释义。",
    },
    {
        "name": "不好过邻近双栏释义归位",
        "old": "不好过 pe13 x41 k055 生病了:我~\n刹 e13 勒紧、捆牢：~车(把车上货物\n不好受 e13 x41 s\n捆牢)1麻袋~不死口\n不犯于\npa13 f 55 y35 不值得： ~和\n刹价 se13 tçiqa55 讨价还价后价格降下\n他生气\n的\n不断头 pa13\ntō55 təu35 连续不断：\n吃 13①接受：我不~你这一套②承\n夜里行人~\n受：穿少了~不住冻1一个月工资~不\n不管乎 po13\nkō41 xu313\n不管用：人老\n住花 撩蜂~蜇③拿工资：一个月~二\n眼~\n百块钱",
        "new": "不好过 pe13 x41 k055 生病了:我~\n刹 e13 勒紧、捆牢：~车(把车上货物捆牢)1麻袋~不死口\n不好受 e13 x41 s\n不犯于 pa13 f 55 y35 不值得： ~和他生气\n刹价 se13 tçiqa55 讨价还价后价格降下的\n不断头 pa13 tō55 təu35 连续不断：夜里行人~\n吃 13①接受：我不~你这一套②承受：穿少了~不住冻1一个月工资~不住花 撩蜂~蜇③拿工资：一个月~二百块钱\n不管乎 po13 kō41 xu313 不管用：人老眼~",
        "evidence": "书页2619 OCR、源稿、HTML 均显示左右栏释义交错；本批只把 `刹/不犯于/刹价/不断头/吃/不管乎` 的相邻断裂释义接回原词条。",
    },
    {
        "name": "不空房释义闭合",
        "old": "不空房 pə13 kor55 far35 蜜月中不分\n吃户 a13 xu55 舍得吃的人家\n居",
        "new": "不空房 pə13 kor55 far35 蜜月中不分居\n吃户 a13 xu55 舍得吃的人家",
        "evidence": "书页2619 `居` 为 `蜜月中不分居` 的尾字，被右栏 `吃户` 隔断。",
    },
    {
        "name": "作古正经至着释义归位",
        "old": "作古正经 tua13 ku41 tar55 tcir313\n撇 piə13 舀取液体的上层：~水|~汤1\n一本正经的样儿\n~油\n作害 tua13 xε55 为害\n撇光光 piə 13 kuar313 kuan 打水飘儿\n作腾 tua3 tə 有意吵闹\n撇清 pia13 tcir313 夸耀自己的清白，\n作兴 u13 cir313 ①可能：~不来了\n无过。养汉老婆好~\n②应该：不~这样1这事~你不~\n铁权 tia13 tq³13 挖土工具\n□tu13 用簸箕平筛着簸：把秕子~\n接嘴 tçia313 ei41 乱插话\n出来\n接骨草 tcia313 kue13 541 木 贼\n着 tua13①派：~人去请②受：先前不\n结壮 tçia13 tua 老人身体结实健壮\n知~了谁的气",
        "new": "作古正经 tua13 ku41 tar55 tcir313 一本正经的样儿\n撇 piə13 舀取液体的上层：~水|~汤1~油\n作害 tua13 xε55 为害\n撇光光 piə 13 kuar313 kuan 打水飘儿\n作腾 tua3 tə 有意吵闹\n撇清 pia13 tcir313 夸耀自己的清白，无过。养汉老婆好~\n作兴 u13 cir313 ①可能：~不来了②应该：不~这样1这事~你不~\n铁权 tia13 tq³13 挖土工具\n□tu13 用簸箕平筛着簸：把秕子~出来\n接嘴 tçia313 ei41 乱插话\n接骨草 tcia313 kue13 541 木 贼\n着 tua13①派：~人去请②受：先前不知~了谁的气\n结壮 tçia13 tua 老人身体结实健壮",
        "evidence": "书页2621 OCR、源稿、HTML 均显示 `作古正经/撇/撇清/作兴/□tu/着` 的释义尾部被相邻词条打断；本批只闭合相邻释义。",
    },
]

HTML_REPLACEMENTS = [
    {
        "name": "嫌好识歹音值碎片并行",
        "old": "<p>嫌好识歹 cie35</p>\n<p><span class=\"dialect-word-head\">x41</span></p>\n<p><span class=\"dialect-word-head\">S13</span></p>\n<p>tε41过份挑剔</p>",
        "new": "<p>嫌好识歹 cie35 x41 S13 tε41过份挑剔</p>",
    },
    {
        "name": "嫌废与甜不拉叽释义归位",
        "old": "<p>嫌废 ciē35 fei55 嫌弃：不~饭，孬好都</p>\n<p>甜不拉叽 t‘iě35 pə13 la313 tci313 ①</p>\n<p>行</p>\n<p>甜味不正②盐少味淡：这烫~的</p>",
        "new": "<p>嫌废 ciē35 fei55 嫌弃：不~饭，孬好都行</p>\n<p>甜不拉叽 t‘iě35 pə13 la313 tci313 ①甜味不正②盐少味淡：这烫~的</p>",
    },
    {
        "name": "不好过邻近双栏释义归位",
        "old": "<p>不好过 pe13 x41 k055 生病了:我~</p>\n<p>刹 e13 勒紧、捆牢：~车(把车上货物</p>\n<p>不好受 e13 x41 s</p>\n<p>捆牢)1麻袋~不死口</p>\n<p>不犯于</p>\n<p>pa13 f 55 y35 不值得： ~和</p>\n<p>刹价 se13 tçiqa55 讨价还价后价格降下</p>\n<p>他生气</p>\n<p>的</p>\n<p>不断头 pa13</p>\n<p>tō55 təu35 连续不断：</p>\n<p>吃 13①接受：我不~你这一套②承</p>\n<p>夜里行人~</p>\n<p>受：穿少了~不住冻1一个月工资~不</p>\n<p>不管乎 po13</p>\n<p>kō41 xu313</p>\n<p>不管用：人老</p>\n<p>住花 撩蜂~蜇③拿工资：一个月~二</p>\n<p>眼~</p>\n<p>百块钱</p>",
        "new": "<p>不好过 pe13 x41 k055 生病了:我~</p>\n<p>刹 e13 勒紧、捆牢：~车(把车上货物捆牢)1麻袋~不死口</p>\n<p>不好受 e13 x41 s</p>\n<p>不犯于 pa13 f 55 y35 不值得： ~和他生气</p>\n<p>刹价 se13 tçiqa55 讨价还价后价格降下的</p>\n<p>不断头 pa13 tō55 təu35 连续不断：夜里行人~</p>\n<p>吃 13①接受：我不~你这一套②承受：穿少了~不住冻1一个月工资~不住花 撩蜂~蜇③拿工资：一个月~二百块钱</p>\n<p>不管乎 po13 kō41 xu313 不管用：人老眼~</p>",
    },
    {
        "name": "不空房释义闭合",
        "old": "<p>不空房 pə13 kor55 far35 蜜月中不分</p>\n<p>吃户 a13 xu55 舍得吃的人家</p>\n<p>居</p>",
        "new": "<p>不空房 pə13 kor55 far35 蜜月中不分居</p>\n<p>吃户 a13 xu55 舍得吃的人家</p>",
    },
    {
        "name": "作古正经至着释义归位",
        "old": "<p>作古正经 tua13 ku41 tar55 tcir313</p>\n<p>撇 piə13 舀取液体的上层：~水|~汤1</p>\n<p>一本正经的样儿</p>\n<p>~油</p>\n<p>作害 tua13 xε55 为害</p>\n<p>撇光光 piə 13 kuar313 kuan 打水飘儿</p>\n<p>作腾 tua3 tə 有意吵闹</p>\n<p>撇清 pia13 tcir313 夸耀自己的清白，</p>\n<p>作兴 u13 cir313 ①可能：~不来了</p>\n<p>无过。养汉老婆好~</p>\n<p>②应该：不~这样1这事~你不~</p>\n<p>铁权 tia13 tq³13 挖土工具</p>\n<p>□tu13 用簸箕平筛着簸：把秕子~</p>\n<p>接嘴 tçia313 ei41 乱插话</p>\n<p>出来</p>\n<p>接骨草 tcia313 kue13 541 木 贼</p>\n<p>着 tua13①派：~人去请②受：先前不</p>\n<p>结壮 tçia13 tua 老人身体结实健壮</p>\n<p>知~了谁的气</p>",
        "new": "<p>作古正经 tua13 ku41 tar55 tcir313 一本正经的样儿</p>\n<p>撇 piə13 舀取液体的上层：~水|~汤1~油</p>\n<p>作害 tua13 xε55 为害</p>\n<p>撇光光 piə 13 kuar313 kuan 打水飘儿</p>\n<p>作腾 tua3 tə 有意吵闹</p>\n<p>撇清 pia13 tcir313 夸耀自己的清白，无过。养汉老婆好~</p>\n<p>作兴 u13 cir313 ①可能：~不来了②应该：不~这样1这事~你不~</p>\n<p>铁权 tia13 tq³13 挖土工具</p>\n<p>□tu13 用簸箕平筛着簸：把秕子~出来</p>\n<p>接嘴 tçia313 ei41 乱插话</p>\n<p>接骨草 tcia313 kue13 541 木 贼</p>\n<p>着 tua13①派：~人去请②受：先前不知~了谁的气</p>\n<p>结壮 tçia13 tua 老人身体结实健壮</p>",
    },
]

OCR_EVIDENCE = [
    "workbench/ocr/paddle_ocr/下/part02/page_0329.txt",
    "workbench/ocr/paddle_ocr/下/part02/page_0335.txt",
    "workbench/ocr/paddle_ocr/下/part02/page_0337.txt",
]
IMAGE_EVIDENCE = [
    "workbench/conversion/page_images/下/part02/page_0329_180dpi.jpg",
    "workbench/conversion/page_images/下/part02/page_0335_180dpi.jpg",
    "workbench/conversion/page_images/下/part02/page_0337_180dpi.jpg",
]


def replace_exact(path: Path, replacements: list[dict[str, str]]) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    changes: list[dict[str, object]] = []
    for replacement in replacements:
        old_count = text.count(replacement["old"])
        new_count = text.count(replacement["new"])
        if old_count == 1:
            text = text.replace(replacement["old"], replacement["new"], 1)
            changes.append({"name": replacement["name"], "count": 1, "status": "applied"})
        elif old_count == 0 and new_count == 1:
            changes.append({"name": replacement["name"], "count": 0, "status": "already_applied"})
        else:
            raise RuntimeError(
                f"{path} {replacement['name']} expected old=1 or already-applied new=1, "
                f"got old={old_count}, new={new_count}"
            )
    path.write_text(text, encoding="utf-8", newline="\n")
    return changes


def upsert_memory(entry: str) -> None:
    marker = "## 2026-07-11 第五十九卷方言词汇挂起项续修"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        start = memory.index(marker)
        next_start = memory.find("\n## ", start + 1)
        new_memory = memory[:start].rstrip() + "\n\n" + entry.strip() + "\n"
        if next_start != -1:
            new_memory += "\n" + memory[next_start:].lstrip()
    else:
        new_memory = memory.rstrip() + "\n\n" + entry.strip() + "\n"
    MEMORY.write_text(new_memory, encoding="utf-8")


def main() -> None:
    file_changes = []
    for path in SOURCE_PATHS:
        file_changes.append({"path": str(path.relative_to(ROOT)), "changes": replace_exact(path, SOURCE_REPLACEMENTS)})
    file_changes.append({"path": str(HTML.relative_to(ROOT)), "changes": replace_exact(HTML, HTML_REPLACEMENTS)})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "generated_at": now,
        "book_pages": [2613, 2619, 2621],
        "scope": "第五十九卷第四章方言词汇挂起断行/串栏续修",
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "file_changes": file_changes,
        "repairs": [{"name": r["name"], "evidence": r["evidence"]} for r in SOURCE_REPLACEMENTS],
        "principle": "只闭合 OCR、源稿、HTML 三处同形且相邻释义明确的断行；不猜改音标，不新增词头。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第五十九卷方言词汇挂起项续修",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第四章方言词汇，书页 2613、2619、2621。",
        "- 原则：只闭合 OCR、源稿、HTML 三处同形且相邻释义明确的断行；不猜改音标，不新增词头。",
        "",
        "## 证据路径",
        "",
    ]
    for path in OCR_EVIDENCE:
        lines.append(f"- OCR：`{path}`")
    for path in IMAGE_EVIDENCE:
        lines.append(f"- 本地页图：`{path}`")
    lines.extend(["", "## 本批修复", ""])
    lines.extend(f"- {repair['name']}：{repair['evidence']}" for repair in payload["repairs"])
    lines.extend(["", "## 改写文件", "", "| 文件 | 修复项 | 命中 |", "|---|---|---:|"])
    for file_change in file_changes:
        for change in file_change["changes"]:
            lines.append(f"| `{file_change['path']}` | {change['name']} | {change['count']} |")
    report_text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report_text, encoding="utf-8")
    PROGRESS_MD.write_text(report_text, encoding="utf-8")

    upsert_memory(f"""## 2026-07-11 第五十九卷方言词汇挂起项续修

- 脚本：`scripts/repair_volume59_vocab_pending_followup_20260711.py`。
- 续修第五十九卷第四章方言词汇书页 2613、2619、2621 中已可闭合的挂起断行/串栏，覆盖 `嫌好识歹`、`嫌废/甜不拉叽`、`刹/不犯于/刹价/不断头/吃/不管乎/不空房`、`作古正经/撇/撇清/作兴/□tu/着` 等相邻释义闭合。
- 同步文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`、`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`output/final_reader/连云港市志_全书.html`。
- 报告：`output/reports/volume59_vocab_pending_followup_20260711.md`；进度：`output/reports/progress/20260711_第五十九卷方言词汇挂起项续修.md`。
""")

    print(json.dumps({"changed_files": len(file_changes), "repairs": len(SOURCE_REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
