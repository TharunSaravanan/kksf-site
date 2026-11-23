import json, html, os

import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thirukkural-project")
kurals = json.load(open(f"{BASE}/data/kurals.json", encoding="utf-8"))
sources = json.load(open(f"{BASE}/data/sources.json", encoding="utf-8"))
adhikarams = json.load(open(f"{BASE}/data/adhikarams.json", encoding="utf-8"))

# Filenames are zero-padded to fit the full 1,330-kural / 133-chapter text, not
# just the batch built so far.
def kural_fn(n):
    return f"kural-{n:04d}.html"

def adhikaram_fn(n):
    return f"adhikaram-{n:03d}.html"

# Chapter number a kural belongs to, and which chapters currently have real
# kural content built (every chapter is exactly 10 kurals, so this is computed,
# not stored per-kural).
def adhikaram_num_for_kural(n):
    return (n - 1) // 10 + 1

AVAILABLE_ADHIKARAMS = sorted({adhikaram_num_for_kural(k["number"]) for k in kurals})
ADHIKARAM_BY_NUM = {a["number"]: a for a in adhikarams}
KURALS_BY_ADHIKARAM = {}
for k in kurals:
    KURALS_BY_ADHIKARAM.setdefault(adhikaram_num_for_kural(k["number"]), []).append(k)

TRAD_LABELS = {
    "hinduism": "Hinduism", "christianity": "Christianity", "islam": "Islam",
    "judaism": "Judaism", "buddhism": "Buddhism", "jainism": "Jainism", "sikhism": "Sikhism", "greek_mythology": "Greek Mythology",
    "philosophy": "Philosophy",
}
TRAD_ORDER = ["hinduism", "christianity", "islam", "judaism", "buddhism", "jainism", "sikhism", "greek_mythology", "philosophy"]
# Jainism / Sikhism / Real Life Example appear only once build_data2.py has published them for every kural.
JAIN_ON = bool(kurals) and all("jainism" in k["cross_references"] for k in kurals)
SIKH_ON = bool(kurals) and all("sikhism" in k["cross_references"] for k in kurals)
HIST_ON = bool(kurals) and all("real_life_example" in k for k in kurals)
TRAD_ORDER = [t for t in TRAD_ORDER if (t != "jainism" or JAIN_ON) and (t != "sikhism" or SIKH_ON)]
N_TRADS_WORD = {7: "seven", 8: "eight", 9: "nine"}[len(TRAD_ORDER)]
_scrip = ["Hindu", "Christian", "Islamic", "Jewish", "Buddhist"] + (["Jain"] if JAIN_ON else []) + (["Sikh"] if SIKH_ON else [])
SCRIPTURE_LIST = ", ".join(_scrip[:-1]) + ", and " + _scrip[-1] + " scripture"
CONF_NOTE = ""

