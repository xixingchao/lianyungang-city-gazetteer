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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_vocab_2599_textflow_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_vocab_2599_textflow_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言词汇2599页断行修复.md"
OCR_EVIDENCE = ["workbench/ocr/paddle_ocr/下/part02/page_0315.txt"]
IMAGE_EVIDENCE = ["workbench/conversion/page_images/下/part02/page_0315_180dpi.jpg"]

SOURCE_REPLACEMENTS = [
    ("哩啷 li3131ar313 边讲边骂，或发出别人\n听不清楚的埋怨的话", "哩啷 li3131ar313 边讲边骂，或发出别人听不清楚的埋怨的话"),
    ("理手划风 li41şəu41xua{5far313 说话时乱\n鼻眵 pi35tsι313 鼻垢\n做手势的样儿", "理手划风 li41şəu41xua{5far313 说话时乱做手势的样儿\n鼻眵 pi35tsι313 鼻垢"),
    ("皮衩子p35tα5 下水摸鱼时穿的\n叽吭 tci313kar313 顶嘴：鱼烂腥的提车\n皮衣\n上，问一声还~的", "皮衩子p35tα5 下水摸鱼时穿的皮衣\n叽吭 tci313kar313 顶嘴：鱼烂腥的提车上，问一声还~的"),
    ("迷膛mi313 ta 迷糊、神志不清：吓~\n起圈 tci41 tcyō55 猪发情\n了", "迷膛mi313 ta 迷糊、神志不清：吓~了\n起圈 tci41 tcyō55 猪发情"),
    ("汽露水 tci41 lu55 suei41 蒸气冷凝而成\n迷迷瞪瞪 mi35 mi35 tar313 tər313 没睡好，\n的水滴\n神志不清的神态\n气t55表示指引语气：去吃~，锅里\n米面子 mi41 mi ē55 tl 大米粉\n有", "汽露水 tci41 lu55 suei41 蒸气冷凝而成的水滴\n迷迷瞪瞪 mi35 mi35 tar313 tər313 没睡好，神志不清的神态\n气t55表示指引语气：去吃~，锅里有\n米面子 mi41 mi ē55 tl 大米粉"),
    ("西瓜萝卜 ci313kua³131035pə 甜而脆的红\n护力xu55li13 做事不肯出力\n心萝卜", "西瓜萝卜 ci313kua³131035pə 甜而脆的红心萝卜\n护力xu55li13 做事不肯出力"),
    ("姨侄513妻子的姐妹生的儿女：~\n缕缕ly411y41连续、成群地向前：蚂蚁\n婿\n~的汗~的|~带趟的", "姨侄513妻子的姐妹生的儿女：~婿\n缕缕ly411y41连续、成群地向前：蚂蚁~的汗~的|~带趟的"),
    ("虚嚷 cy313zαr313 表面上邀请一下：中\n午来吃饭，不~", "虚嚷 cy313zαr313 表面上邀请一下：中午来吃饭，不~"),
    ("伏心天 fu35 gir313 tiě313 中伏，夏天最\n热时", "伏心天 fu35 gir313 tiě313 中伏，夏天最热时"),
    ("□tI313 用簸箕轻颠一下，把细小的筛\n□ tu313 长时间煮：~ 鱼\n出", "□tI313 用簸箕轻颠一下，把细小的筛出\n□ tu313 长时间煮：~ 鱼"),
    ("吐 tu55 ①大人用嘴含着食物轻轻吐到\nQ螃trliə 蝉\n婴儿口中②吐出：小孩~饭了", "吐 tu55 ①大人用嘴含着食物轻轻吐到婴儿口中②吐出：小孩~饭了\nQ螃trliə 蝉"),
    ("夜猫子 m313t 猫头鹰，也喻夜间精\n酥瓜șu313 kuq313青色、长形带长条花\n力旺盛的人\n纹的菜瓜，比黄瓜味甜，一般是生吃", "夜猫子 m313t 猫头鹰，也喻夜间精力旺盛的人\n酥瓜șu313 kuq313青色、长形带长条花纹的菜瓜，比黄瓜味甜，一般是生吃"),
    ("钯pq313①补、钉：~盒铜锅②钉子：洋\n苦ku41①挣、赚：~钱②很：~咸\n盆底打了个~子\n~辣", "钯pq313①补、钉：~盒铜锅②钉子：洋盆底打了个~子\n苦ku41①挣、赚：~钱②很：~咸~辣"),
    ("苦夏ku41εiq55有些人在夏天食欲差、\n扒pq313照着样子剪：~鞋样子\n消瘦", "苦夏ku41εiq55有些人在夏天食欲差、消瘦\n扒pq313照着样子剪：~鞋样子"),
    ("苦淫淫 ku41i35ir35 略有苦味：这药~\n把 pa41① 给、送：把东西~给他了\n的", "苦淫淫 ku41i35ir35 略有苦味：这药~的\n把 pa41① 给、送：把东西~给他了"),
    ("②把守、查路：路上有人~岗|小鬼~\n□xu41①泼：~水②撒：~化肥③花\n门③次、回：再来一~(扑克)一~\n费：钱~出去了\n赢了十块", "②把守、查路：路上有人~岗|小鬼~门③次、回：再来一~(扑克)一~赢了十块\n□xu41①泼：~水②撒：~化肥③花费：钱~出去了"),
]

