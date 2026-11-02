"""Check additive report changes and local lab links against the pre-animation baseline."""
from pathlib import Path
import re, subprocess
for name in ['plasma-lectures/index.html','mxh-2021-reading/report.html','symplectic-neural-operator-reading/report.html']:
    path='reports/'+name
    old=subprocess.check_output(['git','show','2089306bf1347d46a534e9ea8eecde1be17d43ce:'+path]).decode()
    new=Path(path).read_text()
    restored=re.sub(r'\n<aside id="lab-[\s\S]*?</aside>\n','',new)
    restored=restored.replace('<script defer src="../../assets/lab-embed.js"></script>\n','')
    assert restored==old, f'Existing content changed: {path}'
    for src in re.findall(r'<iframe[^>]+src="([^"]+)"',new):
        if 'labs/index.html' in src: assert (Path(path).parent/src.split('?')[0]).resolve().is_file()
lecture=Path('reports/plasma-lectures/index.html').read_text()
for anchor in ['lecture2-s5','lecture3-s8','lecture6-s10']:
    assert f'id="{anchor}"' in lecture, anchor
for name in ['lab.js','lab-embed.js','lab-particles.js','lab-geometry.js','lab.css']:
    assert Path('assets',name).is_file()
print('PASS: all original report bytes retained after removing additive embeds; local iframe resources and lecture return anchors exist.')
