---
type: llm
---

Judge only the copy itself, not any headings, labels or explanation around it.

PASS if the reply gives all three pieces, and:
- the empty state is 15 words or fewer and says what will show up there or how to add the first item
- the upload error is 20 words or fewer, says the file is over 25 MB, and says what to do about it
- the Share tooltip is one sentence of 15 words or fewer
- none of the three uses emoji, exclamation marks, or text in all caps

FAIL if any piece is missing, any piece is over its word limit, or the error doesn't say how to fix it.
