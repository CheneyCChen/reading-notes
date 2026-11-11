"""Audit additive diagrams independently; stripping must recover exact L1–8 page."""
from pathlib import Path
import subprocess,re,json,xml.etree.ElementTree as ET
from plasma_illustration_baseline import before_illustrations
R=Path(__file__).resolve().parents[1];p=R/'reports/plasma-lectures/index.html';s=p.read_text()
base=subprocess.check_output(['git','show','c8a831f73623db5c24bd1ed3da48bbb30edacae0:reports/plasma-lectures/index.html'],cwd=R).decode()
assert before_illustrations(s)==base,'Illustrations changed original content'
manifest=json.loads((p.parent/'illustrations/manifest.json').read_text());assert len(manifest)==8
assert s.count('class="plasma-illustration"')==8
for f in manifest:
 svg=(p.parent/f'illustrations/{f["key"]}.svg').read_text();ET.fromstring(svg);assert svg in s
 assert '<title ' in svg and '<desc ' in svg and 'role="img"' in svg
 section=re.search(r'<section\b[^>]*id="'+f['section']+'"[^>]*>[\\s\\S]*?</section>',s)[0]
 assert 'id="fig-'+f['key']+'"' in section
 assert '<script' not in svg and '<image' not in svg
assert 'plasma-visuals.js' not in s
print('PASS: 8 accessible SVG diagrams; exact reversible preservation of all existing L1–8 content.')