CSS = """
.rle-meta{color:var(--muted);font-size:.9rem;font-style:italic;margin:-.2rem 0 .4rem;}
:root{--ink:#1f1f1f;--muted:#6b6b6b;--accent:#8a4b00;--paper:#fffdf8;--line:#e8e0d2;}
@font-face{font-family:"Noto Sans Tamil";src:url("fonts/NotoSansTamil-Regular.woff2") format("woff2");font-weight:400;}
@font-face{font-family:"Noto Sans Tamil";src:url("fonts/NotoSansTamil-Bold.woff2") format("woff2");font-weight:700;}
*{box-sizing:border-box;}
body{background:var(--paper);color:var(--ink);font-family:Georgia,'Times New Roman',serif;max-width:820px;margin:0 auto;padding:0 1.5rem 5rem;line-height:1.6;}
.tamil{font-family:"Noto Sans Tamil","Latha",sans-serif;}
header.site{padding-top:1.5rem;margin-bottom:2rem;}
header.site .top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1rem;}
header.site .brand{font-weight:bold;}
nav.tabs{display:flex;gap:1.75rem;border-bottom:2px solid var(--line);padding-bottom:.6rem;}
nav.tabs a{color:var(--muted);text-decoration:none;font-size:.95rem;letter-spacing:.02em;}
nav.tabs a.active{color:var(--accent);font-weight:bold;border-bottom:2px solid var(--accent);padding-bottom:.65rem;margin-bottom:-.67rem;}
nav.tabs a:hover{color:var(--accent);}
h1.page-title{color:var(--accent);font-size:1.8rem;margin-bottom:.2rem;}
h1.kural-num{color:var(--accent);font-size:2rem;margin-bottom:.1rem;}
.adhikaram{color:var(--muted);font-style:italic;margin-top:0;margin-bottom:2rem;}
.tamil-text{font-family:"Noto Sans Tamil","Latha",sans-serif;font-size:1.7rem;font-weight:700;text-align:center;margin:1.5rem 0 .5rem;white-space:pre-line;}
.translit{text-align:center;font-style:italic;color:#444;white-space:pre-line;margin-bottom:2rem;}
h2.section{color:var(--accent);font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid var(--line);padding-bottom:.3rem;margin-top:2.2rem;}
.crossref{margin:1.4rem 0;padding-bottom:.2rem;}
.crossref .trad{font-weight:bold;color:var(--accent);font-size:1.05rem;}
.crossref .quote{font-style:italic;}
.crossref .quote.is-paraphrase{font-style:normal;color:#333;}
.crossref .cite{color:var(--muted);font-size:.9rem;margin-bottom:.4rem;}
.crossref .cite a{color:var(--muted);text-decoration:underline dotted;}
.crossref .cite a:hover{color:var(--accent);}
.crossref .cite .idx{color:var(--accent);text-decoration:none;font-weight:bold;margin-left:.15rem;}
.crossref .explain{margin:.4rem 0;}
.crossref .tieback{font-style:italic;color:#444;}
.crossref .suggest{background:#f4ede1;border:1px dashed var(--line);border-radius:6px;padding:.8rem 1rem;font-size:.92rem;color:var(--muted);}
.crossref .suggest a{color:var(--accent);}
nav.pager{display:flex;justify-content:space-between;margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line);font-size:.95rem;}
nav.pager a{color:var(--accent);text-decoration:none;}
footer.sources{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line);font-size:.85rem;color:var(--muted);}
footer.sources ol{padding-left:1.4rem;}
footer.sources li{margin-bottom:.4rem;padding-left:.2rem;}
footer.sources a{color:var(--accent);}
footer.sources .tier{color:#999;font-size:.8rem;}
.toc-list{list-style:none;padding:0;}
.toc-list li{padding:.7rem 0;border-bottom:1px solid var(--line);display:flex;gap:1rem;align-items:baseline;}
.toc-list .n{color:var(--accent);font-weight:bold;width:2.2rem;flex-shrink:0;}
.toc-list a{color:var(--ink);text-decoration:none;}
.toc-list a:hover{color:var(--accent);text-decoration:underline;}
.toc-list .tamil-kural{font-family:"Noto Sans Tamil",sans-serif;font-size:1.15rem;line-height:1.5;}
.prose p{margin:0 0 1.1rem;}
.prose h3{color:var(--accent);font-size:1.05rem;margin-top:1.8rem;margin-bottom:.4rem;}
.callout{background:#f4ede1;border-left:3px solid var(--accent);padding:.9rem 1.1rem;margin:1.5rem 0;font-size:.95rem;}
.home-cards{display:flex;flex-direction:column;gap:.9rem;margin:1.5rem 0;}
.home-card{border:1px solid var(--line);border-radius:8px;padding:1rem 1.2rem;}
.home-card a{color:var(--accent);text-decoration:none;font-weight:bold;}
.home-card p{margin:.3rem 0 0;color:var(--muted);font-size:.92rem;}
sup.src-ref a{color:var(--accent);text-decoration:none;}
.text-entry{border-top:2px solid var(--line);padding-top:1.6rem;margin-top:2.2rem;}
.text-entry:first-of-type{margin-top:1rem;}
.text-entry h2{color:var(--accent);font-size:1.4rem;margin:0 0 .2rem;}
.text-entry .meta{color:var(--muted);font-style:italic;font-size:.9rem;margin-bottom:1rem;}
.text-entry h4{color:#8a4b00;font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;margin:1.1rem 0 .3rem;}
.text-entry p{margin:0 0 .8rem;}
.text-entry .learn-more{font-size:.85rem;color:var(--muted);margin-top:.6rem;}
.text-entry .learn-more a{color:var(--accent);}

.search-wrap{margin:1.2rem 0 1.6rem;}
.search-wrap input{width:100%;font-family:inherit;font-size:1rem;padding:.65rem .9rem;border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink);}
.search-wrap input:focus{outline:2px solid var(--accent);outline-offset:1px;}
.search-count{font-size:.82rem;color:var(--muted);margin-top:.4rem;}
.paal-group{margin-top:2.2rem;}
.paal-group h2{color:var(--accent);font-size:1.15rem;border-bottom:2px solid var(--line);padding-bottom:.4rem;margin-bottom:.2rem;}
.paal-group .paal-sub{color:var(--muted);font-size:.85rem;font-style:italic;margin-bottom:1rem;}
details.chapter{border-bottom:1px solid var(--line);}
details.chapter summary{display:flex;align-items:baseline;gap:.8rem;padding:.7rem 0;cursor:pointer;list-style:none;}
details.chapter summary::-webkit-details-marker{display:none;}
details.chapter summary .arrow{color:var(--muted);font-size:.75rem;transition:transform .15s;flex-shrink:0;width:.9rem;}
details.chapter[open] summary .arrow{transform:rotate(90deg);}
details.chapter summary .cn{color:var(--accent);font-weight:bold;width:2.4rem;flex-shrink:0;}
details.chapter summary .cnames{flex:1;}
details.chapter summary .cnames a{color:var(--ink);text-decoration:none;font-weight:bold;}
details.chapter summary a.cname-link{color:var(--ink);text-decoration:none;font-weight:bold;}
details.chapter summary a.cname-link:hover{color:var(--accent);text-decoration:underline;}
details.chapter summary .cname-plain{font-weight:bold;color:var(--ink);}
details.chapter summary .tamil-name{font-family:"Noto Sans Tamil",sans-serif;color:var(--muted);font-size:.92rem;margin-left:.5rem;}
details.chapter summary .soon-badge{font-size:.72rem;color:var(--muted);background:#f4ede1;border-radius:4px;padding:.1rem .4rem;margin-left:.5rem;flex-shrink:0;}
.chapter-kurals{padding:.2rem 0 1rem 3.2rem;}
.chapter-kurals .k-row{padding:.3rem 0;font-size:.95rem;}
.chapter-kurals .k-row a{color:var(--ink);text-decoration:none;}
.chapter-kurals .k-row a:hover{color:var(--accent);text-decoration:underline;}
.chapter-kurals .k-row .kn{color:var(--accent);font-weight:bold;margin-right:.5rem;}
.chapter-kurals .k-row.pending{color:var(--muted);font-style:italic;}
.chapter-nav{display:flex;justify-content:space-between;margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line);font-size:.95rem;}
.chapter-nav a{color:var(--accent);text-decoration:none;}
.chapter-nav .disabled{color:#bbb;font-style:italic;}
.skip-btn{display:inline-block;font-size:.85rem;color:var(--accent);border:1px solid var(--accent);border-radius:6px;padding:.35rem .8rem;text-decoration:none;}
.skip-btn:hover{background:var(--accent);color:#fff;}
.skip-btn.disabled{color:#bbb;border-color:var(--line);pointer-events:none;}
"""

def source_link_html(src_id, label=None):
    s = sources.get(src_id, {})
    text = label or s.get("title", src_id)
    url = s.get("url")
    if url:
        return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(text)}</a>'
    return html.escape(text)

def source_full_citation(src_id):
    s = sources.get(src_id, {})
    label = s.get("title", src_id)
    url = s.get("url")
    author = s.get("author")
    tier = s.get("tier")
    extra = f" ({author})" if author else ""
    tier_html = f' <span class="tier">[{tier} source]</span>' if tier else ""
    if url:
        return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(label + extra)}</a>{tier_html}'
    return html.escape(label + extra) + tier_html

def strip_quotes(s):
    return s.strip('“”"')

def nav(active):
    tabs = [("index.html", "Home"), ("kurals.html", "The Kurals"), ("history.html", "Learn More"), ("historical-texts.html", "Historical Texts")]
    links = "\n".join(
        f'<a href="{href}" class="{"active" if href == active else ""}">{label}</a>'
        for href, label in tabs
    )
    return f"""<header class="site">
  <div class="top"><span class="brand">The Thirukkural</span><span style="color:var(--muted);font-size:.9rem;">A Cross-Traditional Study Edition</span></div>
  <nav class="tabs">{links}</nav>
</header>"""

def page_shell(title, active_tab, body_html):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | The Thirukkural</title>
<style>{CSS}</style>
</head>
<body>
{nav(active_tab)}
{body_html}
</body>
</html>"""

def render_crossref(trad, refobj, cite_index):
    """cite_index: dict[citation_id] -> page-local footnote number."""
    label = TRAD_LABELS[trad]
    quote = (refobj.get("quote_or_event") or "").strip()
    if not quote:
        return f"""<div class="crossref">
  <div class="trad">{label}</div>
  <div class="suggest">We haven't found a correspondence here that's accurate enough to include yet. <a href="mailto:adhigopal09@gmail.com?subject=Thirukkural%20suggestion">Want to suggest a change?</a> Leave us a message and we'll review it.</div>
