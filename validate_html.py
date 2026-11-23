import glob, os
from html.parser import HTMLParser
os.chdir(os.path.dirname(os.path.abspath(__file__)))
VOID={"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
class C(HTMLParser):
    def __init__(s): super().__init__(); s.st=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in VOID: s.st.append(t)
    def handle_endtag(s,t):
        if t in VOID: return
        if not s.st or s.st[-1]!=t: s.err.append(t)
        else: s.st.pop()
bad=0; fs=glob.glob("thirukkural-project/web/*.html")
for f in fs:
    c=C(); c.feed(open(f,encoding="utf-8").read())
    if c.err or c.st: bad+=1; print(f)
print(len(fs),"files, issues:",bad)
