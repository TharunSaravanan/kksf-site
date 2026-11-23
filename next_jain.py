# Lists the next N built chapters whose kurals still lack a valid Jainism cross-reference
# (either inline in chapter_NN_data.json or in jain/jain_chapter_NN.json).
# Usage: python3 next_jain.py [N]
import json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = {"quote_or_event", "explanation", "tie_back", "source", "citation_id", "is_quote", "_accuracy_percent", "_accuracy_note"}

def ok(x):
    return isinstance(x, dict) and KEYS <= set(x) and isinstance(x["_accuracy_percent"], (int, float)) and x["quote_or_event"]

def built_chapters():
    nums = {1}
    for f in glob.glob(os.path.join(HERE, "chapter_*_data.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
            n = int(os.path.basename(f).split("_")[1])
            if len(d["kurals"]) == 10:
                nums.add(n)
        except Exception:
            pass
    return sorted(nums)

def inline_jain(n):
    if n == 1:
        return {}
    try:
        d = json.load(open(os.path.join(HERE, f"chapter_{n:02d}_data.json"), encoding="utf-8"))
        return {k["number"]: k["cross_references"].get("jainism") for k in d["kurals"]}
    except Exception:
        return {}

def backfill(n):
    try:
        d = json.load(open(os.path.join(HERE, "jain", f"jain_chapter_{n:02d}.json"), encoding="utf-8"))
        return {int(k): v for k, v in d["jainism"].items()}
    except Exception:
        return {}

def complete(n):
    inl, bf = inline_jain(n), backfill(n)
    return all(ok(inl.get(k)) or ok(bf.get(k)) for k in range((n - 1) * 10 + 1, n * 10 + 1))

limit = int(sys.argv[1]) if len(sys.argv) > 1 else 4
built = built_chapters()
missing = [c for c in built if not complete(c)]
print(json.dumps({"built_chapters": len(built), "jain_remaining_count": len(missing),
                  "next": missing[:limit]}, indent=2))
