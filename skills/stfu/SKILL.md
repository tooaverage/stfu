---
name: stfu
description: Writes and edits website and product copy so it's short, plain and free of AI tells, with every fact kept. Use whenever someone writes or changes copy that ships (landing pages, UI text, onboarding, error messages, empty states, product emails, help docs), asks to make copy shorter, clearer or "less AI", or asks to audit or review a page's copy, even if they don't name stfu. Not for chat replies, code comments or personal messages.
license: MIT
metadata:
  author: Jaycee Day
  version: 0.11.0
---

# stfu

Short, To-the-point, Friendly, Useful.

People skim product copy. Every extra word costs attention, and every AI tell costs trust. This skill keeps copy short without losing what the reader came for.

## Start here

Pick the job, and read its file before you do anything else:

- **Writing new copy:** read [references/examples.md](references/examples.md).
- **Editing, auditing or rebuilding a page that already exists:** read [references/editing.md](references/editing.md). Editing existing text pulls you into small tweaks that barely change the page, and that file has the steps that avoid it.

Every job ends with the checks in [references/evals.md](references/evals.md).

## Before you write

1. Read `.stfu.md` at the project root if it exists. Those are the team's house rules, and they win over this file, except that facts stay true.
2. List what the page has to cover: every point in the brief, or every fact on the page you're editing. Short copy that drops what the reader needed is a failure, not a win. Detail can move into a "show more", but nothing on the list disappears.
3. Get facts from the source (the brief, the code, the data, the person), never from memory.

## How to write it

1. **Lead with the answer.** The first line of the page, and of each section, says what the reader came for. Setup comes after, if at all.
2. **Say each thing once.** Repeats are the main reason pages run long. Keep the clearest version and cut the rest.
3. **Stay inside the word budget.** Hard limits work better than "be concise", so every element has one:

   | Element | Max |
   |---|---|
   | Title or headline | 8 words, up to 12 to keep the words people search for |
   | Sub under a title | 1 sentence, 15 words |
   | Section intro | 1 to 2 sentences, or none |
   | Card, row or table note | 12 words |
   | Hint or helper text | 10 words |
   | Button | 3 words |
   | Tooltip | 1 sentence, 15 words |
   | Empty or loading state | 15 words |
   | Error | 20 words: what failed, then what to do |
   | Paragraph | 3 lines |

   The budget wins. When a fact doesn't fit, give it its own element (a table row, a note, a "More" toggle), or cut it if the page says it somewhere else. Don't stretch the element to hold it.

   One idea per element. A title says what to do or what you get, and on a task screen it starts with a verb ("Name your workspace"). A sub says why, or what happens next, not both. A button is a verb and an object ("Connect GitHub", not "Continue"). Use words a 12-year-old knows, unless the right word is harder ("typhoon"), and write whole sentences: fragments and "Nov" mid-sentence are harder to read, not easier.
4. **Show it when it has a shape.** Steps someone follows in order become a numbered list (1, 2, 3). Options compared on the same points become a table. A status becomes a badge with a text label. Ordinary notes stay sentences, because a page of bullets reads like a slide deck.
5. **Be specific.** Real numbers, names and dates instead of "many" or "several". If a sentence could be pasted onto another product's page unchanged, it isn't saying anything: cut it or make it specific.
6. **Sound like a person.** Contractions, "you", active voice. Plain words instead of idioms, since "move the needle" means nothing to a lot of readers. Reuse the terms on nearby screens and sections, and don't invent new metaphors.
7. **Invite, don't push.** Buttons and links say what happens ("See pricing", not "Learn more"). No fake urgency.
8. **Keep it true and findable.** Facts, prices and caveats stay accurate: shorten a caveat, never drop it. Use real numbers only, and make privacy or security claims only when you've seen them in the code or a teammate confirmed them. When editing a live page, keep the words people search for in the title, H1 and first paragraph.
9. **Make it work for everyone.** Images get alt text that says what they show. Errors say what went wrong and how to fix it. Form fields have real labels. Prefer one `aria-label` to lots of hidden text, which makes the page longer and helps no one.

## AI tells to leave out

Readers spot these at a glance and stop trusting the page:

- Em dashes, and any dash used as a dramatic pause. In sentences, write ranges with "to" ("March 24 to April 7"). In tables, badges and labels an en dash is fine ("Mar 24–Apr 7").
- Hype words: leverage, streamline, seamless, effortless, unlock, empower, elevate, supercharge, game-changing, revolutionize, robust, cutting-edge, delve, honestly, quietly, genuinely, solution, offering, "comes alive". They're fine when literal ("Unlock your account").
- Softeners that promise ease: simply, just, easily, "in seconds".
- Comparisons with a vague crowd: "most people", "everyone else", "unlike most", "nobody else".
- Eyebrow labels, the small label above a heading. The heading already does that job.
- All caps, including text styled uppercase in CSS. Sentence case reads faster.
- Emoji. Screen readers read them out ("green square"). Use the project's icon set (Lucide, Heroicons or whatever is installed) with a text label, or suggest adding one.
- Colored or gradient words inside a headline.
- Zero-padded steps (01, 02, 03). Use 1, 2, 3.
- Setup-punchline hooks ("Short line. Fragment twist."), summary closers ("It's that simple."), balanced pairs ("X is fragmented, Y is unsolved."), narrating ("Let's dive in"), filler openers ("In today's fast-paced world") and put-downs of other products.

If the brand already uses caps, emoji or colored words, or the person asks for them, follow the brand.

## Check your work

1. Cut pass: delete every sentence the page works without, then every word each sentence works without. Count the words in each element against the budget.
2. Run the checker from this skill's folder: `python3 <skill folder>/scripts/check.py <file>`. It catches the mechanical tells (dashes, caps, emoji, hype words, vague links, missing alt text) and very long sentences. It can be wrong about literal uses, so judge each flag.
3. Read [references/evals.md](references/evals.md) and answer every check, pass or fail. If you can start a subagent (the Task or Agent tool), give a fresh one only the page, the must-cover list and evals.md, so it grades what a stranger sees. Fix what fails and grade again, at most 3 rounds.
4. Hand it over. New copy: show it with the word count beside each element, then at most two lines on anything folded away or left out and any fact to confirm. Edits: list each changed element as in [references/editing.md](references/editing.md). Start with the first change, not a summary of what you did or which checks ran.

## House rules

When someone edits your copy or says a line sounds off, the edit is the data:

1. Compare their version with yours word by word, and say in 1 to 3 lines what changed. Don't defend the original.
2. A cut is final. Never bring a cut line back in other words. If it solved a real problem, name the problem and offer a different fix.
3. When the same kind of change happens twice, add one rule to `.stfu.md` with the date and their exact words. Write word swaps as `Say "trip", not "journey"` so the checker catches them.
4. Fix the other places the rule applies.

## Examples

[references/examples.md](references/examples.md) has before and after pairs from real pages. One of them:

Before: "Whether you're planning a spring getaway or an autumn adventure, our comprehensive guides leverage monthly weather data to help you seamlessly identify the optimal time to visit. It's that simple."

After: "Find the best month to go. Each guide shows the weather, month by month, for a real city." A 12-month chart replaces the rest.

## Troubleshooting

- **The checker can't be found:** it's in this skill's folder, not the project. Use the full path.
- **The page builds its text with JavaScript:** add `--render` to the checker to read the page as a browser shows it (needs Playwright). Otherwise check the text in the script by hand.
- **Facts on the page contradict each other:** don't pick one. Flag it in your hand-over line.
