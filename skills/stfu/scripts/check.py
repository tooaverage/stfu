#!/usr/bin/env python3
"""stfu checker: flags the mechanical AI tells (em dashes, dashes used as a
pause, small text in all caps, emoji, hype words, eyebrow labels, 01/02/03 steps, strings of
very short sentences), vague links, images with no alt text and very long
sentences.

Usage:
  python3 check.py FILE [FILE ...]
  echo "text" | python3 check.py -
Options:
  --grade N      target reading grade (default 6, or "grade: N" in .stfu.md)
  --render       read pages the way a browser shows them, including text built
                 by JavaScript, and print visible words and page height.
                 Needs Playwright (pip install playwright).
  --before FILE  with --render: also print the old page's words and height,
                 so you can see if the edit made the page shorter.

Without --render it reads the source: Markdown, HTML, and the strings inside
<script> (not the code around them).
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
    "as you can see", "here's the thing", "genuinely", "move the needle",
    "moves the needle", "low-hanging fruit", "deep dive", "at the end of the day",
    "circle back", "best-in-class", "world-class", "comes alive", "simply",
    "easily", "in seconds", "most people", "everyone else", "unlike most",
    "nobody else",
]

# Only very long sentences get flagged. Flagging every sentence over 15 words
# taught the model to split sentences, which made pages longer, not shorter.
MAX_WORDS = 25


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
    # Block tags end a sentence, so a heading never merges with the text under it.
    text = re.sub(r"</?(p|div|section|article|header|footer|nav|main|aside|h[1-6]|li|ul|ol|dl|dt|dd|tr|td|th|table|br|figure|figcaption|blockquote|button|label)\b[^>]*>", "\n\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"^\s{0,3}(#{1,6}|[-*+]|\d+\.|>)\s*", "", text, flags=re.M)
    text = re.sub(r"[*_|]", " ", text)
    text = "\n".join(" ".join(line.split()) for line in text.splitlines())
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



PAUSE_DASH = re.compile(r"\w\s+(?:–|--?)\s+\w")
STRING = re.compile(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"|`([^`]*)`")
VAGUE = r"(?:click here|here|learn more|read more|more|this link|link)"


def script_lines(raw):
    """Line numbers that sit inside <script> blocks."""
    inside, out = False, set()
    for i, line in enumerate(raw.splitlines(), 1):
        low = line.lower()
        opens = "<script" in low
        if inside or opens:
            out.add(i)
        if opens and "</script>" not in low.split("<script", 1)[1]:
            inside = True
        if "</script>" in low:
            inside = False
    return out


TITLE_SELECTOR = re.compile(r"\bh[12]\b|title|headline|hero|display|banner", re.I)


def big_size(css):
    """True when a CSS font-size is title-sized: 28px or 1.75rem and up, or a clamp() that ends there."""
    m = re.search(r"font-size\s*:\s*([^;}]+)", css, flags=re.I)
    if not m:
        return False
    sizes = re.findall(r"([\d.]+)\s*(px|rem|em)\b", m.group(1))
    if not sizes:
        return False
    value, unit = sizes[-1]
    return float(value) >= (28 if unit == "px" else 1.75)


def title_caps(raw):
    """How many times per line uppercase is set on a title. Caps are fine on titles; small labels in caps read as AI."""
    count = {}
    def add(pos):
        line = raw.count("\n", 0, pos) + 1
        count[line] = count.get(line, 0) + 1
    # A rule starts at the top of the file or right after a brace. Without that
    # anchor the search retries from every character and big files take minutes.
    for m in re.finditer(r"(?:^|(?<=[{}]))([^{}]*)\{([^{}]*)\}", raw):
        selector, body = m.group(1), m.group(2)
        t = re.search(r"text-transform\s*:\s*uppercase", body, flags=re.I)
        if t and (TITLE_SELECTOR.search(selector) or big_size(body)):
            add(m.start(2) + t.start())
    for m in re.finditer(r"<(\w+)\b[^>]*\bclass(?:Name)?=\{?[\"'`]([^\"'`]*\buppercase\b[^\"'`]*)", raw):
        tag, classes = m.group(1).lower(), m.group(2)
        big = re.search(r"\btext-(?:[3-9]xl)\b", classes) or any(float(n) >= 28 for n in re.findall(r"\btext-\[([\d.]+)px\]", classes))
        if tag in ("h1", "h2") or big:
            add(m.start())
    return count


def markup_flags(name, raw):
    """Checks that need the source: CSS, classes, links, images."""
    flags = 0
    titles = title_caps(raw)
    for i, line in enumerate(raw.splitlines(), 1):
        hits = []
        caps = len(re.findall(r"text-transform\s*:\s*uppercase", line, flags=re.I))
        if re.search(r"class(Name)?=", line):
            caps += len(re.findall(r"\bclass(?:Name)?=\{?[\"'`][^\"'`]*\buppercase\b", line))
        if caps > titles.get(i, 0):
            hits.append("uppercase on small text")
        if re.search(r"\[\s*" + VAGUE + r"\s*\]\(", line, flags=re.I) or re.search(r">\s*" + VAGUE + r"\s*</a>", line, flags=re.I):
            hits.append("vague link text")
        if re.search(r"<img\b(?![^>]*\balt\s*=)[^>]*>", line, flags=re.I) or re.search(r"!\[\s*\]\(", line):
            hits.append("image with no alt text")
        if re.search(r'class(Name)?="[^"]*\b(eyebrow|kicker|overline|section-label)\b', line, flags=re.I):
            hits.append("eyebrow label")
        if re.search(r">\s*0[1-9]\s*<|decimal-leading-zero|padStart\(2, *.0.\)", line):
            hits.append("zero-padded step number")
        for hit in hits:
            print(f"{name}:{i}: {hit}: {line.strip()[:80]}")
        flags += len(hits)
    return flags


ABBREVIATION = re.compile(r"\b(?:Mt|St|Dr|Mr|Mrs|Ms|Jr|Sr|No|vs|etc|approx|e\.g|i\.e)\.$", re.I)


def short_sentences(text):
    """True when a line or element is only very short sentences, like "Same meaning. Fewer words."
    Lines with numbers are skipped: "The limit is 25 MB." is a fact, not a hook."""
    for part in re.split(r"<[^>]+>|\t|\|", text):  # each element, table cell or column on its own
        part = re.sub(r"^[\s\-*>\"'“”‘’(]*(?:\d+[.)]\s+)?", "", part).strip(" \"'“”‘’)")
        # Skip numbers, and the … that stands in for ${...} in JavaScript templates.
        if not part or re.search(r"[\d…]", part):
            continue
        sents = []
        for s in re.split(r"(?<=[.!?])\s+", part):
            if sents and ABBREVIATION.search(sents[-1]):
                sents[-1] += " " + s  # "Mt. Fuji" is one sentence
            else:
                sents.append(s)
        if len(sents) >= 2 and all(s[-1] in ".!?" and 1 <= len(re.findall(r"[A-Za-z][\w'’-]*", s)) <= 4 for s in sents):
            return True
    return False


def prose_flags(name, lines, banned, is_title=lambda i, text: False):
    """Checks on the words people read. lines: (line number, text) pairs.
    is_title says which lines are titles, where all caps is fine."""
    flags = 0
    for i, text in lines:
        found = []
        if EM_DASH in text:
            found.append("em dash")
        if PAUSE_DASH.search(text.lstrip(" -*>")):
            found.append("dash used as a pause")
        if re.search(r"\b[A-Z]{2,}\b(?:[\s,:!.-]+\b[A-Z]{2,}\b)+", text) and not is_title(i, text):
            found.append("all caps")
        if EMOJI.search(text):
            found.append("emoji")
        if re.fullmatch(r"\s*0[1-9][.)]?\s*", text):
            found.append("zero-padded step number")
        if short_sentences(text):
            found.append("string of very short sentences")
        low = text.lower()
        found += [f"banned '{b}'" for b in banned if re.search(r"(?<![a-z])" + re.escape(b) + r"(?![a-z])", low)]
        for f in found:
            print(f"{name}:{i}: {f}: {text.strip()[:80]}")
        flags += len(found)
    return flags


def source_prose(raw):
    """The readable text in a source file, line by line. In <script> only the strings count."""
    # CSS isn't prose: blank out <style> blocks but keep the line numbers.
    raw = re.sub(r"<style[^>]*>.*?</style>", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S | re.I)
    in_script, in_code, out = script_lines(raw), False, []
    for i, line in enumerate(raw.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if i in in_script:
            # Strings only, and not the ${...} code inside template strings.
            text = " ".join(re.sub(r"\$\{[^}]*\}", "…", g) for m in STRING.finditer(line) for g in m.groups() if g)
        else:
            text = re.sub(r"`[^`]*`", " ", line)
        if text.strip():
            out.append((i, text))
    return out


def grade_flags(name, text, target):
    flags = 0
    sents = split_sentences(strip_markup(text))
    tw = ts = 0
    for s in sents:
        w = words_of(s)
        syl = sum(syllables(x) for x in w)
        tw += len(w)
        ts += syl
        if len(w) > MAX_WORDS:
            print(f"{name}: long sentence ({len(w)} words): {s[:100]}")
            flags += 1
    overall = grade(tw, len(sents), ts)
    status = "OK" if overall <= target + 0.5 else "TOO HARD"
    print(f"{name}: overall grade {overall:.1f} (target {target:g}), {len(sents)} sentences, {tw} words: {status}")
    return flags + (1 if overall > target + 0.5 else 0)


RENDER_JS = """() => {
  // Leave out text only screen readers get (1px boxes, clipped), so the count matches what people see.
  const hidden = [];
  for (const el of document.body.querySelectorAll('*')) {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    if ((r.width <= 1 && r.height <= 1 && el.textContent.trim()) || s.clip === 'rect(0px, 0px, 0px, 0px)' || s.clipPath === 'inset(50%)') hidden.push([el, el.style.display]);
  }
  hidden.forEach(([el]) => el.style.display = 'none');
  const text = document.body.innerText;
  // Title-sized text (28px and up), where all caps is fine.
  const titles = [];
  for (const el of document.body.querySelectorAll('*')) {
    if (parseFloat(getComputedStyle(el).fontSize) >= 28 && el.innerText) titles.push(...el.innerText.split('\\n').map(t => t.trim()).filter(Boolean));
  }
  hidden.forEach(([el, d]) => el.style.display = d);
  return {text, titles, height: document.documentElement.scrollHeight};
}"""


def render(path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.goto("file://" + os.path.abspath(path))
        pg.wait_for_timeout(300)
        r = pg.evaluate(RENDER_JS)
        b.close()
        return r


def check(name, raw, target, banned, rendered=None):
    flags = markup_flags(name, raw)
    if rendered is None:
        headings = {i for i, line in enumerate(raw.splitlines(), 1) if re.search(r"<h[12]\b", line, flags=re.I) or re.match(r"#{1,2}\s", line)}
        flags += prose_flags(name, source_prose(raw), banned, lambda i, text: i in headings)
        text = "\n".join(re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I).splitlines())
        flags += grade_flags(name, text, target)
    else:
        lines = [(f"rendered line {n}", t) for n, t in enumerate(rendered["text"].splitlines(), 1) if t.strip()]
        titles = set(rendered.get("titles", []))
        flags += prose_flags(name, [(i, t) for i, t in lines], banned, lambda i, text: text.strip() in titles)
        flags += grade_flags(name, rendered["text"].replace("\n", "\n\n"), target)
        print(f"{name}: on screen {len(words_of(rendered['text']))} words, page height {rendered['height']}px")
    return flags


def take(argv, flag, has_value=True):
    if flag not in argv:
        return argv, None
    i = argv.index(flag)
    if has_value:
        if i + 1 >= len(argv):
            sys.exit(f"{flag} needs a value.")
        return argv[:i] + argv[i + 2:], argv[i + 1]
    return argv[:i] + argv[i + 1:], True


def main(argv):
    argv, target = take(argv, "--grade")
    argv, before = take(argv, "--before")
    argv, do_render = take(argv, "--render", has_value=False)
    try:
        target = float(target) if target else None
    except ValueError:
        sys.exit(f"--grade needs a number, like --grade 8 (got {target}).")
    if not argv:
        print(__doc__)
        return 2
    if do_render and not _has_playwright():
        print("--render needs Playwright (pip install playwright, then playwright install chromium). Reading the source instead.")
        do_render = False
    total = 0
    for path in argv:
        start = os.getcwd() if path == "-" else os.path.dirname(os.path.abspath(path))
        rules_grade, extra = load_house_rules(find_house_rules(start))
        t = target if target is not None else (rules_grade if rules_grade is not None else 6.0)
        banned = BANNED + [w for w in extra if w not in BANNED]
        if path == "-":
            total += check("stdin", sys.stdin.read(), t, banned)
            continue
        try:
            # errors="replace" so one odd byte doesn't stop the whole check.
            with open(path, encoding="utf-8", errors="replace") as f:
                raw = f.read()
        except OSError as e:
            print(f"{path}: can't read it ({e.strerror}).")
            total += 1
            continue
        total += check(path, raw, t, banned, render(path) if do_render else None)
    if before and not os.path.isfile(before):
        print(f"{before}: can't find the --before file, so there's no before and after.")
    elif do_render and before and argv[-1] != "-":
        was, now = render(before), render(argv[-1])
        print(f"before -> after: {len(words_of(was['text']))} -> {len(words_of(now['text']))} words on screen, "
              f"{was['height']} -> {now['height']}px tall")
    return 1 if total else 0


def _has_playwright():
    try:
        import playwright.sync_api  # noqa: F401
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
