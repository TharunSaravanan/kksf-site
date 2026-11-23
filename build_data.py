import json

sources = {
    "ytamizh-ch1": {"title": "கடவுள் வாழ்த்து (The Praise of God) — Chapter 1, with commentary by Mu. Varadarajan, Solomon Pappaiah, M. Karunanidhi, and Sivayogi Sivakumar", "publisher": "ytamizh.com", "url": "https://www.ytamizh.com/thirukural/chapter-1/", "access_date": "2026-09-21"},
    "thirukkuralnet-adhigaram1": {"title": "The Praise of God — Adhigaram 1 (Tamil text, transliteration, English translation, song setting by Pu. A. Muthukrishnan)", "publisher": "thirukkural.net", "url": "https://www.thirukkural.net/en/kural/adhigaram-001.html", "access_date": "2026-09-21"},
    "pope-1886": {"title": "The Sacred Kurral of Tiruvalluva Nayanar", "author": "G.U. Pope", "year": "1886", "note": "Classic public-domain English translation, referenced for cross-checking couplet renderings"},
    "gita-mukundananda": {"title": "Bhagavad Gita, The Song of God (translation and commentary)", "author": "Swami Mukundananda", "publisher": "holy-bhagavad-gita.org", "url": "https://www.holy-bhagavad-gita.org/"},
    "gita-asitis": {"title": "Bhagavad-gita As It Is", "author": "A.C. Bhaktivedanta Swami Prabhupada", "publisher": "vedabase.io / asitis.com", "url": "https://vedabase.io/en/library/bg/"},
    "mundaka-upanishad": {"title": "Mundaka Upanishad 1.2.12-13 (para vidya / apara vidya)", "publisher": "wisdomlib.org", "url": "https://www.wisdomlib.org/hinduism/book/mundaka-upanishad-shankara-bhashya/d/doc145096.html"},
    "isha-upanishad": {"title": "Isha Upanishad, verse 7", "publisher": "wisdomlib.org / Sri Aurobindo Ashram", "url": "https://www.wisdomlib.org/hinduism/book/ishavasya-bhashya-by-sitarama/d/doc145024.html"},
    "katha-upanishad": {"title": "Katha Upanishad 1.3.3 (the chariot allegory)", "publisher": "wisdomlib.org", "url": "https://www.wisdomlib.org/hinduism/book/katha-upanishad-shankara-bhashya/d/doc145206.html"},
    "kjv": {"title": "The Holy Bible, King James Version", "note": "Public domain"},
    "quran-sahih": {"title": "The Qur'an, Sahih International translation", "publisher": "quran.com / corpus.quran.com"},
    "quran-general": {"title": "The Qur'an, composite of standard English translations (Sahih International, Yusuf Ali, Abdel Haleem) cross-checked for wording", "publisher": "quran.com / islamawakened.com"},
    "dhammapada-buddharakkhita": {"title": "The Dhammapada", "translator": "Acharya Buddharakkhita", "publisher": "accesstoinsight.org / buddhanet.net"},
    "dhammapada-narada": {"title": "The Dhammapada", "translator": "Narada Thera (and composite standard renderings)", "publisher": "wisdomlib.org / vivekavani.com"},
    "majjhima-nikaya-22": {"title": "Alagaddupama Sutta: The Simile of the Snake (Majjhima Nikaya 22) — the Raft Parable", "publisher": "accesstoinsight.org / budsas.org"},
    "hesiod-theogony": {"title": "Theogony", "author": "Hesiod", "translator": "H.G. Evelyn-White", "publisher": "Loeb Classical Library 57 (1914), via theoi.com", "url": "https://www.theoi.com/Text/HesiodTheogony.html"},
    "aristotle-metaphysics": {"title": "Metaphysics, Book XII (Lambda)", "author": "Aristotle", "publisher": "The Internet Classics Archive (MIT)", "url": "https://classics.mit.edu/Aristotle/metaphysics.12.xii.html"},
    "homer-odyssey": {"title": "Odyssey, Book 12 (the Sirens episode)", "author": "Homer", "publisher": "Perseus Digital Library / Theoi Classical Texts", "url": "https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0136%3Abook%3D12"},
    "charon-myth": {"title": "Charon, ferryman of the River Styx", "note": "General Greek mythological tradition", "publisher": "Theoi.com / Encyclopedia.com / Britannica", "url": "https://www.theoi.com/Khthonios/Kharon.html"},
    "ovid-metamorphoses": {"title": "Metamorphoses, Book VI (the myth of Arachne)", "author": "Ovid (Roman poet, recording an originally Greek myth)", "note": "Earliest full surviving literary telling is Roman, not primary Greek-language source"},
    "plato-republic": {"title": "Republic, Book X (the Myth of Er)", "author": "Plato", "publisher": "standard English translations (Jowett/Shorey), cross-checked via multiple summaries"},
    "plato-phaedrus": {"title": "Phaedrus (the charioteer allegory)", "author": "Plato", "publisher": "standard English translations, cross-checked via multiple summaries"},
    "epictetus-enchiridion": {"title": "Enchiridion, Chapter 5", "author": "Epictetus", "translator": "Elizabeth Carter", "publisher": "The Internet Classics Archive (MIT)", "url": "https://classics.mit.edu/Epictetus/epicench.html"},
}

