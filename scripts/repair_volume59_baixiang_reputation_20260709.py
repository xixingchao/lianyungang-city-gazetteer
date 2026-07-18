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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_baixiang_reputation_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_baixiang_reputation_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷败相词条释义断行修复.md"

SOURCE_OLD = "败相 pe55\nciaη 说别人不是，败坏别\n癞蛙子 le55 ue35\nt青蛙\n人声誉\n癞雕子"
SOURCE_NEW = "败相 pe55\nciaη 说别人不是，败坏别人声誉\n癞蛙子 le55 ue35\nt青蛙\n癞雕子"
HTML_OLD = "<p>败相 pe55</p>\n<p>ciaη 说别人不是，败坏别</p>\n<p>癞蛙子 le55 ue35</p>\n<p>t青蛙</p>\n<p>人声誉</p>\n<p>癞雕子 lε55 ti5313</p>"
HTML_NEW = "<p>败相 pe55</p>\n<p>ciaη 说别人不是，败坏别人声誉</p>\n<p>癞蛙子 le55 ue35</p>\n<p>t青蛙</p>\n<p>癞雕子 lε55 ti5313</p>"


def replace_exact(path: Path, old: str, new: str) -> dict:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path} expected 1 match, got {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    return {"path": str(path.relative_to(ROOT)), "count": count}


def main() -> None:
    changes = []
    for path in SOURCE_PATHS:
        changes.append(replace_exact(path, SOURCE_OLD, SOURCE_NEW))
    changes.append(replace_exact(HTML, HTML_OLD, HTML_NEW))

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"generated_at": now, "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷败相词条释义断行修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷方言第四章方言词汇，书页 2603 附近。",
        "- 依据：OCR、源稿和现行阅读器均显示 `败相 pe55 / ciaη 说别人不是，败坏别 / ... / 人声誉`；语义上应为 `败坏别人声誉`，中间被两栏 OCR 行打断。",
        "- 动作：将 `ciaη 说别人不是，败坏别` 与孤立 `人声誉` 合并为 `ciaη 说别人不是，败坏别人声誉`。",
        "- 说明：本处 `人声誉` 不是方言术语 `入声`，不做 `人声 -> 入声` 替换；不重排相邻右栏词条。",
        "",
        "## 改写文件",
        "",
        "| 文件 | 命中 |",
        "|---|---:|",
    ]
    for c in changes:
        lines.append(f"| `{c['path']}` | {c['count']} |")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS_MD.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
