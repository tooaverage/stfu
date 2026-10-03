#!/usr/bin/env python3
"""Before and after test for the stfu skill.

Runs each prompt in evals/prompts.txt twice with Claude Code:
  before: no skills at all
  after:  only the stfu skill from this repo
Then scores both answers with the checker and writes evals/results.md
and a side-by-side evals/results.html.

Usage: python3 evals/compare.py
Needs the `claude` CLI, logged in.
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "skills", "stfu", "scripts", "check.py")
OUT = os.path.join(ROOT, "evals", "results.md")
HTML_OUT = os.path.join(ROOT, "evals", "results.html")

ARMS = {
    "before": ["--disable-slash-commands"],
    "after": ["--plugin-dir", ROOT],
}


def run_claude(prompt, extra, cwd):
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--setting-sources", "project"] + extra
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=300)
    used_skill, answer = False, ""
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "assistant":
            for c in e["message"]["content"]:
                if c.get("type") == "tool_use" and c.get("name") == "Skill" and "stfu" in json.dumps(c.get("input")):
                    used_skill = True
        if e.get("type") == "result":
            answer = e.get("result") or ""
    if not answer:
        sys.exit(f"claude failed: {(p.stderr or p.stdout)[-300:]}\nTry running `claude` once to log in.")
    return answer, used_skill


def score(text):
    p = subprocess.run([sys.executable, CHECK, "-"], input=text, capture_output=True, text=True)
    lines = p.stdout.strip().splitlines()
    flags = len(lines) - 1
    m = re.search(r"overall grade ([\d.-]+).*?(\d+) words", lines[-1]) if lines else None
    return (float(m.group(1)), int(m.group(2)), flags) if m else (0.0, 0, flags)


PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>stfu before and after</title>
<style>
:root{--bg:#fafaf8;--card:#fff;--ink:#1d1d1b;--muted:#6b6b66;--line:#e4e4df;--good:#1f7a4d}
@media (prefers-color-scheme:dark){:root{--bg:#161615;--card:#1f1f1d;--ink:#ededea;--muted:#a3a39d;--line:#33332f;--good:#5fcf95}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,system-ui,sans-serif;padding:24px 16px}
main{max-width:1100px;margin:0 auto}h1{font-size:22px;margin:0 0 4px}p.sub{color:var(--muted);margin:0 0 24px}
section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:20px}
h2{font-size:16px;margin:0 0 12px}.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:700px){.cols{grid-template-columns:1fr}}
h3{font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin:0 0 6px}
.stats{font-size:13px;color:var(--muted);margin-bottom:8px}.after h3{color:var(--good)}
pre{white-space:pre-wrap;word-wrap:break-word;font:15px/1.55 -apple-system,system-ui,sans-serif;margin:0;border-top:1px solid var(--line);padding-top:10px}
</style></head><body><main><h1>stfu: before and after</h1>
<p class="sub">Same prompt, left without the skill, right with it.</p>
{cards}
</main></body></html>"""


def card(i, prompt, b, a):
    def col(cls, title, r):
        g, w, f = r[2]
        return (f'<div class="{cls}"><h3>{title}</h3><div class="stats">grade {g:.1f} \u00b7 {w} words \u00b7 {f} flags</div>'
                f'<pre>{html.escape(r[0])}</pre></div>')
    return (f'<section><h2>{i}. {html.escape(prompt)}</h2><div class="cols">'
            + col("before", "Before", b) + col("after", "After", a) + '</div></section>')


def main():
    prompts = [l.strip() for l in open(os.path.join(ROOT, "evals", "prompts.txt")) if l.strip()]
    rows, details, cards = [], [], []
    with tempfile.TemporaryDirectory() as cwd:
        for i, prompt in enumerate(prompts, 1):
            print(f"[{i}/{len(prompts)}] {prompt[:60]}")
            res = {}
            for arm, extra in ARMS.items():
                answer, used = run_claude(prompt, extra, cwd)
                res[arm] = (answer, used, score(answer))
            b, a = res["before"], res["after"]
            rows.append(f"| {i} | {b[2][0]:.1f} / {a[2][0]:.1f} | {b[2][1]} / {a[2][1]} | {b[2][2]} / {a[2][2]} | {'yes' if a[1] else 'NO'} |")
            details.append(f"## {i}. {prompt}\n\n### Before\n\n{b[0]}\n\n### After\n\n{a[0]}\n")
            cards.append(card(i, prompt, b, a))
    with open(OUT, "w") as f:
        f.write("# stfu: before and after\n\n")
        f.write("| # | Grade | Words | Checker flags | Skill used |\n|---|---|---|---|---|\n")
        f.write("\n".join(rows) + "\n\nEach cell is before / after.\n\n" + "\n".join(details))
    with open(HTML_OUT, "w") as f:
        f.write(PAGE.replace("{cards}", "\n".join(cards)))
    print(f"Wrote {OUT} and {HTML_OUT}")


if __name__ == "__main__":
    main()
