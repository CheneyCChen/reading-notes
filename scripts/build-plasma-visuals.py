#!/usr/bin/env python3
"""Embed maintained sources into the single-file Plasma course, additively."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
page=ROOT/'reports/plasma-lectures/index.html'
text=page.read_text()
text=re.sub(r'<!-- PLASMA-VISUALS:[\s\S]*?<!-- /PLASMA-VISUALS -->','',text)
coverage=json.loads((ROOT/'reports/plasma-lectures/visual-coverage.json').read_text())
expected={f'lecture{n}-s{i}' for n,count in enumerate([10,13,12,16,18,20],1) for i in range(1,count+1)}
assert {x['sectionId'] for x in coverage}==expected and len(coverage)==89
for item in coverage:
    sid=item['sectionId']
    pattern=r'(<section\b[^>]*\bid="'+re.escape(sid)+r'"[^>]*>[\s\S]*?<h3[^>]*>[\s\S]*?</h3>)'
    block=f'<!-- PLASMA-VISUALS:{sid} --><aside class="study-visual" id="visual-{sid}" aria-label="本节教学可视化"><noscript>本节交互图需启用 JavaScript；原有推导、公式与 PDF 不受影响。</noscript></aside><!-- /PLASMA-VISUALS -->'
    text,count=re.subn(pattern,lambda m:m.group(1)+block,text,count=1)
    assert count==1,sid
css=(ROOT/'assets/plasma-visuals.css').read_text()
text=text.replace('</head>',f'<!-- PLASMA-VISUALS:style --><style>{css}</style><!-- /PLASMA-VISUALS --></head>')
data=json.dumps(coverage,ensure_ascii=False).replace('<','\\u003c')
script=f'<script id="plasma-visual-coverage" type="application/json">{data}</script>'
for name in ['plasma-l12.js','plasma-l34.js','plasma-l5.js','plasma-l6.js','plasma-visuals.js']:
    source=(ROOT/'assets'/name).read_text()
    assert '</script' not in source.lower(),name
    script+='\n<script>\n'+source+'\n</script>'
text=text.replace('</body>','<!-- PLASMA-VISUALS:scripts -->'+script+'<!-- /PLASMA-VISUALS --></body>')
page.write_text(text)
print('Built 89 section visuals with inline offline assets.')

# Refresh the presentation layer after the visual layer has been regenerated.
import runpy
runpy.run_path(str(ROOT/'scripts/sync-editorial.py'))