HTML_REPLACEMENTS = [(f"<p>{old.replace(chr(10), '</p>' + chr(10) + '<p>')}</p>", f"<p>{new.replace(chr(10), '</p>' + chr(10) + '<p>')}</p>") for old, new in SOURCE_REPLACEMENTS]
HTML_REPLACEMENTS[15] = (
    "<p>②把守、查路：路上有人~岗|小鬼~</p>\n<p>□xu41①泼：~水②撒：~化肥③花</p>\n<p>门③次、回：再来一~(扑克)一~</p>\n<p>费：钱~出去了</p>\n<p>赢了十块</p>",
    "<p>②把守、查路：路上有人~岗|小鬼~门③次、回：再来一~(扑克)一~赢了十块</p>\n<p>□xu41①泼：~水②撒：~化肥③花费：钱~出去了</p>",
)


def apply_replacements(path: Path, replacements: list[tuple[str, str]]) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    applied = 0
    for old, new in replacements:
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"{path} expected 1 match for {old[:40]!r}, got {count}")
        text = text.replace(old, new, 1)
        applied += 1
    path.write_text(text, encoding="utf-8", newline="\n")
    return {"path": str(path.relative_to(ROOT)), "count": applied}


def main() -> None:
    changes = [apply_replacements(path, SOURCE_REPLACEMENTS) for path in SOURCE_PATHS]
    changes.append(apply_replacements(HTML, HTML_REPLACEMENTS))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "generated_at": now,
        "book_pages": [2599],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "changes": changes,
        "repair": "合并书页2599方言词汇中16组高置信断行/串行释义。",
        "deferred": "不改音标、不补无法闭合的词头；复杂两栏错位继续留待页图逐字精校。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷方言词汇2599页断行修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第四章方言词汇，书页 2599。",
        "- 修复：合并 `哩啷`、`理手划风`、`皮衩子/叽吭`、`迷膛`、`汽露水/迷迷瞪瞪/气`、`西瓜萝卜`、`姨侄/缕缕`、`虚嚷`、`伏心天`、`筛出`、`吐到婴儿口中`、`夜猫子/酥瓜`、`钯/苦`、`苦夏`、`苦淫淫`、`把/□xu` 等 16 组高置信断行。",
        "- 说明：只恢复可由上下文闭合的释义/例句；不改音标、不补无法闭合的词头。",
        "",
        "## 证据路径",
        "",
    ]
    for path in OCR_EVIDENCE:
        lines.append(f"- OCR：`{path}`")
    for path in IMAGE_EVIDENCE:
        lines.append(f"- 本地页图：`{path}`")
    lines.extend(["", "## 改写文件", "", "| 文件 | 替换组 |", "|---|---:|"])
    for change in changes:
        lines.append(f"| `{change['path']}` | {change['count']} |")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS_MD.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
