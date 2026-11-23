# Status of the Oct 2026 revision backfills: Sikhism, Real Life Example, and the
# philosophy cleanup.  Usage: python3 backfill_status.py [N]
# Prints JSON with remaining counts and the next N items for each job.
import json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
XR = {"quote_or_event", "explanation", "tie_back", "source", "citation_id", "is_quote", "_accuracy_percent", "_accuracy_note"}
RLE = {"event_title", "date", "place", "event", "explanation", "tie_back", "citation_ids", "_accuracy_percent", "_accuracy_note"}

def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None

def fn(folder, prefix, n):
    return os.path.join(HERE, folder, f"{prefix}_{n:02d}.json")

def ok_xr(x):
    return isinstance(x, dict) and XR <= set(x) and isinstance(x["_accuracy_percent"], (int, float)) and x["quote_or_event"]

def ok_rle(x):
    return isinstance(x, dict) and RLE <= set(x) and isinstance(x["citation_ids"], list) and len(x["citation_ids"]) >= 2 and x["event"]

def kurals(n):
    return range((n - 1) * 10 + 1, n * 10 + 1)

def sikh_done(n):
    d = load(fn("sikh", "sikh_chapter", n))
    return bool(d) and all(ok_xr(d.get("sikhism", {}).get(str(k))) for k in kurals(n))

def hist_done(n):
    d = load(fn("history", "history_chapter", n))
    return bool(d) and all(ok_rle(d.get("real_life_example", {}).get(str(k))) for k in kurals(n))

cleanup = load(os.path.join(HERE, "overrides", "_done_cleanup_list.json")) or {"philosophy": [], "university": []}
fixed_phil, fixed_uni = set(), set()
for f in glob.glob(os.path.join(HERE, "overrides", "phil_fix_*.json")):
    d = load(f) or {}
    fixed_phil |= {int(k) for k, v in d.get("philosophy", {}).items() if ok_xr(v)}
    fixed_uni |= {int(k) for k, v in d.get("university", {}).items() if isinstance(v, str) and v.strip()}

limit = int(sys.argv[1]) if len(sys.argv) > 1 else 6
sikh_left = [n for n in range(1, 134) if not sikh_done(n)]
hist_left = [n for n in range(1, 134) if not hist_done(n)]
phil_left = [k for k in cleanup["philosophy"] if k not in fixed_phil]
uni_left = [k for k in cleanup["university"] if k not in fixed_uni]
print(json.dumps({
    "sikh_remaining_chapters": len(sikh_left), "sikh_next": sikh_left[:limit],
    "history_remaining_chapters": len(hist_left), "history_next": hist_left[:limit],
    "philosophy_fix_remaining": len(phil_left), "philosophy_fix_next": phil_left[:15],
    "university_fix_remaining": uni_left,
}, indent=1))
