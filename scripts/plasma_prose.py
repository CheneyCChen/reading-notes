"""Apply/reverse audited prose-only edits without serializing HTML or touching math.

Original TeX/PDF sources remain unchanged. Reapplying is idempotent; unexpected
source edits fail closed rather than silently overwriting a newer passage.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
from plasma_course_map import apply_course_map, strip_course_map

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'reports/plasma-lectures/source/prose-edits.json'
SUPPLEMENTS = ROOT / 'reports/plasma-lectures/source/supplements.json'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

class ProseNodes(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = [0] + [m.end() for m in re.finditer('\n', text)]
        self.stack = []
        self.nodes = []
        self.feed(text)

    def position(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        protected = (tag in {'script', 'style', 'svg', 'math'} or
                     'katex' in attrs.get('class', '').split() or
                     'data-preserved-math' in attrs)
        if tag not in VOID:
            self.stack.append((tag, protected, attrs.get('id', '')))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1][0] == tag, f'Unbalanced {tag}'
        self.stack.pop()

    def record(self, raw):
        if any(p for _, p, _ in self.stack):
            return
        start = self.position()
        scope = next((sid for _, _, sid in reversed(self.stack) if re.fullmatch(r'lecture\d+-(?:s\d+|quiz|cautions|references)', sid)), '')
        if self.nodes and self.nodes[-1]['end'] == start:
            self.nodes[-1]['end'] += len(raw)
            self.nodes[-1]['text'] += raw
        else:
            self.nodes.append({'start': start, 'end': start + len(raw), 'text': raw, 'section': scope})

    def handle_data(self, data):
        self.record(data)

    def handle_entityref(self, name):
        self.record('&' + name + ';')

    def handle_charref(self, name):
        self.record('&#' + name + ';')


def strip_supplements(text):
    text = re.sub(r'<!-- PLASMA-SUPPLEMENT:([a-z0-9-]+):start -->[\s\S]*?<!-- PLASMA-SUPPLEMENT:\1:end -->', '', text)
    return re.sub(r'<style id="derivation-supplement-style">[\s\S]*?</style>', '', text)


def supplement_html(block):
    return block['html'] if 'html' in block else (SUPPLEMENTS.parent / block['html_file']).read_text()


def apply_supplements(text):
    if not SUPPLEMENTS.exists():
        return text
    for block in json.loads(SUPPLEMENTS.read_text())['blocks']:
        pattern = rf'<article id="lecture{block["lecture"]}"[\s\S]*?</article>'
        match = re.search(pattern, text)
        assert match and match[0].count(block['anchor']) == 1, block['id']
        fragment = f'<!-- PLASMA-SUPPLEMENT:{block["id"]}:start -->' + supplement_html(block) + f'<!-- PLASMA-SUPPLEMENT:{block["id"]}:end -->'
        article = match[0].replace(block['anchor'], fragment + block['anchor'])
        text = text[:match.start()] + article + text[match.end():]
    css = SUPPLEMENTS.parent / 'derivations/supplements.css'
    if css.exists():
        text = text.replace('</head>', '<style id="derivation-supplement-style">\n' + css.read_text() + '\n</style></head>', 1)
    return text


def transform(text, reverse=False, manifest=None, supplements=True):
    text = strip_supplements(text)
    data = manifest if manifest is not None else json.loads(MANIFEST.read_text())
    for lecture in data['lectures']:
        pattern = rf'<article id="lecture{lecture["lecture"]}"[\s\S]*?</article>'
        match = re.search(pattern, text)
        assert match, f'Missing Lecture {lecture["lecture"]}'
        article = match[0]
        nodes = ProseNodes(article).nodes
        changes = []
        for edit in lecture['edits']:
            node = nodes[edit['node']]
            before, after = (edit['after'], edit['before']) if reverse else (edit['before'], edit['after'])
            assert node['section'] == edit['section'], f'Prose scope moved: {edit["section"]}'
            if node['text'] == after:
                continue
            assert node['text'] == before, f'Unreviewed source change: Lecture {lecture["lecture"]}, {edit["section"]}, node {edit["node"]}'
            changes.append((node['start'], node['end'], after))
        for start, end, replacement in reversed(changes):
            article = article[:start] + replacement + article[end:]
        text = text[:match.start()] + article + text[match.end():]
    return apply_course_map(apply_supplements(text)) if supplements and not reverse else text


def restore_prose_edits(text):
    return transform(strip_course_map(text), reverse=True)


if __name__ == '__main__':
    page = ROOT / 'reports/plasma-lectures/index.html'
    current = page.read_text()
    result = transform(current)
    if result != current:
        page.write_text(result)
    print('PASS: reviewed prose edits applied; formulas, markup and sources unchanged.')
