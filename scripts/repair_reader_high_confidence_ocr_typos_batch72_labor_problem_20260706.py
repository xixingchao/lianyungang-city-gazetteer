from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十二批_劳动力管理问题.md"

OLD = "国务院“关于控制各企、事业单位的人员增长和加强劳动力管理同题的指示”"
NEW = "国务院“关于控制各企、事业单位的人员增长和加强劳动力管理问题的指示”"


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise SystemExit(f"expected exactly 1 hit, got {count}")
    HTML.write_text(text.replace(OLD, NEW), encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七十二批：劳动力管理问题",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
        f"- `{OLD}` -> `{NEW}`（命中 1 处）",
        "",
        "## 证据与边界",
        "",
        "- 位置：`output/final_reader/连云港市志_全书.html` 第四十九卷《劳动人事》劳动力调配段。",
        "- 同页 OCR：`workbench/ocr/paddle_ocr/下/part01/page_0245.txt` 与 `workbench/ocr/raw/下/part01/page_0245.txt` 上一行均为 `关于控制各企、事业单位的人员增长和加强劳动力管理`，下一行受页锚/换行影响在正文汇总中残留为 `同题的指示`。",
        "- 判定：公文标题语境应为 `关于...问题的指示`，`同题` 为 `问题` 形近 OCR 残留；仅修唯一命中的完整引号标题。",
        "- `劳改队撤销，并人徐州第四监狱` 双源仍作 `并人`，本批不猜改。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("changed=1")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
