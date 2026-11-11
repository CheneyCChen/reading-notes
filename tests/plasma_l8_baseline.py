"""Reverse only audited additive Lecture 8 integration for legacy byte tests."""
import re,json
from plasma_illustration_baseline import before_illustrations

def before_lecture8(text):
    text=before_illustrations(text)
    if 'id="lecture8"' not in text:return text
    text=re.sub(r'<!-- PLASMA-L8:(article|nav|node|style):start -->[\s\S]*?<!-- PLASMA-L8:\1:end -->','',text)
    pairs=[('Lecture 1—8','Lecture 1—7'),('LECTURES 01–08','LECTURES 01–07'),('八份讲义','七份讲义'),('八份 PDF','七份 PDF'),('八讲脉络','七讲脉络'),('按 01–08 顺读','按 01–07 顺读'),('更新日期 2026-11-10','更新日期 2026-11-09'),('<strong>8</strong><span>讲原始材料','<strong>7</strong><span>讲原始材料'),('<strong>94</strong><span>页原文逐页对应','<strong>81</strong><span>页原文逐页对应'),('<strong>136</strong><span>个学习单元','<strong>108</strong><span>个学习单元')]
    for a,b in pairs:text=text.replace(a,b)
    text=text.replace('<button data-filter="8">08 MHD 与波</button>','')
    text=text.replace('<a href="#lecture8-s12">06、07 → 08：单流体与闭合选择</a>','')
    def pdfs(m):
        p=json.loads(m[2]);assert len(p)==8 and p[-1]['name']=='Lecture08.pdf'
        return m[1]+json.dumps(p[:-1],ensure_ascii=False,separators=(',',':'))+m[3]
    text=re.sub(r'(<script id="pdf-data"[^>]*>)([\s\S]*?)(</script>)',pdfs,text)
    return text
