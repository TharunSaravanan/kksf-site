You are producing content for a large, ongoing, accuracy-critical annotated translation of the Thirukkural (classical Tamil ethical text, 1330 couplets, 133 chapters of 10 couplets each). Each kural already has cross-references to seven traditions (Hinduism, Christianity, Islam, Judaism, Buddhism, Greek mythology, philosophy). Your job is to ADD an eighth tradition, JAINISM, to existing kurals, held to exactly the same research standard as the other seven. Self-contained task — no prior context available.

PROJECT = /Users/adhigopal/Documents/Thirukkural

ASSIGNMENT: Chapter(s) {chapters}.

CONTEXT TO READ FIRST: For each kural in your chapters, read its existing entry in PROJECT/thirukkural-project/data/kurals.json (fields: number, adhikaram, tamil, transliteration, meaning, university, and the seven existing cross_references). That gives you the verified Tamil text, its meaning, and the commentary tradition. Do not change any of that content. Look at the existing cross-references only to match tone and length — do not copy their ideas into the Jain slot.

OUTPUT: For each chapter N, write ONE file with ONE Write call: PROJECT/jain/jain_chapter_NN.json (two-digit N, e.g. jain_chapter_07.json). Do NOT return JSON in your reply — only a short (2-3 sentence) confirmation listing any entries below 60% and anything you could not verify.

JSON SHAPE: {"chapter": N, "jainism": {"<kural number as string>": entry, ... all 10 kurals ...}, "new_sources": {citation_id: {tier, title, author/translator, publisher, url, access_date}}}

Each entry has exactly these keys:
{"quote_or_event": ..., "explanation": 1-2 sentences, "tie_back": 1 sentence linking to this kural, "source": human-readable citation with chapter/verse/sutra number, "citation_id": slug, "is_quote": bool, "_accuracy_percent": 0-100, "_accuracy_note": 1 honest sentence}

Example (real, Uttaradhyayana Sutra): {"quote_or_event": "“Though a man should conquer thousands and thousands of valiant (foes), greater will be his victory if he conquers nobody but himself.”", "explanation": "Mahavira's teaching ranks mastery of one's own self above every outward conquest.", "tie_back": "<one sentence tying it to the specific kural>", "source": "Uttaradhyayana Sutra 9.34 (tr. Hermann Jacobi, SBE 45)", "citation_id": "uttaradhyayana-jacobi", "is_quote": true, "_accuracy_percent": 85, "_accuracy_note": "<honest note>"}
(The quote above is illustrative of format; verify any wording you actually use against a live source.)

WHERE TO LOOK (prefer primary scripture; use live web sources such as sacred-texts.com, wisdomlib.org, jainqq.org, archive.org, jainworld.com, herenow4u.net):
- Svetambara Agamas in Hermann Jacobi's public-domain translations: Acaranga Sutra and Kalpa Sutra (Sacred Books of the East vol. 22, 1884); Uttaradhyayana Sutra and Sutrakritanga (SBE vol. 45, 1895). Also Dasavaikalika Sutra.
- Tattvartha Sutra of Umasvati (accepted by both Svetambara and Digambara; tr. Nathmal Tatia, "That Which Is", 1994, or other published translations).
- Digambara works: Kundakunda's Samayasara / Pravachanasara / Niyamasara; Samantabhadra's Ratnakaranda Shravakachara (tr. Champat Rai Jain); Amritachandra's Purusharthasiddhyupaya (tr. Ajit Prasada); Hemachandra's Yogashastra.
- Jain narrative: the life of Mahavira (Kalpa Sutra, Acaranga Book 2), Rishabhanatha, Bahubali and Bharata, Parshvanatha, and other well-attested stories from the Jain Puranas / Trishashti-shalaka-purusha-charitra.
- Tamil Jain literature: Naladiyar (tr. G.U. Pope, 1893), Jivaka Chintamani, Neelakesi. These are legitimate Jain sources and often close to the Kural; use them when they are genuinely the best fit, but prefer canonical scripture when a comparable match exists, and say in _accuracy_note when you used a Tamil Jain text.
- Jain readings of the Kural itself (e.g. the long-standing claim that 'Adi Bhagavan' in Kural 1 refers to Rishabhanatha, or that 'malarmisai ekinan' in Kural 3 describes a Jina) may be cited when relevant, framed honestly as an interpretive tradition, not as settled fact.

Canonical citation ids: read PROJECT/jain/canonical_sources.json. Those ids have FIXED definitions (a specific translation/edition) that override anything you put in new_sources. Use a canonical id only when your entry really comes from that exact translation. If you quote a different translation (e.g. a different Tattvartha Sutra translator, or a scripture verse as rendered in the Saman Suttam anthology or in Sangave's book), use the id for the work you actually read (e.g. saman-suttam, tattvartha-sutra-vijayjain, sangave-ethics-jainworld) or create a new id. Any non-canonical id gets a full new_sources entry with tier "primary" | "secondary" | "web".

SOURCE QUALITY: Never use AI-generated sites (e.g. jaingpt.org or any "AI answer" page) as a source or as verification. Use Wikipedia only as a last resort, and only for paraphrased (is_quote=false) entries, with the note saying so. If archive.org or another site rate-limits you, try sacred-texts.com, wisdomlib.org, jainqq.org or herenow4u.net before downgrading.

RULES (same standard as every other tradition in this edition):
- First understand what this chapter is about (its theme in Parimelazhagar's and modern commentaries — the university field helps), then find Jainism's closest genuine teaching on that theme for each kural.
- is_quote=true ONLY for wording you verified verbatim against a live source in this session; give the exact translation used in `source`. Otherwise is_quote=false and write plain descriptive prose with no quotation marks.
- Every kural must get a Jain entry. If no strong match exists, give the best next-best match with _accuracy_percent below 60 and a candid note. Never fabricate a quote, verse/sutra number, or source.
- Represent Jainism accurately on its own terms: non-theistic (no creator God; Jinas/Tirthankaras as perfected souls), ahimsa, anekantavada, karma as subtle matter binding the soul (jiva), the three jewels (right faith, knowledge, conduct), the vows (vratas) for monks and laypeople. Where the Kural's assumption conflicts with Jain doctrine (e.g. a creator God, rain as divine gift, warfare, meat), say so honestly and score accordingly rather than forcing a fit.
- Don't let Jainism duplicate the Buddhism or Hinduism slot for the same kural: find a distinctly Jain source.
- Inbam (love) chapters 109-133: Jain sources on love are mostly about renunciation; look for genuine Jain narrative or Tamil Jain poetry (e.g. Jivaka Chintamani's romances, the Rajimati–Neminatha story) and score honestly. Keep everything tasteful and non-explicit.
- Accuracy scoring should be comparable to the other traditions: 85-95 near one-to-one; 70-84 strong thematic fit; 60-69 reasonable but partial; below 60 next-best only.

Work through every kural with full rigor, compose each chapter's complete JSON, write each file in one call, then reply with only a short confirmation.
