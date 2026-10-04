---
name: stfu
description: Makes website and product copy short, plain and free of AI tells. Grade 6 words, visuals over paragraphs, accessible and safe for search. Use when writing, rewriting or reviewing copy that ships (pages, UI text, onboarding, product emails, docs, empty states, errors), or when someone edits shipped copy, so the edit becomes a house rule.
---

# stfu

Short, To-the-point, Friendly, Useful.

## Before you write

1. Read `.stfu.md` at the project root if it exists. Its rules override this file, except rules 8, 9 and 10.
2. Get facts from the source (data, code, the person), never from memory.

## The rules

**1. Cut first.** If a word, line or section can go without losing meaning, it goes.

**2. Grade 6 reading level.** Short, common words. Sentences under about 15 words. One idea per sentence. Use a harder word only when nothing simpler says it ("typhoon", "subscription").

**3. Visual first.** If it can be an icon, badge, table, chart, list or diagram, it isn't a paragraph. Write prose only if asked.
- Comparisons and data: table or chart.
- Status or rating: badge or color, with a text label.
- Steps: numbered list or diagram.
- Icons get a visible label.
- Add a short line of text (about 8 words) only if the visual needs explaining. Also add one if a page that ranks in search needs the fact.

**4. Lead with the answer.** The most useful thing comes first.

**5. Be specific.** Real numbers, names and dates. Not "many" or "several" when you know the number.

**6. Sound like a person.** Contractions, "you", active voice. Plain verbs: use, not utilize. Help, not facilitate. Idioms are fine.

**7. Friendly, never pushy.** "Try it free", not "Start now or miss out". No fake urgency.

**8. Never change the truth.** Facts, numbers, prices, legal text and caveats stay accurate. You can shorten a caveat, not drop or soften it.

**9. Don't break search.** When editing a live page:
- Keep the words people search for in the title, H1 and first paragraph. Don't swap them for synonyms.
- Keep sections that answer what people search for, even long ones.
- Don't change URLs, slugs or headings other pages link to. Flag them instead.

**10. Works for everyone.** Some people hear the page, zoom it, or read it out of order.
- Link and button text makes sense alone: "See pricing", not "Learn more".
- Don't point by color, shape or place: not "the green button". Name the thing.
- Alt text says what the image shows or means. No "Image of". Decorative images get empty alt.
- Errors say what went wrong and how to fix it: "Enter a date after today", not "Invalid input".
- Form fields have real labels, not just placeholder text.

## Never write these

- **Em dashes.** Use a comma, colon, full stop or parentheses. Not an en dash or " - " either.
- **Hype words:** honestly, quietly, leverage, streamline, seamless, effortless, unlock, empower, elevate, supercharge, game-changing, revolutionize, robust, cutting-edge, delve, solution (for a product), offering, "workflow" as a noun. Fine when literal ("Unlock your account").
- **All caps,** including text the CSS turns uppercase (`text-transform: uppercase` on labels and eyebrows). Use sentence case. Acronyms like "FAQ" are fine.
- **Colored words in headlines.** One color for the whole headline. No accent-colored or gradient word or line.
- **Emoji,** including as icons. Screen readers read them out loud ("green square").
- **Setup-punchline hooks.** "Short line. Fragment twist." Write one plain sentence.
- **Summary closers.** "It's that simple." End on the useful fact.
- **Tacked-on explaining.** "...which is why this matters." Say it once.
- **Narrating.** "As you can see", "Let's dive in", "Here's the thing".
- **Filler openers.** "In today's fast-paced world", "Whether you're X or Y", "Look no further".
- **Put-downs** of other products or people.

Caps, emoji and colored headline words are fine when asked, or when the brand already uses them.

## Check before shipping

The checker is in this skill's folder, not the project. Use the full path:

```
python3 <skill folder>/scripts/check.py path/to/file.md
echo "draft text" | python3 <skill folder>/scripts/check.py -
```

It flags dashes, caps, emoji, hype words, vague links, missing alt text and hard sentences, and prints an overall grade. From `.stfu.md` it reads `grade: N` as the target, and `not "word"` as a banned word. If you can't run it, check by hand.

Fix every flag unless the word is literal or has no simpler swap. The overall grade must pass. Passing is the floor, not the finish.

## Editing an existing page

Keep the design. Rewrite the content as if the page were new.

1. Draft the page from scratch with these rules, using the facts on the current page. Don't look at the old wording while you draft.
2. Pour the draft into the existing design: same fonts, colors, spacing and components. Build tables, lists and badges from the styles the page already has.
3. Fix the never list, including caps and colored words set in the CSS.
4. Then run the checker. Expect about a third fewer words. If a section barely changed, say why in one line.

Rules 8 and 9 still hold: keep every fact and the search words.

## How to hand it over

These rules apply to your reply too.

- Copy first. Nothing before it.
- One version. Options only when asked.
- Don't report your process (checks run, files found). Mention a check only if it found a problem you couldn't fix.
- After the copy, at most one line: a fact to confirm or a placeholder to fill.

## House rules

When someone edits your copy or says a line sounds off:

1. Say in one line what changed ("cut the intro", "'use', not 'utilize'").
2. If it's a pattern, not a one-off, add it to `.stfu.md` with the date. Ask if you can't tell.
3. Fix the other places the rule applies, in the same change.
4. Don't defend the original. The edit is the data.

Write word swaps as `Say "X", not "Y"` so the checker catches them:

```
# House rules

grade: 6

- 2026-09-28: Month notes stay under 12 words.
- 2026-09-30: Say "trip", not "journey".
```

## Example

Before (grade 11.5):
> Whether you're planning a spring getaway or an autumn adventure, our comprehensive guides leverage monthly weather data to help you seamlessly identify the optimal time to visit. It's that simple.

After (grade 1, plus a 12-month heatmap):
> Find the best month to go. Each guide shows the weather, month by month, for a real city.
