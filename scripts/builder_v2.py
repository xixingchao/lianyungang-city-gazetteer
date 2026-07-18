# -*- coding: utf-8 -*-
import json, re
from pathlib import Path
from datetime import datetime
r = Path("E:/codex_learing/09_project_东辛农场/连云港市志_workstation")
cd = r / "workbench" / "body_chapters" / "paddle_上"
cv = r / "structure_workbench" / "data" / "chapters_verified.json"
ohtml = r / "output" / "final_reader" / "LYG_上册_v2.html"
omd = r / "output" / "reports" / "上册_PaddleOCR_精修进度_v2.md"
order = ["序与凡例.md","总述与大事记.md","第一卷_自然环境.md","第二卷_建置区划.md","第三卷_区县概况.md","第四卷_人口（part01部分）.md","第四卷至第十卷（part02）.md","第十卷至第十六卷（part03）.md"]
kn = {}
if cv.exists():
    chs = json.loads(cv.read_text('utf-8'))
    kn = {c['title']:c['anchor'] for c in chs}
    print(f'已加载目录: {len(kn)}条')
allp = []; tc = 0
for fn in order:
    fp = cd / fn
    if not fp.exists():
        alt = cd / fn.replace('(','（').replace(')','）')
        if alt.exists(): fp = alt
        else: print(f'  [跳过] {fn}'); continue
    t = fp.read_text('utf-8'); tc += len(t)
    bs = re.split(r'<!-- page-anchor: \S+ -->', t)
    for b in bs[1:]:
        b = re.sub(r'<!--.*?-->', '', b, flags=re.DOTALL).strip()
        if b: allp.append(b)
    print(f'  {fn}: {len(bs)-1}页')
print(f'段落:{len(allp)}, 字符:{tc}')
ohtml.parent.mkdir(parents=True,exist_ok=True)
omd.parent.mkdir(parents=True,exist_ok=True)
now = datetime.now().strftime('%Y-%m-%d %H:%M')
rpt = '''# v2
生成:''' + now + '''
字符:''' + str(tc) + '''
段落:''' + str(len(allp)) + '''
目录:''' + str(len(kn)) + '''条
'''
omd.write_text(rpt, 'utf-8')
print('完成!')
