"""Reversible, section-scoped scientific corrections; fail closed on source drift.
Apply last after historical generators. --reverse removes only this audit layer.
"""
from pathlib import Path
import argparse,json,re
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'reports/plasma-lectures/index.html'
MANIFEST=ROOT/'reports/plasma-lectures/source/scientific-audit/edits.json'
MARKER='<!-- PLASMA-SCIENTIFIC-AUDIT:2026-11-15 -->'
def transform(text,reverse=False):
    if reverse and MARKER not in text:return text
    edits=json.loads(MANIFEST.read_text())['edits']
    for e in reversed(edits) if reverse else edits:
        scope=re.search(r'<section\b[^>]*id="'+re.escape(e['section_id'])+r'"[^>]*>[\s\S]*?</section>',text)
        assert scope, f'Missing audit scope: {e["section_id"]}'
        old,new=(e['new'],e['old']) if reverse else (e['old'],e['new'])
        fragment=scope[0]
        # Handle nested before/after strings correctly in BOTH directions.
        if (old in new and fragment.count(new)==1) or (old not in fragment and fragment.count(new)==1):continue
        assert fragment.count(old)==1, f'Changed/ambiguous audit source: {e["section_id"]}: {old[:60]}'
        text=text[:scope.start()]+fragment.replace(old,new,1)+text[scope.end():]
    if reverse:return text.replace(MARKER,'')
    if MARKER not in text:
        assert text.count('</head>')==1
        text=text.replace('</head>',MARKER+'</head>',1)
    return text
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--reverse',action='store_true');a=p.parse_args()
    PAGE.write_text(transform(PAGE.read_text(),reverse=a.reverse))
    print('Reversed' if a.reverse else 'Applied','scientific audit')
