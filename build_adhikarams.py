# -*- coding: utf-8 -*-
# Canonical, verified list of all 133 adhikarams (chapters) of the Thirukkural,
# sourced from the "Aram (Kural book)", "Porul (Kural book)", and "Inbam (Kural
# book)" articles on English Wikipedia (each chapter's Tamil name, transliteration,
# English name and couplet range cross-checked against those pages on 2026-09-21).
# This is fixed, canonical structural metadata for the whole text and does not
# change as more kurals are translated in future batches.
import json

import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thirukkural-project")

PAAL = {
    "aram": {"tamil": "அறத்துப்பால்", "english": "Aram (Virtue)", "range": (1, 38)},
    "porul": {"tamil": "பொருட்பால்", "english": "Porul (Wealth & Polity)", "range": (39, 108)},
    "inbam": {"tamil": "காமத்துப்பால்", "english": "Inbam (Love)", "range": (109, 133)},
}

# (number, tamil, transliteration, english)
CHAPTERS = [
    (1, "கடவுள் வாழ்த்து", "Kadavul Vaazhthu", "The Praise of God"),
    (2, "வான் சிறப்பு", "Vaan Sirappu", "The Excellence of Rain"),
    (3, "நீத்தார் பெருமை", "Neethaar Perumai", "The Greatness of Ascetics"),
    (4, "அறன் வலியுறுத்தல்", "Aran Valiyuruthal", "Assertion of the Strength of Virtue"),
    (5, "இல்வாழ்க்கை", "Ilvaazhkkai", "Domestic Life"),
    (6, "வாழ்க்கைத்துணை நலம்", "Vaazhkkaithunai Nalam", "The Worth of a Wife"),
    (7, "புதல்வரைப் பெறுதல்", "Pudhalvaraip Perudhal", "The Wealth of Children"),
    (8, "அன்புடைமை", "Anbudaimai", "The Possession of Love"),
    (9, "விருந்தோம்பல்", "Virundhombal", "Cherishing Guests"),
    (10, "இனியவை கூறல்", "Iniyavai Kooral", "Charming Utterance"),
    (11, "செய்ந்நன்றி அறிதல்", "Seynnanri Arithal", "Gratitude Recognition"),
    (12, "நடுவு நிலைமை", "Naduvu Nilaimai", "Impartiality"),
    (13, "அடக்கமுடைமை", "Adakkamudaimai", "The Possession of Self-restraint"),
    (14, "ஒழுக்கமுடைமை", "Ozhukkamudaimai", "The Possession of Decorum"),
    (15, "பிறனில் விழையாமை", "Piranil Vizhaiyaamai", "Not Coveting Another's Wife"),
    (16, "பொறையுடைமை", "Poraiyudaimai", "The Possession of Patience"),
    (17, "அழுக்காறாமை", "Azhukkaaraamai", "Anti-envy"),
    (18, "வெஃகாமை", "Vehkaamai", "Anti-covet Action"),
    (19, "புறங்கூறாமை", "Purangkooraamai", "Slander Avoidance"),
    (20, "பயனில சொல்லாமை", "Payanila Sollaamai", "Not Speaking Profitless Words"),
    (21, "தீவினையச்சம்", "Theevinaiyaccham", "Dread of Evil Deeds"),
    (22, "ஒப்புரவறிதல்", "Oppuravarithal", "Knowledge of What Is Befitting"),
    (23, "ஈகை", "Eekai", "Philanthropy"),
    (24, "புகழ்", "Pukazh", "Renown"),
    (25, "அருளுடைமை", "Arulodamai", "Benevolence"),
    (26, "புலான் மறுத்தல்", "Pulaan Maruthal", "Flesh Renunciation"),
    (27, "தவம்", "Thavam", "Penance"),
    (28, "கூடாவொழுக்கம்", "Koodaavozhukkam", "Inconsistent Conduct"),
    (29, "கள்ளாமை", "Kallaamai", "The Absence of Fraud"),
    (30, "வாய்மை", "Vaaymai", "Veracity"),
    (31, "வெகுளாமை", "Vekulaamai", "The Not Being Angry"),
    (32, "இன்னா செய்யாமை", "Innaa Seyyaamai", "Not Doing Evil"),
    (33, "கொல்லாமை", "Kollaamai", "Not Killing"),
    (34, "நிலையாமை", "Nilaiyaamai", "Impermanence"),
    (35, "துறவு", "Thuravu", "Renunciation"),
    (36, "மெய்யுணர்தல்", "Meyyunarthal", "Knowledge of the True"),
    (37, "அவாவறுத்தல்", "Avaavaruthal", "The Extirpation of Desire"),
    (38, "ஊழ்", "Uzhi", "Fate"),
    (39, "இறைமாட்சி", "Iraimaatchi", "The Greatness of a King"),
    (40, "கல்வி", "Kalvi", "Learning"),
    (41, "கல்லாமை", "Kallaamai", "Ignorance"),
    (42, "கேள்வி", "Kelvi", "Hearing"),
    (43, "அறிவுடைமை", "Arivudaimai", "Knowledge Possession"),
    (44, "குற்றங்கடிதல்", "Kutrankaditthal", "Error Correction"),
    (45, "பெரியாரைத் துணைக்கோடல்", "Periyaaraith Thunaikkodal", "Seeking the Aid of Great Men"),
    (46, "சிற்றினஞ்சேராமை", "Sitrinanjeraamai", "Avoiding Mean Associations"),
    (47, "தெரிந்து செயல்வகை", "Therindhu Seyalvakai", "Acting after Due Consideration"),
    (48, "வலியறிதல்", "Valiyarithal", "The Knowledge of Power"),
    (49, "காலமறிதல்", "Kaalamarithal", "Knowledge of Apt Timing"),
    (50, "இடனறிதல்", "Idanarithal", "Knowledge of Location"),
    (51, "தெரிந்து தெளிதல்", "Therindhu Thelithal", "Selection and Confidence"),
    (52, "தெரிந்து வினையாடல்", "Therindhu Vinaiyaadal", "Selection and Employment"),
    (53, "சுற்றந்தழால்", "Suttrandhazhaal", "Cherishing One's Kindred"),
    (54, "பொச்சாவாமை", "Pocchaavaamai", "Unforgetfulness"),
    (55, "செங்கோன்மை", "Sengonmai", "The Right Sceptre"),
    (56, "கொடுங்கோன்மை", "Kodungonmai", "The Cruel Sceptre"),
    (57, "வெருவந்த செய்யாமை", "Veruvandha Seyyaamai", "Absence of Terrorism"),
    (58, "கண்ணோட்டம்", "Kannottam", "Benignity"),
    (59, "ஒற்றாடல்", "Otraadal", "Detectives"),
    (60, "ஊக்கமுடைமை", "Ookkamudaimai", "Energetics"),
    (61, "மடியின்மை", "Madiyinmai", "Unsluggishness"),
    (62, "ஆள்வினையுடைமை", "Aalvinaiyudaimai", "Manly Effort"),
    (63, "இடுக்கண் அழியாமை", "Idukkan Azhiyaamai", "Hopefulness in Trouble"),
    (64, "அமைச்சு", "Amaichu", "Ministry of State"),
    (65, "சொல்வன்மை", "Solvanmai", "Oratory"),
    (66, "வினைத்தூய்மை", "Vinaithooymai", "Purity in Execution"),
    (67, "வினைத்திட்பம்", "Vinaithitpam", "Power in Execution"),
    (68, "வினை செயல்வகை", "Vinai Seyalvakai", "The Method of Execution"),
    (69, "தூது", "Thoodhu", "The Envoy"),
    (70, "மன்னரைச் சேர்ந்தொழுதல்", "Mannaraich Serndhozhuthal", "Conduct in the Presence of the King"),
    (71, "குறிப்பறிதல்", "Kurippu Arithal", "The Knowledge of Signals"),
    (72, "அவையறிதல்", "Avaiyarithal", "The Knowledge of the Council Chamber"),
    (73, "அவையஞ்சாமை", "Avaiyanjaamai", "Dread Avoidance"),
    (74, "நாடு", "Naadu", "The Land"),
    (75, "அரண்", "Aran", "The Fortification"),
    (76, "பொருள் செயல்வகை", "Porul Seyalvakai", "Wealth Accumulation"),
    (77, "படைமாட்சி", "Padaimaatchi", "The Excellence of an Army"),
    (78, "படைச்செருக்கு", "Padaiccherukku", "Military Spirit"),
    (79, "நட்பு", "Natpu", "Friendship"),
    (80, "நட்பாராய்தல்", "Natpaaraaythal", "Investigation in Forming Friendships"),
    (81, "பழைமை", "Pazhaimai", "Familiarity"),
    (82, "தீ நட்பு", "Thee Natpu", "Evil Friendship"),
    (83, "கூடா நட்பு", "Koodaa Natpu", "Unreal Friendship"),
    (84, "பேதைமை", "Pedhaimai", "Folly"),
    (85, "புல்லறிவாண்மை", "Pullarivaanmai", "Ignorance of Fools"),
    (86, "இகல்", "Ikal", "Hostility"),
    (87, "பகை மாட்சி", "Pakai Maatchi", "The Might of Hatred"),
    (88, "பகைத்திறந்தெரிதல்", "Pakaithirandherithal", "Recognizing the Quality of Enmity"),
    (89, "உட்பகை", "Utpakai", "Internal Enmity"),
    (90, "பெரியாரைப் பிழையாமை", "Periyaaraip Pizhaiyaamai", "Not Offending the Great"),
    (91, "பெண்வழிச் சேறல்", "Penvazhich Seral", "Being Led by Women"),
    (92, "வரைவின் மகளிர்", "Varaivin Makalir", "Wanton Women"),
    (93, "கள்ளுண்ணாமை", "Kalunnaamai", "Abstinence from Liquor"),
    (94, "சூது", "Soodhu", "Gaming (Gambling)"),
    (95, "மருந்து", "Marundhu", "Medicine"),
    (96, "குடிமை", "Kudimai", "Lineage"),
    (97, "மானம்", "Maanam", "Honour"),
    (98, "பெருமை", "Perumai", "Greatness"),
    (99, "சான்றாண்மை", "Saandraanmai", "Perfectness"),
    (100, "பண்புடைமை", "Panpudaimai", "Courtesy"),
    (101, "நன்றியில் செல்வம்", "Nandriyil Selvam", "Wealth without Benefaction"),
    (102, "நாணுடைமை", "Naanudaimai", "Shame"),
    (103, "குடிசெயல்வகை", "Kudiseyalvakai", "Family Maintenance"),
    (104, "உழவு", "Uzhavu", "Agriculture"),
    (105, "நல்குரவு", "Nalkuravu", "Poverty"),
    (106, "இரவு", "Iravu", "Mendicancy"),
    (107, "இரவச்சம்", "Iravaccham", "The Dread of Mendicancy"),
    (108, "கயமை", "Kayamai", "Baseness"),
    (109, "தகையணங்குறுத்தல்", "Thagaiyanankuruthal", "Mental Disturbance Caused by Her Beauty"),
    (110, "குறிப்பறிதல்", "Kurippu Arithal", "Recognition of the Signs (of Mutual Love)"),
    (111, "புணர்ச்சி மகிழ்தல்", "Punarchi Makizhthal", "Delight in Union"),
    (112, "நலம் புனைந்துரைத்தல்", "Nalam Punaindhuraithal", "The Praise of Her Beauty"),
    (113, "காதற் சிறப்புரைத்தல்", "Kaadhar Sirappuraithal", "Declaration of Love's Special Excellence"),
    (114, "நாணுத் துறவுரைத்தல்", "Naanuth Thuravuraithal", "The Abandonment of Reserve"),
    (115, "அலரறிவுறுத்தல்", "Alararivuruthal", "The Announcement of the Rumour"),
    (116, "பிரிவாற்றாமை", "Pirivaatraamai", "Unendurable Separation"),
    (117, "படர் மெலிந்திரங்கல்", "Padar Melindhirankal", "Complaint"),
    (118, "கண்விதுப்பழிதல்", "Kanvithuppazhithal", "Eyes Consumed with Grief"),
    (119, "பசப்பறு பருவரல்", "Pasapparu Paruvaral", "The Pallid Hue"),
    (120, "தனிப்படர் மிகுதி", "Thanippadar Mikudhi", "The Solitary Anguish"),
    (121, "நினைந்தவர் புலம்பல்", "Ninaindhavar Pulampal", "Sad Memories"),
    (122, "கனவுநிலையுரைத்தல்", "Kanavunilaiyuraithal", "The Visions of the Night"),
    (123, "பொழுதுகண்டிரங்கல்", "Pozhudhukandirankal", "Lamentations at Even-tide"),
    (124, "உறுப்பு நலனழிதல்", "Uruppu Nalanazhithal", "Wasting Away"),
    (125, "நெஞ்சொடு கிளத்தல்", "Nenjodu Kilathal", "Soliloquy"),
    (126, "நிறையழிதல்", "Niraiyazhithal", "Reserve Overcome"),
    (127, "அவர்வயின் விதும்பல்", "Avarvayin Vidhumpal", "Mutual Desire"),
    (128, "குறிப்பறிவுறுத்தல்", "Kuripparivuruthal", "The Reading of the Signs"),
    (129, "புணர்ச்சி விதும்பல்", "Punarchi Vidhumpal", "Desire for Reunion"),
    (130, "நெஞ்சொடு புலத்தல்", "Nenjodu Pulathal", "Expostulation with Oneself"),
    (131, "புலவி", "Pulavi", "Pouting"),
    (132, "புலவி நுணுக்கம்", "Pulavi Nunukkam", "Feigned Anger"),
    (133, "ஊடலுவகை", "Oodaluvakai", "The Pleasures of 'Temporary Variance'"),
]

assert len(CHAPTERS) == 133, f"expected 133 chapters, got {len(CHAPTERS)}"

def paal_for(n):
    for key, meta in PAAL.items():
        lo, hi = meta["range"]
        if lo <= n <= hi:
            return key
    raise ValueError(n)

adhikarams = []
for number, tamil, translit, english in CHAPTERS:
    paal_key = paal_for(number)
    adhikarams.append({
        "number": number,
        "tamil": tamil,
        "transliteration": translit,
        "english": english,
        "paal": paal_key,
        "paal_tamil": PAAL[paal_key]["tamil"],
        "paal_english": PAAL[paal_key]["english"],
        "kural_start": (number - 1) * 10 + 1,
        "kural_end": number * 10,
    })

with open(f"{BASE}/data/adhikarams.json", "w", encoding="utf-8") as f:
    json.dump(adhikarams, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(adhikarams)} adhikarams "
      f"(Aram 1-38, Porul 39-108, Inbam 109-133) to data/adhikarams.json")
