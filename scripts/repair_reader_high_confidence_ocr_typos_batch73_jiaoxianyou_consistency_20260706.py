from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十三批_焦献猷一致性.md"

OLD = "知州冯超、焦献献继续办理。"
NEW = "知州冯超、焦献猷继续办理。"


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise SystemExit(f"expected exactly 1 hit, got {count}")
    HTML.write_text(text.replace(OLD, NEW), encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七十三批：焦献猷一致性",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
        f"- `{OLD}` -> `{NEW}`（命中 1 处）",
        "",
        "## 证据与边界",
        "",
        "- 同书人物条：`workbench/ocr/paddle_ocr/下/part02/page_0383.txt` 明确作 `焦献猷(？~？）字元臣，清陕西榆阳人，由岁贡生入仕，海州知州`，并记其 `捐出俸禄，为地方开设义学`。",
        "- 当前修复处为教育卷社学、义学段，列 `知州杨宗礼`、`知州冯超` 后续办社学者，语境与人物条的海州知州、兴办义学事迹一致。",
        "- 教育页自身 OCR 汇总仍作 `焦献献`，本批仅依据同书已闭合人物条做唯一姓名一致性修复，不扩展到其他人名。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("changed=1")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
