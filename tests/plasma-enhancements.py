"""Verify the map, additive supplements, source formulas and offline markup."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib, html, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from plasma_prose import supplement_html
SOURCE=ROOT/'reports/plasma-lectures/source'
page=(SOURCE.parent/'index.html').read_text()
from plasma_l8_baseline import before_lecture8
page=before_lecture8(page)
blocks=json.loads((SOURCE/'supplements.json').read_text())['blocks']
index=json.loads((SOURCE/'derivations/index.json').read_text())
expr=json.loads((SOURCE/'derivations/math-expressions.json').read_text())
assert len(index)==17 and len(expr)==266
assert sum(e['display'] for e in expr)==69
assert sum(not e['display'] for e in expr)==197
assert hashlib.sha256((SOURCE/'derivations/derivation-supplements.original.md').read_bytes()).hexdigest()=='333fb7e4c20bf3e98475e5b5ce1b8f6fdf4a66043d355ec9681ad055b55f32df'
original_display=re.findall(r'\\\[(.*?)\\\]',(SOURCE/'derivations/derivation-supplements.original.md').read_text(),re.S)
rendered_display=iter(e['tex'] for e in expr if e['display'])
for tex in original_display:assert any(tex.strip()==nexttex.strip() for nexttex in rendered_display)
assert len(original_display)==65
for item in index:
    block=next(b for b in blocks if b['id']==item['id'])
    fragment=supplement_html(block)
    assert page.count(fragment)==1,item['id']
    annotations=[html.unescape(t) for t in re.findall(r'<annotation encoding="application/x-tex">([\s\S]*?)</annotation>',fragment)]
    assert annotations==[e['tex'] for e in expr if e['id']==item['id']],item['id']
    assert len(annotations)==item['rendered_math_expressions']
    assert '<section' not in fragment and '<details>' not in fragment
    assert fragment.count('class="derivation-details"')==int(item['collapsed'])
    assert 'katex-error' not in fragment
    assert not any(token in fragment for token in ['\\[','\\]','\\(','\\)'])

class Structure(HTMLParser):
    def __init__(self):super().__init__();self.stack=[];self.ids=[];self.links=[];self.targets={};self.map_nodes=[];self.edges=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);cl=a.get('class','').split()
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':
            href=a.get('href','')
            if href.startswith('#') and href!='#':self.links.append(href[1:])
            if 'course-map-node' in cl:self.map_nodes.append(href)
        if 'course-map-edge' in cl:self.edges+=1
        if 'derivation-supplement' in cl:
            sections=[x['id'] for t,x in self.stack if t=='section' and x.get('id','').startswith('lecture')]
            assert sections and any('prose' in x.get('class','').split() for _,x in self.stack)
            self.targets[a['id']]=sections[-1]
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append((tag,a))
    def handle_endtag(self,tag):
        assert self.stack and self.stack[-1][0]==tag,tag
        self.stack.pop()
    def handle_startendtag(self,tag,attrs):pass
parsed=Structure();parsed.feed(page)
assert len(parsed.ids)==len(set(parsed.ids))
assert set(parsed.links)<=set(parsed.ids)
assert parsed.map_nodes==[f'#lecture{i}' for i in range(1,8)] and parsed.edges==8
assert parsed.targets=={i['id']:i['target_section'] for i in index}
assert page.index('id="course-map"')<page.index('<section class="read-guide">')<page.index('<article id="lecture1"')
assert page.count('class="derivation-details"')==3
assert page.count('class="supplement-crosslinks"')==6
assert page.count('class="katex"')==2122
assert (SOURCE/'course-map.css').read_text() in page
assert (SOURCE/'course-map.js').read_text() in page
assert (SOURCE/'derivations/supplements.css').read_text() in page
print('PASS: seven map nodes/eight relations, 17 additive derivations, 266 new math expressions, six cross-links, three long disclosures; original 65 source formulas preserved; unique IDs, valid links and exact target sections.')
