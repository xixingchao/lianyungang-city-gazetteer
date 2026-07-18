from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
HTML_PATHS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
REPORT_JSON = ROOT / "output" / "reports" / "volume59_phonology_initials_20260710.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_phonology_initials_20260710.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260710_第五十九卷声母表原文复刻验收.md"

OLD_SOURCE = """一、声母(18)
p帮鼻板布别
p坡瓶浦怕魄
m妈明米梦木
f翻肥粉富福
t灯端顶度笛
t涛同挺兔铁
1拉泥鲁虑糯
招贼主坐织
t村蚕吵醋册
§桑时扫睡拾
z扔人软锐热
to精军酒贱杰
tc秋桥请去确
ε兴贤小线席
k 赶根广贵国
k开狂砍库渴
x花红海汇黑
0牙二然硬闰
1.n、1不分，多数情况下念1。
2. t  的发音部位略靠前，接近 ts tss。
3.f、xu混读，如“飞=灰xuei313、夫=呼 xu³13”。"""

NEW_SOURCE = """一、声母(18)
p帮鼻板布别
p‘坡瓶浦怕魄
m妈明米梦木
f翻肥粉富福
t灯端顶度笛
t‘涛同挺兔铁
l拉泥鲁虑糯
ts招贼主坐织
ts‘村蚕吵醋册
s桑时扫睡拾
z扔人软锐热
tç精军酒贱杰
tç‘秋桥请去确
ç兴贤小线席
k赶根广贵国
k‘开狂砍库渴
x花红海汇黑
0牙二然硬闰
1.n、l不分，多数情况下念l。
2. ts的发音部位略靠前，接近 ts tss。
3.f、xu混读，如“飞=灰xuei313、夫=呼 xu³13”。"""

ROWS = [
    ("p", "帮鼻板布别"),
    ("p‘", "坡瓶浦怕魄"),
    ("m", "妈明米梦木"),
    ("f", "翻肥粉富福"),
    ("t", "灯端顶度笛"),
    ("t‘", "涛同挺兔铁"),
    ("l", "拉泥鲁虑糯"),
    ("ts", "招贼主坐织"),
    ("ts‘", "村蚕吵醋册"),
    ("s", "桑时扫睡拾"),
    ("z", "扔人软锐热"),
    ("tç", "精军酒贱杰"),
    ("tç‘", "秋桥请去确"),
    ("ç", "兴贤小线席"),
    ("k", "赶根广贵国"),
    ("k‘", "开狂砍库渴"),
    ("x", "花红海汇黑"),
    ("0", "牙二然硬闰"),
]

OLD_HTML_TABLE = """<h5>一、声母(18)</h5><table class="dialect-phonology-table"><caption>声母(18)</caption><thead><tr><th>声母</th><th>例字</th></tr></thead><tbody><tr><td>p</td><td>帮鼻板布别</td></tr><tr><td>p</td><td>坡瓶浦怕魄</td></tr><tr><td>m</td><td>妈明米梦木</td></tr><tr><td>f</td><td>翻肥粉富福</td></tr><tr><td>t</td><td>灯端顶度笛</td></tr><tr><td>t</td><td>涛同挺兔铁</td></tr><tr><td>1</td><td>拉泥鲁虑糯</td></tr><tr><td></td><td>招贼主坐织</td></tr><tr><td>t</td><td>村蚕吵醋册</td></tr><tr><td>§</td><td>桑时扫睡拾</td></tr><tr><td>z</td><td>扔人软锐热</td></tr><tr><td>to</td><td>精军酒贱杰</td></tr><tr><td>tc</td><td>秋桥请去确</td></tr><tr><td>ε</td><td>兴贤小线席</td></tr><tr><td>k</td><td>赶根广贵国</td></tr><tr><td>k</td><td>开狂砍库渴</td></tr><tr><td>x</td><td>花红海汇黑</td></tr><tr><td>0</td><td>牙二然硬闰</td></tr></tbody></table><p>1.n、1不分，多数情况下念1。</p>
<p>2. t  的发音部位略靠前，接近 ts tss。</p>
<p>3.f、xu混读，如“飞=灰xuei313、夫=呼 xu³13”。</p>"""

NEW_HTML_TABLE = (
    '<h5>一、声母(18)</h5><table class="dialect-phonology-table"><caption>声母(18)</caption>'
    '<thead><tr><th>声母</th><th>例字</th></tr></thead><tbody>'
    + "".join(f"<tr><td>{html.escape(initial)}</td><td>{chars}</td></tr>" for initial, chars in ROWS)
    + "</tbody></table><p>1.n、l不分，多数情况下念l。</p>\n"
    + "<p>2. ts的发音部位略靠前，接近 ts tss。</p>\n"
    + "<p>3.f、xu混读，如“飞=灰xuei313、夫=呼 xu³13”。</p>"
)


def replace_once(path: Path, old: str, new: str) -> dict[str, str | int]:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path} expected 1 match, got {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    return {"path": str(path.relative_to(ROOT)), "count": count}


def main() -> None:
    changes = []
    for path in SOURCE_PATHS:
        changes.append(replace_once(path, OLD_SOURCE, NEW_SOURCE) | {"kind": "source"})
    for path in HTML_PATHS:
        changes.append(replace_once(path, OLD_HTML_TABLE, NEW_HTML_TABLE) | {"kind": "html"})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "generated_at": now,
        "scope": "第五十九卷 方言 第二章语音系统 第一节声韵调 一、声母(18)",
        "evidence": [
            "workbench/dialect_ipa_review/20260709/pdf_page_0300_声母表_288dpi.jpg",
            "output/final_reader/obsolete/连云港市志_最终阅读版.html 声母残留 OCR",
            "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md 同卷后文转写体系",
        ],
        "rows": [{"initial": initial, "examples": chars} for initial, chars in ROWS],
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 第五十九卷声母表原文复刻验收",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷方言，第二章语音系统，第一节声韵调，`一、声母(18)`。",
        "- 本段动作：只修复声母表和表下注释中的 OCR 代字；不改韵母、声调、表59-1、表59-2。",
        "- 本地证据：`workbench/dialect_ipa_review/20260709/pdf_page_0300_声母表_288dpi.jpg`。",
        "- 交叉依据：旧版残留 OCR 与同卷后文转写体系，采用书内已有的 `p‘/t‘/ts‘/tç/tç‘/ç/k‘` 写法。",
        "",
        "## 声母表",
        "",
        "| 声母 | 例字 |",
        "|---|---|",
    ]
    lines.extend(f"| `{initial}` | {chars} |" for initial, chars in ROWS)
    lines += [
        "",
        "## 同步文件",
        "",
        "| 类型 | 文件 |",
        "|---|---|",
    ]
    lines.extend(f"| {c['kind']} | `{c['path']}` |" for c in changes)
    lines += [
        "",
        "## 待验收命令",
        "",
        "- `python scripts/audit_dialect_volume59_20260709.py`",
        "- `python scripts/audit_full_reader.py`",
        "- `python scripts/audit_delivery_quality.py`",
        "- `python scripts/audit_body_source_integrity_20260709.py`",
    ]
    report_text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report_text, encoding="utf-8")
    PROGRESS_MD.write_text(report_text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
