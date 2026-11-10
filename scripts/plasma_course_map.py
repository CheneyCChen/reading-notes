"""Idempotently integrate the source-backed, offline seven-lecture map."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'reports/plasma-lectures/source'
NAV = '<a class="nav-major" href="#course-map">七讲脉络网络图</a>'

def strip_course_map(text):
    text = re.sub(r'<!-- PLASMA-COURSE-MAP:start -->[\s\S]*?<!-- PLASMA-COURSE-MAP:end -->\n?', '', text)
    text = re.sub(r'<style id="course-map-style">[\s\S]*?</style>', '', text)
    text = re.sub(r'<script id="course-map-script">[\s\S]*?</script>', '', text)
    return text.replace(NAV, '')


def apply_course_map(text):
    text = strip_course_map(text)
    marker = '<section class="read-guide">'
    assert text.count(marker) == 1
    text = text.replace(marker, (SOURCE / 'course-map.html').read_text() + marker, 1)
    text = text.replace('</head>', '<style id="course-map-style">\n' + (SOURCE / 'course-map.css').read_text() + '\n</style></head>', 1)
    text = text.replace('</body>', '<script id="course-map-script">\n' + (SOURCE / 'course-map.js').read_text() + '\n</script></body>', 1)
    anchor = '<a class="nav-major" href="#overview">总览与学习路线</a>'
    assert text.count(anchor) == 1
    return text.replace(anchor, anchor + NAV, 1)
