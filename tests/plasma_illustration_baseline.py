"""Remove only additive illustration blocks for unchanged legacy regressions."""
import re
def before_illustrations(text):
 return re.sub(r'<!-- PLASMA-ILLUSTRATION:([^>]*):start -->[\s\S]*?<!-- PLASMA-ILLUSTRATION:\1:end -->','',text)
