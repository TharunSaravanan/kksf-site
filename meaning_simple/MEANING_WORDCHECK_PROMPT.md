# Task: word-accuracy pass on kural "meaning" lines (third pass)

First read /Users/adhigopal/Documents/Thirukkural/meaning_simple/MEANING_SIMPLE_PROMPT.md and MEANING_POLISH_PROMPT.md and keep all their rules. Do not mention or draw on the removed tradition or its texts anywhere.

Adhi's instruction for this pass: each key Tamil word must be rendered by the English word that is literally and logically correct for it, in modern spoken English (example: kalavu = "stealing", not "cheating"). Translations cannot always be word-for-word, so use judgment: keep the couplet's real meaning, make the English natural for a middle-school reader, and do not change the meaning or add ideas.

Input: input3/in_NN.json (current_meaning is the live text). For each kural, check every key Tamil word against the English used (use the Tamil, transliteration and university notes). Change a line ONLY if a word is wrong, too loose or too strong/weak for the Tamil (e.g. cheating/stealing, love/desire, wealth/riches, anger/hatred, wise/learned, loose generalisations), or a modern speaker would find it unnatural. If the line is already accurate, leave it out.
Output: output3/out_NN.json ({"<number>": text}, changed kurals only) and output3/log_NN.json ({number: "Tamil word: old English -> new English, why"}). Validate JSON by re-opening. Reply with counts and any kurals where the Tamil can be read two ways (number + why).
