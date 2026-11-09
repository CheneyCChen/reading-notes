"""Full-coverage, additive-content and offline-asset checks."""
import re,json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'reports/plasma-lectures/index.html'
text=p.read_text(); coverage=json.loads((p.parent/'visual-coverage.json').read_text())
assert len(coverage)==89 and len({x['sectionId'] for x in coverage})==89
for item in coverage:
    assert text.count('id="visual-'+item['sectionId']+'"')==1
    assert item['moduleId'] and len(item['note'])>15
restored=re.sub(r'<!-- PLASMA-VISUALS:[\s\S]*?<!-- /PLASMA-VISUALS -->','',text)
# Remove only the documented presentation layer and restore the old masthead.
restored=re.sub(r'<!-- READING-THEME:start -->[\s\S]*?<!-- READING-THEME:end -->','',restored)
restored=restored.replace('<body class="reading-course">','<body>')
restored=restored.replace('<a class="brand" href="../../index.html">Reading Club <small>等离子体物理 · 学习手册</small></a>','<div class="brand">PLASMA / 学习手册 <small>从尺度与轨道到动理学与流体</small></div>')
original=subprocess.check_output(['git','show','2089306bf1347d46a534e9ea8eecde1be17d43ce:reports/plasma-lectures/index.html'],cwd=root).decode()
assert restored==original,'Original lesson/PDF bytes changed outside generated visual additions'
for filename in ['plasma-l12.js','plasma-l34.js','plasma-l5.js','plasma-l6.js','plasma-visuals.js','plasma-visuals.css']:
    assert (root/'assets'/filename).read_text() in text,filename
assert 'labs/index.html' not in text and 'reading-lab-frame' not in text
print('PASS: 89 unique inline sections; all module sources embedded offline; original course bytes/PDFs intact; no standalone lab links.')