</div>"""
    cite_id = refobj.get("citation_id")
    cite_html = source_link_html(cite_id, refobj["source"]) if cite_id else html.escape(refobj["source"])
    idx = cite_index.get(cite_id)
    idx_html = f' <a class="idx" href="#cite-{idx}">[{idx}]</a>' if idx else ""
    is_quote = bool(refobj.get("is_quote"))
    if is_quote:
        quote_html = f'<div class="quote">&ldquo;{html.escape(strip_quotes(quote))}&rdquo;</div>'
    else:
        quote_html = f'<div class="quote is-paraphrase">{html.escape(strip_quotes(quote))}</div>'
    return f"""<div class="crossref">
  <div class="trad">{label}</div>
  {quote_html}
  <div class="cite">&mdash; {cite_html}{idx_html}</div>
  <div class="explain">{html.escape(refobj['explanation'])}</div>
  <div class="tieback">{html.escape(refobj['tie_back'])}</div>
</div>"""

def render_real_life(r, cite_index):
    refs = " ".join(f'<a class="idx" href="#cite-{cite_index[c]}">[{cite_index[c]}]</a>' for c in r["citation_ids"] if c in cite_index)
    meta = " &middot; ".join(html.escape(x) for x in (r.get("date"), r.get("place")) if x)
    return f"""<h2 class="section">Real Life Example</h2>
<div class="crossref real-life">
  <div class="trad">{html.escape(r['event_title'])}</div>
  <div class="rle-meta">{meta}</div>
  <div class="quote is-paraphrase">{html.escape(r['event'])}</div>
  <div class="cite">&mdash; Sources: {refs}</div>
  <div class="explain">{html.escape(r['explanation'])}</div>
  <div class="tieback">{html.escape(r['tie_back'])}</div>
</div>"""

def kural_page(k, prev_k, next_k):
    # Build a page-local numbered citation index: base Tamil-text sources first,
    # then every source actually used in the cross-references, in reading order.
    cite_index = {}
    cite_order = []
    for s in k["sources"]:
        if s not in cite_index:
            cite_index[s] = len(cite_order) + 1
            cite_order.append(s)
    for t in TRAD_ORDER:
        cid = k["cross_references"][t].get("citation_id")
        if cid and k["cross_references"][t].get("quote_or_event") and cid not in cite_index:
            cite_index[cid] = len(cite_order) + 1
            cite_order.append(cid)

    rle = k.get("real_life_example") if HIST_ON else None
    if rle:
        for cid in rle["citation_ids"]:
            if cid not in cite_index:
                cite_index[cid] = len(cite_order) + 1
                cite_order.append(cid)
    cross_html = "\n".join(render_crossref(t, k["cross_references"][t], cite_index) for t in TRAD_ORDER)
    rle_html = render_real_life(rle, cite_index) if rle else ""
    src_list = "\n".join(
        f'<li id="cite-{cite_index[s]}">{source_full_citation(s)}</li>' for s in cite_order
    )
    prev_link = f'<a href="{kural_fn(prev_k)}">&larr; Kural {prev_k}</a>' if prev_k else "<span></span>"
    next_link = f'<a href="{kural_fn(next_k)}">Kural {next_k} &rarr;</a>' if next_k else "<span></span>"

    chapter_num = adhikaram_num_for_kural(k["number"])
    chapter_link = f'<a href="{adhikaram_fn(chapter_num)}">{html.escape(k["adhikaram"]["english"])}</a>'

    # "Skip to next chapter" always lands on the first kural of the next adhikaram,
    # not the chapter's overview page — only active once that chapter has content.
    next_chapter_num = chapter_num + 1
    if next_chapter_num in AVAILABLE_ADHIKARAMS:
        first_kural_of_next = KURALS_BY_ADHIKARAM[next_chapter_num][0]["number"]
        skip_html = f'<a class="skip-btn" href="{kural_fn(first_kural_of_next)}">Skip to Next Chapter &rarr;</a>'
    elif next_chapter_num <= 133:
        skip_html = '<span class="skip-btn disabled">Next Chapter (coming soon)</span>'
    else:
        skip_html = ""

    tamil_lines = html.escape(k["tamil"])
    translit_lines = html.escape(k["transliteration"])
    body = f"""<h1 class="kural-num">Kural {k['number']}</h1>
<p class="adhikaram">{chapter_link} &middot; {html.escape(k['adhikaram']['transliteration'])} &middot; <span class="tamil">{html.escape(k['adhikaram']['tamil'])}</span></p>

<div class="tamil-text">{tamil_lines}</div>
<div class="translit">{translit_lines}</div>

<h2 class="section">Meaning</h2>
<p>{html.escape(k['meaning'])}</p>

<h2 class="section">Elementary</h2>
<p>{html.escape(k['elementary'])}</p>

<h2 class="section">University</h2>
<p>{html.escape(k['university']).replace('&#39;','&rsquo;')}</p>

<h2 class="section">Through the Lens of</h2>
{cross_html}
{rle_html}

<footer class="sources">
  <strong>Sources for this page</strong>
  <ol>
    {src_list}
  </ol>
</footer>

<nav class="pager">
  {prev_link}
  {next_link}
</nav>
<nav class="chapter-nav">
  {chapter_link}
  {skip_html}
</nav>"""
    return page_shell(f"Kural {k['number']} — {k['adhikaram']['english']}", "kurals.html", body)

PAAL_LABELS = {
    "aram": ("Aram", "அறத்துப்பால்", "Virtue &mdash; chapters 1&ndash;38"),
    "porul": ("Porul", "பொருட்பால்", "Wealth &amp; Polity &mdash; chapters 39&ndash;108"),
    "inbam": ("Inbam", "காமத்துப்பால்", "Love &mdash; chapters 109&ndash;133"),
}
PAAL_ORDER = ["aram", "porul", "inbam"]

def chapter_row_html(a):
    n = a["number"]
    has_data = n in AVAILABLE_ADHIKARAMS
    soon = "" if has_data else '<span class="soon-badge">coming soon</span>'
    name_html = (
        f'<a class="cname-link" href="{adhikaram_fn(n)}">{html.escape(a["english"])}</a>'
        if has_data else
        f'<span class="cname-plain">{html.escape(a["english"])}</span>'
    )
    search_terms = " ".join([str(n), a["english"], a["transliteration"], a["tamil"]]).lower()

    if has_data:
        kural_rows = "\n".join(
            f'<div class="k-row"><a href="{kural_fn(k["number"])}"><span class="kn">{k["number"]}.</span>'
            f'<span class="tamil">{html.escape(k["tamil"]).replace(chr(10), " / ")}</span></a></div>'
            for k in KURALS_BY_ADHIKARAM[n]
        )
        search_terms += " " + " ".join(k["tamil"] + " " + k["transliteration"] for k in KURALS_BY_ADHIKARAM[n]).lower()
    else:
        kural_rows = f'<div class="k-row pending">Kurals {a["kural_start"]}&ndash;{a["kural_end"]} &mdash; not yet added</div>'

    return f"""<details class="chapter" data-search="{html.escape(search_terms)}">
  <summary><span class="arrow">&#9654;</span><span class="cn">{n}</span><span class="cnames">{name_html}{soon}<span class="tamil-name">{html.escape(a['tamil'])}</span></span></summary>
  <div class="chapter-kurals">
    {kural_rows}
  </div>
