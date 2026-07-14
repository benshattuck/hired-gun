#!/usr/bin/env python3
"""Read the wanted poster, weigh it against your record, give it back to you straight.

Usage:
    python score_fit.py --posting posting.txt
    cat posting.txt | python score_fit.py
    python score_fit.py --posting posting.txt --profile my/profile.yaml --criteria my/criteria.yaml

Output: a 0-100 fit score plus a one-line rationale and a short breakdown.
Pure heuristic keyword/criteria matching, no network calls, no oracle bones.
Method is documented in full in ../references/ats.md.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _common import load_yaml, posting_terms, profile_keywords, read_posting, substring_matches


def score_keyword_coverage(profile_kw: set[str], terms: list[str], text: str) -> tuple[int, set[str]]:
    if not terms:
        return 0, set()
    term_set = set(terms)
    matched = substring_matches(profile_kw, text) | (term_set & profile_kw)
    coverage = len(matched) / max(1, len(term_set))
    return round(min(1.0, coverage * 2.5) * 60), matched  # scaled: ~40% coverage -> full marks


def score_title_seniority(criteria: dict, text: str) -> tuple[int, list[str]]:
    lowered = text.lower()
    roles = criteria.get("roles", {}) or {}
    hits = []
    for phrase in (roles.get("titles") or []) + (roles.get("seniority") or []):
        if phrase and phrase.lower() in lowered:
            hits.append(phrase)
    return (20 if hits else 0), hits


def score_location(criteria: dict, text: str) -> tuple[int, str]:
    lowered = text.lower()
    loc = criteria.get("location", {}) or {}
    modes = [m.lower() for m in (loc.get("mode") or [])]
    for mode in modes:
        if mode in lowered:
            return 20, f"posting mentions '{mode}'"
    for city in loc.get("cities") or []:
        if city.lower() in lowered:
            return 15, f"posting mentions '{city}'"
    return 0, "no location signal matched"


_NEGATION_CUES = ("no ", "not ", "without ", "never ", "isn't", "doesn't", "won't", "don't")


def check_dealbreakers(criteria: dict, text: str) -> list[str]:
    # Split into sentences so a negation ("no on-call heavier than...") is
    # only checked against the clause it actually applies to.
    sentences = re.split(r"(?<=[.!?\n])\s+", text.lower())
    hits = []
    for phrase in criteria.get("dealbreakers") or []:
        # Only flag on a real keyword hit within the dealbreaker phrase,
        # since dealbreakers are written as constraints, not exact posting text.
        significant = [w for w in phrase.lower().split() if len(w) > 4]
        if not significant:
            continue
        for sentence in sentences:
            if not all(w in sentence for w in significant):
                continue
            # A negation cue in the same sentence means the posting is
            # stating the dealbreaker condition does NOT apply (e.g. "no
            # on-call heavier than 1 week/month") — that's compliant, not a hit.
            if any(cue in sentence for cue in _NEGATION_CUES):
                continue
            hits.append(phrase)
            break
    return hits


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posting", help="path to a text file with the job posting")
    parser.add_argument("--profile", default="profile.yaml")
    parser.add_argument("--criteria", default="criteria.yaml")
    args = parser.parse_args()

    text = read_posting(args.posting)
    profile = load_yaml(Path(args.profile))
    criteria = load_yaml(Path(args.criteria))

    profile_kw = profile_keywords(profile)
    terms = posting_terms(text)

    kw_score, matched = score_keyword_coverage(profile_kw, terms, text)
    title_score, title_hits = score_title_seniority(criteria, text)
    loc_score, loc_reason = score_location(criteria, text)
    dealbreaker_hits = check_dealbreakers(criteria, text)

    total = kw_score + title_score + loc_score
    if dealbreaker_hits:
        total = min(total, 20)  # floor, don't zero out — still show the rest of the signal

    total = max(0, min(100, total))

    print(f"Fit score: {total}/100")
    print(f"  keyword coverage: {kw_score}/60 ({len(matched)} matched terms)")
    print(f"  title/seniority match: {title_score}/20 ({', '.join(title_hits) or 'none'})")
    print(f"  location fit: {loc_score}/20 ({loc_reason})")
    if dealbreaker_hits:
        print(f"  DEALBREAKER(S) HIT: {', '.join(dealbreaker_hits)}")

    top_matches = ", ".join(sorted(matched)[:3]) or "little overlap"
    rationale = f"{total}/100 — {top_matches}"
    if dealbreaker_hits:
        rationale += f"; but hits dealbreaker: {dealbreaker_hits[0]}"
    elif loc_score == 0:
        rationale += "; location fit unclear from posting"
    print(f"\nRationale: {rationale}")


if __name__ == "__main__":
    main()
