"""Apply the shared editorial theme without reserializing report contents.

Theme CSS and JavaScript are inlined so standalone report downloads retain their
layout and controls. Newsreader is local to the site; standalone files fall back
to installed serif fonts. Original math, figures, PDFs and scripts are untouched.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
css = (ROOT / 'assets/editorial.css').read_text()
js = (ROOT / 'assets/theme.js').read_text()
for page in sorted((ROOT / 'reports').rglob('*.html')):
    content = page.read_text()
    prefix = '../' * len(page.relative_to(ROOT).parent.parts)
    content = re.sub(r'<!-- READING-THEME:start -->.*?<!-- READING-THEME:end -->', '', content, flags=re.S)
    theme = css.replace('url("fonts/', f'url("{prefix}assets/fonts/')
    content = content.replace('</head>', f'<!-- READING-THEME:start --><style>{theme}</style><script>{js}</script><!-- READING-THEME:end --></head>')
    course = page.parent.name == 'plasma-lectures'
    body_class = 'reading-course' if course else 'reading-report'
    content = re.sub(r'<body(?: class="reading-(?:course|report)")?>', f'<body class="{body_class}">', content, count=1)
    if course:
        content = content.replace('<div class="brand">PLASMA / 学习手册 <small>从尺度与轨道到动理学与流体</small></div>', '<a class="brand" href="../../index.html">Reading Club <small>等离子体物理 · 学习手册</small></a>')
    else:
        content = re.sub(r'<div class="reading-home"[^>]*>.*?</div>', '', content, flags=re.S)
        content = re.sub(r'<!-- READING-NAV:start -->.*?<!-- READING-NAV:end -->', '', content, flags=re.S)
        nav = f'<!-- READING-NAV:start --><div class="reading-masthead"><a href="{prefix}index.html" aria-label="返回 Reading Club">Reading Club</a><button class="theme-toggle" data-theme-toggle aria-label="切换到深色模式" aria-pressed="false" title="切换到深色模式"></button></div><!-- READING-NAV:end -->'
        content = content.replace(f'<body class="{body_class}">', f'<body class="{body_class}">{nav}', 1)
    page.write_text(content)
print('Updated 17 report and course pages.')
