const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, PageBreak,
  AlignmentType, BorderStyle, Table, TableRow, TableCell, WidthType,
  ShadingType, Header, Footer, PageNumber, TabStopType, TabStopPosition,
  Bookmark, InternalHyperlink, LeaderType
} = require("docx");

const kurals = JSON.parse(fs.readFileSync(__dirname + "/thirukkural-project/data/kurals.json", "utf-8"));
const sources = JSON.parse(fs.readFileSync(__dirname + "/thirukkural-project/data/sources.json", "utf-8"));
// Jainism / Sikhism / Real Life Example appear only once build_data2.py has published them for every kural.
const JAIN_ON = kurals.length > 0 && kurals.every(k => "jainism" in k.cross_references);
const SIKH_ON = kurals.length > 0 && kurals.every(k => "sikhism" in k.cross_references);
const HIST_ON = kurals.length > 0 && kurals.every(k => "real_life_example" in k);
const TRAD_ORDER = ["hinduism", "christianity", "islam", "judaism", "buddhism", "jainism", "sikhism", "greek_mythology", "philosophy"]
  .filter(t => (JAIN_ON || t !== "jainism") && (SIKH_ON || t !== "sikhism"));
const SCRIP = ["Hindu", "Christian", "Islamic", "Jewish", "Buddhist"].concat(JAIN_ON ? ["Jain"] : []).concat(SIKH_ON ? ["Sikh"] : []);
const SCRIPTURE_LIST = SCRIP.slice(0, -1).join(", ") + ", and " + SCRIP[SCRIP.length - 1] + " scripture";

const TRAD_LABELS = {
  hinduism: "Hinduism",
  christianity: "Christianity",
  islam: "Islam",
  judaism: "Judaism",
  buddhism: "Buddhism",
  jainism: "Jainism",
  sikhism: "Sikhism",
  greek_mythology: "Greek Mythology",
  philosophy: "Philosophy",
};

function heading(text, size, opts = {}) {
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
    children: [new TextRun({ text, bold: true, size, color: opts.color || "1F1F1F" })],
  });
}

const TAMIL_RE = /[஀-௿]+/;

function mixedRuns(text, opts = {}) {
  // Tamil -> Noto Sans Tamil; the Arabic honorific ligature (U+FDFA) -> Noto Naskh Arabic
  const parts = text.split(/([\u0B80-\u0BFF]+|\uFDFA)/g).filter(p => p.length);
  return parts.map(p => new TextRun({
    text: p,
    italics: !!opts.italics,
    bold: !!opts.bold,
    size: opts.size || 22,
    color: opts.color,
    font: /[\u0B80-\u0BFF]/.test(p) ? "Noto Sans Tamil" : (p === "\uFDFA" ? "Noto Naskh Arabic" : undefined),
  }));
}

function body(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 160, line: 300 },
    children: mixedRuns(text, opts),
  });
}

function label(text) {
  return new Paragraph({
    spacing: { before: 200, after: 60 },
    children: [new TextRun({ text, bold: true, size: 20, color: "8A4B00" })],
  });
}

function stripQuotes(s) {
  return s.replace(/^[“"]+/, "").replace(/[”"]+$/, "");
}

function crossRefRow(tradition, ref, citeIndex) {
  const rows = [];
  rows.push(new Paragraph({
    spacing: { before: 160, after: 60 },
    children: [new TextRun({ text: TRAD_LABELS[tradition], bold: true, size: 22, color: "8A4B00" })],
  }));
  if (!ref.quote_or_event) {
    rows.push(new Paragraph({
      spacing: { after: 160 },
      children: [new TextRun({ text: "We haven't found a correspondence here that's accurate enough to include yet. Want to suggest a change? Leave us a message and we'll review it.", italics: true, size: 20, color: "8A7860" })],
    }));
    return rows;
  }
  // Only wrap in quotation marks when the text is a verbatim quote of the source;
  // paraphrased event/teaching descriptions are rendered plainly, without quote marks.
  const quoteText = ref.is_quote ? "“" + stripQuotes(ref.quote_or_event) + "”" : stripQuotes(ref.quote_or_event);
  rows.push(new Paragraph({
    spacing: { after: 40 },
    children: mixedRuns(quoteText, { italics: !!ref.is_quote, size: 20 }),
  }));
  const idx = citeIndex[ref.citation_id];
  const citeText = idx ? `— ${ref.source}  [${idx}]` : `— ${ref.source}`;
  rows.push(new Paragraph({
    spacing: { after: 40 },
    children: [new TextRun({ text: citeText, size: 18, color: "555555" })],
  }));
  rows.push(new Paragraph({
    spacing: { after: 40 },
    children: mixedRuns(ref.explanation, { size: 20 }),
  }));
  rows.push(new Paragraph({
    spacing: { after: 160 },
    children: mixedRuns(ref.tie_back, { size: 20, italics: true, color: "444444" }),
  }));
  return rows;
}

