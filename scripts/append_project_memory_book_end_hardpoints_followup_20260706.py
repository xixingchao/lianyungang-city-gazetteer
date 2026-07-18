from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"
NOTE = """
## 2026-07-06 书末硬点复核补记：避选、上尽
- 复核 `避选`：raw 为 `避选`，整页 Tesseract 为 `遂选`，既有局部 OCR 为 `洒选/迟选`，新增高倍局部 OCR 又读作 `遗选`，多路不一致；语义疑似 `遴选` 但证据未闭合，主阅读版暂不改。
- 复核 `上尽，然长逝`：raw 为 `征途 / 上尽，然长逝` 断行残留，整页和局部 OCR 仍不能稳定读出后半句；主阅读版暂不改。
- 已更新待核记录 `output/reports/progress/20260706_书末剩余硬点待核记录.md`，补入新增局部 OCR 路径和第六十八批 `崇高献身精神` 已处理结论。未展示、未嵌入页图。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 书末硬点复核补记：避选、上尽"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