</details>"""

def kurals_hub_page():
    groups_html = []
    for paal_key in PAAL_ORDER:
        label, tamil, sub = PAAL_LABELS[paal_key]
        chapters = [a for a in adhikarams if a["paal"] == paal_key]
        rows = "\n".join(chapter_row_html(a) for a in chapters)
        groups_html.append(f"""<div class="paal-group">
  <h2><span class="tamil">{tamil}</span> &middot; {label}</h2>
  <p class="paal-sub">{sub}</p>
  {rows}
</div>""")

    body = f"""<h1 class="page-title">The Kurals</h1>
<p>All 133 chapters (adhikarams) of the Thirukkural. Search, or click a chapter to expand it; click a chapter's name to open its full page. Chapters 1&ndash;{max(AVAILABLE_ADHIKARAMS)} (Kurals 1&ndash;{max(AVAILABLE_ADHIKARAMS)*10}) are built out so far &mdash; the rest are being added in batches.</p>

<div class="search-wrap">
  <input type="search" id="chapter-search" placeholder="Search chapters or kurals&hellip;" autocomplete="off">
  <div class="search-count" id="search-count"></div>
</div>

{''.join(groups_html)}

<script>
(function() {{
  var input = document.getElementById('chapter-search');
  var count = document.getElementById('search-count');
  var chapters = Array.prototype.slice.call(document.querySelectorAll('details.chapter'));
  input.addEventListener('input', function() {{
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    chapters.forEach(function(d) {{
      var match = !q || (d.getAttribute('data-search') || '').indexOf(q) !== -1;
      d.style.display = match ? '' : 'none';
      if (match) shown++;
      if (q && match) d.open = true;
      if (!q) d.open = false;
    }});
    count.textContent = q ? (shown + ' of ' + chapters.length + ' chapters match') : '';
  }});
}})();
</script>"""
    return page_shell("The Kurals", "kurals.html", body)

def adhikaram_page(a):
    n = a["number"]
    chap_kurals = KURALS_BY_ADHIKARAM.get(n, [])
    label, tamil_book, _ = PAAL_LABELS[a["paal"]]
    rows = "\n".join(
        f'<li><span class="n">{k["number"]}</span>'
        f'<a href="{kural_fn(k["number"])}"><span class="tamil-kural">{html.escape(k["tamil"]).replace(chr(10), "<br>")}</span></a></li>'
        for k in chap_kurals
    )

    prev_n, next_n = n - 1, n + 1
    if prev_n in AVAILABLE_ADHIKARAMS:
        prev_html = f'<a href="{adhikaram_fn(prev_n)}">&larr; {html.escape(ADHIKARAM_BY_NUM[prev_n]["english"])}</a>'
    elif prev_n >= 1:
        prev_html = f'<span class="disabled">&larr; {html.escape(ADHIKARAM_BY_NUM[prev_n]["english"])} (coming soon)</span>'
    else:
        prev_html = "<span></span>"
    if next_n in AVAILABLE_ADHIKARAMS:
        next_html = f'<a href="{adhikaram_fn(next_n)}">{html.escape(ADHIKARAM_BY_NUM[next_n]["english"])} &rarr;</a>'
    elif next_n <= 133:
        next_html = f'<span class="disabled">{html.escape(ADHIKARAM_BY_NUM[next_n]["english"])} (coming soon) &rarr;</span>'
    else:
        next_html = "<span></span>"

    body = f"""<h1 class="page-title">{html.escape(a['english'])}</h1>
<p class="adhikaram"><span class="tamil">{html.escape(a['tamil'])}</span> &middot; {html.escape(a['transliteration'])} &middot; Chapter {n} of 133 &middot; {label} ({tamil_book}) &middot; Kurals {a['kural_start']}&ndash;{a['kural_end']}</p>
<p>Click a kural, in Tamil, for its comprehensive breakdown.</p>
<ul class="toc-list">
{rows}
</ul>
<nav class="chapter-nav">
  {prev_html}
  {next_html}
</nav>"""
    return page_shell(f"Chapter {n}: {a['english']}", "kurals.html", body)

def home_page():
    body = """<h1 class="page-title">The One Thirukkural Guide</h1>
<div class="prose">
<p>The Thirukkural (<span class="tamil">திருக்குறள்</span>) is a work of 1,330 short couplets on ethics, worldly life, and love, traditionally attributed to the Tamil poet Thiruvalluvar. It's one of the most translated and most quoted works in the Tamil language, read by people of many faiths and by secular readers, because it was written to hold up across belief systems rather than argue for any one of them.</p>
<p>This project is an attempt to build a single, trustworthy, all-in-one guide to it &mdash; the Tamil text as Valluvar wrote it, a careful translation, an explanation simple enough for a child, a deeper explanation for a university-level reader, and &mdash; because a 2,000-year-old ethical text tends to rhyme with ideas everywhere else in the world &mdash; a look at how the same idea shows up in Hindu, Christian, Islamic, Jewish, and Buddhist scripture, in Greek mythology, and in philosophy.</p>

<h3>What's on each page</h3>
<p>Every kural gets the same five-part treatment: the Tamil couplet itself, its transliteration and a plain meaning, an <strong>Elementary</strong> explanation (as simple as it can honestly be made, built for a first read), a <strong>University</strong> explanation (the deeper, more technical reading), and <strong>Through the Lens of</strong> &mdash; a look at the same idea through seven different traditions, each backed by a real, checkable quote or story.</p>

<h3>How accurate is this?</h3>
<p>Every quote from a religious or historical text on this site has been individually checked against a primary source before being included. Where a genuinely close match exists across traditions, it's used; where only a looser, next-best parallel could be found, it's included but framed honestly as a looser fit rather than dressed up as an exact one. We keep our own internal record of how confident we are in every citation and why &mdash; that log isn't published here, but it drives the standard behind what you do see.</p>