def blank(note):
    return {"text": None, "source": None, "citation_id": None, "note": note}

def ref(text, source, citation_id):
    return {"text": text, "source": source, "citation_id": citation_id, "note": None}

NO_MATCH_BUDDHISM_THEISM = "Classical Buddhism does not posit a creator-God as first cause (dependent origination avoids a single first cause), so a citation here would misrepresent the tradition rather than genuinely correspond to it."

kurals = []

kurals.append({
    "number": 1,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "அகர முதல எழுத்தெல்லாம் ஆதி\nபகவன் முதற்றே உலகு.",
    "transliteration": "Agara mudhala ezhuthu ellaam aadhi,\nPakavan mudhatre ulagu.",
    "meaning": "Just as the letter “A” stands first among all the letters of the alphabet, God stands first as the origin and foundation of the whole world.",
    "explanation_simple": "Think about the alphabet — it always starts with the letter A, and everything else builds on it. This kural says God is like that letter A for the whole world: the very first thing, the starting point that everything else comes from.",
    "explanation_scholarly": "Valluvar opens his work not with an invocation to a specific deity but with a logical analogy drawn from language itself: just as அ (a) is structurally primary in the Tamil alphabet — the vowel from which the entire phonetic system is generated — so too is “Pahavan” (rendered here “God”/“the Primal Being”) ontologically primary to the cosmos. The term is deliberately non-sectarian, part of why the Thirukkural has been embraced across Saiva, Vaishnava, Jain, and secular-humanist readings alike. The appeal to a “first principle” or arche is one of the oldest moves in both theology and philosophy — found equally in Vedic cosmology, biblical self-declaration, and Aristotelian metaphysics.",
    "cross_references": {
        "hinduism": ref("“I am the Self, O Gudakesha, seated in the hearts of all creatures. I am the beginning, the middle, and the end of all beings.”", "Bhagavad Gita 10.20", "gita-asitis"),
        "christianity": ref("“I am Alpha and Omega, the beginning and the end, the first and the last.”", "Revelation 22:13 (KJV)", "kjv"),
        "islam": ref("“He is the First and the Last, the Ascendant and the Intimate, and He is, of all things, Knowing.”", "Qur'an 57:3, Al-Hadid (Sahih International)", "quran-sahih"),
        "judaism": ref("“I am the first, and I am the last; and beside me there is no God.”", "Isaiah 44:6 (Tanakh / KJV)", "kjv"),
        "buddhism": blank(NO_MATCH_BUDDHISM_THEISM),
        "greek_mythology": ref("“Verily at the first Chaos came to be” (πρώτιστα Χάος γένετ’) — in Greek cosmogony, Chaos is the primeval void from which all subsequent gods and the ordered cosmos emerge.", "Hesiod, Theogony, lines 116–117", "hesiod-theogony"),
        "philosophy": ref("Aristotle argues for a first, eternal, unmoved substance — “it is necessary that there should be an eternal unmovable substance... substances are the first of existing things” — the “Prime Mover,” the ultimate first cause of all motion and existence.", "Aristotle, Metaphysics, Book XII (Lambda)", "aristotle-metaphysics"),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1", "pope-1886"],
})

kurals.append({
    "number": 2,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "கற்றதனால் ஆய பயனென்கொல் வாலறிவன்\nநற்றாள் தொழாஅர் எனின்.",
    "transliteration": "Katradhanaal aaya payan en kol vaal-arivan,\nnatraal thozhaaar enin.",
    "meaning": "What good is all of a person’s learning, if they never bow in reverence to the good feet of the One of pure, perfect wisdom?",
    "explanation_simple": "Imagine studying really hard and knowing lots of facts, but never once being humble about where real wisdom comes from. This kural says that kind of learning doesn’t truly help you — real learning should make you humble, not just full of facts.",
    "explanation_scholarly": "This verse critiques a purely instrumental or accumulative view of education. “Vaal-arivan” (“the one of spotless/pure knowledge”) refers to a transcendent, perfect intelligence — the ground of all true knowing, not a sectarian god. Valluvar’s claim is that erudition divorced from reverence toward that ultimate source is functionally sterile: it produces information without transformation. This is a recurring cross-cultural theme — the distinction between accumulated data and lived, humbling wisdom — found in the Upanishadic distinction between “para vidya” and “apara vidya,” in Pauline theology’s contrast of knowledge and love, and in the Buddhist critique of reciting scripture without practicing it.",
    "cross_references": {
        "hinduism": ref("Distinguishes “aparā vidyā” (lower knowledge: the Vedas, phonetics, grammar, ritual, etc.) from “parā vidyā” (higher knowledge: that by which the imperishable Self is realized). Worldly learning without the higher knowledge of ultimate reality is, in the text’s own terms, incomplete.", "Mundaka Upanishad 1.2.12–13", "mundaka-upanishad"),
        "christianity": ref("“And though I have the gift of prophecy, and understand all mysteries, and all knowledge... and have not charity, I am nothing.”", "1 Corinthians 13:2 (KJV)", "kjv"),
        "islam": ref("“...it is only those who have knowledge among His servants that fear/revere Allah.”", "Qur'an 35:28, Fatir", "quran-general"),
        "judaism": ref("“The fear of the LORD is the beginning of wisdom, and the knowledge of the Holy One is understanding.”", "Proverbs 9:10 (Tanakh, Mishlei / KJV)", "kjv"),
        "buddhism": ref("“Though he recites much the sacred texts, but is negligent and does not practice according to the Dhamma, like a cowherd who counts the cattle of others, he has no share in the benefits of the holy life.”", "Dhammapada, verses 19–20", "dhammapada-buddharakkhita"),
        "greek_mythology": blank("No genuine, directly citable episode was found addressing this specific theme (learning vs. reverence) without over-reaching."),
        "philosophy": blank("Candidates considered (e.g., Socratic humility) did not match closely enough to a single, precisely citable passage."),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 3,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "மலர்மிசை ஏகினான் மாணடி சேர்ந்தார்\nநிலமிசை நீடுவாழ் வார்.",
    "transliteration": "Malar-misai Ekinaan maanadi serndhaar,\nnila-misai needu vaazhvaar.",
    "meaning": "Those who cling to the glorious feet of Him who moves lightly even upon a flower will live long and flourish upon this earth.",
    "explanation_simple": "Picture someone so light and pure they could stand on a flower without crushing it. This kural says if you hold on tight to someone that good — meaning you stay close to God — your life on earth will go well for a long, long time.",
    "explanation_scholarly": "The image of the divine “moving upon a flower” (malar-misai ekinaan) evokes both lightness/purity and the lotus-throne motif common to Tamil and broader Indic religious iconography. “Nilamisai needuvaazhvaar” — “shall live long upon the earth” — is classically read not as mere biological longevity but as a durable, well-founded flourishing (fame, stability, inner peace) that outlasts the transient. The pairing of devotion with durable flourishing is one of the most cross-culturally attested religious claims: attachment to the sacred is repeatedly figured as a root system keeping a person stable and fruitful.",
    "cross_references": {
        "hinduism": ref("“To those who worship Me alone, thinking of no other... I bring what they lack and preserve what they already possess (yoga-kshema).”", "Bhagavad Gita 9.22", "gita-mukundananda"),
        "christianity": ref("“I am the vine, ye are the branches: he that abideth in me, and I in him, the same bringeth forth much fruit: for without me ye can do nothing.”", "John 15:5 (KJV)", "kjv"),
        "judaism": ref("“And he shall be like a tree planted by the rivers of water, that bringeth forth his fruit in his season; his leaf also shall not wither; and whatsoever he doeth shall prosper.”", "Psalm 1:3 (Tanakh, Ketuvim / KJV)", "kjv"),
        "buddhism": ref("“To one ever eager to revere and serve the elders, these four blessings accrue: long life and beauty, happiness and power.” Note: the object of reverence here is elders/teachers rather than a deity — a precise structural parallel (reverence → long life), not a full theological match.", "Dhammapada, verse 109", "dhammapada-narada"),
        "islam": blank("No sufficiently precise, directly citable match found."),
        "greek_mythology": blank("No sufficiently precise, directly citable match found."),
        "philosophy": blank("No sufficiently precise, directly citable match found."),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 4,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "வேண்டுதல் வேண்டாமை இலானடி சேர்ந்தார்க்கு\nயாண்டும் இடும்பை இல.",
    "transliteration": "Vendudhal vendaamai ilaan adi serndhaarkku,\nyaandum idumbai ila.",
    "meaning": "No suffering will ever touch those who take refuge in the feet of the One who is beyond all craving and all aversion.",
    "explanation_simple": "This kural says that if you stay close to someone who never gets too excited about getting what they want, or too upset about not getting it — someone completely calm — then bad things won’t really be able to shake you the way they shake other people.",
    "explanation_scholarly": "The verse names two categories — raga (craving/attachment, “vendudhal”) and dvesha (aversion, “vendaamai”) — as the very things the Divine transcends. This dyad is the central diagnostic pair in most Indian soteriologies (Hindu, Buddhist, and Jain alike) for why beings suffer. The claim is thus not that worship magically wards off misfortune, but that participation in a consciousness beyond craving/aversion is itself what removes vulnerability to affliction (“idumbai”) — functionally identical to the Stoic and Buddhist claims that suffering arises from the mind’s reactive patterns rather than from external events themselves.",
    "cross_references": {
        "hinduism": ref("“One who is not disturbed by sorrows, who has no craving for joy, who is free from attachment, fear, and anger — is called a sage of steady wisdom (sthitaprajna).”", "Bhagavad Gita 2.56", "gita-mukundananda"),
        "christianity": ref("“Thou wilt keep him in perfect peace, whose mind is stayed on thee: because he trusteth in thee.”", "Isaiah 26:3 (KJV)", "kjv"),
        "judaism": ref("“Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me.”", "Psalm 23:4 (Tanakh, Ketuvim / KJV)", "kjv"),
        "islam": ref("“Unquestionably, [for] the allies of Allah there will be no fear concerning them, nor will they grieve.”", "Qur'an 10:62, Yunus", "quran-general"),
        "buddhism": blank("Closely related Dhammapada material (v.39, on freedom from craving/aversion) fits Kural 5’s specific claim (transcending merit/demerit) more precisely and is cited there instead, to avoid stretching one verse across two distinct claims."),
        "greek_mythology": blank("No sufficiently precise, directly citable match found."),
        "philosophy": ref("“Men are disturbed not by the things which happen, but by the opinions about the things.”", "Epictetus, Enchiridion, Chapter 5", "epictetus-enchiridion"),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 5,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "இருள்சேர் இருவினையும் சேரா இறைவன்\nபொருள்சேர் புகழ்புரிந்தார் மாட்டு.",
    "transliteration": "Irul-ser iru-vinaiyum seraa iraivan,\nporul-ser pukazh-purindhaar maattu.",
    "meaning": "The two dark deeds — the good and bad karma born of ignorance — will not attach themselves to those who truly delight in praising God with real understanding.",
    "explanation_simple": "This kural talks about two kinds of “marks” people collect from doing good or bad things without understanding what they really mean — like getting stars or strikes without knowing why they matter. It says that truly understanding and loving God stops those confusing marks from piling up on you.",
    "explanation_scholarly": "“Irul” (darkness) signifies avidya (ignorance), and “iru vinai” (the twin deeds) refers to punya and papa — meritorious and demeritorious karma — both of which, in classical Indian thought, bind the soul to rebirth regardless of whether the deeds were “good” or “bad,” because both are performed from a standpoint of ignorance about ultimate reality. Valluvar’s claim is radical in the way several Indian soteriologies are radical: liberation is not more good karma outweighing bad, but a shift in understanding (“porul-ser pukazh” — praise “joined with true meaning”) that removes a person from the karmic ledger altogether.",
    "cross_references": {
        "hinduism": ref("“buddhi-yukto jahātīha ubhe sukṛta-duṣkṛte” — “One who is united with wisdom casts off, even in this life, both good and evil deeds.”", "Bhagavad Gita 2.50", "gita-asitis"),
        "buddhism": ref("Describes one whose mind is unaffected by lust or hatred as having “gone beyond both merit and demerit” (puñña-pāpa-pahīnassa), for whom “there is no fear.”", "Dhammapada, verse 39", "dhammapada-buddharakkhita"),
        "christianity": ref("“There is therefore now no condemnation to them which are in Christ Jesus.”", "Romans 8:1 (KJV)", "kjv"),
        "judaism": blank("Classical Tanakh theology has no citable concept of “transcending the karmic ledger” as such; forcing a parallel here would misrepresent the tradition."),
        "islam": blank("No sufficiently precise, directly citable match found."),
        "greek_mythology": blank("No sufficiently precise, directly citable match found."),
        "philosophy": blank("No sufficiently precise, directly citable match found."),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 6,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "பொறிவாயில் ஐந்தவித்தான் பொய்தீர் ஒழுக்க\nநெறிநின்றார் நீடுவாழ் வார்.",
    "transliteration": "Pori-vaayil aindhu avithaan poi-theer ozhukka,\nneri ninRaar needu vaazhvaar.",
    "meaning": "Those who stand firm in the untainted, truthful path of Him who has mastered the five sense-desires will live long, flourishing lives.",
    "explanation_simple": "We have five senses — seeing, hearing, smelling, tasting, and touching — and they can pull us toward all kinds of wants. This kural says that if you follow someone who has fully mastered those wants, instead of being controlled by them, and you stay on that honest path, your life will go really well.",
    "explanation_scholarly": "“Pori” refers to the five sense-faculties (indriyas); “aindhu avithaan” — “who has extinguished the five” — depicts the divine as the paradigm of complete indriya-nigraha (sense-mastery), a central discipline across nearly all Indian contemplative systems. The verse makes mastery of the senses, rather than mere rule-following, the actual mechanism of a flourishing life — free from the erratic disturbance the unchecked senses cause. Sense-restraint as the gateway discipline to a stable, virtuous life is one of the most universally attested ethical claims across religious and philosophical traditions.",
    "cross_references": {
        "hinduism": ref("“Know the Self as the rider in a chariot, the body as the chariot; the intellect as the charioteer, and the mind as the reins” (the senses being the horses).", "Katha Upanishad 1.3.3", "katha-upanishad"),
        "buddhism": ref("“Restraint in the eye is good, good is restraint in the ear... in the body restraint is good... restraint everywhere is good. A bhikkhu restrained in every way is freed from all suffering.”", "Dhammapada, verses 360–361", "dhammapada-buddharakkhita"),
        "christianity": ref("“But I keep under my body, and bring it into subjection.”", "1 Corinthians 9:27 (KJV)", "kjv"),
        "judaism": ref("“He that is slow to anger is better than the mighty; and he that ruleth his spirit than he that taketh a city.”", "Proverbs 16:32 (Tanakh, Ketuvim / KJV)", "kjv"),
        "islam": ref("“As for him who feared to stand before his Lord and restrained himself from [his] desire, then indeed, Paradise will be his refuge.”", "Qur'an 79:40–41, An-Nazi'at", "quran-general"),
        "greek_mythology": ref("Odysseus has himself bound to the mast and his crew’s ears sealed with wax so they can resist the fatal lure of the Sirens’ song — the classical image of willed restraint against overpowering sensory temptation.", "Homer, Odyssey, Book 12", "homer-odyssey"),
        "philosophy": ref("The allegory of the soul as a charioteer (reason) driving two horses, one noble and one appetitive/unruly, which must be mastered for the soul to rise rather than be dragged down.", "Plato, Phaedrus", "plato-phaedrus"),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 7,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "தனக்குவமை இல்லாதான் தாள்சேர்ந்தார்க் கல்லால்\nமனக்கவலை மாற்றல் அரிது.",
    "transliteration": "Thanakku-uvamai illaadhaan thaal serndhaark kallaal,\nmana-kavalai maatral aridhu.",
    "meaning": "Except for those who cling to the feet of the One beyond all comparison, it is very hard for anyone to be free of the mind’s anxieties.",
    "explanation_simple": "Everybody worries sometimes, but this kural says the only real way to truly let go of worry deep down is to hold onto something — or Someone — so great that nothing else compares. Then your small worries don’t feel so huge anymore.",
    "explanation_scholarly": "“Thanakku uvamai illaadhaan” (“the One with no likeness to Himself,” utterly incomparable) situates the removal of mental anxiety not in technique or willpower but in relationship to a reality that relativizes every other object of comparison — and therefore every other source of anxious grasping. If nothing else is truly comparable, nothing else is commensurable with one’s ultimate wellbeing, so ordinary anxieties (always anxieties about something comparable — status, loss, gain) lose their grip. This mirrors a recurring move across theistic and philosophical traditions: relocating the anxious self’s center of gravity onto something that cannot be lost or reduced by comparison.",
    "cross_references": {
        "hinduism": ref("“To the seer, all things have verily become the Self: what delusion, what sorrow, can there be for him who beholds that oneness?”", "Isha Upanishad, verse 7", "isha-upanishad"),
        "christianity": ref("“Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God. And the peace of God, which passeth all understanding, shall keep your hearts and minds.”", "Philippians 4:6–7 (KJV)", "kjv"),
        "judaism": ref("“Cast thy burden upon the LORD, and he shall sustain thee: he shall never suffer the righteous to be moved.”", "Psalm 55:22 (Tanakh, Ketuvim / KJV)", "kjv"),
        "islam": ref("“Those who have believed and whose hearts are assured by the remembrance of Allah. Unquestionably, by the remembrance of Allah hearts are assured.”", "Qur'an 13:28, Ar-Ra'd", "quran-sahih"),
        "buddhism": blank("Classical Theravada Buddhism locates freedom from anxiety in insight into anatta/impermanence rather than union with an incomparable personal being; no directly parallel citation was used, to avoid misrepresenting the tradition’s own framework."),
        "greek_mythology": blank("No sufficiently precise, directly citable match found."),
        "philosophy": blank("Stoic material (Epictetus) was already used for Kural 4’s closely related theme; left open here rather than repeat the same source for a second, distinct claim."),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 8,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "அறவாழி அந்தணன் தாள்சேர்ந்தார்க் கல்லால்\nபிறவாழி நீந்தல் அரிது.",
    "transliteration": "Aravaazhi andhanan thaal serndhaark kallaal,\npiRa vaazhi neendhal aridhu.",
    "meaning": "Except for those who cling to the feet of the gracious One who is like an ocean of virtue, it is hard for anyone to swim across the other ocean — the ocean of worldly existence.",
    "explanation_simple": "Imagine two oceans: one is God’s goodness, so big it’s like an ocean; the other is all of life’s ups and downs, also huge, like an ocean you’re trying to swim across. This kural says the only way to really make it across the hard ocean is by holding onto the good one — by holding onto God.",
    "explanation_scholarly": "“Aravaazhi” (“ocean of dharma/virtue”) figures the divine not as a static point of refuge but as boundless moral reality, an ocean whose scale matches the scale of the second ocean it lets one cross — “piravaazhi,” the vast ocean of embodied/worldly existence one must traverse. The parallel construction (aravaazhi / piravaazhi — a saving “sea” against a trapping “sea”) is a deliberate rhetorical mirroring in the Tamil, reinforcing that only something of equal or greater vastness than the ocean of worldly existence — a comparable ocean of grace — can carry a being across it.",
    "cross_references": {
        "hinduism": ref("“Even if you are considered to be the most sinful of all sinners, when you are situated in the boat of transcendental knowledge, you will be able to cross over the ocean of miseries.”", "Bhagavad Gita 4.36", "gita-asitis"),
        "buddhism": ref("The Buddha’s raft parable: the Dharma is like a raft, useful “for the purpose of crossing over, not for the purpose of holding onto,” once one has reached the far shore.", "Majjhima Nikaya 22, Alagaddupama Sutta", "majjhima-nikaya-22"),
        "christianity": ref("“I am the way, the truth, and the life: no man cometh unto the Father, but by me.”", "John 14:6 (KJV)", "kjv"),
        "judaism": ref("The parting of the Sea of Reeds: “the LORD caused the sea to go back... and made the sea dry land... and the children of Israel went into the midst of the sea upon the dry ground” — a crossing made possible only by God’s direct intervention.", "Exodus 14:21–22 (Tanakh, Torah)", "kjv"),
        "islam": blank("No sufficiently precise, directly citable match found."),
        "greek_mythology": ref("Charon, ferryman of the River Styx, alone can carry souls across to the realm of the dead, and only for those who can pay his fee (Charon’s obol) — a mythic figuring of a sea/river crossable only with aid.", "Greek mythological tradition (Charon and the Styx)", "charon-myth"),
        "philosophy": blank("No sufficiently precise, directly citable match found."),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 9,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "கோளில் பொறியின் குணமிலவே எண்குணத்தான்\nதாளை வணங்காத் தலை.",
    "transliteration": "Kolil poRiyin guNam-ilavey,\neN-guNaththaan thaalai vaNangaadha thalai.",
    "meaning": "A head that will not bow to the feet of the One possessed of the eight great virtues is as useless as a sense-organ that has lost its power to sense.",
    "explanation_simple": "Imagine an eye that can’t see, or an ear that can’t hear — totally pointless, right? This kural says a person’s pride, their whole sense of self, is just as pointless if it refuses to bow down in respect to God.",
    "explanation_scholarly": "“Eṇ-guṇam” — “the eight qualities” — refers to a specific theological catalogue of divine perfections found in Tamil Saiva/Vaishnava theology (enumerations vary, but typically include self-existence, essential purity, innate intelligence, omniscience, freedom from bondage, infinite grace, omnipotence, and infinite bliss). The verse’s force lies in its analogy: a sense organ (pori) that has lost its functional capacity is not merely deficient but categorically useless — it fails at the one thing that defines it. Likewise, a head that will not bow is said to fail at the one thing Valluvar treats as most defining meaningful personhood: right relationship, through humility, to the ultimate reality. Pride as the paradigmatic failure-that-negates-one’s-purpose recurs across traditions in strikingly similar terms.",
    "cross_references": {
        "hinduism": blank("No sufficiently precise, directly citable match found for this specific image (the eight qualities) without over-reaching."),
        "christianity": ref("“God resisteth the proud, but giveth grace unto the humble.”", "James 4:6 (KJV)", "kjv"),
        "judaism": ref("“Pride goeth before destruction, and an haughty spirit before a fall.”", "Proverbs 16:18 (Tanakh, Ketuvim / KJV)", "kjv"),
        "islam": ref("Recounting Iblis’s refusal to prostrate before Adam at God’s command: “so they [the angels] prostrated, except for Iblees. He refused and was arrogant and became of the disbelievers.”", "Qur'an 2:34, Al-Baqarah", "quran-general"),
        "buddhism": blank("No sufficiently precise, directly citable match found."),
        "greek_mythology": ref("The weaver Arachne’s arrogant refusal to acknowledge the goddess Athena’s superiority leads to her transformation and ruin. (Our earliest full surviving telling is the Roman poet Ovid’s, though the figures and myth are Greek in origin.)", "Ovid, Metamorphoses, Book VI (recording the Greek myth of Arachne)", "ovid-metamorphoses"),
        "philosophy": blank("No sufficiently precise, directly citable match found."),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

kurals.append({
    "number": 10,
    "adhikaram": {"tamil": "கடவுள் வாழ்த்து", "transliteration": "Kadavul Vaazhthu", "english": "The Praise of God", "paal": "அறத்துப்பால் (Aram / Virtue)"},
    "tamil": "பிறவிப் பெருங்கடல் நீந்துவர் நீந்தார்\nஇறைவன் அடிசேரா தார்.",
    "transliteration": "PiRavi-p perungadal neendhuvar neendhaar,\niRaivan adi seraadhaar.",
    "meaning": "Only those who reach the feet of God can swim across the great ocean of repeated births; no one else can.",
    "explanation_simple": "This is the last kural in this chapter, and it repeats an important idea: life — with all its ups, downs, and being born again and again — is like a huge ocean. This kural says the only way anyone can really swim all the way across it is by holding onto God.",
    "explanation_scholarly": "This closing verse functions as a capstone, restating and intensifying kural 8’s ocean imagery but now naming the object to be crossed explicitly as “piravi” — birth/rebirth itself — invoking the doctrine of samsara common to the Indian religious milieu in which Valluvar wrote. The repetition (kurals 8 and 10 both use ocean imagery for worldly existence) is a structural device: the chapter opens by establishing God as “first” of all things (kural 1) and closes by establishing God as the only viable “crossing” out of the cycle those very origins set in motion — a ring composition tying the chapter’s cosmological opening to its soteriological close.",
    "cross_references": {
        "hinduism": ref("“This divine energy of Mine, consisting of the three modes of material nature, is difficult to overcome. But those who have surrendered unto Me can easily cross beyond it.”", "Bhagavad Gita 7.14", "gita-asitis"),
        "buddhism": ref("“Few among men are those who cross to the farther shore. The rest, the bulk of men, only run up and down the hither bank... those who act according to the perfectly taught Dhamma will cross the realm of Death, so difficult to cross.”", "Dhammapada, verses 85–86", "dhammapada-buddharakkhita"),
        "christianity": ref("“For by grace are ye saved through faith; and that not of yourselves: it is the gift of God: not of works, lest any man should boast.”", "Ephesians 2:8–9 (KJV)", "kjv"),
        "islam": ref("“And there is none of you except he will come to it [Hell]... Then We will save those who feared Allah and leave the wrongdoers within it, on their knees.”", "Qur'an 19:71–72, Maryam", "quran-general"),
        "judaism": blank("Classical Tanakh theology does not teach cyclical rebirth (gilgul is a later Kabbalistic development, not a Tanakh doctrine); no citation was forced here."),
        "greek_mythology": blank("The Charon/River Styx motif was already used for the closely related image in kural 8; repeating it here would not add a genuinely distinct citation."),
        "philosophy": ref("The philosophic soul, uniquely equipped by the pursuit of wisdom, is said to be able to choose its next life wisely and ultimately escape the compulsory wheel of rebirth and reward/punishment that entraps other souls.", "Plato, Republic, Book X (the Myth of Er)", "plato-republic"),
    },
    "sources": ["ytamizh-ch1", "thirukkuralnet-adhigaram1"],
})

with open("/sessions/lucid-blissful-fermat/mnt/outputs/thirukkural-project/data/kurals.json", "w", encoding="utf-8") as f:
    json.dump(kurals, f, ensure_ascii=False, indent=2)

with open("/sessions/lucid-blissful-fermat/mnt/outputs/thirukkural-project/data/sources.json", "w", encoding="utf-8") as f:
    json.dump(sources, f, ensure_ascii=False, indent=2)

print("Wrote", len(kurals), "kurals and", len(sources), "sources")
