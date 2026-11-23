# Task: rewrite the "meaning" of each kural at a middle-school reading level

Adhi (the project owner) found that the current "meaning" line is often too hard to read; he has to read the "elementary" version to understand it. The new meaning must sit BETWEEN the elementary version and the high-school level: think grades 6-8 (ages 11-14).

You are given an input file of kurals (number, Tamil text, transliteration, current_meaning, elementary_explanation, university_explanation). For EACH kural write ONE new "meaning".

## Rules
1. FAITHFUL FIRST. The new meaning must say what Valluvar's couplet says, in the same order of ideas, and must stay true to the Tamil. Use the Tamil, the transliteration, the current meaning and the university explanation (which discusses word choices and commentators) to get it right. Do not add ideas that are not in the couplet, do not drop any of its ideas, and do not soften or reverse it. If the current meaning contains a deliberate choice that reflects the Tamil (a metaphor, a comparison, a list of items), keep it.
2. EVERYDAY WORDS. Use words a 12-year-old uses or has met in school. No poetic, old-fashioned or bookish words (e.g. avoid: doting, refuge, cling, tempted, toil, forsake, foe, wealth-getting, indulgence, perish, grace, virtuous, endeavour, wrath, bestow, adversity, humble-oneself). Prefer: help, hard, hurt, rich, anger, enemy, give, trouble, good, kind.
3. If a harder word or a term from Tamil/Indian culture really is needed to keep the meaning (e.g. amrita, karma, dharma, the "ocean of births"), keep it but explain it in plain English right there, in a few words (e.g. "amrita (the drink that makes gods live forever)"). Never leave a hard word unexplained.
4. SHORT, CLEAR SENTENCES. 1-2 sentences, usually 15-35 words, at most 40. Active voice, direct. No stacked clauses, no semicolons or long dashes inside a sentence. Write so it reads smoothly aloud.
5. Do NOT copy the elementary version's style: no "Imagine...", no made-up stories, no examples about puppies, teams or pools. The meaning is a plain, direct statement of what the kural says (the elementary text does the storytelling). Do not start with "This kural says".
6. Keep the voice of the couplet (advice, observation, or a lover speaking). For the love chapters (Inbam) keep the speaker clear (a wife, a husband, a friend) in simple words and keep it gentle and tasteful.
7. Gender: use "a person", "people", "they", "you", or "someone" unless the Tamil is clearly about a man or a woman (e.g. a wife, a king).
8. Do not mention any religion or tradition unless the couplet itself does. Do not mention or draw on the removed tradition or its texts anywhere. No citations, no commentary, no opinions.
9. Self-check each line: Could a 6th grader understand it on first read with no dictionary? Is every idea from the couplet there, and nothing extra? If not, rewrite.

## Output
Write a JSON file to the path you are told, an object mapping the kural number (as a string) to the new meaning string, e.g. {"1": "...", "2": "..."}. Include EVERY kural in your input file, and nothing else. Use plain straight quotes inside text only if escaped; use curly apostrophes/quotes sparingly. Write the file with a short python script using json.dump(..., ensure_ascii=False, indent=1) so the JSON is valid, then re-open it and confirm the count matches the input. Reply with just the count and any kurals where you are unsure the meaning is exactly right (give the number and why).
