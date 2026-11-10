"""Lecture 8 additive regression and complete source/PDF integrity checks."""
from pathlib import Path
from html.parser import HTMLParser
import re,json,hashlib,base64,subprocess
from plasma_l8_baseline import before_lecture8
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'reports/plasma-lectures/index.html').read_text()
old=subprocess.check_output(['git','show','a51309d004c52408f643d7069ef3d08e47bee96d:reports/plasma-lectures/index.html'],cwd=ROOT).decode()
assert before_lecture8(s)==old,'L8 reversal must reproduce exact published L1–7 page'
a=re.search(r'<article class="lecture" data-lecture="8" id="lecture8">[\s\S]*?</article>',s)[0]
assert len(re.findall(r'data-done="lecture8-s\d+"',a))==28
assert a.count('<details>')==12 and a.count('<figure')==3
assert a.count('class="katex"')==213 and a.count('class="katex-display"')==70
assert 'katex-error' not in a and '{{FIG' not in a
assert not re.search(r'\\\(|\\\)|\$\$',a)
tags=re.findall(r'data-equation="L8-(\d+)',a)
assert set(map(int,tags))==set(range(1,56))
assert s.count('data-done=')==136 and s.count('<details>')==75
pdfs=json.loads(re.search(r'<script id="pdf-data"[^>]*>(.*?)</script>',s,re.S)[1])
assert len(pdfs)==8 and sum(p['pages'] for p in pdfs)==94
pdf=base64.b64decode(pdfs[-1]['base64'],validate=True)
assert pdf==(ROOT/'reports/plasma-lectures/source/Lecture08.pdf').read_bytes()
assert hashlib.sha256(pdf).hexdigest()==pdfs[-1]['sha256']=='7f0e3852b9cfb582c82dd37664d09fb7f99bfb638cd0cacdcd38ca379ce32903'
class Check(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[]
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.append(d['id'])
  if t=='a' and d.get('href','').startswith('#') and d['href']!='#':self.links.append(d['href'][1:])
c=Check();c.feed(s);assert len(c.ids)==len(set(c.ids));assert set(c.links)<=set(c.ids)
print('PASS L08: 28 units, 12 quizzes, all 55 source equation numbers, 213 rendered formulas, 3 figures, exact PDF; byte-perfect reversal to L1–7; eight-lecture metadata and valid links.')
