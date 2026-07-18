from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十四批_双学双比贡献.md"

OLD = "全国妇联开展“双学双比”（即学文化、学技术，比成绩、比责献）竞赛"
NEW = "全国妇联开展“双学双比”（即学文化、学技术，比成绩、比贡献）竞赛"


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise SystemExit(f"expected exactly 1 hit, got {count}")
    HTML.write_text(text.replace(OLD, NEW), encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七十四批：双学双比贡献",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
        f"- `{OLD}` -> `{NEW}`（命中 1 处）",
        "",
        "## 证据与边界",
        "",
        "- 页级 PaddleOCR：`workbench/ocr/paddle_ocr/下/part01/page_0333.txt` 明确作 `比成绩、比贡献`。",
        "- raw OCR：`workbench/ocr/raw/下/part01/page_0333.txt` 与当前 reader 作 `比责献`，判定为 `贡/责` 形近 OCR 残留。",
        "- `双学双比` 固定解释语境为 `学文化、学技术，比成绩、比贡献`，与 PaddleOCR 闭合。",
        "- 本批仅处理该唯一命中，不处理书末 `避选`、`上尽，然长逝`、旧志序文 `编繁` 等证据未闭合硬点；未展示、未嵌入页图。",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("changed=1")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
