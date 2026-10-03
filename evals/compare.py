#!/usr/bin/env python3
"""Before and after test for the stfu skill.

Runs each prompt in evals/prompts.txt twice with Claude Code:
  before: no skills at all
  after:  only the stfu skill from this repo
Then scores both answers with the checker and writes evals/results.md.

Usage: python3 evals/compare.py
Needs the `claude` CLI, logged in.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "skills", "stfu", "scripts", "check.py")
OUT = os.path.join(ROOT, "evals", "results.md")

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


def main():
    prompts = [l.strip() for l in open(os.path.join(ROOT, "evals", "prompts.txt")) if l.strip()]
    rows, details = [], []
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
    with open(OUT, "w") as f:
        f.write("# stfu: before and after\n\n")
        f.write("| # | Grade | Words | Checker flags | Skill used |\n|---|---|---|---|---|\n")
        f.write("\n".join(rows) + "\n\nEach cell is before / after.\n\n" + "\n".join(details))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