<h3>Where to go next</h3>
</div>
<div class="home-cards">
  <div class="home-card"><a href="kurals.html">The Kurals &rarr;</a><p>Start reading. Browse all available kurals in Tamil and open any one for the full translation, both explanation levels, and the cross-tradition study.</p></div>
  <div class="home-card"><a href="history.html">Learn More &rarr;</a><p>Who Thiruvalluvar was (and wasn't, as far as we can tell), when the text was likely written, how it's structured, and how it reached the rest of the world.</p></div>
  <div class="home-card"><a href="historical-texts.html">Historical Texts &rarr;</a><p>Background on the seven traditions cited in &ldquo;Through the Lens of&rdquo; &mdash; where each text comes from, its impact today, and its core principles.</p></div>
</div>
<div class="callout">This guide is complete: all 1,330 kurals across all 133 adhikarams, from Adhikaram 1, &ldquo;The Praise of God,&rdquo; through the final chapter on lovers&rsquo; sulking.</div>"""
    if HIST_ON:
        body = body.replace("each backed by a real, checkable quote or story.</p>", "each backed by a real, checkable quote or story &mdash; followed by a <strong>Real Life Example</strong>: a well-documented event from world history, the kind taught in schools and confirmed by multiple reference sources, that shows the kural&rsquo;s idea playing out in practice.</p>").replace("same five-part treatment", "same six-part treatment")
    body = body.replace("that log isn't published here, but it drives the standard behind what you do see.</p>", "that log isn't published here, but it drives the standard behind what you do see." + CONF_NOTE + "</p>").replace("Hindu, Christian, Islamic, Jewish, and Buddhist scripture", SCRIPTURE_LIST).replace("seven different traditions", f"{N_TRADS_WORD} different traditions").replace("the seven traditions", f"the {N_TRADS_WORD} traditions")
    return page_shell("Home", "index.html", body)

TEXT_ENTRIES = [
    {
        "label": "Hindu Scriptures",
        "sub": "Vedas &middot; Upanishads &middot; Bhagavad Gita &middot; Ramayana &middot; Mahabharata &middot; Puranas",
        "meta": "Composed roughly 1500 BCE &ndash; 200 CE &middot; oral tradition, later written down in Sanskrit",
        "history": "Hindu scripture isn't one book but a layered library built up over more than a thousand years. The four Vedas (Rigveda, Samaveda, Yajurveda, Atharvaveda) are the oldest layer, hymns and ritual texts from roughly 1500&ndash;500 BCE. The Upanishads, composed mostly between 800 and 200 BCE, turn from ritual toward philosophy &mdash; the nature of the self (Atman) and ultimate reality (Brahman). The Bhagavad Gita, a 700-verse dialogue embedded in the sixth book of the epic Mahabharata, is traditionally attributed to the sage Vyasa but was most likely assembled between 400 BCE and 200 CE through centuries of oral transmission. The Ramayana and Puranas add narrative and devotional material to the same tradition.",
        "impact": "These texts remain the living scripture of roughly 1.2 billion Hindus worldwide, recited, performed, and studied daily. The Bhagavad Gita in particular has traveled far outside Hindu practice: it shaped Mahatma Gandhi's philosophy of nonviolent resistance and influenced Western writers and thinkers including Ralph Waldo Emerson, Henry David Thoreau, and Aldous Huxley. Its language of \"acting without attachment to outcomes\" is now common currency in modern leadership and mindfulness writing.",
        "principles": "Central ideas include dharma (one's duty or right action), karma (action and consequence across lifetimes), and moksha (liberation from the cycle of rebirth). The Gita teaches three principal paths toward that liberation &mdash; karma yoga (selfless action), bhakti yoga (devotion), and jnana yoga (knowledge) &mdash; and argues, distinctively, that liberation doesn't require withdrawing from worldly duties, only performing them without attachment to their results.",
        "sources": [("Bhagavad Gītā — Internet Encyclopedia of Philosophy", "https://iep.utm.edu/bhagavad-gita/"), ("Bhagavad Gita — Wikipedia", "https://en.wikipedia.org/wiki/Bhagavad_Gita")],
    },
    {
        "label": "Christianity",
        "sub": "The Holy Bible &mdash; Old and New Testament",
        "meta": "Old Testament ≈ 1000–100 BCE &middot; New Testament ≈ 50–100 CE &middot; 66 books (Protestant canon)",
        "history": "The Bible was written over roughly a thousand years by many authors in Hebrew, Aramaic, and Greek. The Old Testament's 39 books were composed mainly between 1000 and 100 BCE, though they preserve older oral material; they tell the story of Israel's covenant with God, from creation through the prophets. The New Testament's 27 books were written within decades of Jesus's death and resurrection, in the second half of the 1st century CE &mdash; four Gospels recounting his life and teaching, the Book of Acts describing the early church, and letters (many attributed to Paul) addressed to those first Christian communities.",
        "impact": "The Bible is the most translated and most widely distributed book in history, central to the practice of roughly 2.3 billion Christians worldwide. Its framework of universal human dignity is among the most cited foundations of modern international human-rights law, and it has been a primary driver of literacy programs, hospitals, orphanages, and relief organizations across history. Its stories and language run through Western art, from Michelangelo and da Vinci to Handel's Messiah, and remain a constant reference point in law, politics, and everyday English idiom.",
        "principles": "Its central claims are monotheism and covenant &mdash; a binding relationship between God and God's people &mdash; expressed through commandments (most famously the Ten Commandments) and summarized by Jesus as loving God and loving one's neighbor. The New Testament adds the claim of redemption through Christ's death and resurrection, and an ethic built around grace, humility, and forgiveness rather than merit alone.",
        "sources": [("Books of the Bible — Bible Study Tools", "https://www.biblestudytools.com/books-of-the-bible/"), ("New Testament — Encyclopædia Britannica", "https://www.britannica.com/topic/New-Testament")],
    },
    {
        "label": "Islam",
        "sub": "The Qur'an",
        "meta": "Revealed 610–632 CE &middot; 114 surahs, 6,000+ verses (ayahs) &middot; Classical Arabic",
        "history": "Muslims hold that the Qur'an was revealed to the Prophet Muhammad by the angel Jibril (Gabriel) in installments over 23 years, beginning in 610 CE and continuing until Muhammad's death in 632 CE. It was compiled into the single standardized written text still used today within about two decades of his death, under the caliph Uthman. The 114 surahs (chapters) are arranged roughly from longest to shortest rather than chronologically, and are further divided into 30 sections (juz) to support recitation and memorization.",
        "impact": "The Qur'an holds central spiritual, legal, and linguistic authority for more than 1.9 billion Muslims worldwide. It shaped the law, governance, art, architecture, and science of Islamic civilization across more than a millennium, and its principles of justice and accountability remain foundational to Islamic jurisprudence today. Millions of Muslims memorize the entire text (hifz), and though it is recited in its original Arabic, translations have carried its message to non-Arabic-speaking Muslims worldwide.",
        "principles": "Its central tenet is tawhid, the oneness and uniqueness of God, expressed through the Five Pillars of Islam &mdash; testimony of faith, prayer, almsgiving, fasting, and pilgrimage. Alongside theology, the Qur'an offers detailed ethical and legal guidance covering personal conduct, family life, and social responsibility, consistently emphasizing justice, humility, patience, and care for the poor.",
        "sources": [("About the Quran — Quran.com", "https://quran.com/about-the-quran"), ("Structure of the Quran — Islamic Mentors", "https://islamicmentors.com/structure-of-the-quran/")],
    },
    {
        "label": "Judaism",
        "sub": "Torah &middot; Tanakh (Hebrew Bible)",
        "meta": "Torah tradition: c. 13th century BCE &middot; canon finalized ≈ 2nd century CE &middot; 24 books",
        "history": "The Torah &mdash; the five books of Moses, also called the Pentateuch &mdash; is traditionally understood as given to Moses at Sinai; modern scholarship dates its final compilation to roughly the 6th&ndash;5th centuries BCE, drawn from older sources. \"Tanakh\" is an acronym for its three sections: Torah (the five books), Nevi'im (Prophets), and Ketuvim (Writings), a 24-book canon finalized by around the 2nd century CE. Alongside this Written Torah, Jewish tradition holds an Oral Torah &mdash; interpretation and legal discussion eventually recorded in the Mishnah and Talmud.",
        "impact": "The Tanakh remains the foundational text for roughly 15 million Jews worldwide and for Jewish law (halakha), identity, and communal life, studied continuously across generations in its original Hebrew. It is also the shared root of both Christian and Islamic scripture, making it one of the most consequential texts in world history well beyond its own community of readers.",
        "principles": "Its core narrative is the covenant between God and the people of Israel: creation, the patriarchs and matriarchs, the Exodus from Egypt, and the giving of the Law at Sinai. Central themes include ethical monotheism, justice, the 613 commandments (mitzvot) governing daily and communal life, and a continuing relationship between a people and God worked out across historical time rather than resolved once and for all.",
        "sources": [("Tanakh — The Sefaria Library", "https://www.sefaria.org/texts/Tanakh"), ("Torah — New World Encyclopedia", "https://www.newworldencyclopedia.org/entry/Torah")],
    },
    {
        "label": "Buddhism",
        "sub": "The Tripitaka (Pali Canon), including the Dhammapada",
        "meta": "Buddha's teachings c. 5th–4th century BCE &middot; first written down c. 1st century BCE, Sri Lanka",
        "history": "The Tripitaka (\"three baskets\") is the earliest surviving canon of Buddhist scripture, preserving teachings attributed to the Buddha in the 5th&ndash;4th century BCE. Passed down orally by his disciples for centuries, it was first committed to writing in Sri Lanka around the 1st century BCE to protect it amid political upheaval. Its three sections are the Vinaya Pitaka (monastic discipline), the Sutta Pitaka (the Buddha's discourses), and the Abhidhamma Pitaka (philosophical analysis). The Dhammapada &mdash; 423 verses across 26 chapters, among the most-read Buddhist texts anywhere &mdash; sits within the Sutta Pitaka.",
        "impact": "The Pali Canon is the scriptural foundation of Theravada Buddhism, practiced widely across Sri Lanka, Thailand, Myanmar, and Southeast Asia, within a global Buddhist population estimated at roughly 500 million. Despite existing in written form for two thousand years, memorization and oral recitation remain living practice &mdash; many laypeople still know passages by heart. The Dhammapada specifically has been translated into dozens of languages and is a frequent entry point for readers outside the tradition, including through the modern mindfulness movement.",
        "principles": "At its core are the Four Noble Truths (the reality of suffering, its cause, its cessation, and the path to that cessation) and the Noble Eightfold Path that follows from them. Other central ideas include anatta (there is no fixed, permanent self), anicca (impermanence), karma and rebirth, and the ultimate goal of Nirvana &mdash; release from the cycle of craving and rebirth.",
        "sources": [("Buddhism: The Pali Canon (Tipitaka) — Encyclopædia Britannica", "https://www.britannica.com/topic/Buddhism/The-Pali-canon-Tipitaka"), ("Tipitaka: The Pali Canon — Access to Insight", "https://accesstoinsight.org/tipitaka/")],
    },
    {
        "label": "Greek Mythology",
        "sub": "Hesiod &middot; Homer &middot; Ovid &middot; the broader mythological corpus",
        "meta": "Oral tradition from c. 1600 BCE &middot; first written down c. 8th century BCE (Homer, Hesiod)",
        "history": "Greek mythology isn't a single scripture but a body of story handed down orally from the Minoan (c. 3000&ndash;1450 BCE) and Mycenaean (c. 1600&ndash;1100 BCE) civilizations, first fixed in writing around the 8th century BCE. Homer's epics, the Iliad and the Odyssey, established the character of the gods and the great mythic heroes; Hesiod's Theogony gave the fullest early account of the gods' origins and genealogy. Centuries later, the Roman poet Ovid's Metamorphoses (1st century CE) retold and reshaped over 250 of these myths for a Roman audience, becoming, after the Renaissance rediscovery of antiquity, the version most later European art and poetry actually drew on.",
        "impact": "Greek mythology is a cornerstone of Western literature, art, and language: everyday expressions like \"Achilles' heel,\" \"narcissism,\" and \"Oedipal\" trace straight back to these stories. Its themes are continually retold in modern film, fiction, and psychology, and its imagery has shaped Western visual art from classical sculpture through the Renaissance to the present.",
        "principles": "Rather than a single moral system, these myths circle recurring themes: fate versus free will, hubris (overreaching pride) and its inevitable punishment, the uneasy relationship between mortals and gods, and transformation as both punishment and revelation. A moral order (often called dike, or justice) runs underneath the stories even when the gods themselves behave capriciously.",
        "sources": [("Greek mythology — Encyclopædia Britannica", "https://www.britannica.com/topic/Greek-mythology"), ("Classical mythology in culture — Wikipedia", "https://en.wikipedia.org/wiki/Classical_mythology_in_culture")],
    },
    {
        "label": "Philosophy",
        "sub": "Plato &middot; Aristotle &middot; the Stoics &middot; Plotinus &middot; Boethius, and the wider classical tradition",
        "meta": "Begins c. 6th century BCE (Pre-Socratics) &middot; continues through late antiquity",
        "history": "Western philosophy in this tradition begins with the Pre-Socratic thinkers of the 6th century BCE and comes into its own with Socrates, Plato, and Aristotle in 5th&ndash;4th century BCE Athens. Plato's dialogues located ultimate truth in a realm of eternal Forms; his student Aristotle turned instead to careful, systematic observation of the natural world and human life, and developed formal logic as a tool for reasoning about both. In the Hellenistic period, Zeno of Citium founded Stoicism around 300 BCE, teaching that a good life comes from living in harmony with reason and nature rather than chasing pleasure or fleeing pain — a line of thought later carried forward by the Roman-era writers Epictetus and Boethius, and, in a different key, by the Neoplatonist Plotinus.",
        "impact": "These texts are foundational to Western philosophy, science, logic, and political thought; medieval Jewish, Muslim, and Christian scholars all rediscovered and absorbed Plato and Aristotle into their own theology. Stoicism in particular has seen a major modern revival, both in popular self-help writing and, more substantively, as an intellectual ancestor of cognitive behavioral therapy's core insight that our reactions to events, not the events themselves, are what we can actually control.",
        "principles": "Across these different schools runs a shared commitment to pursuing truth, virtue, and the good life (eudaimonia) through reasoned argument rather than myth or tradition alone. Aristotle's ethics center on virtue as a mean between extremes; the Stoics distinguish sharply between what is and isn't within a person's control; and later writers like Plotinus and Boethius fold this ethical inquiry into a search for a single highest Good underlying all of reality.",
        "sources": [("Greek philosophy — Encyclopædia Britannica", "https://www.britannica.com/topic/Greek-philosophy"), ("Ancient Greek Philosophy — Internet Encyclopedia of Philosophy", "https://iep.utm.edu/ancient-greek-philosophy/")],
    },
]

# Jainism entry (researched separately) is inserted after Buddhism once Jainism is live.
_JAIN_ENTRY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jain", "historical_entry.json")
if JAIN_ON and os.path.exists(_JAIN_ENTRY_FILE):
    _je = json.load(open(_JAIN_ENTRY_FILE, encoding="utf-8"))
    _je["sources"] = [tuple(x) for x in _je["sources"]]
    _bi = next(i for i, e in enumerate(TEXT_ENTRIES) if e["label"] == "Buddhism")
    TEXT_ENTRIES.insert(_bi + 1, _je)

# Sikhism entry is inserted after Jainism (or Buddhism) once Sikhism is live.
_SIKH_ENTRY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sikh", "historical_entry.json")
if SIKH_ON and os.path.exists(_SIKH_ENTRY_FILE):
    _se = json.load(open(_SIKH_ENTRY_FILE, encoding="utf-8"))
    _se["sources"] = [tuple(x) for x in _se["sources"]]
    _after = "Jainism" if any(e["label"] == "Jainism" for e in TEXT_ENTRIES) else "Buddhism"
    _bi = next(i for i, e in enumerate(TEXT_ENTRIES) if e["label"] == _after)
    TEXT_ENTRIES.insert(_bi + 1, _se)

def historical_texts_page():
    entries_html = []
    for e in TEXT_ENTRIES:
        src_links = " &middot; ".join(f'<a href="{url}" target="_blank" rel="noopener">{html.escape(title)}</a>' for title, url in e["sources"])
        entries_html.append(f"""<div class="text-entry">
  <h2>{e['label']}</h2>
  <p class="meta">{e['sub']}<br>{e['meta']}</p>
  <h4>Brief History</h4>
  <p>{e['history']}</p>
  <h4>Impact Today</h4>
  <p>{e['impact']}</p>
  <h4>Morals, Philosophy &amp; Core Principles</h4>
  <p>{e['principles']}</p>
  <p class="learn-more">Learn more: {src_links}</p>
</div>""")
    body = f"""<h1 class="page-title">Historical Texts</h1>
<p>&ldquo;Through the Lens of&rdquo; draws a correspondence for every kural from {N_TRADS_WORD} traditions. This page is background on those {N_TRADS_WORD} sources themselves &mdash; where each comes from, what it looks like today, and the core principles it teaches &mdash; independent of any single kural.</p>
{''.join(entries_html)}"""
    return page_shell("Historical Texts", "historical-texts.html", body)

def history_page():
    body = """<h1 class="page-title">History of the Thirukkural</h1>
<div class="prose">

<h3>Who was Thiruvalluvar?</h3>
<p>Very little about Thiruvalluvar's life can actually be verified. Even basic details, such as where he lived, what work he did, what faith he followed, and when he lived, are debated by historians, and different traditions and scholars say different things. Because the evidence is so thin, this project does not pick a side. What we can say is that the Thirukkural itself never argues for one religion, and that people of many backgrounds have claimed it as their own.<sup class="src-ref"><a href="#src-1">[1]</a></sup> Popular stories about his life, including the one about his wife Vasuki and the handful of sand she turned into rice, are loved legends passed down over centuries. They are not documented history.<sup class="src-ref"><a href="#src-2">[2]</a></sup></p>

<h3>When was it written?</h3>
<p>Dating the Thirukkural is a genuinely open scholarly question, and estimates vary widely depending on the method used. Tamil Nadu's government officially adopted 31 BCE as Valluvar's year of birth in January 1935, and built an entire calendar system &mdash; the Valluvar Year, currently 31 years ahead of the Gregorian calendar &mdash; around that date.<sup class="src-ref"><a href="#src-3">[3]</a></sup> Scholars who work from the text's internal linguistic and cultural evidence tend to land elsewhere: Kamil Zvelebil, a Czech scholar of Tamil literature, considered dates earlier than 1 BCE unsupported by the text itself; a commonly cited scholarly window is roughly 200 BCE&ndash;200 CE; and Stuart Blackburn has described the present scholarly consensus as centering closer to 500 CE.<sup class="src-ref"><a href="#src-4">[4]</a></sup> In short: the traditional/official date and the range favored by textual scholars don't agree, and neither is settled beyond dispute.</p>

<h3>How the text is organized</h3>
<p>The Thirukkural's 1,330 couplets (kurals) are grouped into 133 chapters (adhikarams) of exactly 10 couplets each, and those 133 chapters are in turn organized into three books: <strong>Aram</strong> (virtue, chapters 1&ndash;38), <strong>Porul</strong> (wealth, statecraft, and worldly life, chapters 39&ndash;108), and <strong>Inbam</strong> (love, chapters 109&ndash;133).<sup class="src-ref"><a href="#src-5">[5]</a></sup> Each kural itself is written in a tight, fixed couplet form &mdash; traditionally described as seven metrical feet in total, four in the first line and three in the second &mdash; which is part of why the text reads so much like proverb or aphorism even in translation.<sup class="src-ref"><a href="#src-5">[5]</a></sup></p>

<h3>The commentary tradition</h3>
<p>Ten medieval commentators are traditionally credited with writing authoritative commentaries on the Kural; of these, five have survived and reached the modern era: Manakkudavar, Pari Perumal, Kaalingar, Paridhi, and Parimelalhagar.<sup class="src-ref"><a href="#src-6">[6]</a></sup> Parimelalhagar, writing around the 13th century CE, is generally regarded by scholars as having produced the finest of these commentaries, both textually and as literature, and his reading of the text remains the most influential traditional interpretation used today.<sup class="src-ref"><a href="#src-6">[6]</a></sup></p>

<h3>Reaching the rest of the world</h3>
<p>The Thirukkural's best-known bridge into English came in 1886, when the missionary-scholar G.U. Pope published <em>The Sacred Kurral of Tiruvalluva Nayanar</em> in London &mdash; the translation still most widely cross-referenced today, including throughout this project.<sup class="src-ref"><a href="#src-7">[7]</a></sup> Since then the text has been rendered into roughly 30 English versions on its own, and into more than 100 versions across around 30 languages worldwide.<sup class="src-ref"><a href="#src-7">[7]</a></sup></p>

<h3>A living text in Tamil Nadu</h3>
<p>The Thirukkural remains a genuinely public, civic text in Tamil Nadu rather than a purely academic or purely religious one. Thiruvalluvar Day is an official state holiday, observed as part of the Pongal harvest festival in mid-January.<sup class="src-ref"><a href="#src-8">[8]</a></sup> And at Kanyakumari, a 133-foot statue of Thiruvalluvar &mdash; dedicated on January 1, 2000 &mdash; encodes the text's own structure into its architecture: the statue and pedestal together stand 133 feet tall for the text's 133 chapters, with the 95-foot figure of Valluvar resting on a 38-foot pedestal representing the 38 chapters of the Aram (Virtue) book alone.<sup class="src-ref"><a href="#src-9">[9]</a></sup></p>

</div>

<footer class="sources">
  <strong>Sources</strong>
  <ol>
    <li id="src-1">Thiruvalluvar &mdash; biographical summary, composite of standard sources including <a href="https://en.wikipedia.org/wiki/Thiruvalluvar" target="_blank" rel="noopener">Wikipedia: Thiruvalluvar</a> and <a href="https://www.britannica.com/biography/Tiruvalluvar" target="_blank" rel="noopener">Encyclop&aelig;dia Britannica: Tiruvalluvar</a>.</li>
    <li id="src-2">Vasuki (wife of Valluvar) &mdash; traditional accounts and historians' caveats, <a href="https://en.wikipedia.org/wiki/Vasuki_(wife_of_Valluvar)" target="_blank" rel="noopener">Wikipedia: Vasuki (wife of Valluvar)</a>.</li>
    <li id="src-3">Valluvar Year &mdash; official Tamil Nadu calendar reform of January 1935, <a href="https://en.wikipedia.org/wiki/Valluvar_year" target="_blank" rel="noopener">Wikipedia: Valluvar year</a>.</li>
    <li id="src-4">Dating the Tirukkural &mdash; range of scholarly estimates (Zvelebil, Blackburn, and others), <a href="https://en.wikipedia.org/wiki/Dating_the_Tirukkural" target="_blank" rel="noopener">Wikipedia: Dating the Tirukkural</a>.</li>
    <li id="src-5">Structure of the Tirukkural &mdash; 1,330 couplets / 133 chapters / 3 books, composite of standard reference sources including <a href="https://en.wikipedia.org/wiki/Aram_(Kural_book)" target="_blank" rel="noopener">Wikipedia: Aram (Kural book)</a> and <a href="https://en.wikipedia.org/wiki/Inbam_(Kural_book)" target="_blank" rel="noopener">Wikipedia: Inbam (Kural book)</a>.</li>
    <li id="src-6">Parimelalhagar and the medieval commentary tradition, <a href="https://en.wikipedia.org/wiki/Parimelalhagar" target="_blank" rel="noopener">Wikipedia: Parimelalhagar</a>.</li>
    <li id="src-7">G.U. Pope's 1886 translation and the Kural's translation history, composite of standard sources including the <a href="https://en.wikipedia.org/wiki/Tirukkural_translations_into_English" target="_blank" rel="noopener">Wikipedia: Tirukkural translations into English</a>.</li>
    <li id="src-8">Thiruvalluvar Day as a Tamil Nadu public holiday during Pongal, composite of standard holiday-reference sources.</li>
    <li id="src-9">Thiruvalluvar Statue, Kanyakumari &mdash; dimensions and symbolism, <a href="https://en.wikipedia.org/wiki/Thiruvalluvar_Statue" target="_blank" rel="noopener">Wikipedia: Thiruvalluvar Statue</a>.</li>
  </ol>
</footer>"""
    return page_shell("History of the Thirukkural", "history.html", body)

os.makedirs(f"{BASE}/web", exist_ok=True)
with open(f"{BASE}/web/index.html", "w", encoding="utf-8") as f:
    f.write(home_page())
with open(f"{BASE}/web/kurals.html", "w", encoding="utf-8") as f:
    f.write(kurals_hub_page())
with open(f"{BASE}/web/historical-texts.html", "w", encoding="utf-8") as f:
    f.write(historical_texts_page())
with open(f"{BASE}/web/history.html", "w", encoding="utf-8") as f:
    f.write(history_page())

for i, k in enumerate(kurals):
    prev_k = kurals[i-1]["number"] if i > 0 else None
    next_k = kurals[i+1]["number"] if i < len(kurals)-1 else None
    with open(f"{BASE}/web/{kural_fn(k['number'])}", "w", encoding="utf-8") as f:
        f.write(kural_page(k, prev_k, next_k))

for n in AVAILABLE_ADHIKARAMS:
    with open(f"{BASE}/web/{adhikaram_fn(n)}", "w", encoding="utf-8") as f:
        f.write(adhikaram_page(ADHIKARAM_BY_NUM[n]))

print("Wrote", len(kurals) + len(AVAILABLE_ADHIKARAMS) + 4, "html files "
      f"({len(kurals)} kurals, {len(AVAILABLE_ADHIKARAMS)} chapter pages, "
      "4 hub/static pages)")
