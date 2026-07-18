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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_vocab_2597_textflow_followup_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_vocab_2597_textflow_followup_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言词汇2597页断行续修.md"

SOURCE_OLD = "□□t$1313t1313形容快：小树~长\n嗞声3sa出声、讲话：莫~，外边\n大了\n来人了\n跐41滑：路不好走，一下~倒了\n子舅 t41 tçiəu55 子女的舅舅\n翅拐子 ι5 kuε4  翅膀\n仔细鬼 t141 gi55 kuei41 ①吝啬的人②\n□物 s313u 修理：~车子\n形容心细的人\n时气 s3⁵tci 运气：这月~不好，老是\n志 55①量：用竹杆子~~河有多深\n掉钱\n②复秤：管~秤，少一钱罚一斤\n死41①非常：~沉的，抬不动~辈\n志号55x55记号：划道线留个~\n②在：你~哪块去了，找不到\n恣5舒服：透~\n死眼皮 s41i ā41pi35 不机灵,固执\n呲313讽刺、挖苦：说话~人\n死瘟贼$41or313tsei35 沉默寡言的人\n 1313 跑：上了路直~吓~了\n使41①用：~啥写的②累：干活不多\n泚t313喷射：路边水管破了，直~\n~要命\n痴痴霉霉 t1313 1313 mei35 mei35 呆头\n四季莓 55tci55mei35 芸豆\n呆脑，发愣的样子"
SOURCE_NEW = "□□t$1313t1313形容快：小树~长大了\n嗞声3sa出声、讲话：莫~，外边来人了\n跐41滑：路不好走，一下~倒了\n子舅 t41 tçiəu55 子女的舅舅\n翅拐子 ι5 kuε4  翅膀\n仔细鬼 t141 gi55 kuei41 ①吝啬的人②形容心细的人\n□物 s313u 修理：~车子\n时气 s3⁵tci 运气：这月~不好，老是掉钱\n志 55①量：用竹杆子~~河有多深\n②复秤：管~秤，少一钱罚一斤\n死41①非常：~沉的，抬不动~辈\n志号55x55记号：划道线留个~\n②在：你~哪块去了，找不到\n恣5舒服：透~\n死眼皮 s41i ā41pi35 不机灵,固执\n呲313讽刺、挖苦：说话~人\n死瘟贼$41or313tsei35 沉默寡言的人\n 1313 跑：上了路直~吓~了\n使41①用：~啥写的②累：干活不多\n泚t313喷射：路边水管破了，直~\n~要命\n痴痴霉霉 t1313 1313 mei35 mei35 呆头呆脑，发愣的样子\n四季莓 55tci55mei35 芸豆"

HTML_OLD = "<p>□□t$1313t1313形容快：小树~长</p>\n<p>嗞声3sa出声、讲话：莫~，外边</p>\n<p>大了</p>\n<p>来人了</p>\n<p>跐41滑：路不好走，一下~倒了</p>\n<p>子舅 t41 tçiəu55 子女的舅舅</p>\n<p>翅拐子 ι5 kuε4  翅膀</p>\n<p>仔细鬼 t141 gi55 kuei41 ①吝啬的人②</p>\n<p>□物 s313u 修理：~车子</p>\n<p>形容心细的人</p>\n<p>时气 s3⁵tci 运气：这月~不好，老是</p>\n<p>志 55①量：用竹杆子~~河有多深</p>\n<p>掉钱</p>\n<p>②复秤：管~秤，少一钱罚一斤</p>\n<p>死41①非常：~沉的，抬不动~辈</p>\n<p>志号55x55记号：划道线留个~</p>\n<p>②在：你~哪块去了，找不到</p>\n<p>恣5舒服：透~</p>\n<p>死眼皮 s41i ā41pi35 不机灵,固执</p>\n<p>呲313讽刺、挖苦：说话~人</p>\n<p>死瘟贼$41or313tsei35 沉默寡言的人</p>\n<p>1313 跑：上了路直~吓~了</p>\n<p>使41①用：~啥写的②累：干活不多</p>\n<p>泚t313喷射：路边水管破了，直~</p>\n<p>~要命</p>\n<p>痴痴霉霉 t1313 1313 mei35 mei35 呆头</p>\n<p>四季莓 55tci55mei35 芸豆</p>\n<p>呆脑，发愣的样子</p>"
HTML_NEW = "<p>□□t$1313t1313形容快：小树~长大了</p>\n<p>嗞声3sa出声、讲话：莫~，外边来人了</p>\n<p>跐41滑：路不好走，一下~倒了</p>\n<p>子舅 t41 tçiəu55 子女的舅舅</p>\n<p>翅拐子 ι5 kuε4  翅膀</p>\n<p>仔细鬼 t141 gi55 kuei41 ①吝啬的人②形容心细的人</p>\n<p>□物 s313u 修理：~车子</p>\n<p>时气 s3⁵tci 运气：这月~不好，老是掉钱</p>\n<p>志 55①量：用竹杆子~~河有多深</p>\n<p>②复秤：管~秤，少一钱罚一斤</p>\n<p>死41①非常：~沉的，抬不动~辈</p>\n<p>志号55x55记号：划道线留个~</p>\n<p>②在：你~哪块去了，找不到</p>\n<p>恣5舒服：透~</p>\n<p>死眼皮 s41i ā41pi35 不机灵,固执</p>\n<p>呲313讽刺、挖苦：说话~人</p>\n<p>死瘟贼$41or313tsei35 沉默寡言的人</p>\n<p>1313 跑：上了路直~吓~了</p>\n<p>使41①用：~啥写的②累：干活不多</p>\n<p>泚t313喷射：路边水管破了，直~</p>\n<p>~要命</p>\n<p>痴痴霉霉 t1313 1313 mei35 mei35 呆头呆脑，发愣的样子</p>\n<p>四季莓 55tci55mei35 芸豆</p>"
OCR_EVIDENCE = ["workbench/ocr/paddle_ocr/下/part02/page_0313.txt"]
IMAGE_EVIDENCE = ["workbench/conversion/page_images/下/part02/page_0313_180dpi.jpg"]


def replace_exact(path: Path, old: str, new: str) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path} expected 1 match, got {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    return {"path": str(path.relative_to(ROOT)), "count": count}


def main() -> None:
    changes = [replace_exact(path, SOURCE_OLD, SOURCE_NEW) for path in SOURCE_PATHS]
    changes.append(replace_exact(HTML, HTML_OLD, HTML_NEW))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "generated_at": now,
        "book_pages": [2597],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "changes": changes,
        "repair": "合并 2597 页方言词汇中 `长大了`、`外边来人了`、`形容心细的人`、`老是掉钱`、`呆头呆脑，发愣的样子` 五处高置信断行。",
        "deferred": "`~要命` 归属未闭合，暂不处理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷方言词汇2597页断行续修",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第四章方言词汇，书页 2597。",
        "- 修复：合并 `小树~长大了`、`外边来人了`、`仔细鬼...②形容心细的人`、`老是掉钱`、`呆头呆脑，发愣的样子`。",
        "- 说明：`~要命` 归属未闭合，本批暂不处理；不改音标、不补词头缺字。",
        "",
        "## 证据路径",
        "",
    ]
    for path in OCR_EVIDENCE:
        lines.append(f"- OCR：`{path}`")
    for path in IMAGE_EVIDENCE:
        lines.append(f"- 本地页图：`{path}`")
    lines.extend(["", "## 改写文件", "", "| 文件 | 命中 |", "|---|---:|"])
    for change in changes:
        lines.append(f"| `{change['path']}` | {change['count']} |")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS_MD.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
