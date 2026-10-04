---
name: stfu
description: Use when writing, rewriting or reviewing copy that ships in a website or product (pages, UI text, onboarding, emails from the product, docs, empty states, errors). Makes it short, plain, grade 6 reading level, visual where possible, and free of AI tells. Also use when someone edits shipped copy, so the edit becomes a house rule.
---

# stfu

Short, To-the-point, Friendly, Useful.

This skill is for words that ship: website pages, product UI, onboarding, docs, notifications.

## Before you write

1. Look for a `.stfu.md` file at the project root. If it exists, read it. Its rules override everything below except rules 8, 9 and 10.
2. Get facts from the source (data, code, the person), never from memory.
3. Ask: does this need words at all? If it can be a visual, make it a visual.

## The rules

**1. Cut first.** Every word earns its place. If a word, line or section can go without losing meaning, it goes. Shorter wins.

**2. Grade 6 reading level.** Short, common words. Sentences under about 15 words. One idea per sentence. Use a harder word only when no simpler one says the same thing (for example "typhoon" or "subscription"). Technical docs can set a higher target with `grade: 8` in `.stfu.md`. Run the check script before shipping.

**3. Visual first.** If it can be an icon, badge, table, chart, list or diagram, it is not a paragraph, unless the person asks for prose.
- Comparisons and data: table or chart.
- Status or rating: badge or color, with a text label.
- Steps: numbered list or diagram.
- Every icon has a visible label or alt text. Use one icon set across the product.
- Every chart, image or diagram gets one short line of text (about 8 words) with the key fact. It's what search engines, screen readers and skimmers get.

**4. Lead with the answer.** The most useful thing comes first. Detail comes after, if at all.

**5. Be specific.** Real numbers, names and dates. Never "many", "several", "various" or "a number of" when you know the number.

**6. Sound like a person, not a brochure.**
- Use contractions: it's, don't, you'll, can't.
- Use "you". Use active voice.
- Plain verbs over fancy ones: use, not utilize. Help, not facilitate. Start, not commence.
- Common idioms are fine. Parallel structure is fine when it makes things clearer.

**7. Keep it friendly, never pushy.** Calls to action invite: "Try it free", not "Start now or miss out". No fake urgency.

**8. Never change the truth.** Facts, numbers, prices, legal text and caveats stay accurate. You can shorten a caveat. You can't drop it or soften what it means.

**9. Don't break search.** When editing a live page, keep what it ranks for:
- Keep the words people search for in the title, H1 and first paragraph. Shorten around them, don't swap them for synonyms.
- Don't cut a section that answers a question people search for, even if it's long.
- Don't change URLs, slugs or headings other pages link to. Flag them instead.

**10. Works for everyone.** Some people hear the page, zoom it, or read it out of order.
- Link and button text makes sense on its own: "See pricing", not "Learn more" or "Click here".
- Never point by color, shape or place alone: not "the green button" or "the chart on the right". Name the thing.
- Alt text says what the image shows or means, in plain words. Don't start with "Image of". Decorative images get empty alt.
- Errors say what went wrong and how to fix it, next to the field: "Enter a date after today", not "Invalid input".
- Form fields have real labels. Placeholder text isn't a label.
- Emoji don't replace words. Screen readers read their names out loud ("green square").
- Tables are for data, with a header row. Never for layout.

## Never write these

- **Em dashes (the long dash).** Use a comma, colon, full stop or parentheses. Don't swap in an en dash or " - " either.
- **Words:** honestly, quietly, leverage, streamline, seamless, effortless, unlock, empower, elevate, supercharge, game-changing, revolutionize, robust, cutting-edge, delve, solution (for a product), offering, "workflow" as a noun. These are fine when literal ("Unlock your account").
- **All caps.** No uppercase text, including small labels and eyebrows styled with `text-transform: uppercase`. Use sentence case. Only use caps when asked, or when the project's design system already does (check its tokens and existing components first). Acronyms like "MB" or "FAQ" are fine.
- **Setup-punchline hooks.** "Short line. Fragment twist." Write one plain sentence instead.
- **Neat summary closers.** "That's the power of X." "It's that simple." End on the useful fact.
- **Tacked-on explaining.** "...which is why this matters." Say it once.
- **Narrating.** "As you can see", "Let's dive in", "Here's the thing". State the fact.
- **Put-downs.** Don't make other products or people look bad to make this one look good.
- **Filler openers.** "In today's fast-paced world", "Whether you're X or Y", "Look no further".

## Check before shipping

Run the checker on the changed files or on the draft text. It lives in this skill's own folder (the base directory shown when the skill loads), not in the project, so use the full path:

```
python3 <skill folder>/scripts/check.py path/to/file.md
echo "your draft text" | python3 <skill folder>/scripts/check.py -
```

It flags dashes, all caps, banned words, vague link text, images with no alt text, long sentences and hard sentences, and prints an overall grade. It also reads `.stfu.md`: `grade: N` sets the target, and any rule written as `not "word"` adds that word to the banned list. If you can't run it, check the same things by hand.

Fix every flag, unless the word is literal or has no simpler swap. The overall grade must pass. Then check by eye: facts match the source, caveats are there, anything that could be a visual is one.

## How to hand it over

The rules apply to your reply too, not just the copy.

- Give the copy first. Nothing before it.
- Give one version. Give options only when asked.
- Don't report your process: which checks ran, whether `.stfu.md` exists, what you did by hand. Mention a check only when it found a problem you couldn't fix.
- After the copy, at most one line: a fact to confirm or a placeholder to fill.

## House rules (the ratchet)

When someone edits copy you wrote, or says a line sounds off:

1. Compare their version with yours.
2. Say in one line what changed ("cut the intro sentence", "swapped 'utilize' for 'use'").
3. If it's a pattern, not a one-off fix, add it as a rule to `.stfu.md` at the project root, with the date. Create the file if it doesn't exist. Ask if you can't tell.
4. List the other places the new rule applies and fix them in the same change.
5. Don't defend the original. The edit is the data.

`.stfu.md` format. Write word swaps as `Say "X", not "Y"` so the checker picks them up:

```
# House rules

grade: 6

- 2026-09-28: Month notes stay under 12 words.
- 2026-09-30: Say "trip", not "journey".
```

## Example

Before (grade 11.5, 30 words):
> Whether you're planning a spring getaway or an autumn adventure, our comprehensive guides leverage monthly weather data to help you seamlessly identify the optimal time to visit. It's that simple.

After (grade 1, 18 words, plus a 12-month heatmap in place of the rest):
> Find the best month to go. Each guide shows the weather, month by month, for a real city.
