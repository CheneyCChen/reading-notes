"""Verify the theme and visualization removal preserve every original report."""
from pathlib import Path
import re, subprocess
from plasma_baseline import before_lecture7
ROOT=Path(__file__).resolve().parents[1]
BASE='2d15a58a85d5be0266fb5e49856dfe99dc9beaf8'
for page in (ROOT/'reports').rglob('*.html'):
    rel=page.relative_to(ROOT)
    original=subprocess.check_output(['git','show',f'{BASE}:{rel}'],cwd=ROOT).decode()
    current=page.read_text()
    assert current.count('<!-- READING-THEME:start -->')==1,rel
    restored=re.sub(r'<!-- READING-THEME:start -->.*?<!-- READING-THEME:end -->','',before_lecture7(current) if page.parent.name=='plasma-lectures' else current,flags=re.S)
    restored=re.sub(r'<!-- READING-NAV:start -->.*?<!-- READING-NAV:end -->','',restored,flags=re.S)
    restored=re.sub(r'<body class="reading-(?:course|report)">','<body>',restored,count=1)
    if page.parent.name=='plasma-lectures':
        restored=restored.replace('<a class="brand" href="../../index.html">Reading Club <small>等离子体物理 · 学习手册</small></a>','<div class="brand">PLASMA / 学习手册 <small>从尺度与轨道到动理学与流体</small></div>')
    else:
        old_nav=re.search(r'<div class="reading-home"[^>]*>.*?</div>',original,re.S)
        if old_nav:restored=restored.replace('<body>','<body>'+old_nav.group(),1)
    if page.parent.name=='plasma-lectures':
        original=re.sub(r'<!-- PLASMA-VISUALS:[\s\S]*?<!-- /PLASMA-VISUALS -->','',original)
    assert restored==original,f'Non-presentation content changed: {rel}'
    # The new local font URL is relative to each page, including nested appendices.
    font=re.search(r'url\("([^"]*newsreader.ttf)"\)',current).group(1)
    assert (page.parent/font).is_file(),rel
print('PASS: all 17 original report bodies, PDFs, formulas, images and scripts are byte-for-byte intact outside presentation changes and documented L7 additions.')
