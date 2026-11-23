# Task: second-pass polish of kural "meaning" lines (middle-school reading level)

First read /Users/adhigopal/Documents/Thirukkural/meaning_simple/MEANING_SIMPLE_PROMPT.md and follow ALL its rules (faithfulness, everyday words, short sentences, explain any needed hard term in plain words, no religion unless the couplet has it). Do not mention or draw on the removed tradition or its texts anywhere.

Adhi's requirement: every meaning must be understood by an intermediate (middle) school student. No advanced vocabulary; if a fancy word can be explained in simpler terms, always do that.

Input: an input2/in_NN.json file with `current_meaning` already rewritten once. For EACH kural, judge the current_meaning:
- If it is already clear, natural, faithful, and uses only everyday words, keep it EXACTLY as is.
- Otherwise rewrite it. Fix: bookish/rare words (e.g. recognised, revenue-stream, celestials, righteousness, perish, wealth, covet, lofty, ruin when "destroy/hurt" is clearer), awkward or unnatural phrasing, riddle-like or confusing sentences, stacked clauses, and anything that misstates the Tamil (check the Tamil/transliteration/university text; fix any inaccuracy). Keep one idea order as the couplet.
- Every meaning must read smoothly aloud, 1-2 sentences, ideally 15-35 words.
Output: write /Users/adhigopal/Documents/Thirukkural/meaning_simple/output2/out_NN.json as {"<number>": text} containing ONLY the kurals you changed (unchanged ones omitted), plus a sibling output2/log_NN.json listing {number: short reason}. Write with python json.dump(ensure_ascii=False, indent=1) and re-open to validate. Reply with: kurals reviewed, kurals changed, and any you are unsure are faithful (number + why).
