from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/上/总述与大事记.md"),
        "replacements": [
            ("滨海地区牺性的烈士", "滨海地区牺牲的烈士", "workbench/body_chapters/paddle_上/总述与大事记.md:1251"),
            ("为抢救落水社\n员而牺性", "为抢救落水社\n员而牺牲", "workbench/body_chapters/paddle_上/总述与大事记.md:2925-2926"),
            ("追捕两犯中牺性的孙爱国", "追捕两犯中牺牲的孙爱国", "workbench/body_chapters/paddle_上/总述与大事记.md:3348"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_上册_正文汇总.md"),
        "replacements": [
            ("滨海地区牺性的烈士", "滨海地区牺牲的烈士", "workbench/body_chapters/paddle_上/总述与大事记.md:1251"),
            ("为抢救落水社\n员而牺性", "为抢救落水社\n员而牺牲", "workbench/body_chapters/paddle_上/总述与大事记.md:2925-2926"),
            ("追捕两犯中牺性的孙爱国", "追捕两犯中牺牲的孙爱国", "workbench/body_chapters/paddle_上/总述与大事记.md:3348"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("滨海地区牺性的烈士", "滨海地区牺牲的烈士", "workbench/body_chapters/paddle_上/总述与大事记.md:1251"),
            ("为抢救落水社\n员而牺性", "为抢救落水社\n员而牺牲", "workbench/body_chapters/paddle_上/总述与大事记.md:2925-2926"),
            ("追捕两犯中牺性的孙爱国", "追捕两犯中牺牲的孙爱国", "workbench/body_chapters/paddle_上/总述与大事记.md:3348"),
        ],
    },
]

BAD = [old for task in TASKS for old, _, _ in task["replacements"]]


def main():
    changes = []
    for task in TASKS:
        path = ROOT / task["path"]
        text = path.read_text(encoding="utf-8")
        file_changes = []
        for old, new, evidence in task["replacements"]:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            file_changes.append({"old": old, "new": new, "count": count, "evidence": evidence})
        path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": str(task["path"]), "changes": file_changes})

    residuals = {}
    for rel in sorted({str(task["path"]) for task in TASKS}):
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD if text.count(bad)}
        if hits:
            residuals[rel] = hits

    total = sum(item["count"] for file in changes for item in file["changes"])
    report_md = ROOT / "output/reports/upper_chronicle_sacrifice_batch256_20260707.md"
    report_json = ROOT / "output/reports/upper_chronicle_sacrifice_batch256_20260707.json"
    lines = [
        "# 上册大事记牺牲残留修复 batch256",
        "",
        f"- 修复总数：{total}",
        "- 范围：上册总述与大事记旧正文源稿、上册正文汇总、全书正文汇总。当前全书 HTML 已无对应残留。",
        "- 原则：依据上册 PaddleOCR 正文汇总同事件文本定点同步，不处理无证据泛化项。",
        "",
        "## 替换明细",
    ]
    for file in changes:
        lines.append(f"\n### {file['path']}")
        for item in file["changes"]:
            lines.append(f"- `{item['old']}` -> `{item['new']}`；次数 {item['count']}；证据 `{item['evidence']}`")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for rel, hits in residuals.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标文件中均为 0。")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps({"total": total, "changes": changes, "residuals": residuals}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
