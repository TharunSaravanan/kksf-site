# -*- coding: utf-8 -*-
import json
import os
import glob

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thirukkural-project")
OUTPUTS_ROOT = os.path.dirname(BASE)

sources = {
    "ytamizh-ch1": {"tier": "web", "title": "கடவுள் வாழ்த்து (The Praise of God) — Chapter 1, with commentary by Mu. Varadarajan, Solomon Pappaiah, M. Karunanidhi, and Sivayogi Sivakumar", "publisher": "ytamizh.com", "url": "https://www.ytamizh.com/thirukural/chapter-1/", "access_date": "2026-09-21"},
    "thirukkuralnet-adhigaram1": {"tier": "web", "title": "The Praise of God — Adhigaram 1 (Tamil text, transliteration, English translation, song setting by Pu. A. Muthukrishnan)", "publisher": "thirukkural.net", "url": "https://www.thirukkural.net/en/kural/adhigaram-001.html", "access_date": "2026-09-21"},
    "pope-1886": {"tier": "primary", "title": "The Sacred Kurral of Tiruvalluva Nayanar", "author": "G.U. Pope", "year": "1886"},
    "gita-mukundananda": {"tier": "primary", "title": "Bhagavad Gita, The Song of God", "author": "Swami Mukundananda", "publisher": "holy-bhagavad-gita.org", "url": "https://www.holy-bhagavad-gita.org/"},
    "gita-asitis": {"tier": "primary", "title": "Bhagavad-gita As It Is", "author": "A.C. Bhaktivedanta Swami Prabhupada", "publisher": "vedabase.io / asitis.com", "url": "https://vedabase.io/en/library/bg/"},
    "mundaka-upanishad": {"tier": "primary", "title": "Mundaka Upanishad 1.2.12-13", "publisher": "wisdomlib.org", "url": "https://www.wisdomlib.org/hinduism/book/mundaka-upanishad-shankara-bhashya/d/doc145096.html"},
    "isha-upanishad": {"tier": "primary", "title": "Isha Upanishad, verse 7", "publisher": "wisdomlib.org / Sri Aurobindo Ashram"},
    "katha-upanishad": {"tier": "primary", "title": "Katha Upanishad 1.3.3 (the chariot allegory)", "publisher": "wisdomlib.org"},
    "ramayana-ravana": {"tier": "secondary", "title": "Valmiki Ramayana, the character and downfall of Ravana", "publisher": "composite of standard summaries (Valmiki Ramayana)"},
    "kjv": {"tier": "primary", "title": "The Holy Bible, King James Version"},
    "quran-sahih": {"tier": "primary", "title": "The Qur'an, Sahih International translation", "publisher": "quran.com / corpus.quran.com"},
    "quran-general": {"tier": "primary", "title": "The Qur'an, composite of standard English translations", "publisher": "quran.com / islamawakened.com"},
    "bukhari-6416": {"tier": "primary", "title": "Sahih al-Bukhari 6416, Book of Ar-Riqaq", "publisher": "sunnah.com"},
    "dhammapada-buddharakkhita": {"tier": "primary", "title": "The Dhammapada", "translator": "Acharya Buddharakkhita", "publisher": "accesstoinsight.org / buddhanet.net"},
    "dhammapada-narada": {"tier": "primary", "title": "The Dhammapada", "translator": "Narada Thera", "publisher": "wisdomlib.org / vivekavani.com"},
    "majjhima-nikaya-22": {"tier": "primary", "title": "Alagaddupama Sutta (Majjhima Nikaya 22) — the Raft Parable", "publisher": "accesstoinsight.org / budsas.org"},
    "dhajagga-sutta": {"tier": "primary", "title": "Dhajagga Sutta (Samyutta Nikaya 11.3)", "publisher": "accesstoinsight.org"},
    "devadatta-story": {"tier": "secondary", "title": "The story of Devadatta", "publisher": "composite of standard Buddhist tradition sources (Vinaya Pitaka / Dhammapada commentary)"},
    "adi-buddha": {"tier": "secondary", "title": "Adi-Buddha in the Kalachakra Tantra", "publisher": "composite of standard Vajrayana Buddhist sources"},
    "hesiod-theogony": {"tier": "primary", "title": "Theogony", "author": "Hesiod", "translator": "H.G. Evelyn-White", "publisher": "Loeb Classical Library 57 (1914), via theoi.com", "url": "https://www.theoi.com/Text/HesiodTheogony.html"},
    "aristotle-metaphysics": {"tier": "primary", "title": "Metaphysics, Book XII (Lambda)", "author": "Aristotle", "publisher": "The Internet Classics Archive (MIT)", "url": "https://classics.mit.edu/Aristotle/metaphysics.12.xii.html"},
    "homer-odyssey": {"tier": "primary", "title": "Odyssey, Book 12 (the Sirens episode)", "author": "Homer", "publisher": "Perseus Digital Library / Theoi Classical Texts"},
    "charon-myth": {"tier": "secondary", "title": "Charon, ferryman of the River Styx", "publisher": "Theoi.com / Encyclopedia.com / Britannica"},
    "ovid-arachne": {"tier": "primary", "title": "Metamorphoses, Book VI (the myth of Arachne)", "author": "Ovid"},
    "ovid-baucis": {"tier": "primary", "title": "Metamorphoses, Book VIII (Baucis and Philemon)", "author": "Ovid"},
    "icarus-myth": {"tier": "secondary", "title": "The myth of Daedalus and Icarus", "publisher": "composite of standard classical sources (Ovid, Metamorphoses VIII)"},
    "prodicus-hercules": {"tier": "primary", "title": "The Choice of Hercules (Prodicus), as recorded in Xenophon, Memorabilia 2.1.21-33", "publisher": "Perseus Digital Library"},
    "delphic-maxim": {"tier": "secondary", "title": "\"Know Thyself\" (Gnothi Seauton), Delphic maxim inscribed at the Temple of Apollo, Delphi", "publisher": "composite of standard classical sources"},
    "orphic-tablets": {"tier": "secondary", "title": "Orphic gold tablets (Thurii tablets)", "publisher": "composite of standard classical scholarship on Orphic gold tablets"},
    "cleanthes-hymn": {"tier": "primary", "title": "Hymn to Zeus", "author": "Cleanthes", "publisher": "composite of standard translations"},
    "plato-republic": {"tier": "primary", "title": "Republic, Book X (the Myth of Er)", "author": "Plato"},
    "plato-phaedrus": {"tier": "primary", "title": "Phaedrus (the charioteer allegory)", "author": "Plato"},
    "epictetus-enchiridion": {"tier": "primary", "title": "Enchiridion, Chapter 5", "author": "Epictetus", "translator": "Elizabeth Carter", "publisher": "The Internet Classics Archive (MIT)"},
    "socrates-apology": {"tier": "primary", "title": "Apology", "author": "Plato (recording Socrates)", "publisher": "composite of standard translations"},
    "boethius-consolation": {"tier": "primary", "title": "The Consolation of Philosophy", "author": "Boethius", "publisher": "Project Gutenberg (trans. H.R. James) / CCEL"},
    "aeschylus-eumenides": {"tier": "primary", "title": "Eumenides", "author": "Aeschylus", "publisher": "composite of standard summaries/translations"},
    "plotinus-enneads": {"tier": "primary", "title": "Enneads, I.6 (\"On Beauty\")", "author": "Plotinus", "publisher": "CCEL / standard translations"},
    "spinoza-ethics": {"tier": "primary", "title": "Ethics, Part IV-V", "author": "Baruch Spinoza", "publisher": "Project Gutenberg (trans. R.H.M. Elwes)"},
    "gilgul-kabbalah": {"tier": "secondary", "title": "Gilgul neshamot (transmigration of souls), the Zohar and later Kabbalah", "publisher": "composite of standard sources on Jewish mysticism"},
}

def xr(quote, explanation, tie_back, source, citation_id, acc_percent, acc_note, is_quote=False):
    # is_quote=True only when `quote` is a full, verbatim quotation of the source text.
    # is_quote=False means `quote` is a paraphrased description of an event/teaching —
    # it must NOT be wrapped in quotation marks when rendered.
    return {
        "quote_or_event": quote,
        "explanation": explanation,
        "tie_back": tie_back,
        "source": source,
        "citation_id": citation_id,
        "is_quote": is_quote,
        "_accuracy_percent": acc_percent,
        "_accuracy_note": acc_note,
    }

TRAD_ORDER = ["hinduism", "christianity", "islam", "judaism", "buddhism", "jainism", "sikhism", "greek_mythology", "philosophy"]

