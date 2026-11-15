"""Verify precise review scope, preservation and failure on unknown source edits."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from plasma_scientific_audit import transform,MANIFEST,MARKER
page=(ROOT/'reports/plasma-lectures/index.html').read_text()
d=json.loads(MANIFEST.read_text())
base=subprocess.check_output(['git','show',d['baseline_commit']+':reports/plasma-lectures/index.html'],cwd=ROOT).decode()
assert hashlib.sha256(base.encode()).hexdigest()==d['baseline_sha256']
assert transform(base)==page
assert transform(page)==page
assert transform(page,reverse=True)==base
assert transform(base,reverse=True)==base
assert page.count(MARKER)==1
assert len(d['edits'])==26
for e in d['edits']:
 assert all(e.get(k) for k in ['old','new','section_id','reason','source'])
 assert e['old']!=e['new']
 assert re.findall(r'<[^>]*>',e['old'])==re.findall(r'<[^>]*>',e['new']),e['section_id']
 assert re.findall(r'<annotation[^>]*>.*?</annotation>',e['old'],re.S)==re.findall(r'<annotation[^>]*>.*?</annotation>',e['new'],re.S)
 assert not any(x in e['new'] for x in ['\\(','\\[','$$','<script','<style'])
e=d['edits'][0]
try:transform(base.replace(e['old'],'UNREVIEWED_SOURCE_CHANGE',1))
except AssertionError:pass
else:raise AssertionError('Unexpected source change accepted')
for key,n in [('data-done=',136),('class="katex"',2335),('class="plasma-illustration"',8)]:assert page.count(key)==base.count(key)==n
pattern=r'<script id="pdf-data"[^>]*>(.*?)</script>'
assert re.search(pattern,page,re.S)[1]==re.search(pattern,base,re.S)[1]
assert len(json.loads(re.search(pattern,page,re.S)[1]))==8
class Structure(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a' and a.get('href','').startswith('#') and a['href']!='#':self.links.append(a['href'][1:])
c=Structure();c.feed(page);assert len(c.ids)==len(set(c.ids));assert set(c.links)<=set(c.ids)
print('PASS: 26 exact scientific edits; reversible/idempotent/fail-closed; 136 units, 2335 formulas, 8 diagrams and 8 PDFs preserved.')
