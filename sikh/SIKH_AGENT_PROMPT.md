You are producing content for a large, accuracy-critical annotated translation of the Thirukkural (classical Tamil ethical text, 1330 couplets, 133 chapters of 10 couplets each). Each kural already has cross-references to eight traditions (Hinduism, Christianity, Islam, Judaism, Buddhism, Jainism, Greek mythology, philosophy). Your job is to ADD SIKHISM to existing kurals, held to exactly the same research standard. Self-contained task — no prior context available.

PROJECT = /Users/adhigopal/Documents/Thirukkural

ASSIGNMENT: Chapter(s) {chapters}.

CONTEXT TO READ FIRST: For each kural in your chapters, read its entry in PROJECT/thirukkural-project/data/kurals.json (fields: number, adhikaram, tamil, transliteration, meaning, university, and the existing cross_references). That gives you the verified Tamil text, its meaning and the commentary tradition. Do not change any of it. Look at the existing cross-references only to match tone and length — do not reuse their ideas for the Sikh slot.

OUTPUT: For each chapter N, write ONE file with ONE Write call: PROJECT/sikh/sikh_chapter_NN.json (two-digit N, e.g. sikh_chapter_07.json; three digits for 100+). Do NOT return JSON in your reply — only a short (2-3 sentence) confirmation listing any entries below 60% and anything you could not verify.

JSON SHAPE: {"chapter": N, "sikhism": {"<kural number as string>": entry, ... all 10 kurals ...}, "new_sources": {citation_id: {tier, title, author/translator, publisher, url, access_date}}}

Each entry has exactly these keys:
{"quote_or_event": ..., "explanation": 1-2 sentences, "tie_back": 1 sentence linking to this kural, "source": human-readable citation, "citation_id": slug, "is_quote": bool, "_accuracy_percent": 0-100, "_accuracy_note": 1 honest sentence}

For Guru Granth Sahib quotes, `source` must give the Guru/author, the bani or raag, and the Ang (page) number, e.g. "Guru Granth Sahib, Ang 62, Sri Raag, Guru Nanak (tr. Sant Singh Khalsa)". Gurmukhi wording is not required; the English translation used must be named.

WHERE TO LOOK (live web sources; verify every verbatim quote in this session):
- Sri Guru Granth Sahib with Sant Singh Khalsa's English translation: srigranth.org, sikhitothemax.org, searchgurbani.com (all show Ang numbers). Use citation id `sggs-khalsa`. If you quote a different translation (e.g. Manmohan Singh, Gopal Singh), make a new id naming that translator.
- Japji Sahib (Ang 1-8) is part of the SGGS — cite it as SGGS with Ang.
- Vaaran Bhai Gurdas (searchgurbani.com, with Pauri numbers): `bhai-gurdas-vaaran` — important early exegesis, not scripture; say so in the note.
- Max Arthur Macauliffe, The Sikh Religion (1909, 6 vols, public domain; sacred-texts.com/skh/): `macauliffe-1909` — for paraphrased accounts of the Gurus' lives.
- Well-attested events from Sikh history (Guru Nanak's "true bargain" feeding of sadhus, the institution of langar, Guru Angad and Gurmukhi, Guru Amar Das requiring visitors to eat in the langar, Guru Arjan compiling the Adi Granth (1604) and his martyrdom (1606), Guru Tegh Bahadur's martyrdom (1675), Guru Gobind Singh founding the Khalsa (1699), Bhai Kanhaiya giving water to wounded on both sides). Cite these as paraphrase (is_quote=false) from Macauliffe, Britannica, or a university/encyclopedic source. Janamsakhi stories are hagiography: say "according to the Janamsakhi tradition" and score accordingly.
- Dasam Granth: its authorship is contested within Sikhism. Use only if nothing in the SGGS fits, and say so in the note.

Canonical citation ids: read PROJECT/sikh/canonical_sources.json. Those ids have FIXED definitions that override anything you put in new_sources. Use a canonical id only when your entry really comes from that exact work/translation. Any other id gets a full new_sources entry with tier "primary" | "secondary" | "web".

SOURCE QUALITY: Never use AI-generated sites (any "AI answer" page, chatbots) as a source or verification. Use Wikipedia only as a last resort and only for paraphrased (is_quote=false) entries, saying so in the note. If one Gurbani site rate-limits you, try the others before downgrading.

RULES (same standard as every other tradition in this edition):
- First understand what the chapter is about (the university field helps), then find Sikhism's closest genuine teaching on that theme for each kural.
- is_quote=true ONLY for wording verified verbatim against a live source in this session, with the translation named in `source`. Otherwise is_quote=false and write plain descriptive prose with no quotation marks.
- Every kural must get a Sikh entry. If no strong match exists, give the best next-best match with _accuracy_percent below 60 and a candid note. Never fabricate a quote, Ang number, pauri number, or source.
- Represent Sikhism accurately on its own terms: one formless God (Ik Onkar, Waheguru), the Guru's word (Gurbani/shabad), naam simran, kirat karni (honest work), vand chhakna (sharing), seva, rejection of caste and empty ritual, the householder path over renunciation, haumai (ego) as the root problem, hukam (divine order), the five thieves (kaam, krodh, lobh, moh, ahankar). Where the Kural conflicts with Sikh teaching (e.g. asceticism, ritual, caste-based duty), say so honestly and score accordingly.
- Don't duplicate the Hinduism, Islam or Jainism slot for the same kural: find a distinctly Sikh source.
- Inbam (love) chapters 109-133: Gurbani uses the bride-soul longing for the divine Husband-Lord as a central image (e.g. separation, longing, union). That is a genuine and often strong parallel, but say in the note that it is spiritual, not romantic, love. Keep everything tasteful.
- Accuracy scoring: 85-95 near one-to-one; 70-84 strong thematic fit; 60-69 reasonable but partial; below 60 next-best only.
- Time budget: about 20 minutes. If a page won't load or is rate-limited, don't wait on it — use another source, or mark the entry is_quote=false with an honest note.

Work through every kural with full rigor, compose each chapter's complete JSON, write each file in one call, then reply with only a short confirmation.
