# stfu evals

Grade the copy once it's written. Each check is pass or fail, never a score, because a model can't reliably tell a 3 out of 5 from a 4. For every fail, quote the line and give the fix in a few words. Grade what a first-time visitor sees.

## Every page

1. The first line of the page and of each section gives the answer, not a setup.
2. Everything on the must-cover list is still there and still true, either visible or in a "show more".
3. No fact is said twice for the same reason. Warnings still sit next to the thing they warn about.
4. Numbers, names and dates are specific. No "many", "several" or "various".
5. No sentence could be pasted onto another product's page unchanged.
6. Every element is inside its word budget in SKILL.md (titles, subs, intros, notes, hints, buttons, tooltips, empty states, errors, paragraphs). Over budget is a fail, even by one word.
7. Each element holds one idea. Buttons are a verb and an object. A sub says why or what happens next, not both. A heading that names what's there has no sub, unless the sub warns about a consequence, cost or requirement.
8. Anything with a shape is shown, not told: places on a map, numbers over time on a chart, scores in a colored grid, options in a table, 3 or more setup steps numbered 1, 2, 3. A paragraph that could be one of these is a fail. Everything else is sentences: a list where sentences would read fine is a fail.
9. Sentences are whole and plain: contractions, "you", active voice. No fragments, no "Nov" mid-sentence, no idioms.
10. Buttons and links say what happens, and nothing pushes with fake urgency.
11. None of the AI tells listed in SKILL.md.
12. Images have alt text, errors say how to fix them, and form fields have labels. Empty states say what will show up there, not just that it's empty.

## Editing an existing page

13. Same fonts, colors and style as before.
14. Shorter on screen than before (`check.py --render --before <copy> <page>` shows both).
15. The search words are still in the title, H1 and first paragraph.

## When to stop

Stop when everything passes, or after 3 rounds. If a check still fails, name it in the hand-over line.
