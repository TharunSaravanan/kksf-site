# Builds the single offline data file bundled inside both mobile apps, from the same
# published data the website uses (so the apps show exactly what the site shows —
# Sikhism / Real Life Example appear automatically once build_data2.py publishes them).
#
# Run from anywhere AFTER build_data2.py and build_web.py:
#     python3 apps/build_app_data.py
# Writes:
#     apps/ios/Thirukkural/Resources/thirukkural_data.json
#     apps/android/app/src/main/assets/thirukkural_data.json
import json, os, re, datetime, html

APPS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(APPS)
DATA = os.path.join(ROOT, "thirukkural-project", "data")
WEB = os.path.join(ROOT, "thirukkural-project", "web")

kurals = json.load(open(os.path.join(DATA, "kurals.json"), encoding="utf-8"))
adhikarams = json.load(open(os.path.join(DATA, "adhikarams.json"), encoding="utf-8"))
sources = json.load(open(os.path.join(DATA, "sources.json"), encoding="utf-8"))

ORDER = ["hinduism", "christianity", "islam", "judaism", "buddhism", "jainism", "sikhism", "greek_mythology", "philosophy"]
LABELS = {"hinduism": "Hinduism", "christianity": "Christianity", "islam": "Islam", "judaism": "Judaism",
          "buddhism": "Buddhism", "jainism": "Jainism", "sikhism": "Sikhism",
          "greek_mythology": "Greek Mythology", "philosophy": "Philosophy"}
traditions = [t for t in ORDER if all(t in k["cross_references"] for k in kurals)]
has_rle = all("real_life_example" in k for k in kurals)

used = set()
for k in kurals:
    used.update(k.get("sources", []))
    for t in traditions:
        cid = k["cross_references"][t].get("citation_id")
        if cid:
            used.add(cid)
    if has_rle:
        used.update(k["real_life_example"]["citation_ids"])

def src_entry(cid):
    s = sources.get(cid, {})
    who = s.get("author") or s.get("translator") or ""
    return {"title": s.get("title", cid), "by": who, "publisher": s.get("publisher", ""),
            "url": s.get("url", ""), "tier": s.get("tier", "")}

out_kurals = []
for k in kurals:
    o = {"n": k["number"], "ta": k["tamil"], "tr": k["transliteration"], "meaning": k["meaning"],
         "elementary": k["elementary"], "university": k["university"], "src": k.get("sources", []),
         "x": {t: {"q": k["cross_references"][t]["quote_or_event"], "isq": bool(k["cross_references"][t]["is_quote"]),
                   "ex": k["cross_references"][t]["explanation"], "tb": k["cross_references"][t]["tie_back"],
                   "s": k["cross_references"][t]["source"], "c": k["cross_references"][t].get("citation_id", "")}
               for t in traditions}}
    if has_rle:
        r = k["real_life_example"]
        o["rle"] = {"title": r["event_title"], "date": r.get("date", ""), "place": r.get("place", ""),
                    "event": r["event"], "ex": r["explanation"], "tb": r["tie_back"], "c": r["citation_ids"]}
    out_kurals.append(o)

def page_fragment(name):
    """Body of a generated web page minus the site nav, with links between site pages removed
    (the app has its own navigation). External links are kept."""
    t = open(os.path.join(WEB, name), encoding="utf-8").read()
    body = t.split("<body>", 1)[1].rsplit("</body>", 1)[0]
    body = re.sub(r"<header class=\"site\">.*?</header>", "", body, flags=re.S)
    body = re.sub(r"<nav[^>]*>.*?</nav>", "", body, flags=re.S)
    body = re.sub(r"<div class=\"home-cards\">.*?</div>\s*</div>", "", body, flags=re.S)
    body = re.sub(r'<a href="(?!https?:|mailto:)[^"]*">(.*?)</a>', r"\1", body, flags=re.S)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    return body.strip()

data = {
    "generated": datetime.date.today().isoformat(),
    "traditions": [{"key": t, "label": LABELS[t]} for t in traditions],
    "has_real_life_example": has_rle,
    "chapters": [{"n": a["number"], "ta": a["tamil"], "tr": a["transliteration"], "en": a["english"],
                  "paal": a["paal"], "start": a["kural_start"], "end": a["kural_end"]} for a in adhikarams],
    "paals": [{"key": "aram", "en": "Aram", "ta": "அறத்துப்பால்", "sub": "Virtue — chapters 1–38"},
              {"key": "porul", "en": "Porul", "ta": "பொருட்பால்", "sub": "Wealth & Polity — chapters 39–108"},
              {"key": "inbam", "en": "Inbam", "ta": "காமத்துப்பால்", "sub": "Love — chapters 109–133"}],
    "kurals": out_kurals,
    "sources": {cid: src_entry(cid) for cid in sorted(used)},
    "pages": {"home": page_fragment("index.html"), "learn_more": page_fragment("history.html"),
              "historical_texts": page_fragment("historical-texts.html")},
}

blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
targets = [os.path.join(APPS, "ios", "Thirukkural", "Resources", "thirukkural_data.json"),
           os.path.join(APPS, "android", "app", "src", "main", "assets", "thirukkural_data.json")]
for p in targets:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(blob)
print(f"App data: {len(out_kurals)} kurals, {len(data['traditions'])} traditions "
      f"({', '.join(LABELS[t] for t in traditions)}), real life example: {has_rle}, "
      f"{len(data['sources'])} sources, {len(blob)/1e6:.1f} MB -> ios + android")
