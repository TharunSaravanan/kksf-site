# Quality checks on jain/jain_chapter_*.json (and inline jainism in chapter files).
import json, glob, os
HERE = os.path.dirname(os.path.abspath(__file__))
canon = json.load(open(os.path.join(HERE, "jain", "canonical_sources.json"), encoding="utf-8"))
BANNED = ("jaingpt", "chatgpt", "openai", "perplexity", "gemini.google")
problems = 0
for f in sorted(glob.glob(os.path.join(HERE, "jain", "jain_chapter_*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    ns = d.get("new_sources", {})
    n = d["chapter"]
    want = {str(k) for k in range((n - 1) * 10 + 1, n * 10 + 1)}
    if set(d["jainism"]) != want:
        print(os.path.basename(f), "wrong kural set"); problems += 1
    for k, v in d["jainism"].items():
        cid = v["citation_id"]
        info = canon.get(cid) or ns.get(cid)
        tag = f"{os.path.basename(f)} kural {k}"
        if not info:
            print(tag, "citation id has no definition:", cid); problems += 1; continue
        url = (info.get("url") or "") + " " + (info.get("publisher") or "")
        if any(b in url.lower() for b in BANNED):
            print(tag, "AI-generated source:", cid); problems += 1
        if v["is_quote"] and "wikipedia" in url.lower():
            print(tag, "quote verified only against Wikipedia:", cid); problems += 1
        if not v["is_quote"] and ("“" in v["quote_or_event"] or v["quote_or_event"].lstrip().startswith('"')):
            print(tag, "paraphrase contains quotation marks"); problems += 1
print("jain_check problems:", problems)
