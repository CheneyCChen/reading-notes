"""Lecture 7 source fidelity, static/offline rendering and additive integration."""
from pathlib import Path
from html.parser import HTMLParser
import re, json, base64, hashlib, subprocess
from plasma_baseline import restore_prose_edits
from plasma_prose import strip_supplements

ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT/'reports/plasma-lectures'
text=(COURSE/'index.html').read_text()
article=strip_supplements(re.search(r'<article id="lecture7"[\s\S]*?</article>',text)[0])
source='\n'.join((COURSE/'source'/f'lecture07-part{i}.tex').read_text() for i in (1,2))
expected_tags=re.findall(r'\\tag\{([^}]+)\}',source)
actual_tags=re.findall(r'data-equation="([^\"]+)"',article)
assert actual_tags==expected_tags and len(actual_tags)==73
assert len(re.findall(r'data-done="lecture7-s\d+"',article))==19
assert len(re.findall(r'id="lecture\d+-s\d+"',text))==108
assert article.count('<details>')==14 and text.count('<details>')==63
assert len(re.findall(r'class="footnote-ref"',article))==5
assert article.count('class="correction"')==source.count(r'\begin{correction}')==11
assert article.count('class="learning-note"')==18
assert article.count('class="katex"')==441
assert not any(x in article for x in ['katex-error','class="math display"','class="math inline"','<canvas','study-visual','<img'])
assert 'Braginskii, S. I. 1965' in article and 'Dodin, I. Y. 2022' in article

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.ids=[]; self.links=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='a' and attrs.get('href','').startswith('#') and attrs['href']!='#':self.links.append(attrs['href'][1:])
parsed=Links();parsed.feed(text)
assert len(parsed.ids)==len(set(parsed.ids)), 'Duplicate HTML ID'
assert set(parsed.links)<=set(parsed.ids), 'Broken internal anchor'

pdf_pattern=r'<script id="pdf-data"[^>]*>([\s\S]*?)</script>'
pdfs=json.loads(re.search(pdf_pattern,text)[1]);assert len(pdfs)==7
assert sum(p['pages'] for p in pdfs)==81
bytes7=base64.b64decode(pdfs[6]['base64'],validate=True)
assert bytes7==(COURSE/'source/Lecture07.pdf').read_bytes()
assert hashlib.sha256(bytes7).hexdigest()==pdfs[6]['sha256']=='f8e1fd0bea5479bdd076f616ae229a63fc9c8be995c68405d7da48f431407176'

# This independent baseline predates both the demonstration additions and L7.
original=subprocess.check_output(['git','show','2089306bf1347d46a534e9ea8eecde1be17d43ce:reports/plasma-lectures/index.html'],cwd=ROOT).decode()
without_visuals=re.sub(r'<!-- PLASMA-VISUALS:[\s\S]*?<!-- /PLASMA-VISUALS -->','',restore_prose_edits(text))
for lecture in range(1,7):
    pattern=rf'<article id="lecture{lecture}"[\s\S]*?</article>'
    assert re.search(pattern,without_visuals)[0]==re.search(pattern,original)[0],f'Lecture {lecture} changed'
assert pdfs[:6]==json.loads(re.search(pdf_pattern,original)[1])
print('PASS: L7 has 19 units, 73 original equation tags, 14 answered source questions, 5 footnotes, 11 corrections, 441 offline math nodes; 7 exact PDFs, 81 pages, all first-six lecture articles unchanged outside audited prose edits; unique IDs and valid internal links.')
