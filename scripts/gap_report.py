#!/usr/bin/env python3
"""Count what's missing from your saddlebags before you ride into town.

Usage:
    python gap_report.py --posting posting.txt
    cat posting.txt | python gap_report.py
    python gap_report.py --posting posting.txt --profile my/profile.yaml

Prints keywords the posting wants that the profile doesn't currently
cover, ranked by frequency in the posting text, plus the ones that already
match for confirmation. Method documented in ../references/ats.md.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from _common import (
    load_yaml,
    posting_terms,
    profile_keywords,
    read_posting,
    substring_matches,
    uncovered_terms,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posting", help="path to a text file with the job posting")
    parser.add_argument("--profile", default="profile.yaml")
    parser.add_argument("--top", type=int, default=15, help="max gap terms to print")
    args = parser.parse_args()

    text = read_posting(args.posting)
    profile = load_yaml(Path(args.profile))
    profile_kw = profile_keywords(profile)

    terms = posting_terms(text)
    counts = Counter(terms)

    matched_via_profile = substring_matches(profile_kw, text)
    matched = {t for t in counts if t in profile_kw} | matched_via_profile

    gaps = uncovered_terms(terms, matched)
    gap_ranked = sorted(gaps, key=lambda t: (-gaps[t], t))[: args.top]

    coverage = len(matched) / max(1, len(set(terms)))

    print(f"Coverage: {coverage:.0%} of posting terms found in profile.yaml\n")

    print("Covered (already in your profile):")
    if matched:
        for term in sorted(matched):
            print(f"  - {term}")
    else:
        print("  (none matched)")

    print("\nGaps (posting mentions, profile doesn't):")
    if gap_ranked:
        for term in gap_ranked:
            print(f"  - {term}  (mentioned {counts[term]}x)")
    else:
        print("  (no significant gaps found)")

    print(
        "\nA gap here doesn't mean you're unqualified — it means the term "
        "isn't in profile.yaml yet. Add it if it's real; otherwise it's a "
        "genuine skill gap worth knowing about before you apply."
    )


if __name__ == "__main__":
    main()