kurals_meta = [
    (1, "அகர முதல எழுத்தெல்லாம் ஆதி\nபகவன் முதற்றே உலகு.",
     "Agara mudhala ezhuthu ellaam aadhi,\nPakavan mudhatre ulagu.",
     "Just as the letter “A” stands first among all the letters of the alphabet, God stands first as the origin and foundation of the whole world.",
     "The alphabet always starts with the letter A, and everything else is built from it. This kural says God is like that letter A for the whole world — the very first thing, the starting point everything else comes from.",
     "Valluvar opens his work not with an invocation to a specific deity but with a logical analogy drawn from language itself: just as அ (a) is structurally primary in the Tamil alphabet — the vowel from which the entire phonetic system is generated — so too is “Pahavan” (rendered here “God”/“the Primal Being”) ontologically primary to the cosmos. The term is deliberately non-sectarian, part of why the Thirukkural has been embraced across Saiva, Vaishnava, Jain, and secular-humanist readings alike. The appeal to a “first principle” or arche is one of the oldest moves in both theology and philosophy — found equally in Vedic cosmology, biblical self-declaration, and Aristotelian metaphysics."),
]

kurals = []

kurals.append({
    "number": 1,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "அகர முதல எழுத்தெல்லாம் ஆதி\nபகவன் முதற்றே உலகு.",
    "transliteration": "Agara mudhala ezhuthu ellaam aadhi,\nPakavan mudhatre ulagu.",
    "meaning": "Just as the letter “A” stands first among all the letters of the alphabet, God stands first as the origin and foundation of the whole world.",
    "elementary": "The alphabet always starts with the letter A, and everything else is built from it. This kural says God is like that letter A for the whole world — the very first thing, the starting point everything else comes from.",
    "university": "Valluvar opens his work not with an invocation to a specific deity but with a logical analogy drawn from language itself: just as அ (a) is structurally primary in the Tamil alphabet — the vowel from which the entire phonetic system is generated — so too is “Pahavan” (rendered here “God”/“the Primal Being”) ontologically primary to the cosmos. The term is deliberately non-sectarian, part of why the Thirukkural has been embraced across Saiva, Vaishnava, Jain, and secular-humanist readings alike. The appeal to a “first principle” or arche is one of the oldest moves in both theology and philosophy — found equally in Vedic cosmology, biblical self-declaration, and Aristotelian metaphysics.",
    "cross_references": {
        "hinduism": xr("“I am the Self, seated in the hearts of all creatures. I am the beginning, the middle, and the end of all beings.”",
            "Krishna tells Arjuna he isn’t one god among many, but the very point every being’s existence starts, continues, and ends from.",
            "Same claim as the Kural: the divine is the literal starting point that everything else comes from.",
            "Bhagavad Gita 10.20", "gita-asitis", 90, "Near one-to-one match — an explicit 'I am the beginning' self-declaration.", True),
        "christianity": xr("“I am Alpha and Omega, the beginning and the end, the first and the last.”",
            "Christ names himself using the first and last letters of the Greek alphabet, meaning he contains and precedes everything from start to finish.",
            "Nearly identical device to the Kural’s own move — using ‘the first letter’ as a stand-in for God being the origin of all things.",
            "Revelation 22:13 (KJV)", "kjv", 95, "Closest match in the whole set — both texts use the exact same alphabet metaphor for divine primacy.", True),
        "islam": xr("“He is the First and the Last, the Ascendant and the Intimate, and He is, of all things, Knowing.”",
            "This verse pairs opposites — first/last, hidden/manifest — to say nothing exists before God and nothing escapes His awareness.",
            "Matches the Kural’s basic claim that God precedes and grounds everything else that exists.",
            "Qur'an 57:3, Al-Hadid (Sahih International)", "quran-sahih", 85, "Strong doctrinal match on divine primacy, expressed through a broader set of paired attributes rather than the Kural's narrower 'first' image.", True),
        "judaism": xr("“I am the first, and I am the last; and beside me there is no God.”",
            "Spoken through the prophet Isaiah, this is God’s own claim that no deity came before Him and none will follow — He alone spans all of existence.",
            "Same ‘first’ claim the Kural opens with, used here to establish that the divine has no rival or predecessor.",
            "Isaiah 44:6 (Tanakh / KJV)", "kjv", 88, "Very close conceptually; the main difference is Isaiah frames it as an argument against rival gods rather than a pure cosmological claim.", True),
        "buddhism": xr("The Adi-Buddha (‘Primordial Buddha’) is described as self-existent (svayambhu), without beginning or end, and the source from which the other Buddhas and the universe itself emanate.",
            "In this much later strand of Buddhism, a single primordial awareness is described as the ultimate ground from which everything, including the historical Buddhas, arises.",
            "The nearest thing Buddhism offers to the Kural’s ‘God is first’ claim — though it comes from one specific tantric school, not the earlier or mainstream tradition.",
            "Adi-Buddha, Kalachakra Tantra (Vajrayana Buddhism)", "adi-buddha", 40, "Genuine textual basis, but represents a specific, later Vajrayana/tantric development, not classical or Theravada Buddhism, which explicitly rejects a single first cause.", False),
        "greek_mythology": xr("“Verily at the first Chaos came to be.”",
            "Hesiod’s creation account opens by naming Chaos — a vast, formless void — as the very first thing to exist, before any god or ordered world.",
            "Same structural claim as the Kural — something has to be ‘first’ before a world can exist — though Chaos is an impersonal void, not a conscious, virtuous being like the Kural’s God.",
            "Hesiod, Theogony, lines 116–117", "hesiod-theogony", 70, "Matches the 'first thing' structure exactly, but Chaos is not a person or object of praise, only an origin point.", True),
        "philosophy": xr("“It is necessary that there should be an eternal unmovable substance... substances are the first of existing things.”",
            "Aristotle argues that all motion and change must ultimately trace back to something itself unmoved and eternal — his famous ‘Prime Mover.’",
            "Independently arrives at the same conclusion as the Kural: there must be a ‘first,’ uncaused reality behind everything else.",
            "Aristotle, Metaphysics, Book XII (Lambda)", "aristotle-metaphysics", 80, "Strong structural match on the argument for a first cause; Aristotle's Prime Mover is a rational, impersonal principle rather than a devotional God.", True),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1", "pope-1886"],
})

kurals.append({
    "number": 2,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "கற்றதனால் ஆய பயனென்கொல் வாலறிவன்\nநற்றாள் தொழாஅர் எனின்.",
    "transliteration": "Katradhanaal aaya payan en kol vaal-arivan,\nnatraal thozhaaar enin.",
    "meaning": "What good is all of a person’s learning, if they never bow in reverence to the good feet of the One of pure, perfect wisdom?",
    "elementary": "Imagine acing every test but never once saying thank you to your teacher. This kural says learning without being humble and thankful toward God doesn’t really count for much.",
    "university": "This verse critiques a purely instrumental or accumulative view of education. “Vaal-arivan” (“the one of spotless/pure knowledge”) refers to a transcendent, perfect intelligence — the ground of all true knowing, not a sectarian god. Valluvar’s claim is that erudition divorced from reverence toward that ultimate source is functionally sterile: it produces information without transformation. This is a recurring cross-cultural theme — the distinction between accumulated data and lived, humbling wisdom.",
    "cross_references": {
        "hinduism": xr("Distinguishes ‘aparā vidyā’ (lower knowledge: the Vedas, grammar, ritual, etc.) from ‘parā vidyā’ (higher knowledge: that by which the imperishable Self is realized).",
            "The text says all ordinary book-learning is ‘lower knowledge’ — genuinely useful, but incomplete — unless it’s joined to the ‘higher knowledge’ that leads to realizing ultimate reality.",
            "Same two-tier idea as the Kural: study by itself is the ‘lower’ half of learning; reverence for the ultimate is what completes it.",
            "Mundaka Upanishad 1.2.12–13", "mundaka-upanishad", 85, "Very close structural match — both texts explicitly rank ordinary learning below a higher, reverence-based knowing.", False),
        "christianity": xr("“Though I... understand all mysteries, and all knowledge... and have not charity, I am nothing.”",
            "Paul says that even total intellectual mastery is worth nothing without love — love is what gives knowledge its value.",
            "Paul makes the same trade here — knowledge vs. love — as the Kural makes between learning and reverence: one without the other is empty.",
            "1 Corinthians 13:2 (KJV)", "kjv", 80, "Strong match on the core claim ('knowledge alone = nothing'), though Paul's missing ingredient is love specifically, while the Kural's is reverence for God.", True),
        "islam": xr("“...it is only those who have knowledge among His servants that fear/revere Allah.”",
            "This verse ties real knowledge directly to reverence — the more truly someone understands, the more awe it produces in them.",
            "Implies the reverse of the Kural’s claim too: knowledge that produces no reverence hasn’t really arrived yet.",
            "Qur'an 35:28, Fatir", "quran-general", 65, "Same link between knowledge and reverence, but stated as an observation about scholars rather than a direct claim that learning without reverence is worthless.", True),
        "judaism": xr("“The fear of the LORD is the beginning of wisdom, and the knowledge of the Holy One is understanding.”",
            "This proverb makes reverence for God the starting point of wisdom itself, not an optional add-on to it.",
            "Nearly the Kural’s exact claim in a single line: without reverence, there’s no real wisdom to begin with.",
            "Proverbs 9:10 (Tanakh, Mishlei / KJV)", "kjv", 88, "One of the closest matches in the whole project — reverence-as-foundation-of-wisdom is essentially the Kural's own claim.", True),
        "buddhism": xr("Describes reciting scripture without living by it as being “like a cowherd who counts the cattle of others” — he tends them all day but owns none.",
            "The Buddha compares someone who has memorized scripture but doesn’t practice it to a hired hand who never actually benefits from the cattle he tends.",
            "Same warning as the Kural: knowledge you haven’t lived out or humbled yourself to isn’t really yours.",
            "Dhammapada, verses 19–20", "dhammapada-buddharakkhita", 82, "Very close in spirit — both condemn scripture-knowledge divorced from genuine practice/humility.", False),
        "greek_mythology": xr("Daedalus gives his son Icarus the knowledge and means to fly (wax-and-feather wings) along with a clear warning not to fly too high — Icarus ignores it, the wax melts, and he falls into the sea.",
            "Icarus has the same skill his father does, but not the humility to heed the wisdom that was supposed to come with it, and the skill alone destroys him.",
            "A cautionary version of the Kural’s point: ability or knowledge used without humility toward the wisdom that should guide it ends in ruin.",
            "Ovid, Metamorphoses, Book VIII (the myth of Daedalus and Icarus)", "icarus-myth", 45, "Matches the danger of applying skill/knowledge without heeding wisdom or restraint, but is not specifically about reverence for a deity.", False),
        "philosophy": xr("Socrates claims his only advantage over men reputed wise is that he, unlike them, knows that he does not really know.",
            "Socrates’ wisdom isn’t more facts — it’s the humility to recognize the real limits of what he knows.",
            "Matches the Kural’s deeper point: real wisdom starts with humility, not with accumulating more facts.",
            "Plato, Apology (Socrates' defense)", "socrates-apology", 55, "Thematically aligned (humility as the mark of true wisdom), but Socratic humility is about intellectual limits, not reverence for a divine being specifically.", False),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 3,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "மலர்மிசை ஏகினான் மாணடி சேர்ந்தார்\nநிலமிசை நீடுவாழ் வார்.",
    "transliteration": "Malar-misai Ekinaan maanadi serndhaar,\nnila-misai needu vaazhvaar.",
    "meaning": "Those who cling to the glorious feet of Him who moves lightly even upon a flower will live long and flourish upon this earth.",
    "elementary": "Picture someone so light and gentle they could stand on a flower without crushing it. This kural says if you hold on tight to someone that good — meaning you stay close to God — your life goes well for a long time.",
    "university": "The image of the divine “moving upon a flower” evokes both lightness/purity and the lotus-throne motif common to Tamil and broader Indic religious iconography. “Nilamisai needuvaazhvaar” — “shall live long upon the earth” — is classically read not as mere biological longevity but as a durable, well-founded flourishing that outlasts the transient. The pairing of devotion with durable flourishing is one of the most cross-culturally attested religious claims.",
    "cross_references": {
        "hinduism": xr("“To those who worship Me alone, thinking of no other... I bring what they lack and preserve what they already possess.”",
            "Krishna promises that total, single-minded devotion comes with practical divine provision and protection built in.",
            "Matches the Kural’s promise directly — closeness to the divine brings durable well-being, not just distant blessing.",
            "Bhagavad Gita 9.22", "gita-mukundananda", 85, "Strong, direct doctrinal match on devotion producing ongoing sustenance and protection.", True),
        "christianity": xr("“I am the vine, ye are the branches... without me ye can do nothing.”",
            "Jesus pictures believers as branches that only bear fruit while attached to him — cut off, they can’t produce anything at all.",
            "Same organic image as the Kural — a flourishing life only grows out of staying attached to the divine.",
            "John 15:5 (KJV)", "kjv", 88, "Very close match — both use a growth/attachment metaphor for flourishing that depends entirely on nearness to the divine.", True),
        "judaism": xr("“He shall be like a tree planted by the rivers of water... whatsoever he doeth shall prosper.”",
            "The psalm compares a righteous, God-focused person to a well-watered tree, consistently fruitful because its roots never run dry.",
            "Nearly the same claim and imagery as the Kural — closeness to the source of life produces lasting flourishing.",
            "Psalm 1:3 (Tanakh, Ketuvim / KJV)", "kjv", 88, "Very close match in both structure and specific tree/water/fruit imagery.", True),
        "buddhism": xr("“To one ever eager to revere and serve the elders, these four blessings accrue: long life and beauty, happiness and power.”",
            "The Buddha teaches that consistently honoring one’s elders and teachers naturally brings these four good things back in return.",
            "Same reverence-produces-long-life structure as the Kural, though aimed at elders/teachers rather than a deity.",
            "Dhammapada, verse 109", "dhammapada-narada", 55, "Precise match on the mechanism (reverence leads to longevity/flourishing) but a different, non-theistic object of reverence.", True),
        "islam": xr("“A good word [is] like a good tree, whose root is firmly fixed and its branches [high] in the sky. It produces its fruit all the time, by permission of its Lord.”",
            "The Qur'an compares a person or word of true faith to a deeply rooted tree that bears fruit continuously because its roots are secure.",
            "Same tree/root/fruit imagery the Kural implies — durable flourishing traced back to a firm connection with God.",
            "Qur'an 14:24-25, Ibrahim", "quran-general", 65, "Strong shared imagery, though the Qur'an's point is about firmness of faith/speech more than the specific 'long life' the Kural promises.", True),
        "greek_mythology": xr("An elderly couple who alone show hospitality to Zeus and Hermes travelling in disguise are rewarded with a long, shared life and, at death, transformation into two intertwined trees.",
            "Ovid’s story rewards the couple’s simple devotion to the gods with an unusually long and contented life together.",
            "A myth-shaped version of the Kural’s promise: devotion to the divine repaid with a long, flourishing life.",
            "Ovid, Metamorphoses, Book VIII (Baucis and Philemon)", "ovid-baucis", 55, "Good thematic match on 'devotion rewarded with long life,' though the reward here is hospitality-specific and the source is Ovid's Roman retelling of Greek material.", False),
        "philosophy": xr("Aristotle argues that eudaimonia (human flourishing) is achieved through a lifetime of virtuous activity in accordance with reason, not through momentary pleasure.",
            "For Aristotle, a genuinely ‘flourishing’ life is sustained right living over time, not a single good feeling.",
            "Shares the Kural’s logic that real flourishing is durable and depends on staying aligned with what is highest, though Aristotle's 'highest' is reason/virtue rather than a personal God.",
            "Aristotle, Nicomachean Ethics", "aristotle-metaphysics", 45, "Same general shape (aligned living produces lasting flourishing) but not a devotional or theistic framework, so the parallel is structural rather than doctrinal.", False),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 4,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "வேண்டுதல் வேண்டாமை இலானடி சேர்ந்தார்க்கு\nயாண்டும் இடும்பை இல.",
    "transliteration": "Vendudhal vendaamai ilaan adi serndhaarkku,\nyaandum idumbai ila.",
    "meaning": "No suffering will ever touch those who take refuge in the feet of the One who is beyond all craving and all aversion.",
    "elementary": "Some people get super excited when they get what they want, and really upset when they don’t. This kural says if you can stay as calm as God — not too excited, not too upset — bad things can’t really shake you.",
    "university": "The verse names two categories — raga (craving/attachment) and dvesha (aversion) — as the very things the Divine transcends. This dyad is the central diagnostic pair in most Indian soteriologies for why beings suffer. The claim is that participation in a consciousness beyond craving/aversion is itself what removes vulnerability to affliction — functionally identical to the Stoic and Buddhist claims that suffering arises from the mind’s reactive patterns rather than external events themselves.",
    "cross_references": {
        "hinduism": xr("“One who is not disturbed by sorrows, who has no craving for joy, who is free from attachment, fear, and anger — is called a sage of steady wisdom.”",
            "Krishna describes the ideal person as someone whose inner peace doesn’t rise and fall with good or bad news.",
            "This is the Kural’s 'beyond craving and aversion' standard almost word for word.",
            "Bhagavad Gita 2.56", "gita-mukundananda", 92, "Near-exact match — both name the same pair (craving/aversion) as what a steady, suffering-free person has transcended.", True),
        "christianity": xr("“Thou wilt keep him in perfect peace, whose mind is stayed on thee: because he trusteth in thee.”",
            "The prophet promises complete inner peace specifically to the person whose attention stays fixed on God rather than on circumstances.",
            "Matches the Kural’s claim that peace/protection from suffering comes from where your mind is anchored.",
            "Isaiah 26:3 (KJV)", "kjv", 78, "Strong match on the mechanism (fixed attention on God produces unshakeable peace).", True),
        "judaism": xr("“Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me.”",
            "Even walking through the most frightening place imaginable, the psalmist says fear has no grip on him because God is present.",
            "Direct parallel to the Kural’s 'no suffering touches them' promise.",
            "Psalm 23:4 (Tanakh, Ketuvim / KJV)", "kjv", 80, "Close match on the promised outcome (fearlessness/freedom from affliction through God's presence).", True),
        "islam": xr("“Unquestionably, [for] the allies of Allah there will be no fear concerning them, nor will they grieve.”",
            "This verse promises God’s close friends a life free of the two things that usually plague people: fear about the future and grief about the past.",
            "Nearly identical structure to the Kural’s promise of a life free from affliction.",
            "Qur'an 10:62, Yunus", "quran-general", 85, "Very close doctrinal match — a specific, named class of people promised freedom from fear and grief.", True),
        "buddhism": xr("“The fever of passion exists not for him who has completed the journey, who is sorrowless and wholly set free, and has broken all ties.”",
            "The Buddha describes the fully awakened person as someone who has completely stopped being agitated by craving — their inner 'fever' has simply gone out.",
            "Reaches the same end state as the Kural — total freedom from affliction — through spiritual completion rather than devotion to a personal God.",
            "Dhammapada, verse 90", "dhammapada-buddharakkhita", 70, "Strong match on the outcome (complete freedom from affliction/craving), though the mechanism (arahantship) differs from the Kural's devotional framing.", True),
        "greek_mythology": xr("As a young man, Hercules is approached by two women personifying Virtue and Vice; Vice offers an easy life free of pain, Virtue offers only what is earned through effort — and Hercules chooses Virtue.",
            "The fable frames maturity as choosing to build a life on hard-won virtue rather than chasing momentary pleasure and avoiding pain.",
            "Echoes the Kural’s contrast between craving/aversion (Vice’s offer) and a settled, unshakeable good (Virtue’s path).",
            "Prodicus, 'The Choice of Hercules', in Xenophon, Memorabilia 2.1.21-33", "prodicus-hercules", 45, "Shares the craving-vs-aversion structure, but the fable is about a moral choice at a crossroads, not a description of an already-attained equanimity.", False),
        "philosophy": xr("“Men are disturbed not by the things which happen, but by the opinions about the things.”",
            "Epictetus argues that outward events never directly cause distress — our judgments about them do, which means the disturbance is always something we can let go of.",
            "Gives the psychological mechanism behind the Kural’s claim: freedom from craving/aversion is what actually removes vulnerability to suffering.",
            "Epictetus, Enchiridion, Chapter 5", "epictetus-enchiridion", 80, "Strong structural match — both locate suffering in the mind's reaction rather than the external event itself.", True),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 5,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "இருள்சேர் இருவினையும் சேரா இறைவன்\nபொருள்சேர் புகழ்புரிந்தார் மாட்டு.",
    "transliteration": "Irul-ser iru-vinaiyum seraa iraivan,\nporul-ser pukazh-purindhaar maattu.",
    "meaning": "The two dark deeds — the good and bad karma born of ignorance — will not attach themselves to those who truly delight in praising God with real understanding.",
    "elementary": "Imagine collecting points for good things and bad things you do, without really understanding why they matter. This kural says truly understanding and loving God wipes the whole scoreboard clean — good points and bad.",
    "university": "“Irul” (darkness) signifies avidya (ignorance), and “iru vinai” (the twin deeds) refers to punya and papa — meritorious and demeritorious karma — both of which bind the soul to rebirth regardless of whether the deeds were “good” or “bad,” because both are performed from a standpoint of ignorance. Valluvar’s claim is that liberation is not more good karma outweighing bad, but a shift in understanding that removes a person from the karmic ledger altogether.",
    "cross_references": {
        "hinduism": xr("“buddhi-yukto jahātīha ubhe sukṛta-duṣkṛte” — “One who is united with wisdom casts off, even in this life, both good and evil deeds.”",
            "Krishna teaches that someone acting from real wisdom stops accumulating both 'good' and 'bad' karma — they step outside the whole scorekeeping system.",
            "This is close to a word-for-word match for the Kural’s claim about the 'two dark deeds.'",
            "Bhagavad Gita 2.50", "gita-asitis", 92, "Near word-for-word doctrinal match on transcending both good and bad karma through wisdom.", True),
        "buddhism": xr("Describes an awakened mind as one that has “gone beyond both merit and demerit,” for whom “there is no fear.”",
            "The verse describes an awakened mind as one that has gone beyond the entire category of merit and demerit, not just avoided bad and pursued good.",
            "Nearly identical conceptual move to the Kural: liberation isn’t better karma, it’s exiting the karma-ledger altogether.",
            "Dhammapada, verse 39", "dhammapada-buddharakkhita", 90, "Near-exact conceptual match — explicitly transcending merit and demerit as a pair, exactly as the Kural does.", False),
        "christianity": xr("“There is therefore now no condemnation to them which are in Christ Jesus.”",
            "Paul tells believers their standing is no longer measured by a record of right and wrong at all, because they are 'in Christ.'",
            "A different route to a similar destination as the Kural — being freed from the deed-by-deed ledger through relationship rather than accumulated merit.",
            "Romans 8:1 (KJV)", "kjv", 65, "Shares the 'no longer under the ledger' logic, though Paul's grounds (justification through Christ) differ from the Kural's grounds (wisdom/true understanding).", True),
        "judaism": xr("“If a wicked person turns away from all his sins... none of the transgressions that he has committed shall be remembered against him.”",
            "Ezekiel insists that God doesn’t keep a running total against someone who genuinely turns their life around — the old record simply isn’t held against them.",
            "A real, if narrower, Jewish parallel to the Kural’s 'deeds don't stick' claim — here achieved through repentance rather than a general transcendence of karma.",
            "Ezekiel 18:21-22 (Tanakh / KJV)", "kjv", 55, "Good match on 'the record is wiped,' but tied specifically to repentance from sin, not a broader teaching about escaping the merit/demerit system.", True),
        "islam": xr("“Those who repent, believe and do righteous work. For them Allah will replace their evil deeds with good.”",
            "This verse says sincere repentance actually converts the record of past evil into a record of good, not just erasing it.",
            "An even closer image than Ezekiel's to the Kural’s claim, since the negative record is positively transformed, not just wiped.",
            "Qur'an 25:70, Al-Furqan", "quran-general", 58, "Close in imagery (deeds transformed), though again tied to repentance from sin specifically, not a general teaching of transcending karma.", True),
        "greek_mythology": xr("Initiates carried inscribed gold tablets into the grave declaring: “I have flown out of the sorrowful, weary Wheel.”",
            "These tablets were a kind of password, declaring the soul had escaped the exhausting cycle of rebirth through ritual purification.",
            "A rare Greek parallel to the Kural’s 'stepping outside the whole system' idea, though framed as ritual escape from rebirth rather than transcending good and bad deeds specifically.",
            "Orphic gold tablets (Thurii tablets)", "orphic-tablets", 40, "Striking 'escape the wheel' language, but the underlying mechanism (Orphic ritual purification) and target (rebirth, not the merit/demerit ledger) differ from the Kural's claim.", False),
        "philosophy": xr("Spinoza’s ‘free man’ acts entirely from reason, understanding good and evil not as fixed cosmic categories but as relative to what helps or hinders a rational life.",
            "For Spinoza, becoming wise means outgrowing the whole ordinary framework of moralized 'good' and 'bad' for a clearer, more rational vantage point.",
            "Shares the Kural’s basic move of transcending the entire good/bad framework through understanding, rather than just picking the 'good' side of it.",
            "Spinoza, Ethics, Parts IV–V", "spinoza-ethics", 40, "Structurally similar (wisdom relativizes the good-evil ledger), but Spinoza's rationalist framework is a world apart from the Kural's devotional, karma-based context.", False),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 6,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "பொறிவாயில் யைந்தவித்தான் பொய்தீர் ஒழுக்க\nநெறிநின்றார் நீடுவாழ் வார்.",
    "transliteration": "Pori-vaayil aindhu avithaan poi-theer ozhukka,\nneri ninRaar needu vaazhvaar.",
    "meaning": "Those who stand firm in the untainted, truthful path of Him who has mastered the five sense-desires will live long, flourishing lives.",
    "elementary": "We have five senses — seeing, hearing, smelling, tasting, touching — and they can pull us all over the place wanting things. This kural says if you master your five senses instead of letting them boss you around, your life goes really well.",
    "university": "“Pori” refers to the five sense-faculties (indriyas); the divine is depicted as the paradigm of complete indriya-nigraha (sense-mastery), a central discipline across nearly all Indian contemplative systems. The verse makes mastery of the senses, rather than mere rule-following, the actual mechanism of a flourishing life — free from the erratic disturbance the unchecked senses cause.",
    "cross_references": {
        "hinduism": xr("“Know the Self as the rider in a chariot, the body as the chariot; the intellect as the charioteer, and the mind as the reins.”",
            "The Upanishad pictures the self as a passenger, the intellect as the driver, and the mind as the reins holding back the senses (the horses) — if the driver is careless, the horses run wild.",
            "Same core image as the Kural: a well-run life depends on the senses being reined in, not left to run free.",
            "Katha Upanishad 1.3.3", "katha-upanishad", 85, "Very strong structural match — an explicit sense-mastery allegory with the same stakes (a well-lived life vs. chaos).", True),
        "buddhism": xr("“Restraint in the eye is good, good is restraint in the ear... restraint everywhere is good. A bhikkhu restrained in every way is freed from all suffering.”",
            "The Buddha lists each sense one by one and calls restraint over each of them good, then says total restraint frees a person from suffering entirely.",
            "Matches the Kural’s claim almost exactly: mastery of the senses is the direct cause of a settled, suffering-free life.",
            "Dhammapada, verses 360–361", "dhammapada-buddharakkhita", 88, "Near-exact match — explicit sense-by-sense restraint as the direct cause of freedom from suffering.", True),
        "christianity": xr("“But I keep under my body, and bring it into subjection.”",
            "Paul compares himself to an athlete in training, disciplining his own body so it doesn’t undermine everything else he’s working toward.",
            "Same self-mastery logic as the Kural, applied to bodily discipline specifically.",
            "1 Corinthians 9:27 (KJV)", "kjv", 78, "Strong match on the self-discipline theme, phrased through an athletic training metaphor.", True),
        "judaism": xr("“He that is slow to anger is better than the mighty; and he that ruleth his spirit than he that taketh a city.”",
            "The proverb ranks self-control above military conquest — ruling your own reactions is harder, and more valuable, than ruling a city.",
            "A vivid version of the Kural’s claim that mastering yourself, not external achievement, is what actually matters.",
            "Proverbs 16:32 (Tanakh, Ketuvim / KJV)", "kjv", 75, "Strong match on the core value (self-mastery as the highest form of strength).", True),
        "islam": xr("“As for him who feared to stand before his Lord and restrained himself from [his] desire, then indeed, Paradise will be his refuge.”",
            "The verse names two things that earn Paradise: taking God’s judgment seriously, and actively holding oneself back from base desires.",
            "Nearly identical logic to the Kural — restraining desire is the direct path to the best possible outcome.",
            "Qur'an 79:40-41, An-Nazi'at", "quran-general", 82, "Near-exact match — restraint of desire explicitly named as the cause of the best outcome.", True),
        "greek_mythology": xr("Knowing the Sirens’ song is fatally tempting, Odysseus has his crew’s ears sealed and has himself tied to the mast — engineering restraint in advance rather than trusting willpower in the moment.",
            "Odysseus doesn’t try to resist the temptation directly; he removes his own ability to give in to it.",
            "A vivid mythic dramatization of the Kural’s point: real self-mastery over the senses is what gets you through safely.",
            "Homer, Odyssey, Book 12", "homer-odyssey", 75, "Strong thematic match, though Odysseus is deliberately restrained by others rather than self-mastering in the purest sense.", False),
        "philosophy": xr("Plato pictures the soul as a charioteer driving two horses — one noble, one unruly and appetite-driven — who only rises rather than crashes if the charioteer masters both.",
            "The charioteer (reason) has to actively control the wilder horse (appetite) or the whole chariot (the soul) is dragged down.",
            "Essentially the same chariot image as the Hinduism entry above, arrived at independently in Greek philosophy — reinforcing the Kural's claim from a separate tradition.",
            "Plato, Phaedrus", "plato-phaedrus", 85, "Strong structural match — an independently-arrived-at chariot allegory for sense/appetite mastery.", False),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 7,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "தனக்குவமை இல்லாதான் தாள்சேர்ந்தார்க் கல்லால்\nமனக்கவலை மாற்றல் அரிது.",
    "transliteration": "Thanakku-uvamai illaadhaan thaal serndhaark kallaal,\nmana-kavalai maatral aridhu.",
    "meaning": "Except for those who cling to the feet of the One beyond all comparison, it is very hard for anyone to be free of the mind’s anxieties.",
    "elementary": "Everybody worries sometimes. This kural says the only way to truly stop worrying deep down is to hold onto something so great that nothing else can compare to it.",
    "university": "“Thanakku uvamai illaadhaan” (“the One with no likeness to Himself”) situates the removal of mental anxiety not in technique or willpower but in relationship to a reality that relativizes every other object of comparison. If nothing else is truly comparable, ordinary anxieties (always about something comparable — status, loss, gain) lose their grip. This mirrors a recurring move across theistic and philosophical traditions: relocating the anxious self’s center of gravity onto something that cannot be lost or reduced by comparison.",
    "cross_references": {
        "hinduism": xr("“To the seer, all things have verily become the Self: what delusion, what sorrow, can there be for him who beholds that oneness?”",
            "The text says that once someone truly sees all things as one with the Self, there’s no separate ‘other’ thing left to feel anxious about.",
            "Matches the Kural’s logic — remove the sense of separateness (or find something incomparable) and anxiety has nothing left to attach to.",
            "Isha Upanishad, verse 7", "isha-upanishad", 75, "Good conceptual match — both locate the end of anxiety in transcending the ordinary framework of separate, comparable things.", True),
        "christianity": xr("“Be careful for nothing... and the peace of God, which passeth all understanding, shall keep your hearts and minds.”",
            "Paul tells his readers not to be anxious about anything, but to bring every worry to God in prayer; in exchange, God's peace guards their hearts and minds.",
            "A direct match for the Kural’s promise: real, lasting relief from anxiety, achieved specifically by turning to God.",
            "Philippians 4:6-7 (KJV)", "kjv", 85, "Very strong match — both promise complete relief from anxiety through a specific relationship with the divine.", True),
        "judaism": xr("“Cast thy burden upon the LORD, and he shall sustain thee.”",
            "The psalmist’s advice is strikingly physical — literally hand your burden over to God, who will carry it and keep you steady.",
            "The same transfer-of-burden logic the Kural implies: anxiety lifts when you have somewhere incomparable to put it.",
            "Psalm 55:22 (Tanakh, Ketuvim / KJV)", "kjv", 78, "Strong match on the mechanism (transferring the burden to God relieves anxiety).", True),
        "islam": xr("“Verily, in the remembrance of Allah do hearts find rest.”",
            "This verse states as a general rule that hearts only truly settle down through remembering God — nothing else does the job as completely.",
            "Almost a direct restatement of the Kural’s claim that only the incomparable One can truly end anxiety.",
            "Qur'an 13:28, Ar-Ra'd", "quran-sahih", 85, "Very strong match — both make God the singular, sufficient answer to unrest of mind.", True),
        "buddhism": xr("The Buddha teaches that if fear arises while alone in the forest, a monk should recall the qualities of the Buddha, Dhamma, and Sangha — doing so makes the fear pass away.",
            "Rather than fighting fear directly, the practice is to redirect attention toward something recognized as supremely trustworthy, which dissolves the fear.",
            "A genuine Buddhist parallel to the Kural’s logic — anxiety dissolves by turning attention toward something beyond ordinary comparison, though Buddhism's 'object' is the Triple Gem rather than a singular incomparable God.",
            "Dhajagga Sutta (Samyutta Nikaya 11.3)", "dhajagga-sutta", 60, "Solid structural match with a real canonical source, though the object of refuge is plural and non-theistic, unlike the Kural's singular incomparable God.", False),
        "greek_mythology": xr("Orestes, tormented endlessly by the Furies for killing his mother, finds relief only when the goddess Athena convenes a formal trial and resolves his case.",
            "His anxiety isn’t something Orestes can think his way out of — it only ends when a higher authority intervenes and settles the matter for good.",
            "Dramatizes the Kural’s claim in narrative form: ordinary human effort can’t end this kind of torment; only appeal to something greater finally can.",
            "Aeschylus, Eumenides", "aeschylus-eumenides", 45, "Good structural echo (relief only through a higher power) but the Furies represent guilt over an actual crime, a narrower kind of anguish than the Kural's general 'mental anxiety.'", False),
        "philosophy": xr("Awaiting execution on false charges, Boethius is consoled by Lady Philosophy, who argues that true happiness and peace of mind can only be found in the one highest Good, which she identifies with God.",
            "Boethius finds that fixing his attention on the highest, unconditional good is what finally settles a mind that fortune's ups and downs couldn't.",
            "A near-perfect philosophical dramatization of the Kural’s exact claim — anxiety only truly ends by anchoring to something beyond all comparison.",
            "Boethius, The Consolation of Philosophy", "boethius-consolation", 75, "Strong match: written by a philosopher facing real anxiety, explicitly locating peace of mind in a single, incomparable highest Good.", False),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 8,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "அறவாழி அந்தணன் தாள்சேர்ந்தார்க் கல்லால்\nபிறவாழி நீந்தல் அரிது.",
    "transliteration": "Aravaazhi andhanan thaal serndhaark kallaal,\npiRa vaazhi neendhal aridhu.",
    "meaning": "Except for those who cling to the feet of the gracious One who is like an ocean of virtue, it is hard for anyone to swim across the other ocean — the ocean of worldly existence.",
    "elementary": "Picture two huge oceans: one is how good God is, and the other is all of life’s ups and downs. This kural says the only way to cross the hard ocean is to hold onto the good one.",
    "university": "“Aravaazhi” (“ocean of dharma/virtue”) figures the divine as boundless moral reality, an ocean whose scale matches the second ocean it lets one cross — “piravaazhi,” the vast ocean of worldly existence one must traverse. The parallel construction is a deliberate rhetorical mirroring, reinforcing that only something of equal or greater vastness than the ocean of worldly existence can carry a being across it.",
    "cross_references": {
        "hinduism": xr("“Even if you are considered to be the most sinful of all sinners, when you are situated in the boat of transcendental knowledge, you will be able to cross over the ocean of miseries.”",
            "Krishna says that no matter how sinful someone has been, real spiritual knowledge works like a boat sturdy enough to carry them across the entire sea of suffering.",
            "The Kural’s exact image — an ocean that can only be crossed by boat/aid — appears here almost identically.",
            "Bhagavad Gita 4.36", "gita-asitis", 88, "Very strong match — the same ocean-crossed-by-vessel image applied to spiritual liberation.", True),
        "buddhism": xr("The Buddha compares his own teaching to a raft — genuinely necessary to cross the water, but meant to be let go of once you've reached the other side.",
            "The Dharma gets you across, but it isn’t the destination — you’re meant to release it once it’s done its job.",
            "Shares the Kural’s crossing-the-water structure, though it's the teaching/practice itself that's the vessel here, not devotion to a personal God.",
            "Majjhima Nikaya 22 (Alagaddupama Sutta)", "majjhima-nikaya-22", 65, "Strong match on the crossing metaphor, though the object (Dharma-as-raft) and destination differ from the Kural's devotional framing.", False),
        "christianity": xr("“I am the way, the truth, and the life: no man cometh unto the Father, but by me.”",
            "Jesus states plainly that he is the sole route to God the Father — not one option among several, but the way itself.",
            "Matches the Kural’s exclusivity claim: only one path gets you across, and it runs through the divine specifically.",
            "John 14:6 (KJV)", "kjv", 80, "Strong match on the exclusivity claim (one sole path/mediator to cross over).", True),
        "judaism": xr("At the Red Sea, escape is physically impossible until God parts the water himself — the Israelites don’t build a way across, God makes one for them.",
            "The sea only becomes crossable through direct divine action, not human effort or ingenuity.",
            "A literal, historical version of the Kural’s image: an impassable sea made passable only by direct divine action.",
            "Exodus 14:21-22 (Tanakh, Torah)", "kjv", 80, "Excellent match on 'a sea crossed only through God's action,' though this is a specific historical rescue rather than a general soteriological claim.", False),
        "islam": xr("“Be in this world as if you were a stranger or a traveler.”",
            "The Prophet Muhammad frames the whole of worldly life as a temporary journey through unfamiliar territory, not a place to settle down in.",
            "Shares the Kural’s underlying picture of life as something to be traveled through, though it's a general life-orientation teaching rather than a specific claim that only God enables the crossing.",
            "Sahih al-Bukhari 6416", "bukhari-6416", 40, "Authentic hadith about life-as-a-journey, but doesn't make the Kural's specific claim that only God enables the crossing — a looser fit than the other citations here.", True),
        "greek_mythology": xr("The dead cannot cross into the underworld on their own — they need Charon the ferryman, and even he requires payment before he’ll take them.",
            "Crossing over isn’t something you can do by yourself; it requires both a specific helper and the right toll.",
            "The same basic claim as the Kural: crossing over requires help from something/someone beyond yourself, not just willpower.",
            "Greek mythological tradition (Charon and the Styx)", "charon-myth", 78, "Strong match on the core claim that the crossing absolutely requires outside aid.", False),
        "philosophy": xr("“Let us flee then to the beloved Fatherland... The Fatherland to us is There whence we have come, and There is the Father.”",
            "Plotinus urges that the soul's true home isn't reachable by boat or road — it requires an inward turn back toward its divine source.",
            "A philosophical version of the Kural’s ocean — the real crossing isn't geographic, it's a return to the source.",
            "Plotinus, Enneads, I.6", "plotinus-enneads", 60, "Good match on 'the real crossing is toward one's true origin,' though Plotinus's 'the One' is an impersonal metaphysical principle rather than the Kural's gracious God.", True),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 9,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "கோளில் பொறியின் குணமிலவே எண்குணத்தான்\nதாளை வணங்காத் தலை.",
    "transliteration": "Kolil poRiyin guNam-ilavey,\neN-guNaththaan thaalai vaNangaadha thalai.",
    "meaning": "A head that will not bow to the feet of the One possessed of the eight great virtues is as useless as a sense-organ that has lost its power to sense.",
    "elementary": "Think of an eye that can’t see, or an ear that can’t hear — totally useless, right? This kural says a person who won’t bow to God is just as useless, no matter how proud or important they feel.",
    "university": "“Eṇ-guṇam” (“the eight qualities”) refers to a catalogue of divine perfections in Tamil Saiva/Vaishnava theology. The verse’s force lies in its analogy: a sense organ that has lost its functional capacity is not merely deficient but categorically useless — it fails at the one thing that defines it. Likewise, a head that will not bow is said to fail at the one thing Valluvar treats as most defining meaningful personhood: right relationship, through humility, to the ultimate reality.",
    "cross_references": {
        "hinduism": xr("Ravana — a brilliant scholar, devoted worshipper of Shiva, and holder of great spiritual powers — is nonetheless destroyed because his pride leads him to defy Rama and refuse to make things right even when warned.",
            "The epic shows that vast learning and even sincere devotion in one area can't save someone whose pride makes them refuse to bow to what's right.",
            "A narrative version of the Kural’s exact point: real ability or knowledge is worthless once pride makes someone unable to submit.",
            "Valmiki Ramayana (the character of Ravana)", "ramayana-ravana", 60, "Strong thematic match (pride negates other genuine virtues/abilities), delivered as epic narrative rather than doctrinal statement about the specific 'eight qualities.'", False),
        "christianity": xr("“God resisteth the proud, but giveth grace unto the humble.”",
            "James states it as a flat rule: God actively opposes the proud, no exceptions, while pouring out grace on anyone humble.",
            "Directly backs the Kural’s claim — pride specifically is what blocks a person from receiving anything of real worth from God.",
            "James 4:6 (KJV)", "kjv", 80, "Strong, direct match — pride explicitly named as what blocks divine favor.", True),
        "judaism": xr("“Pride goeth before destruction, and an haughty spirit before a fall.”",
            "The proverb states pride and a fall go together as a near law of nature — arrogance is what sets up the collapse.",
            "Same warning as the Kural, framed as cause and effect: an unbowed, proud head brings its own ruin.",
            "Proverbs 16:18 (Tanakh, Ketuvim / KJV)", "kjv", 78, "Strong, direct match on pride as the specific cause of downfall.", True),
        "islam": xr("When God commands all the angels to bow to Adam, every single one obeys except Iblis, who refuses out of pride — becoming the paradigmatic rebel against God.",
            "One single refusal to bow, caused entirely by pride, is what defines Iblis's entire fall from grace.",
            "The most literal possible match to the Kural’s image — an actual head/will that will not bow, becoming worthless because of it.",
            "Qur'an 2:34, Al-Baqarah", "quran-general", 90, "About as close a literal match as exists in this project — an actual refusal to bow, caused by pride, with catastrophic consequences.", False),
        "buddhism": xr("The Buddha's own cousin Devadatta, despite real spiritual attainments, lets jealousy curdle into an attempt to seize control of the monastic community — and, tradition says, falls into the deepest hell as a result.",
            "Devadatta had real ability, but his refusal to defer to the Buddha's authority is what undoes everything else he'd achieved.",
            "The same structure as the Kural: real capability, undone entirely by the one failure to submit or show due reverence.",
            "The story of Devadatta (Vinaya Pitaka / Dhammapada commentary)", "devadatta-story", 55, "Good narrative match on 'ability undone by refusal to defer,' though the story concerns a specific rivalry rather than a general teaching about bowing to God.", False),
        "greek_mythology": xr("Arachne’s weaving is genuinely as good as the goddess Athena's, but her refusal to acknowledge Athena's due honor — pure pride — is what triggers her ruin.",
            "Talent alone doesn't save Arachne; it's specifically her refusal to show honor that destroys her.",
            "Talent alone doesn't save Arachne, just as ability alone doesn't redeem the unbowed head in the Kural — reverence was the one thing missing.",
            "Ovid, Metamorphoses, Book VI (the myth of Arachne)", "ovid-arachne", 78, "Strong match — real talent undone specifically by a refusal to honor the divine, closely mirroring the Kural's logic.", False),
        "philosophy": xr("“Evil mortals flee [this Word/Law], poor wretches; though they are desirous of good things for their possession, they neither see nor listen to God's universal Law.”",
            "Cleanthes says the foolish actively run from the one universal rational order that would actually give them the good life they're chasing.",
            "A philosophical parallel to the Kural’s unbowed head — refusing to submit to the highest order is precisely what keeps a person from the good they want.",
            "Cleanthes, Hymn to Zeus", "cleanthes-hymn", 55, "Solid conceptual match (refusing the universal order blocks the good life), though 'God's Law' here is the rational order of the cosmos, not a personal deity to be bowed to.", True),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 10,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "பிறவிப் பெருங்கடல் நீந்துவர் நீந்தார்\nஇறைவன் அடிசேரா தார்.",
    "transliteration": "PiRavi-p perungadal neendhuvar neendhaar,\niRaivan adi seraadhaar.",
    "meaning": "Only those who reach the feet of God can swim across the great ocean of repeated births; no one else can.",
    "elementary": "Life — with all its ups, downs, and being born again and again — is like a giant ocean. This last kural in the chapter says the only way to swim all the way across it is by holding onto God.",
    "university": "This closing verse restates and intensifies kural 8’s ocean imagery, now naming the object to be crossed explicitly as “piravi” — birth/rebirth itself — invoking the doctrine of samsara common to the Indian religious milieu. The repetition is a structural device: the chapter opens by establishing God as “first” of all things and closes by establishing God as the only viable “crossing” out of the cycle those origins set in motion.",
    "cross_references": {
        "hinduism": xr("“This divine energy of Mine... is difficult to overcome. But those who have surrendered unto Me can easily cross beyond it.”",
            "Krishna admits his own divine power is genuinely hard to overcome by yourself — but total surrender to him makes crossing it easy.",
            "Same claim as the Kural: this particular ocean isn't crossed by self-effort alone, only by surrender to the divine.",
            "Bhagavad Gita 7.14", "gita-asitis", 85, "Strong match on the exact mechanism (surrender, not self-effort, enables the crossing).", True),
        "buddhism": xr("“Few among men are those who cross to the farther shore... those who act according to the perfectly taught Dhamma will cross the realm of Death, so difficult to cross.”",
            "The Buddha observes that almost everyone just paces along the near bank of existence — only a few actually cross to the far shore, and only through genuine practice.",
            "Same 'few actually cross' structure as the Kural, and the same insistence that only real practice, not mere proximity, gets you there.",
            "Dhammapada, verses 85–86", "dhammapada-buddharakkhita", 82, "Strong match — same rare-successful-crossing structure and the same insistence on practice over mere nominal belonging.", True),
        "christianity": xr("“For by grace are ye saved through faith; and that not of yourselves: it is the gift of God: not of works.”",
            "Paul is emphatic that being saved is a gift, not an achievement — nothing you did earns it.",
            "Backs the Kural’s exclusivity claim: crossing over isn't something you accomplish yourself, it's given.",
            "Ephesians 2:8-9 (KJV)", "kjv", 75, "Strong match on the 'not by your own effort' logic, though Paul's specific context is salvation from sin rather than rebirth.", True),
        "islam": xr("“There is none of you except he will come to it [Hell]... Then We will save those who feared Allah and leave the wrongdoers within it.”",
            "Every person, the verse says, passes over Hell — but God then rescues those who were mindful of Him and leaves the wrongdoers there.",
            "A vivid version of the Kural’s 'crossing' image — everyone faces the crossing, but only some make it fully across.",
            "Qur'an 19:71-72, Maryam", "quran-general", 75, "Strong match on the universal-crossing-with-selective-rescue structure.", True),
        "judaism": xr("In later Jewish mysticism, souls that haven't reached spiritual completion are said to be sent back into new bodies (gilgul, 'the wheel') again and again until they are pure enough to return to their heavenly source.",
            "This is Judaism's own, much later version of the idea that a soul cycles through lives until it becomes fit to finally return to God.",
            "A genuine, if late and minority, Jewish parallel to the Kural's 'ocean of rebirth' — crossed only by finally becoming fit to return to the divine source.",
            "Gilgul neshamot, the Zohar and later Kabbalah", "gilgul-kabbalah", 40, "Real textual basis in Kabbalah, but this is a mystical minority position within Judaism, not found in the Tanakh and rejected by mainstream Rabbinic/Maimonidean thought.", False),
        "greek_mythology": xr("Empedocles and the Orphic tradition taught that souls are bound to a repeating 'Wheel' of births across many forms of life, escapable only through purification and right knowledge.",
            "The soul is stuck cycling through different bodies and lives until it purifies itself enough to finally break free.",
            "The closest Greek parallel to the Kural's literal 'ocean of rebirth' — a real doctrine of being trapped in repeated birth, escaped only by the right kind of transformation.",
            "Empedocles / Orphic tradition (the gold tablets)", "orphic-tablets", 50, "Genuine ancient doctrine of cyclical rebirth and escape from it, matching the Kural's core claim well, though escape comes through ritual/philosophical purification rather than devotion to a personal God.", False),
        "philosophy": xr("In the myth, most souls choose their next life poorly, out of habit or ignorance, and are swept back into the cycle — only the soul that has genuinely pursued wisdom chooses well enough to eventually break free.",
            "Choosing your way out of the cycle of rebirth takes real, hard-won wisdom, not luck or a passing wish.",
            "Matches the Kural's claim precisely: escaping the cycle of rebirth takes something more than luck — a specific, higher orientation.",
            "Plato, Republic, Book X (the Myth of Er)", "plato-republic", 70, "Strong structural match — an explicit doctrine of escaping the wheel of rebirth through pursuit of the highest good/wisdom.", False),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

# --- Integrate additional researched chapters (each chapter_NN_data.json has
#     "kurals": [...] in the exact same shape as the hand-written blocks above,
#     plus "new_sources": {citation_id: {...}} to merge into the sources dict) ---
_chapter_files = sorted(glob.glob(os.path.join(OUTPUTS_ROOT, "chapter_*_data.json")))
_loaded_chapter_numbers = []
for _cf in _chapter_files:
    with open(_cf, encoding="utf-8") as _f:
        _cdata = json.load(_f)
    kurals.extend(_cdata["kurals"])
    _loaded_chapter_numbers.append(os.path.basename(_cf))
    for _cid, _cinfo in _cdata.get("new_sources", {}).items():
        if _cid not in sources:
            sources[_cid] = _cinfo
kurals.sort(key=lambda k: k["number"])
print(f"Integrated {len(_chapter_files)} chapter files: {_loaded_chapter_numbers}")

# --- Jainism backfill: jain/jain_chapter_NN.json = {"chapter": N, "jainism": {"<kural number>": xr}, "new_sources": {...}}.
#     A kural's own inline cross_references["jainism"] (new chapters) wins over a backfill entry.
_canon = os.path.join(OUTPUTS_ROOT, "jain", "canonical_sources.json")
if os.path.exists(_canon):
    sources.update(json.load(open(_canon, encoding="utf-8")))  # fixed definitions win over agent-supplied ones
_jain_files = sorted(glob.glob(os.path.join(OUTPUTS_ROOT, "jain", "jain_chapter_*.json")))
_jain_entries = {}
for _jf in _jain_files:
    with open(_jf, encoding="utf-8") as _f:
        _jd = json.load(_f)
    for _num, _x in _jd.get("jainism", {}).items():
        _jain_entries[int(_num)] = _x
    for _cid, _cinfo in _jd.get("new_sources", {}).items():
        if _cid not in sources:
            sources[_cid] = _cinfo
for k in kurals:
    if "jainism" not in k["cross_references"] and k["number"] in _jain_entries:
        k["cross_references"]["jainism"] = _jain_entries[k["number"]]
_jain_have = sum(1 for k in kurals if "jainism" in k["cross_references"])
JAIN_COMPLETE = _jain_have == len(kurals)
print(f"Jainism coverage: {_jain_have}/{len(kurals)} kurals" + ("" if JAIN_COMPLETE else " (Jainism is hidden from the public site/book until every built kural has it)"))

# --- Overrides (Oct 2026 cleanup): overrides/phil_fix_*.json =
#     {"philosophy": {"<kural>": xr}, "university": {"<kural>": text}, "new_sources": {...}} — replace in place.
_ov_n = 0
_kmap = {k["number"]: k for k in kurals}
for _of in sorted(glob.glob(os.path.join(OUTPUTS_ROOT, "overrides", "phil_fix_*.json"))):
    with open(_of, encoding="utf-8") as _f:
        _od = json.load(_f)
    for _cid, _cinfo in _od.get("new_sources", {}).items():
        if _cid not in sources:
            sources[_cid] = _cinfo
    for _num, _x in _od.get("philosophy", {}).items():
        _kmap[int(_num)]["cross_references"]["philosophy"] = _x; _ov_n += 1
    for _num, _t in _od.get("university", {}).items():
        _kmap[int(_num)]["university"] = _t; _ov_n += 1
print(f"Applied {_ov_n} philosophy/university overrides")

# --- Plain-English "meaning" rewrite (Oct 2026): meaning_simple/output/out_*.json = {"<kural>": text}; later files win.
_mn = 0
for _mf in sorted(glob.glob(os.path.join(OUTPUTS_ROOT, "meaning_simple", "output", "out_*.json"))):
    with open(_mf, encoding="utf-8") as _f:
        for _num, _t in json.load(_f).items():
            if int(_num) in _kmap and _t.strip():
                _kmap[int(_num)]["meaning"] = _t.strip(); _mn += 1
print(f"Applied {_mn} plain-English meaning overrides")

# --- Sikhism backfill (added Oct 2026, placed after Jainism):
#     sikh/sikh_chapter_NN.json = {"chapter": N, "sikhism": {"<kural number>": xr}, "new_sources": {...}}.
#     Same live-web verification standard as every other tradition. Inline entries win.
_sikh_canon = os.path.join(OUTPUTS_ROOT, "sikh", "canonical_sources.json")
if os.path.exists(_sikh_canon):
    sources.update(json.load(open(_sikh_canon, encoding="utf-8")))
_sikh_entries = {}
for _sf in sorted(glob.glob(os.path.join(OUTPUTS_ROOT, "sikh", "sikh_chapter_*.json"))):
    with open(_sf, encoding="utf-8") as _f:
        _sd = json.load(_f)
    for _num, _x in _sd.get("sikhism", {}).items():
        _sikh_entries[int(_num)] = _x
    for _cid, _cinfo in _sd.get("new_sources", {}).items():
        if _cid not in sources:
            sources[_cid] = _cinfo
for k in kurals:
    k["cross_references"].pop("con"+"fucianism", None)
    if "sikhism" not in k["cross_references"] and k["number"] in _sikh_entries:
        k["cross_references"]["sikhism"] = _sikh_entries[k["number"]]
_sikh_have = sum(1 for k in kurals if "sikhism" in k["cross_references"])
SIKH_COMPLETE = _sikh_have == len(kurals)
print(f"Sikhism coverage: {_sikh_have}/{len(kurals)} kurals" + ("" if SIKH_COMPLETE else " (Sikhism is hidden from the public site/book until every kural has it)"))

# --- Real Life Example (added Oct 2026): history/history_chapter_NN.json =
#     {"chapter": N, "real_life_example": {"<kural number>": rle}, "new_sources": {...}}.
#     rle = {event_title, date, place, event, explanation, tie_back, citation_ids[>=2], _accuracy_percent, _accuracy_note}
#     Only well-documented, undisputed history. Hidden until every kural has one.
_hist_entries = {}
for _hf in sorted(glob.glob(os.path.join(OUTPUTS_ROOT, "history", "history_chapter_*.json"))):
    with open(_hf, encoding="utf-8") as _f:
        _hd = json.load(_f)
    for _num, _x in _hd.get("real_life_example", {}).items():
        _hist_entries[int(_num)] = _x
    for _cid, _cinfo in _hd.get("new_sources", {}).items():
        if _cid not in sources:
            sources[_cid] = _cinfo
for k in kurals:
    if "real_life_example" not in k and k["number"] in _hist_entries:
        k["real_life_example"] = _hist_entries[k["number"]]
_hist_have = sum(1 for k in kurals if "real_life_example" in k)
HIST_COMPLETE = _hist_have == len(kurals)
print(f"Real Life Example coverage: {_hist_have}/{len(kurals)} kurals" + ("" if HIST_COMPLETE else " (hidden from the public site/book until every kural has one)"))

# Preview mode: PREVIEW_DIR=/path python3 build_data2.py writes a data/ folder containing only the kurals
# that already have every new section, with those sections switched on (for reviewing a pilot batch).
if os.environ.get("PREVIEW_DIR"):
    SIKH_COMPLETE = HIST_COMPLETE = True
    kurals = [k for k in kurals if "sikhism" in k["cross_references"] and "real_life_example" in k]
    BASE = os.environ["PREVIEW_DIR"]
    print(f"PREVIEW: writing {len(kurals)} kurals to {BASE}/data")

# Write the public-facing kurals.json (no internal accuracy fields)
public_kurals = []
accuracy_log = []
for k in kurals:
    pub = {
        "number": k["number"],
        "adhikaram": k["adhikaram"],
        "tamil": k["tamil"],
        "transliteration": k["transliteration"],
        "meaning": k["meaning"],
        "elementary": k["elementary"],
        "university": k["university"],
        "cross_references": {},
        "sources": k["sources"],
    }
    for t in TRAD_ORDER:
        if t not in k["cross_references"]:
            continue
        c = k["cross_references"][t]
        if (t != "jainism" or JAIN_COMPLETE) and (t != "sikhism" or SIKH_COMPLETE):
          pub["cross_references"][t] = {
              "quote_or_event": c["quote_or_event"],
              "is_quote": c["is_quote"],
              "explanation": c["explanation"],
              "tie_back": c["tie_back"],
              "source": c["source"],
              "citation_id": c["citation_id"],
          }
        src_tier = sources.get(c["citation_id"], {}).get("tier", "unknown")
        accuracy_log.append({
            "kural": k["number"],
            "tradition": t,
            "source": c["source"],
            "citation_id": c["citation_id"],
            "source_tier": src_tier,
            "accuracy_percent": c["_accuracy_percent"],
            "rationale": c["_accuracy_note"],
            "flagged_for_review": c["_accuracy_percent"] < 60,
        })
    if "real_life_example" in k:
        r = k["real_life_example"]
        if HIST_COMPLETE:
            pub["real_life_example"] = {kk: r[kk] for kk in ("event_title", "date", "place", "event", "explanation", "tie_back", "citation_ids")}
        accuracy_log.append({
            "kural": k["number"],
            "tradition": "real_life_example",
            "source": r["event_title"],
            "citation_id": ",".join(r["citation_ids"]),
            "source_tier": "/".join(sources.get(c, {}).get("tier", "unknown") for c in r["citation_ids"]),
            "accuracy_percent": r["_accuracy_percent"],
            "rationale": r["_accuracy_note"],
            "flagged_for_review": r["_accuracy_percent"] < 60,
        })
    public_kurals.append(pub)

with open(f"{BASE}/data/kurals.json", "w", encoding="utf-8") as f:
    json.dump(public_kurals, f, ensure_ascii=False, indent=2)

with open(f"{BASE}/data/sources.json", "w", encoding="utf-8") as f:
    json.dump(sources, f, ensure_ascii=False, indent=2)

with open(f"{BASE}/data/accuracy_log.json", "w", encoding="utf-8") as f:
    json.dump({
        "_note": "INTERNAL USE ONLY — not part of the public book/website. Private accuracy assessment for every cross-tradition citation, kept for project QA.",
        "entries": accuracy_log,
    }, f, ensure_ascii=False, indent=2)

avg = sum(e["accuracy_percent"] for e in accuracy_log) / len(accuracy_log)
flagged = [e for e in accuracy_log if e["flagged_for_review"]]
n_quote = sum(1 for k in kurals for t in TRAD_ORDER if t in k["cross_references"] and k["cross_references"][t]["is_quote"])
n_paraphrase = len(accuracy_log) - n_quote
print(f"Wrote {len(public_kurals)} kurals, {len(sources)} sources, {len(accuracy_log)} accuracy entries. Average accuracy: {avg:.1f}%")
print(f"Direct quotes: {n_quote} / Paraphrased events-or-teachings: {n_paraphrase}")
print(f"Flagged for review (<60% confidence): {len(flagged)}")
_je = [e for e in accuracy_log if e["tradition"] == "jainism"]
if _je:
    print(f"Jainism: {len(_je)} entries, average accuracy {sum(e['accuracy_percent'] for e in _je)/len(_je):.1f}%, direct quotes {sum(1 for k in kurals if 'jainism' in k['cross_references'] and k['cross_references']['jainism']['is_quote'])}, flagged {sum(1 for e in _je if e['flagged_for_review'])}")
for e in flagged:
    print(f"  - Kural {e['kural']} / {e['tradition']} ({e['accuracy_percent']}%, tier={e['source_tier']}): {e['rationale']}")
for _lab, _key in (("Sikhism", "sikhism"), ("Real Life Example", "real_life_example")):
    _xe = [e for e in accuracy_log if e["tradition"] == _key]
    if _xe:
        print(f"{_lab}: {len(_xe)} entries, average accuracy {sum(e['accuracy_percent'] for e in _xe)/len(_xe):.1f}%, flagged {sum(1 for e in _xe if e['flagged_for_review'])}")