function sourcesBlock(citeOrder, citeIndex) {
  const rows = [];
  rows.push(new Paragraph({
    spacing: { before: 200, after: 60 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: "E8E0D2", space: 4 } },
    children: [new TextRun({ text: "SOURCES FOR THIS PAGE", bold: true, size: 16, color: "8A4B00" })],
  }));
  citeOrder.forEach(id => {
    const s = sources[id] || {};
    const label = s.title || id;
    const author = s.author ? ` (${s.author})` : "";
    const tier = s.tier ? `  [${s.tier} source]` : "";
    rows.push(new Paragraph({
      spacing: { after: 30 },
      indent: { left: 200, hanging: 200 },
      children: [new TextRun({ text: `${citeIndex[id]}. ${label}${author}${tier}`, size: 16, color: "666666" })],
    }));
  });
  return rows;
}

const children = [];

// Title page
const TAMIL_FONT = "Noto Sans Tamil";

children.push(
  new Paragraph({ spacing: { before: 2000 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "திருக்குறள்", bold: true, size: 64, font: TAMIL_FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
    children: [new TextRun({ text: "THE THIRUKKURAL", bold: true, size: 40 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: "A Cross-Traditional Study Edition", size: 26, italics: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 2000 },
    children: [new TextRun({ text: "Tamil text · transliteration · meaning · commentary\nwith verified correspondences in Hindu, Christian, Islamic, Jewish,\n" + "Buddhist, " + (JAIN_ON ? "Jain, " : "") + (SIKH_ON ? "Sikh, " : "") + "Greek, and philosophical sources" + (HIST_ON ? ",\nplus a documented real-life example from history for every kural" : ""), size: 20 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "1,330 kurals · 133 chapters · three books: Aram, Porul, Inbam", size: 18, color: "666666" })] }),
  new Paragraph({ children: [new PageBreak()] })
);

// ---- Front matter: About This Guide ----
function frontHeading(text) {
  return new Paragraph({ spacing: { before: 100, after: 200 },
    children: [new TextRun({ text, bold: true, size: 32, color: "8A4B00" })] });
}
function frontBody(text) {
  return new Paragraph({ spacing: { after: 200, line: 300 },
    children: [new TextRun({ text, size: 22 })] });
}
function frontSubhead(text) {
  return new Paragraph({ spacing: { before: 240, after: 100 },
    children: [new TextRun({ text, bold: true, size: 24, color: "8A4B00" })] });
}


// ---- Contents (clickable; page numbers come from book/toc_pages.json when present) ----
let TOC_PAGES = {};
try { TOC_PAGES = JSON.parse(fs.readFileSync(__dirname + "/thirukkural-project/book/toc_pages.json", "utf-8")); } catch (e) {}
const BOOKS = [
  { en: "Book I \u00b7 Aram \u2014 Virtue", ta: "அறத்துப்பால்", from: 1, to: 38 },
  { en: "Book II \u00b7 Porul \u2014 Wealth and Statecraft", ta: "பொருட்பால்", from: 39, to: 108 },
  { en: "Book III \u00b7 Inbam \u2014 Love", ta: "காமத்துப்பால்", from: 109, to: 133 },
];
children.push(frontHeading("Contents"));
BOOKS.forEach(b => {
  children.push(new Paragraph({ spacing: { before: 160, after: 60 }, keepNext: true,
    children: [new TextRun({ text: b.en + "  \u00b7  ", bold: true, size: 22, color: "8A4B00" }),
               new TextRun({ text: b.ta, bold: true, size: 22, color: "8A4B00", font: TAMIL_FONT })] }));
  for (let c = b.from; c <= b.to; c++) {
    const first = kurals[(c - 1) * 10];
    const a = first.adhikaram;
    const pg = TOC_PAGES[String(c)] ? String(TOC_PAGES[String(c)]) : "";
    children.push(new Paragraph({
      spacing: { after: 20 },
      tabStops: [{ type: TabStopType.RIGHT, position: 9360, leader: LeaderType.DOT }],
      children: [new InternalHyperlink({ anchor: "ch" + c, children: [
        new TextRun({ text: `${c}.  ${a.english} \u00b7 `, size: 19, color: "1F3A68" }),
        new TextRun({ text: a.tamil, size: 19, color: "1F3A68", font: TAMIL_FONT }),
        new TextRun({ text: `   (kurals ${(c - 1) * 10 + 1}\u2013${c * 10})`, size: 17, color: "666666" }),
        new TextRun({ text: "\t" + pg, size: 19, color: "1F3A68" }),
      ] })],
    }));
  }
});
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(
  frontHeading("About This Guide"),
  frontBody("The Thirukkural (திருக்குறள்) is a work of 1,330 short couplets on ethics, worldly life, and love, traditionally attributed to the Tamil poet Thiruvalluvar. It is one of the most translated and most quoted works in the Tamil language, read by people of many faiths and by secular readers alike, because it was written to hold up across belief systems rather than argue for any one of them."),
  frontBody("This guide is an attempt to build a single, trustworthy, all-in-one resource for it: the Tamil text as Valluvar wrote it, a careful translation, an explanation simple enough for a child, a deeper explanation for a university-level reader, and — because a two-thousand-year-old ethical text tends to rhyme with ideas everywhere else in the world — a look at how the same idea shows up in " + SCRIPTURE_LIST + ", in Greek mythology, and in philosophy." + (HIST_ON ? " Each kural also closes with a Real Life Example: a well-documented event from world history, of the kind taught in schools and confirmed by multiple reference sources, that shows the kural\u2019s idea playing out in practice." : "")),
  frontBody("Every quote from a religious or historical text in this book has been individually checked against a primary source before being included. Where a genuinely close match exists across traditions, it is used; where only a looser, next-best parallel could be found, it is included but framed honestly as a looser fit rather than dressed up as an exact one. Paraphrased descriptions of events or teachings are presented as paraphrase, not as direct quotation. A private internal record tracks a confidence assessment and rationale for every citation, which drives the editorial standard behind what appears on these pages."),
  new Paragraph({ children: [new PageBreak()] })
);

// ---- Front matter: History of the Thirukkural ----
children.push(
  frontHeading("History of the Thirukkural"),
  frontSubhead("Who was Thiruvalluvar?"),
  frontBody("Very little about Thiruvalluvar's life can actually be verified. Even basic details, such as where he lived, what work he did, what faith he followed, and when he lived, are debated by historians, and different traditions and scholars say different things. Because the evidence is so thin, this book does not pick a side. What we can say is that the Thirukkural itself never argues for one religion, and that people of many backgrounds have claimed it as their own. Popular stories about his life, including the one about his wife Vasuki and the handful of sand she turned into rice, are loved legends passed down over centuries. They are not documented history."),
  frontSubhead("When was it written?"),
  frontBody("Dating the Thirukkural is a genuinely open scholarly question. Tamil Nadu's government officially adopted 31 BCE as Valluvar's year of birth in January 1935, and built a calendar system — the Valluvar Year, currently 31 years ahead of the Gregorian calendar — around that date. Scholars working from the text's internal linguistic and cultural evidence tend to land elsewhere: Kamil Zvelebil considered dates earlier than 1 BCE unsupported by the text itself, a commonly cited scholarly window is roughly 200 BCE–200 CE, and Stuart Blackburn has described the present scholarly consensus as centering closer to 500 CE. The traditional/official date and the range favored by textual scholars do not agree, and neither is settled beyond dispute."),
  frontSubhead("How the text is organized"),
  frontBody("The Thirukkural's 1,330 couplets are grouped into 133 chapters (adhikarams) of exactly 10 couplets each, organized into three books: Aram (virtue, chapters 1–38), Porul (wealth, statecraft, and worldly life, chapters 39–108), and Inbam (love, chapters 109–133). Each kural is written in a tight, fixed couplet form — traditionally seven metrical feet in total, four in the first line and three in the second."),
  frontSubhead("The commentary tradition"),
  frontBody("Ten medieval commentators are traditionally credited with authoritative commentaries on the Kural; five survive: Manakkudavar, Pari Perumal, Kaalingar, Paridhi, and Parimelalhagar. Parimelalhagar, writing around the 13th century CE, is generally regarded as having produced the finest of these commentaries, and his reading remains the most influential traditional interpretation used today."),
  frontSubhead("Reaching the rest of the world"),
  frontBody("The Thirukkural's best-known bridge into English came in 1886, when the missionary-scholar G.U. Pope published The Sacred Kurral of Tiruvalluva Nayanar in London. Since then the text has been rendered into roughly 30 English versions on its own, and into more than 100 versions across around 30 languages worldwide."),
  frontSubhead("A living text in Tamil Nadu"),
  frontBody("The Thirukkural remains a genuinely public, civic text in Tamil Nadu. Thiruvalluvar Day is an official state holiday, observed as part of the Pongal harvest festival in mid-January. At Kanyakumari, a 133-foot statue of Thiruvalluvar — dedicated on January 1, 2000 — encodes the text's own structure into its architecture: the statue and pedestal together stand 133 feet tall for the text's 133 chapters, with the 95-foot figure resting on a 38-foot pedestal representing the 38 chapters of the Aram (Virtue) book alone."),
  new Paragraph({ spacing: { before: 300 },
    children: [new TextRun({ text: "Sources: Wikipedia (Thiruvalluvar; Vasuki (wife of Valluvar); Valluvar year; Dating the Tirukkural; Aram (Kural book); Parimelalhagar; Tirukkural translations into English; Thiruvalluvar Statue); Encyclopædia Britannica (Tiruvalluvar).", size: 16, italics: true, color: "999999" })] }),
  new Paragraph({ children: [new PageBreak()] })
);

kurals.forEach((k, idx) => {
  children.push(
    new Paragraph({
      spacing: { before: 120, after: 120 }, alignment: AlignmentType.CENTER, keepNext: true,
      children: [ ...(k.number % 10 === 1 ? [new Bookmark({ id: "ch" + Math.ceil(k.number / 10), children: [new TextRun({ text: "" })] })] : []),
        new Bookmark({ id: "kural" + k.number, children: [new TextRun({ text: `Kural ${k.number}`, bold: true, size: 32, color: "8A4B00" })] }) ],
    }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
      children: [
        new TextRun({ text: `${k.adhikaram.english}  ·  ${k.adhikaram.transliteration}  ·  `, size: 20, italics: true, color: "555555" }),
        new TextRun({ text: k.adhikaram.tamil, size: 20, italics: true, color: "555555", font: TAMIL_FONT }),
      ] }),
  );

  // Tamil text block
  k.tamil.split("\n").forEach(line => {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: line, size: 32, bold: true, font: TAMIL_FONT })] }));
  });

  // Transliteration
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 100, after: 300 },
    children: k.transliteration.split("\n").flatMap((line, i, arr) => {
      const runs = [new TextRun({ text: line, italics: true, size: 22, color: "444444" })];
      if (i < arr.length - 1) runs.push(new TextRun({ break: 1 }));
      return runs;
    }) }));

  children.push(label("MEANING"));
  children.push(body(k.meaning));

  children.push(label("ELEMENTARY"));
  children.push(body(k.elementary));

  children.push(label("UNIVERSITY"));
  children.push(body(k.university));

  children.push(label("THROUGH THE LENS OF"));
  const tradOrder = TRAD_ORDER;

  // Page-local numbered citation index: base Tamil-text sources first, then every
  // source actually used across the cross-references, in reading order.
  const citeIndex = {};
  const citeOrder = [];
  (k.sources || []).forEach(s => {
    if (!(s in citeIndex)) { citeIndex[s] = citeOrder.length + 1; citeOrder.push(s); }
  });
  tradOrder.forEach(t => {
    const cid = k.cross_references[t].citation_id;
    if (cid && k.cross_references[t].quote_or_event && !(cid in citeIndex)) {
      citeIndex[cid] = citeOrder.length + 1;
      citeOrder.push(cid);
    }
  });

  const rle = HIST_ON ? k.real_life_example : null;
  if (rle) rle.citation_ids.forEach(cid => {
    if (!(cid in citeIndex)) { citeIndex[cid] = citeOrder.length + 1; citeOrder.push(cid); }
  });
  tradOrder.forEach(t => {
    children.push(...crossRefRow(t, k.cross_references[t], citeIndex));
  });
  if (rle) {
    children.push(label("REAL LIFE EXAMPLE"));
    children.push(new Paragraph({ spacing: { before: 120, after: 20 },
      children: [new TextRun({ text: rle.event_title, bold: true, size: 22, color: "8A4B00" })] }));
    children.push(new Paragraph({ spacing: { after: 60 },
      children: [new TextRun({ text: [rle.date, rle.place].filter(Boolean).join(" · "), italics: true, size: 18, color: "666666" })] }));
    children.push(new Paragraph({ spacing: { after: 40 }, children: mixedRuns(rle.event, { size: 20 }) }));
    children.push(new Paragraph({ spacing: { after: 40 },
      children: [new TextRun({ text: "— Sources: " + rle.citation_ids.map(c => `[${citeIndex[c]}]`).join(" "), size: 18, color: "555555" })] }));
    children.push(new Paragraph({ spacing: { after: 40 }, children: mixedRuns(rle.explanation, { size: 20 }) }));
    children.push(new Paragraph({ spacing: { after: 160 }, children: mixedRuns(rle.tie_back, { size: 20, italics: true, color: "444444" }) }));
  }
  children.push(...sourcesBlock(citeOrder, citeIndex));

  if (idx < kurals.length - 1) {
    children.push(new Paragraph({ children: [new PageBreak()] }));
  }
});

const doc = new Document({
  title: "The Thirukkural \u2014 A Cross-Traditional Study Edition",
  creator: "Thirukkural Translation Project",
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 }, // US Letter
        margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
      },
    },
    headers: {
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "The Thirukkural — A Cross-Traditional Study Edition", size: 16, color: "999999" })] })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(__dirname + "/thirukkural-project/book/thirukkural_book.docx", buf);
  console.log("Wrote book docx");
});
