#!/usr/bin/env python3
"""stfu checker: flags dashes, all caps, emoji, banned words, vague links,
missing alt text and hard-to-read sentences.

Usage:
  python3 check.py FILE [FILE ...]
  echo "text" | python3 check.py -
Options:
  --grade N      target reading grade (default 6, or "grade: N" in .stfu.md)
  --before FILE  the page before your edit. Fails if fewer than 30% of the
                 words were cut.

No dependencies. Strips Markdown, HTML and code blocks before scoring.
Reads .stfu.md from the current folder or any parent: a "grade: N" line sets
the target, and any rule written as 'not "word"' adds that word to the list.
Exit code 1 if anything was flagged, 0 if clean.
"""
import os
import re
import sys

EM_DASH = "\u2014"
EN_DASH = "\u2013"
# Emoji and pictographs. Leaves out simple marks like \u2713 and \u2714 (check marks).
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u2712\u2719-\u27BF\u2B50\u2B55]")

BANNED = [
    "honestly", "quietly", "leverage", "leverages", "leveraging", "streamline",
    "streamlines", "seamless", "seamlessly", "effortless", "effortlessly",
    "unlock", "unlocks", "empower", "empowers", "elevate", "elevates",
    "supercharge", "game-changing", "game changer", "revolutionize",
    "revolutionary", "robust", "cutting-edge", "delve", "utilize", "utilise",
    "facilitate", "commence", "offering", "in today's fast-paced world",
    "look no further", "whether you're", "it's that simple", "let's dive in",
    "as you can see", "here's the thing",
]

# A sentence is flagged when it is longer than this, or when it is both
# fairly long and far above the target grade. Grade formulas swing wildly on
# short sentences ("Your subscription renews automatically" scores 18), so
# short sentences only count toward the overall grade.
MAX_WORDS = 15
HARD_MIN_WORDS = 8
HARD_MARGIN = 3


def find_house_rules(start):
    d = os.path.abspath(start)
    while True:
        p = os.path.join(d, ".stfu.md")
        if os.path.isfile(p):
            return p
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def load_house_rules(path):
    grade_target, extra = None, []
    if not path:
        return grade_target, extra
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^\s*-?\s*grade:\s*(\d+(?:\.\d+)?)\s*$", text, flags=re.M | re.I)
    if m:
        grade_target = float(m.group(1))
    extra = [w.lower() for w in re.findall(r'\bnot\s+"([^"]+)"', text, flags=re.I)]
    return grade_target, extra


def strip_markup(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"^\s{0,3}(#{1,6}|[-*+]|\d+\.|>)\s*", "", text, flags=re.M)
    text = re.sub(r"[*_|]", " ", text)
    return text


def syllables(word):
    word = word.lower()
    word = re.sub(r"[^a-z]", "", word)
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    word = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", word)
    word = re.sub(r"^y", "", word)
    count = len(re.findall(r"[aeiouy]{1,2}", word))
    return max(1, count)


def words_of(s):
    return re.findall(r"[A-Za-z][A-Za-z'-]*", s)


def grade(sentence_words, sentence_count, syllable_count):
    if not sentence_words or not sentence_count:
        return 0.0
    return 0.39 * (sentence_words / sentence_count) + 11.8 * (syllable_count / sentence_words) - 15.59


def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n{2,}|\n(?=\S)", text)
    return [p.strip() for p in parts if len(words_of(p)) >= 3]


MIN_CUT = 0.30
LONG_BLOCK = 15


def visible_words(raw):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    return len(words_of(strip_markup(t)))


INLINE = {"a", "b", "strong", "em", "i", "span", "code", "small", "abbr", "sup", "sub", "br", "mark"}
VOID = {"img", "input", "meta", "link", "hr", "wbr", "source", "area", "base", "col", "embed", "track", "path", "rect", "circle", "line"}


def text_blocks(raw):
    """Text of each block element (inline tags merged in), or Markdown paragraphs."""
    if not re.search(r"<(p|li|td|div|section)\b", raw, flags=re.I):
        return [strip_markup(b) for b in re.split(r"\n\s*\n", raw)]
    from html.parser import HTMLParser

    class P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack, self.out, self.skip = [[]], [], 0

        def handle_starttag(self, tag, attrs):
            if tag in ("script", "style", "svg"):
                self.skip += 1
            elif tag not in INLINE and tag not in VOID and not self.skip:
                self.stack.append([])

        def handle_endtag(self, tag):
            if tag in ("script", "style", "svg"):
                self.skip = max(0, self.skip - 1)
            elif tag not in INLINE and tag not in VOID and not self.skip and len(self.stack) > 1:
                self.out.append(" ".join(self.stack.pop()))

        def handle_data(self, data):
            if not self.skip:
                self.stack[-1].append(data)

    p = P()
    p.feed(raw)
    return [" ".join(b.split()) for b in p.out + [" ".join(x) for x in p.stack] if b.strip()]


