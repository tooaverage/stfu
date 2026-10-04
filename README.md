# stfu

**S**hort, **T**o-the-point, **F**riendly, **U**seful.

A skill that makes AI write copy people can read. Use it for words that ship: website pages, product UI, onboarding, docs, errors and empty states.

| Rule | What it means |
|---|---|
| Cut first | If a word can go, it goes. |
| Grade 6 | Short, common words. Sentences under 15 words. |
| Visual first | Tables, badges and lists beat paragraphs. |
| Lead with the answer | The useful thing comes first. |
| Be specific | Real numbers, names and dates. |
| Sound like a person | Contractions, "you", plain verbs. |
| Friendly, not pushy | No fake urgency. |
| Never change the truth | Facts, prices and caveats stay right. |
| Don't break search | Edits keep the words a page ranks for. |
| Works for everyone | Clear links, alt text, no color-only cues. |

It also bans the usual AI tells (em dashes, all-caps labels, emoji, colored headline words, "seamless", "leverage", "It's that simple") and learns from your edits. When you fix a line, the fix becomes a house rule in `.stfu.md`.

## Install

### Claude Code

```
/plugin marketplace add tooaverage/stfu
/plugin install stfu@stfu
```

Or copy `skills/stfu` into `~/.claude/skills/`.

### Claude.ai

Zip the `skills/stfu` folder and upload it in Settings > Capabilities > Skills.

### Other tools

Paste `skills/stfu/SKILL.md` into your tool's rules file (`AGENTS.md`, `.cursor/rules`, etc).

## Check your copy

The checker needs only Python 3.

```
python3 skills/stfu/scripts/check.py page.md
echo "your draft" | python3 skills/stfu/scripts/check.py -
```

It flags dashes, all caps, emoji, banned words, vague link text, images with no alt text, long sentences and hard sentences, and prints an overall grade. It exits with 1 if anything is flagged, so you can run it in CI.

## House rules

Each project can have a `.stfu.md` at its root. It overrides the defaults.

```
# House rules

grade: 8

- 2026-09-30: Say "trip", not "journey".
```

`grade: 8` raises the target (useful for technical docs). `Say "X", not "Y"` adds Y to the checker's banned list. See [examples/](examples/).

## For chat

Want your AI assistant to talk to you this way too? See [prompts/conversation.md](prompts/conversation.md).

## License

MIT
