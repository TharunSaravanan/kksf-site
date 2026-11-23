#!/usr/bin/env python3
"""Add bookmarks (Book > Chapter > Kural) and metadata to the LibreOffice-exported book PDF.
usage: finalize_pdf.py in.pdf out.pdf kurals.json"""
import re, sys, json, subprocess, pypdf
src, out, kj = sys.argv[1:4]
txt = subprocess.run(['pdftotext', '-layout', src, '-'], capture_output=True, text=True).stdout
pages = txt.split('\f')
km = {}
for i, p in enumerate(pages, 1):
    for l in [l.strip() for l in p.split('\n') if l.strip()][:3]:
        m = re.fullmatch(r'Kural (\d+)', l)
        if m: km.setdefault(int(m.group(1)), i)
assert len(km) == 1330, len(km)
def find(t):
    for i, p in enumerate(pages, 1):
        if any(l.strip() == t for l in p.split('\n')[:8]): return i
kur = json.load(open(kj))
w = pypdf.PdfWriter(clone_from=pypdf.PdfReader(src))
w.add_outline_item("Cover", 0); w.add_outline_item("Contents", 1)
w.add_outline_item("About This Guide", find("About This Guide")-1)
w.add_outline_item("History of the Thirukkural", find("History of the Thirukkural")-1)
for bn, a, b in [("Book I · Aram — Virtue",1,38),("Book II · Porul — Wealth and Statecraft",39,108),("Book III · Inbam — Love",109,133)]:
    bp = w.add_outline_item(bn, km[(a-1)*10+1]-1)
    for c in range(a, b+1):
        k = kur[(c-1)*10]['adhikaram']
        cp = w.add_outline_item(f"{c}. {k['english']} · {k['tamil']} (kurals {(c-1)*10+1}–{c*10})", km[(c-1)*10+1]-1, parent=bp)
        for n in range((c-1)*10+1, c*10+1):
            w.add_outline_item(f"Kural {n}", km[n]-1, parent=cp)
w.add_metadata({"/Title":"The Thirukkural — A Cross-Traditional Study Edition","/Author":"Thirukkural Translation Project","/Subject":"1,330 kurals with Tamil text, transliteration, meanings, and cross-traditional commentary","/Keywords":"Thirukkural, Tirukkural, Thiruvalluvar, Tamil"})
w.page_mode = "/UseOutlines"
w.create_viewer_preferences(); w.viewer_preferences.display_doc_title = True
w.write(out)
print("ok", len(km), "kurals bookmarked")
