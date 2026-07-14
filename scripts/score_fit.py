#!/usr/bin/env python3
"""Read the wanted poster, weigh it against your record, give it back to you straight.

Usage:
    python score_fit.py --posting posting.txt
    cat posting.txt | python score_fit.py
    python score_fit.py --posting posting.txt --profile my/profile.yaml --criteria my/criteria.yaml

Output: a 0-100 fit score plus a one-line rationale and a short breakdown.
Pure heuristic keyword/criteria matching, no network calls, no divining
rods. Method is documented in full in ../references/ats.md.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from _common import (
    load_yaml,
    phrase_hits,
    posting_terms,
    profile_keywords,
    read_posting,
    substring_matches,
    uncovered_terms,
)


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
    for mode in loc.get("mode") or []:
        if mode.lower() in lowered:
            return 20, f"posting mentions '{mode.lower()}'"
    for city in loc.get("cities") or []:
        if city.lower() in lowered:
            return 15, f"posting mentions '{city}'"
    return 0, "no location signal matched"


def check_dealbreakers(criteria: dict, text: str) -> list[str]:
    return phrase_hits(criteria.get("dealbreakers"), text)


def score_nice_to_haves(criteria: dict, text: str) -> tuple[int, list[str]]:
    """+2 per nice-to-have the posting affirmatively mentions, capped at +6."""
    hits = phrase_hits(criteria.get("nice_to_haves"), text)
    return min(6, 2 * len(hits)), hits


def criteria_known_wants(criteria: dict) -> set[str]:
    """Phrases from criteria.yaml the user already told us they want —
    a posting mentioning "remote" or "Senior Engineer" isn't revealing a
    skill gap, it's answering the criteria."""
    roles = criteria.get("roles", {}) or {}
    loc = criteria.get("location", {}) or {}
    phrases = (
        (roles.get("titles") or [])
        + (roles.get("seniority") or [])
        + (loc.get("mode") or [])
        + (loc.get("cities") or [])
        + (criteria.get("nice_to_haves") or [])
    )
    return {p.lower() for p in phrases if p}


def biggest_gap(terms: list[str], covered_by: set[str]) -> str | None:
    """The most-mentioned posting term with no echo in the covered set.

    Ties break toward single words, then longer ones — "kubernetes"
    should beat both "month" and a leftover bigram.
    """
    gaps = uncovered_terms(terms, covered_by)
    if not gaps:
        return None
    return max(gaps, key=lambda t: (gaps[t], " " not in t, len(t)))


def build_rationale(
    total: int,
    kw_score: int,
    matched: set[str],
    title_score: int,
    title_hits: list[str],
    loc_score: int,
    loc_reason: str,
    gap: str | None,
    dealbreaker_hits: list[str],
    nice_hits: list[str],
) -> str:
    """One line: the strongest signal, the biggest gap, any dealbreaker."""
    if dealbreaker_hits:
        return f"{total}/100 — posting hits your dealbreaker: {dealbreaker_hits[0]}"

    components = [
        (kw_score / 60, f"keyword overlap ({', '.join(sorted(matched)[:3]) or 'none'})"),
        (title_score / 20, f"title match ({', '.join(title_hits[:2])})" if title_hits else "no title match"),
        (loc_score / 20, f"location fit ({loc_reason})"),
    ]
    strength, desc = max(components, key=lambda c: c[0])
    lead = f"strongest signal is {desc}" if strength > 0 else "little signal on any front"

    parts = [f"{total}/100 — {lead}"]
    if gap:
        parts.append(f"biggest gap: posting wants '{gap}', not in your profile")
    if nice_hits:
        parts.append(f"bonus: {', '.join(nice_hits[:2])}")
    return "; ".join(parts)


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
    nice_bonus, nice_hits = score_nice_to_haves(criteria, text)
    dealbreaker_hits = check_dealbreakers(criteria, text)
    gap = biggest_gap(terms, matched | criteria_known_wants(criteria))

    total = kw_score + title_score + loc_score + nice_bonus
    if dealbreaker_hits:
        total = min(total, 20)  # floor, don't zero out — still show the rest of the signal

    total = max(0, min(100, total))

    print(f"Fit score: {total}/100")
    print(f"  keyword coverage: {kw_score}/60 ({len(matched)} matched terms)")
    print(f"  title/seniority match: {title_score}/20 ({', '.join(title_hits) or 'none'})")
    print(f"  location fit: {loc_score}/20 ({loc_reason})")
    print(f"  nice-to-have bonus: +{nice_bonus} ({', '.join(nice_hits) or 'none'})")
    if dealbreaker_hits:
        print(f"  DEALBREAKER(S) HIT: {', '.join(dealbreaker_hits)}")

    rationale = build_rationale(
        total, kw_score, matched, title_score, title_hits,
        loc_score, loc_reason, gap, dealbreaker_hits, nice_hits,
    )
    print(f"\nRationale: {rationale}")


if __name__ == "__main__":
    main()