def check(name, raw, target, banned):
    flags = 0
    in_code = False
    for i, line in enumerate(raw.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        prose = re.sub(r"`[^`]*`", " ", line)
        if EM_DASH in prose:
            print(f"{name}:{i}: em dash: {line.strip()[:80]}")
            flags += 1
        if EN_DASH in prose or re.search(r"\s--?\s", prose.lstrip(" -*>")):
            print(f"{name}:{i}: dash used as a pause: {line.strip()[:80]}")
            flags += 1
        if re.search(r"text-transform\s*:\s*uppercase", prose, flags=re.I) or re.search(r"\buppercase\b", prose) and re.search(r"class(Name)?=", prose):
            print(f"{name}:{i}: uppercase style: {line.strip()[:80]}")
            flags += 1
        elif re.search(r"\b[A-Z]{2,}\b(?:[\s,:!.-]+\b[A-Z]{2,}\b)+", prose):
            print(f"{name}:{i}: all caps: {line.strip()[:80]}")
            flags += 1
        vague = r"(?:click here|here|learn more|read more|more|this link|link)"
        if re.search(r"\[\s*" + vague + r"\s*\]\(", prose, flags=re.I) or re.search(r">\s*" + vague + r"\s*</a>", prose, flags=re.I):
            print(f"{name}:{i}: vague link text: {line.strip()[:80]}")
            flags += 1
        if re.search(r"<img\b(?![^>]*\balt\s*=)[^>]*>", prose, flags=re.I) or re.search(r"!\[\s*\]\(", prose):
            print(f"{name}:{i}: image with no alt text: {line.strip()[:80]}")
            flags += 1
        if EMOJI.search(prose):
            print(f"{name}:{i}: emoji: {line.strip()[:80]}")
            flags += 1
        low = prose.lower()
        for b in banned:
            if re.search(r"(?<![a-z])" + re.escape(b) + r"(?![a-z])", low):
                print(f"{name}:{i}: banned '{b}': {line.strip()[:80]}")
                flags += 1

    for b in text_blocks(raw):
        n = len(words_of(b))
        if n > LONG_BLOCK:
            print(f"{name}: long block ({n} words), cut it or make it a list or table: {' '.join(b.split())[:80]}")
            flags += 1

    text = strip_markup(raw)
    sents = split_sentences(text)
    tw = ts = 0
    for s in sents:
        w = words_of(s)
        syl = sum(syllables(x) for x in w)
        tw += len(w)
        ts += syl
        g = grade(len(w), 1, syl)
        if len(w) > MAX_WORDS or (g > target + HARD_MARGIN and len(w) >= HARD_MIN_WORDS):
            print(f"{name}: grade {g:.1f} ({len(w)} words): {s[:100]}")
            flags += 1
    overall = grade(tw, len(sents), ts)
    status = "OK" if overall <= target + 0.5 else "TOO HARD"
    print(f"{name}: overall grade {overall:.1f} (target {target:g}), {len(sents)} sentences, {tw} words: {status}")
    if overall > target + 0.5:
        flags += 1
    return flags


def main(argv):
    target = None
    if "--grade" in argv:
        i = argv.index("--grade")
        target = float(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    before = None
    if "--before" in argv:
        i = argv.index("--before")
        before = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        print(__doc__)
        return 2
    total = 0
    for path in argv:
        start = os.getcwd() if path == "-" else os.path.dirname(os.path.abspath(path))
        rules_grade, extra = load_house_rules(find_house_rules(start))
        t = target if target is not None else (rules_grade if rules_grade is not None else 6.0)
        banned = BANNED + [w for w in extra if w not in BANNED]
        if path == "-":
            total += check("stdin", sys.stdin.read(), t, banned)
        else:
            with open(path, encoding="utf-8") as f:
                total += check(path, f.read(), t, banned)
    if before and argv[-1] != "-":
        with open(before, encoding="utf-8") as f:
            was = visible_words(f.read())
        with open(argv[-1], encoding="utf-8") as f:
            now = visible_words(f.read())
        cut = 1 - now / was if was else 0
        status = "OK" if cut >= MIN_CUT else f"NOT ENOUGH (aim for {MIN_CUT:.0%})"
        print(f"{argv[-1]}: words {was} -> {now}, cut {cut:.0%}: {status}")
        if cut < MIN_CUT:
            total += 1
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
