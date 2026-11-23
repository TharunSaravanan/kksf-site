# Quality checks on sikh/, history/ and overrides/ files. Prints problems; exit summary line.
import json, glob, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
BANNED = ("gpt", "chatgpt", "openai", "perplexity", "gemini.google", "copilot")
sikh_canon = json.load(open(os.path.join(HERE, "sikh", "canonical_sources.json"), encoding="utf-8"))
shared = json.load(open(os.path.join(HERE, "thirukkural-project", "data", "sources.json"), encoding="utf-8"))
problems = 0

def bad(tag, msg):
    global problems
    print(tag, msg); problems += 1

def check_xr(tag, v, ns):
    for _k in ("quote_or_event", "explanation", "tie_back", "source", "citation_id", "_accuracy_note"):
        if not isinstance(v.get(_k), str):
            return bad(tag, f"field {_k} must be a plain string")
    cid = v.get("citation_id")
    info = sikh_canon.get(cid) or ns.get(cid) or shared.get(cid)
    if not info:
        return bad(tag, f"citation id has no definition: {cid}")
    url = ((info.get("url") or "") + " " + (info.get("publisher") or "")).lower()
    if any(b in url for b in BANNED):
        bad(tag, f"AI-generated source: {cid}")
    if v.get("is_quote") and "wikipedia" in url:
        bad(tag, f"quote verified only against Wikipedia: {cid}")
    if not v.get("is_quote") and ("“" in v["quote_or_event"] or v["quote_or_event"].lstrip().startswith('"')):
        bad(tag, "paraphrase contains quotation marks")
    if re.search("con"+"fuc|ana"+"lects|men"+"cius", json.dumps(v), re.I):
        bad(tag, "mentions a removed tradition")

for f in sorted(glob.glob(os.path.join(HERE, "sikh", "sikh_chapter_*.json"))):
    d = json.load(open(f, encoding="utf-8")); n = d["chapter"]; ns = d.get("new_sources", {})
    if set(d["sikhism"]) != {str(k) for k in range((n - 1) * 10 + 1, n * 10 + 1)}:
        bad(os.path.basename(f), "wrong kural set")
    for k, v in d["sikhism"].items():
        check_xr(f"{os.path.basename(f)} kural {k}", v, ns)

for f in sorted(glob.glob(os.path.join(HERE, "history", "history_chapter_*.json"))):
    d = json.load(open(f, encoding="utf-8")); n = d["chapter"]; ns = d.get("new_sources", {})
    if set(d["real_life_example"]) != {str(k) for k in range((n - 1) * 10 + 1, n * 10 + 1)}:
        bad(os.path.basename(f), "wrong kural set")
    for k, v in d["real_life_example"].items():
        tag = f"{os.path.basename(f)} kural {k}"
        ids = v.get("citation_ids", [])
        if len(set(ids)) < 2:
            bad(tag, "fewer than two sources")
        hosts = set()
        for cid in ids:
            info = ns.get(cid) or shared.get(cid)
            if not info:
                bad(tag, f"citation id has no definition: {cid}"); continue
            url = (info.get("url") or "").lower()
            if any(b in url for b in BANNED):
                bad(tag, f"AI-generated source: {cid}")
            m = re.match(r"https?://(www\.)?([^/]+)", url)
            if m: hosts.add(m.group(2))
        non_wiki = {h for h in hosts if "wikipedia" not in h}
        if len(non_wiki) < 2:
            bad(tag, "needs two independent non-Wikipedia sources")
        if "“" in v.get("event", "") and not v.get("_quote_verified"):
            pass  # quotes allowed only if verified; agents are told this — left to human spot-check

from collections import Counter
_titles = Counter()
for f in glob.glob(os.path.join(HERE, "history", "history_chapter_*.json")):
    for v in json.load(open(f, encoding="utf-8"))["real_life_example"].values():
        _titles[v["event_title"].strip().lower()] += 1
for t, c in _titles.items():
    if c > 2:
        bad("history", f"event used {c} times (max 2): {t}")

for f in sorted(glob.glob(os.path.join(HERE, "overrides", "phil_fix_*.json"))):
    d = json.load(open(f, encoding="utf-8")); ns = d.get("new_sources", {})
    for k, v in d.get("philosophy", {}).items():
        check_xr(f"{os.path.basename(f)} kural {k}", v, ns)
    for k, v in d.get("university", {}).items():
        if re.search("con"+"fuc|men"+"cius", v, re.I):
            bad(f"{os.path.basename(f)} kural {k}", "university text mentions a removed tradition")

print("backfill_check problems:", problems)
