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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_homophone_2591_io_ime_textflow_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_homophone_2591_io_ime_textflow_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷同音字汇2591页io_ime行界修复.md"

SOURCE_OLD = "p ①飘漂~浮 ②瓢嫖剽 ③瞟~上一\nx ①购 ②侯喉猴瘊 ③吼 ④后厚候\n眼 ④票漂~白\n0 ①欧殴讴鸥区姓沤 ③呕偶藕烟~狼烟\nm ②苗描瞄喵 ③秒眇渺藐 ④庙妙\n④枢\nt ① 雕凋碉刁叼貂 ④吊掉钓调~查\nime\n铫\nt ①挑~水 ②条条调~和答迢 ③挑\nt ①丢\n~选窕 ④跳眺 旐宋~立交桥果"
SOURCE_NEW = "p ①飘漂~浮 ②瓢嫖剽 ③瞟~上一眼 ④票漂~白\nx ①购 ②侯喉猴瘊 ③吼 ④后厚候\n0 ①欧殴讴鸥区姓沤 ③呕偶藕烟~狼烟\nm ②苗描瞄喵 ③秒眇渺藐 ④庙妙\n④枢\nt ① 雕凋碉刁叼貂 ④吊掉钓调~查铫\nime\nt ①挑~水 ②条条调~和答迢 ③挑~选窕 ④跳眺 旐宋~立交桥果\nt ①丢"
HTML_OLD = "<p>p ①飘漂~浮 ②瓢嫖剽 ③瞟~上一</p>\n<p>x ①购 ②侯喉猴瘊 ③吼 ④后厚候</p>\n<p>眼 ④票漂~白</p>\n<p>0 ①欧殴讴鸥区姓沤 ③呕偶藕烟~狼烟</p>\n<p>m ②苗描瞄喵 ③秒眇渺藐 ④庙妙</p>\n<p>④枢</p>\n<p>t ① 雕凋碉刁叼貂 ④吊掉钓调~查</p>\n<p><span class=\"dialect-word-head\">ime</span></p>\n<p>铫</p>\n<p>t ①挑~水 ②条条调~和答迢 ③挑</p>\n<p>t ①丢</p>\n<p>~选窕 ④跳眺 旐宋~立交桥果</p>"
HTML_NEW = "<p>p ①飘漂~浮 ②瓢嫖剽 ③瞟~上一眼 ④票漂~白</p>\n<p>x ①购 ②侯喉猴瘊 ③吼 ④后厚候</p>\n<p>0 ①欧殴讴鸥区姓沤 ③呕偶藕烟~狼烟</p>\n<p>m ②苗描瞄喵 ③秒眇渺藐 ④庙妙</p>\n<p>④枢</p>\n<p>t ① 雕凋碉刁叼貂 ④吊掉钓调~查铫</p>\n<p><span class=\"dialect-word-head\">ime</span></p>\n<p>t ①挑~水 ②条条调~和答迢 ③挑~选窕 ④跳眺 旐宋~立交桥果</p>\n<p>t ①丢</p>"
OCR_EVIDENCE = ["workbench/ocr/paddle_ocr/下/part02/page_0307.txt"]
IMAGE_EVIDENCE = ["workbench/conversion/page_images/下/part02/page_0307_180dpi.jpg"]


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
        "book_pages": [2591],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "changes": changes,
        "repair": "合并 `瞟~上一眼`、`调~查铫`、`挑~选窕` 三处行界；保留 `④枢` 待页图精校。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷同音字汇2591页io_ime行界修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第三章同音字汇，书页 2591。",
        "- 依据：OCR、源稿、全书汇总和阅读器均显示 `瞟~上一/眼`、`调~查/铫`、`挑/~选窕` 三处断行，均可由上下文闭合。",
        "- 修复：合并为 `瞟~上一眼`、`调~查铫`、`挑~选窕`。",
        "- 说明：`④枢` 暂不处理；不改音标、不改字表，只恢复高置信行界。",
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
