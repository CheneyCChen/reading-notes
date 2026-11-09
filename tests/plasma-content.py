"""Keep the original course intact and prevent removed visual demos returning."""
import base64
import json
import re
import subprocess
from pathlib import Path
from plasma_baseline import before_lecture7

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / 'reports/plasma-lectures/index.html'
text = page.read_text()
removed_files = [
    'assets/plasma-l12.js', 'assets/plasma-l34.js', 'assets/plasma-l5.js',
    'assets/plasma-l6.js', 'assets/plasma-visuals.js', 'assets/plasma-visuals.css',
    'scripts/build-plasma-visuals.py',
    'reports/plasma-lectures/visual-coverage.json',
    'reports/plasma-lectures/visual-coverage.md',
]
for filename in removed_files:
    assert not (ROOT / filename).exists(), filename
for pattern in ['PLASMA-VISUALS:', 'study-visual', 'plasma-visual-coverage',
                'pv-controls', 'labs/index.html', 'reading-lab-frame']:
    assert pattern not in text, pattern
assert '<canvas' not in text

# Only the documented reading theme and linked masthead differ from the course
# published before the interactive demonstrations were added.
restored = re.sub(r'<!-- READING-THEME:start -->[\s\S]*?<!-- READING-THEME:end -->', '', before_lecture7(text))
restored = restored.replace('<body class="reading-course">', '<body>')
restored = restored.replace(
    '<a class="brand" href="../../index.html">Reading Club <small>等离子体物理 · 学习手册</small></a>',
    '<div class="brand">PLASMA / 学习手册 <small>从尺度与轨道到动理学与流体</small></div>',
)
original = subprocess.check_output([
    'git', 'show',
    '2089306bf1347d46a534e9ea8eecde1be17d43ce:reports/plasma-lectures/index.html',
], cwd=ROOT).decode()
assert restored == original, 'Original lesson, formula, image or PDF bytes changed'
assert len(re.findall(r'id="lecture\d+-s\d+"', text)) == 108
assert text.count('<details>') == 63
pdfs = json.loads(re.search(r'<script id="pdf-data"[^>]*>([\s\S]*?)</script>', text)[1])
assert len(pdfs) == 7
for pdf in pdfs:
    assert base64.b64decode(pdf['base64'], validate=True).startswith(b'%PDF-'), pdf['name']
print('PASS: visual demos remain removed; original six-lecture page is byte-for-byte intact after removing documented L7 additions; 108 lessons, 63 self-tests and seven PDFs.')
