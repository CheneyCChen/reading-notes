"""Remove only additive illustration blocks for unchanged legacy regressions."""
import re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from plasma_scientific_audit import transform as scientific_audit
def before_illustrations(text):
 text=scientific_audit(text,reverse=True)
 return re.sub(r'<!-- PLASMA-ILLUSTRATION:([^>]*):start -->[\s\S]*?<!-- PLASMA-ILLUSTRATION:\1:end -->','',text)
