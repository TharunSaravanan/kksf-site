import os,re,sys,glob,json
ROOT=os.path.dirname(os.path.abspath(__file__))
PAT=re.compile("con"+"fuci|ana"+"lects|men"+"cius|xun"+"zi|con"+"fucian",re.I)
SKIP={".git","node_modules","_rejected"}
hits=[]
for dp,dn,fn in os.walk(ROOT):
    dn[:]=[d for d in dn if d not in SKIP]
    for f in fn:
        if not f.endswith((".html",".json",".py",".js",".md",".txt",".kt",".swift",".xml",".css",".csv",".docx",".dart",".gradle")) or f=="removed_check.py": continue
        p=os.path.join(dp,f)
        try:
            data=open(p,"rb").read()
            if f.endswith(".docx"):
                import zipfile; data=b" ".join(zipfile.ZipFile(p).read(n) for n in zipfile.ZipFile(p).namelist() if n.endswith(".xml"))
            if PAT.search(data.decode("utf-8","ignore")): hits.append(os.path.relpath(p,ROOT))
        except Exception as e: pass
print("removed_check hits:",len(hits))
for h in hits[:50]: print(" ",h)
sys.exit(1 if hits else 0)
