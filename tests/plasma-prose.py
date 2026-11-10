"""Verify prose edits are the sole change to all seven original articles.

A reversible, node-level allowlist supplements (never replaces) the original
whole-page, formula, media and source fidelity regressions.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from plasma_prose import ProseNodes, transform, restore_prose_edits, strip_supplements

manifest = json.loads((ROOT / 'reports/plasma-lectures/source/prose-edits.json').read_text())
current = (ROOT / 'reports/plasma-lectures/index.html').read_text()
baseline = subprocess.check_output(['git', 'show', manifest['baseline_commit'] + ':reports/plasma-lectures/index.html'], cwd=ROOT).decode()
assert hashlib.sha256(baseline.encode()).hexdigest() == manifest['baseline_sha256']
assert restore_prose_edits(current) == baseline, 'Change outside reviewed prose text nodes'
assert transform(baseline) == current, 'Prose patch does not reproduce the page'
assert transform(current) == current, 'Prose patch is not idempotent'
assert [x['lecture'] for x in manifest['lectures']] == list(range(1, 8))

all_edits = 0
for lecture in manifest['lectures']:
    number = lecture['lecture']
    pattern = rf'<article id="lecture{number}"[\s\S]*?</article>'
    old, new = (re.search(pattern, s)[0] for s in (baseline, strip_supplements(current)))
    old_nodes, new_nodes = (ProseNodes(s).nodes for s in (old, new))
    assert len(old_nodes) == len(new_nodes)
    # Stripping only ordinary text leaves exact tags, attributes and all KaTeX
    # markup/MathML/TeX bytes, images, links and layout whitespace outside text.
    def protected_bytes(article, nodes):
        for n in reversed(nodes):
            article = article[:n['start']] + article[n['end']:]
        return article
    assert protected_bytes(old, old_nodes) == protected_bytes(new, new_nodes), number
    assert re.findall(r'<h[23][^>]*>[\s\S]*?</h[23]>', old) == re.findall(r'<h[23][^>]*>[\s\S]*?</h[23]>', new), number
    assert [n['section'] for n in old_nodes] == [n['section'] for n in new_nodes]
    actual_edits = [i for i, pair in enumerate(zip(old_nodes, new_nodes)) if pair[0]['text'] != pair[1]['text']]
    assert actual_edits == [e['node'] for e in lecture['edits']]
    for e in lecture['edits']:
        assert '<' not in e['before'] + e['after'] and '>' not in e['before'] + e['after']
        assert e['after'].strip(), 'Do not empty a teaching text node'
    assert len(re.findall(r'class="katex"', new)) == lecture['math_expressions']
    assert len(re.findall(r'data-done=', new)) == lecture['learning_units']
    assert new.count('<details>') == lecture['self_tests']
    all_edits += len(actual_edits)
    print(f'PASS: L{number}: {lecture["learning_units"]} units, {lecture["math_expressions"]} original formulas, {lecture["self_tests"]} quizzes; {len(actual_edits)} reviewed text edits.')
assert len(re.findall(r'class="katex"', current)) == 2122
assert current.count('<details>') == 63
assert len(re.findall(r'data-done=', current)) == 108
print(f'PASS: {all_edits} text edits plus the separately audited mirror-direction correction; all original formulas, markup, figures, PDFs and other course bytes preserved. Full reversal equals {manifest["baseline_commit"][:7]}.')

supplements = json.loads((ROOT / 'reports/plasma-lectures/source/supplements.json').read_text())['blocks']
assert len(supplements) == 24 and supplements[0]['id'] == 'mirror-direction'
assert supplements[0]['html'].count('class="katex"') == 3
assert 'katex-error' not in supplements[0]['html']
assert 'v_\\parallel\\partial_\\parallel B&gt;0' in supplements[0]['html']
assert current.count('id="mirror-direction-correction"') == 1
print('PASS: mirror-work sign correction is labelled, rendered offline, and keeps all original equations.')
