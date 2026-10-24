# stfu

**S**hort, **T**o-the-point, **F**riendly, **U**seful.

A skill that makes AI write copy people can read: website pages, product UI, onboarding, docs, errors and empty states.

| Rule | Why |
|---|---|
| Lead with the answer | Readers decide in the first line whether to keep reading. |
| Say each thing once | Repeats are the main reason pages run long. |
| Short and plain | Headlines about 10 words, intros 1 to 2 sentences, paragraphs 3 lines at most. |
| Visual first | Places get a map, numbers over time a chart, comparisons a table and steps numbers. Notes stay sentences. |
| Be specific | Real numbers, names and dates. |
| Keep every fact | Detail can fold into "show more". Nothing on the brief disappears. |
| Works for everyone | Clear links, alt text, errors that say how to fix them. |

It also leaves out the usual AI tells: em dashes, hype words, eyebrow labels and other small all-caps text, emoji, colored headline words and 01/02/03 steps.

## Use it

Two ways, depending on what you want:

- **Keep your design, fix the words:** "Audit the copy on index.html with stfu" gives you up to 10 fixes and changes nothing until you pick. "Use stfu on index.html" makes the edits. The layout, colors and fonts stay, and every fact is kept.
- **Visual first, simple copy first:** start with stfu. Ask for a new page or screen and it loads on its own. Anything with a shape becomes a visual: places on a map, numbers on a chart, steps in a numbered list.

Each run grades itself against [references/evals.md](skills/stfu/references/evals.md), a list of pass/fail checks.

## Install

```
npx skills add tooaverage/stfu
```

Works with Claude Code, Cursor, Codex and other agents.

In Claude Code you can also install it as a plugin:

```
/plugin marketplace add tooaverage/stfu
/plugin install stfu@stfu
```

To get new versions on their own, turn on auto-update: run `/plugin`, open **Marketplaces**, pick **stfu** and choose **Enable auto-update**.

For Claude.ai, zip the `skills/stfu` folder and upload it as a skill in Settings.

## Check your copy

```
python3 skills/stfu/scripts/check.py page.html
python3 skills/stfu/scripts/check.py --render --before old.html page.html
```

The first catches the mechanical tells. `--render` reads the page the way a browser shows it (needs Playwright) and prints words on screen and page height, before and after. It exits with 1 if anything is flagged, so it works in CI.

## House rules

Add a `.stfu.md` to your project root to change the defaults.

```
# House rules

grade: 8

- 2026-09-30: Say "sign in", not "log in".
```

`grade: 8` raises the target, for technical docs. `Say "X", not "Y"` adds Y to the banned words.

## Testing the skill

[evals/evals.json](evals/evals.json) has test prompts in skill-creator's format, and [evals/triggers.json](evals/triggers.json) has prompts that should and shouldn't load the skill. Run them with and without stfu and grade both against the evals list.

## For chat

Want your AI to talk to you this way too? See [prompts/conversation.md](prompts/conversation.md).

## License

MIT
