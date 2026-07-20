#!/usr/bin/env python3
"""Pick your best rounds for this job, verbatim — no rewording, no reformatting.

Usage:
    python select_bullets.py --posting posting.txt --profile profile.yaml
    python select_bullets.py --posting posting.txt --profile profile.yaml --max-per-role 4

For each role in profile.yaml, selects the existing bullets most relevant
to a posting — unchanged in wording — and separately reports which of the
profile's real skills to surface first, flagging when the posting uses a
known alias of a skill already on record (never a skill that isn't).
Nothing here rewrites a word; it only picks and groups what's already
true. Method in ../references/ats.md.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from _common import load_yaml, posting_terms, read_posting, substring_matches


def score_bullet(bullet: dict, text: str, posting_term_set: set[str]) -> int:
    """How many of a bullet's tags are wanted by the posting, directly or
    via a known alias (matched against the raw text so short aliases like
    "ts" are found even though the tokenizer drops them) — plus 1 if the
    bullet's own words also echo the posting's vocabulary."""
    tags = {t.lower() for t in bullet.get("tags", []) or []}
    tag_hits = len(substring_matches(tags, text))
    lowered_bullet = bullet.get("text", "").lower()
    text_hit = 1 if any(term in lowered_bullet for term in posting_term_set if len(term) > 4) else 0
    return tag_hits + text_hit


def select_for_role(bullets: list[dict], text: str, posting_term_set: set[str], max_per_role: int) -> tuple[list[dict], list[dict]]:
    """Returns (selected, left_out), both in original order. Falls back to
    the role's first bullets if nothing scores, so no role goes empty."""
    scores = [score_bullet(b, text, posting_term_set) for b in bullets]
    if not any(scores):
        keep = set(range(min(max_per_role, len(bullets))))
    else:
        ranked = sorted(range(len(bullets)), key=lambda i: (-scores[i], i))
        keep = set(ranked[:max_per_role])
    selected = [b for i, b in enumerate(bullets) if i in keep]
    left_out = [b for i, b in enumerate(bullets) if i not in keep]
    return selected, left_out


def format_skills_section(profile: dict, text: str) -> list[str]:
    """One line per skill category, each skill marked '*' if the posting
    wants it (directly or via a known alias, matched against the raw
    text) — grouping and wording both stay exactly as written in
    profile.yaml."""
    lines = []
    skills = profile.get("skills", {}) or {}
    for category, values in skills.items():
        if not isinstance(values, list):
            continue
        hits = substring_matches({s.lower() for s in values}, text)
        marked = [f"{s}*" if s.lower() in hits else s for s in values]
        lines.append(f"  {category}: {', '.join(marked)}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posting", help="path to a text file with the job posting")
    parser.add_argument("--profile", default="profile.yaml")
    parser.add_argument("--max-per-role", type=int, default=4, help="max bullets to keep per role")
    args = parser.parse_args()

    text = read_posting(args.posting)
    profile = load_yaml(Path(args.profile))
    posting_term_set = set(posting_terms(text))

    print(f"Selected bullets (verbatim, unchanged) — max {args.max_per_role} per role:\n")
    all_left_out = []
    for entry in profile.get("experience", []) or []:
        bullets = entry.get("bullets", []) or []
        selected, left_out = select_for_role(bullets, text, posting_term_set, args.max_per_role)
        header = f"{entry.get('company', '?')} — {entry.get('title', '?')}"
        print(header)
        for b in selected:
            print(f"  - {b.get('text', '')}")
        print()
        for b in left_out:
            all_left_out.append((header, b.get("text", "")))

    print("Skills section (grouped as in profile.yaml; * = this posting wants it, directly or via a known alias):")
    for line in format_skills_section(profile, text):
        print(line)

    if all_left_out:
        print("\nNot selected this time (still true, still on record):")
        for header, text_ in all_left_out:
            print(f"  - \"{text_}\" ({header})")


if __name__ == "__main__":
    main()
