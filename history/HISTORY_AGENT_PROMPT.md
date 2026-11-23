You are producing content for a large, accuracy-critical annotated study edition of the Thirukkural (classical Tamil ethical text, 1330 couplets, 133 chapters of 10 couplets each). Each kural already has a translation, commentary, and cross-references to religious and philosophical traditions. Your job is to ADD a "Real Life Example" to each kural: one real, well-documented event from history that shows the kural's idea playing out. Self-contained task — no prior context available.

PROJECT = /Users/adhigopal/Documents/Thirukkural

ASSIGNMENT: Chapter(s) {chapters}.

CONTEXT TO READ FIRST: For each kural, read its entry in PROJECT/thirukkural-project/data/kurals.json (meaning, elementary, university). Understand the kural's actual claim before looking for an event. Do not change any existing content.

ALSO READ FIRST: every existing PROJECT/history/history_chapter_*.json file, and note the event_title values already used. Do not reuse an event that already appears twice anywhere in the book, and prefer events not yet used at all.

OUTPUT: For each chapter N, write ONE file with ONE Write call: PROJECT/history/history_chapter_NN.json (two-digit N; three digits for 100+). Do NOT return JSON in your reply — only a short (2-3 sentence) confirmation listing any entries below 60%.

JSON SHAPE: {"chapter": N, "real_life_example": {"<kural number as string>": entry, ... all 10 kurals ...}, "new_sources": {citation_id: {tier, title, author, publisher, url, access_date}}}

Each entry has exactly these keys:
{
 "event_title": short name of the event, e.g. "Jonas Salk declines to patent the polio vaccine",
 "date": year or date as reference works give it, e.g. "1955" or "1 December 1955",
 "place": e.g. "Montgomery, Alabama, United States",
 "event": 2-3 sentences stating only the documented facts of what happened, in plain prose,
 "explanation": 1-2 sentences on why the event matters / what it shows,
 "tie_back": 1 sentence connecting it to this specific kural,
 "citation_ids": [at least two ids, from independent reputable sources],
 "_accuracy_percent": 0-100 — how well the event illustrates THIS kural (the facts themselves must be 100% solid regardless),
 "_accuracy_note": 1 honest sentence on the fit
}

WHAT COUNTS AS A VALID EVENT (all must be true):
- Popular, mainstream history: the kind of event found in school textbooks and standard reference works, that most educated people would recognise or could easily confirm.
- The basic facts are not in dispute among historians (who, what, when, where). No legends, apocrypha or "it is said" anecdotes (e.g. Washington's cherry tree, Newton's apple falling on his head, Nero fiddling, Canute and the tide as commonly told, Marie Antoinette's "let them eat cake").
- Confirmed by at least TWO independent reputable sources, checked live in this session: e.g. Encyclopaedia Britannica, national archives or libraries (Library of Congress, UK National Archives), government history offices, major museums, university pages, the Nobel Prize site, UNESCO, established history publishers (History.com is acceptable as one of the two), reputable newspapers of record. Wikipedia may be used to orient yourself but does NOT count toward the two sources.
- Not ongoing, not from the last 20 years, and not a live partisan political controversy. Avoid events whose very meaning is still fiercely contested between nations or communities; if a war or conflict is relevant, use an uncontested, specific, documented act within it.
- No graphic violence, no sexual content; keep it suitable for school readers.
- No direct quotations unless you verified the exact words against a live reputable source and the quote is famous and undisputed (e.g. a recorded speech). Otherwise describe in prose, with no quotation marks.
- Do not attribute motives or private thoughts that the sources don't document. The explanation and tie_back may interpret; the event field may not.

VARIETY: Draw from the whole world and all eras — ancient, medieval, modern; Asia, Africa, Europe, the Americas, the Middle East, Oceania; science, exploration, medicine, sport, the arts, civil rights, statecraft, business, everyday heroism. Indian and Tamil history are welcome (e.g. Raja Raja Chola's Brihadeeswarar temple, Ashoka after Kalinga, the Salt March) but should not dominate. Within a chapter, try not to use the same country twice.

QUALITY OF FIT: First understand the kural's precise claim (the university field helps). Pick the event that illustrates THAT claim, not just the chapter's general theme. Love chapters (109-133) are about romantic love, longing and separation: use well-documented, tasteful real-life examples (famous documented marriages, letters, long separations, devotion — e.g. Shah Jahan building the Taj Mahal for Mumtaz Mahal) and score honestly. If no strong fit exists, give the best well-documented next-best event with _accuracy_percent below 60 and a candid note. Never stretch or embellish the facts to make a better fit.

Scoring: 85-95 the event is almost a dramatisation of the kural; 70-84 strong illustration; 60-69 reasonable but partial; below 60 next-best only.

new_sources: every citation id you use needs a full entry: {"tier": "secondary" (reference works, museums, archives, scholarly sites) | "primary" (original documents, e.g. an archive's scan of a law or letter) | "web" (general sites such as History.com), "title": page title, "author" if known, "publisher", "url" (the exact page you checked), "access_date": today's date}. Use descriptive, unique ids, e.g. "britannica-salk-polio", "loc-montgomery-bus-boycott".

Time budget: about 20 minutes. If a page won't load or is rate-limited, use another reputable source rather than waiting.

Work through every kural with full rigor, compose each chapter's complete JSON, write each file in one call, then reply with only a short confirmation.
