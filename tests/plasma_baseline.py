"""Remove only the documented Lecture 7 additions for whole-page byte regression."""
import re, json

def before_lecture7(text):
    if 'id="lecture7"' not in text:
        return text
    text=re.sub(r'<!-- PLASMA-L7:(nav|article|style):start -->[\s\S]*?<!-- PLASMA-L7:\1:end -->','',text)
    text=text.replace('等离子体物理讲义自学手册 Lecture 1—7','等离子体物理讲义自学手册 Lecture 1—6')
    text=text.replace('LECTURES 01–07','LECTURES 01–06')
    text=text.replace('<strong>7</strong><span>讲原始材料','<strong>6</strong><span>讲原始材料')
    text=text.replace('<strong>81</strong><span>页原文','<strong>69</strong><span>页原文')
    text=text.replace('<strong>108</strong><span>个学习单元','<strong>89</strong><span>个学习单元')
    text=text.replace('七份讲义整理','六份讲义整理')
    text=text.replace('Lecture 6 的流体矩、波与无碰撞闭合 → Lecture 7 的输运与有碰撞闭合。','Lecture 6 的流体矩、波与无碰撞闭合。')
    text=text.replace('<button data-filter="7">07 输运与闭合</button>','')
    text=text.replace('更新日期 2026-11-09 · 本地自学版。七份 PDF','更新日期 2026-10-28 · 本地自学版。六份 PDF')
    pattern=r'(<script id="pdf-data"[^>]*>)([\s\S]*?)(</script>)'
    def restore_pdfs(match):
        pdfs=json.loads(match[2]); assert len(pdfs)==7
        return match[1]+json.dumps(pdfs[:6],ensure_ascii=False,separators=(',',':'))+match[3]
    return re.sub(pattern,restore_pdfs,text)
