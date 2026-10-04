# Editing or auditing an existing page

Starting from existing text makes you cautious: you keep its structure and nudge the sentences. In tests that cut only 4 to 7% of a page. Trimming a long draft keeps the structure that made it long, so write the short version first.

## Edit

1. Save a copy of the page. Note its look (fonts, colors, spacing, how cards and badges look) and keep it.
2. List every fact on the page. That's the must-cover list. Text built by JavaScript (data arrays, templates) is copy too, and usually most of it.
3. Go section by section. Write the short version from the section's facts without looking at the old wording, then swap it in where it's clearer.
4. Delete before you add: repeats, intros that restate the heading, labels nobody needs. Add only what a reader is missing.
5. Inside a section you can change the form (steps to a numbered list, options to a table), built from styles the page already has. Detail that only some readers need can fold under a "More..." toggle, so it stays on the page without making it longer. Leave the page layout, section order and look alone unless asked to rebuild.
6. Expect the page to come out about a third shorter on screen. If it doesn't, look again for repeats and for detail to fold before you hand it over. Never cut a fact to hit a number.
7. Check your work as SKILL.md describes, including the editing checks in evals.md. Run `check.py --render --before <copy> <page>` to see the change on screen.
8. If the real problem is the structure (sections that repeat each other, a grid of cards that should be one table), say so in one line and offer a rebuild.

## Audit

When asked to audit or review a page, don't change it. Reply with the findings, biggest first, 10 at most, one line each:

`1. Where: what's wrong. Fix: the exact new text, or the change.`

Then ask which to apply. When the person picks, apply them with the edit steps above.

## Rebuild

When asked to rebuild or redo a page, keep its look and write a new page from the must-cover list with every rule in SKILL.md. Card grids can become tables and repeated sections can merge.
