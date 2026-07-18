from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

text = HTML.read_text(encoding="utf-8")
needle = " 附录 一、重要文献 山东省鲁中南区新海连特区行政专员公署布告总字第1号案奉："
replacement = (
    "</p>\n"
    "<h2 id=\"附录\">附录</h2>\n"
    "<h3 id=\"附录-一、重要文献\">一、重要文献</h3>\n"
    "<p>山东省鲁中南区新海连特区行政专员公署布告总字第1号案奉："
)

if '<h2 id="附录">附录</h2>' in text:
    raise SystemExit("appendix h2 already present; no change made")
if needle not in text:
    raise SystemExit("appendix split marker not found")

text = text.replace(needle, replacement, 1)
HTML.write_text(text, encoding="utf-8")
print("restored appendix h2/h3 anchor before important documents")
