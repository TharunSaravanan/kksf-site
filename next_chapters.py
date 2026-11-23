# Prints the next N chapters that still lack a valid chapter_NN_data.json.
# Usage: python3 next_chapters.py [N]
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("adh", os.path.join(HERE, "build_adhikarams.py"))
src = open(os.path.join(HERE, "build_adhikarams.py"), encoding="utf-8").read()
ns = {"__file__": os.path.join(HERE, "build_adhikarams.py")}
exec(src.split("assert len(CHAPTERS)")[0], ns)  # load PAAL + CHAPTERS without writing files
CHAPTERS, PAAL = ns["CHAPTERS"], ns["PAAL"]

PAAL_FIELD = {
    "aram": "அறத்துப்பால் (Aram / Virtue)",
    "porul": "பொருட்பால் (Porul / Wealth & Polity)",
    "inbam": "காமத்துப்பால் (Inbam / Love)",
}

def paal_key(n):
    for k, m in PAAL.items():
        lo, hi = m["range"]
        if lo <= n <= hi:
            return k

def valid(n):
    if n == 1:
        return True  # chapter 1 is hand-written in build_data2.py
    f = os.path.join(HERE, f"chapter_{n:02d}_data.json")
    try:
        d = json.load(open(f, encoding="utf-8"))
        ks = d["kurals"]
        want = set(range((n - 1) * 10 + 1, n * 10 + 1))
        trads = {"hinduism", "christianity", "islam", "judaism", "buddhism", "greek_mythology", "philosophy"}
        return len(ks) == 10 and {k["number"] for k in ks} == want and all(trads <= set(k["cross_references"]) for k in ks)
    except Exception:
        return False

limit = int(sys.argv[1]) if len(sys.argv) > 1 else 5
missing = [c for c in CHAPTERS if not valid(c[0])]
print(json.dumps({
    "remaining_count": len(missing),
    "next": [
        {"chapter": n, "tamil": t, "transliteration": tr, "english": e,
         "paal": PAAL_FIELD[paal_key(n)], "kural_start": (n - 1) * 10 + 1, "kural_end": n * 10,
         "output_file": f"chapter_{n:02d}_data.json"}
        for (n, t, tr, e) in missing[:limit]
    ],
}, ensure_ascii=False, indent=2))
