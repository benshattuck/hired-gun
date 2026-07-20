"""Shared helpers for score_fit.py and gap_report.py.

Pure standard library plus PyYAML (the one runtime dependency). No network
calls, no telemetry — everything here reads local files only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit(
        "Missing dependency: PyYAML.\n"
        "Install it with:  pip install pyyaml"
    )

STOPWORDS = {
    "a", "ability", "able", "about", "all", "an", "and", "any", "are",
    "as", "at", "based", "be", "big", "but", "by", "can", "candidate",
    "candidates", "company", "description", "environment", "etc",
    "excellent", "expected", "experience", "for", "from", "fully", "has",
    "have", "how", "ideal", "in", "including", "into", "is", "it", "its",
    "job", "join", "looking", "more", "most", "not", "of", "on", "or",
    "other", "our", "per", "plus", "preferred", "qualifications",
    "required", "requirements", "responsibilities", "role", "strong",
    "such", "team", "than", "that", "the", "their", "these", "they",
    "this", "those", "to", "us", "use", "used", "using", "we", "what",
    "when", "where", "who", "why", "will", "with", "work", "working",
    "year", "years", "you", "your",
    # spelled-out numbers are never skills
    "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten",
}

# Tokens that flip a phrase's meaning when they sit just before it —
# "no on-call" is a promise, not a warning. Apostrophes split in the
# tokenizer, so "don't" arrives as "don".
NEGATION_TOKENS = {
    "no", "not", "never", "without", "non", "cannot",
    "don", "doesn", "isn", "won", "aren", "wasn", "shouldn",
}

# A small, curated alias map — not a general synonym engine. Each entry
# is a shorthand/alternate spelling that ATS scans and postings routinely
# use interchangeably with the canonical form. Extend this list rather
# than inventing a bigger NLP pipeline; see CONTRIBUTING.md.
SYNONYMS = {
    "k8s": "kubernetes",
    "js": "javascript",
    "ts": "typescript",
    "postgres": "postgresql",
    "py": "python",
    "golang": "go",
    "csharp": "c#",
    "node": "node.js",
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "ml": "machine learning",
    "ci/cd": "continuous integration",
}


def canonical_terms(term: str) -> set[str]:
    """A term's own form plus any known alias/canonical counterpart.

    "k8s" -> {"k8s", "kubernetes"}; "kubernetes" -> {"kubernetes", "k8s"}.
    Used so a profile tag and a posting's wording match each other even
    when they're not the same string, without pretending this is a real
    synonym engine.
    """
    t = term.lower().strip()
    out = {t}
    if t in SYNONYMS:
        out.add(SYNONYMS[t])
    for alias, canon in SYNONYMS.items():
        if canon == t:
            out.add(alias)
    return out

_SENTENCE_RE = re.compile(r"(?<=[.!?\n;:])\s+")
_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+.#]*")


def load_yaml(path: Path) -> dict:
    if not path.exists():
        sys.exit(
            f"Missing file: {path}\n"
            f"Copy templates/{path.name.replace('.yaml', '.example.yaml')} "
            f"to {path.name} and fill it in."
        )
    with path.open() as f:
        return yaml.safe_load(f) or {}


def flatten(value: Any) -> list[str]:
    """Recursively pull every string out of nested dict/list structures."""
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for v in value.values():
            out.extend(flatten(v))
    elif isinstance(value, list):
        for v in value:
            out.extend(flatten(v))
    return out


def profile_keywords(profile: dict) -> set[str]:
    """Flatten profile.yaml's skills + bullet tags into a lowercase set."""
    keywords: set[str] = set()
    for term in flatten(profile.get("skills", {})):
        keywords.add(term.strip().lower())
    for entry in profile.get("experience", []) or []:
        for bullet in entry.get("bullets", []) or []:
            for tag in bullet.get("tags", []) or []:
                keywords.add(tag.strip().lower())
        if entry.get("title"):
            keywords.add(entry["title"].strip().lower())
    return {k for k in keywords if k}


def stem(word: str) -> str:
    """Crude suffix-stripping stemmer — just enough that "requires",
    "required", and "require" land on the same stem. Not linguistics,
    plumbing."""
    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            word = word[: -len(suffix)]
            break
    if word.endswith("e") and len(word) >= 4:
        word = word[:-1]
    return word


def sentence_tokens(text: str) -> list[list[str]]:
    """Lowercase, split into sentences/clauses, tokenize each.

    Hyphens become spaces so "on-call" and "on call" match each other;
    trailing periods are stripped so "Kafka." matches "kafka" (while
    "node.js" keeps its internal dot). "+" and "#" survive for c++ / c#.
    """
    lowered = text.lower().replace("-", " ")
    sentences = _SENTENCE_RE.split(lowered)
    return [[t.rstrip(".") for t in _TOKEN_RE.findall(s)] for s in sentences]


def posting_terms(text: str) -> list[str]:
    """Tokenize posting text into significant unigrams + bigrams.

    Bigrams are built within a sentence only — "…Kafka. Kubernetes…" must
    not produce the phantom term "kafka kubernetes".
    """
    terms: list[str] = []
    for tokens in sentence_tokens(text):
        words = [w for w in tokens if len(w) >= 3 and w not in STOPWORDS]
        terms.extend(words)
        terms.extend(f"{a} {b}" for a, b in zip(words, words[1:]))
    return terms


def significant_stems(phrase: str) -> set[str]:
    """The stems of a criteria phrase's load-bearing words."""
    words = _TOKEN_RE.findall(phrase.lower().replace("-", " "))
    return {stem(w) for w in words if len(w) >= 4 and w not in STOPWORDS}


def phrase_hits(phrases: list[str] | None, text: str) -> list[str]:
    """Which criteria phrases the posting affirmatively states.

    A phrase hits when every one of its significant word-stems appears in
    a single sentence/clause of the posting, and no negation token sits
    within the two tokens just before the first matched word. So "no
    on-call heavier than one week per month" reads as a promise kept,
    while "we don't sugarcoat it: on-call is heavier…" (negation in a
    different clause) is still flagged.
    """
    all_sentences = sentence_tokens(text)
    hits: list[str] = []
    for phrase in phrases or []:
        wanted = significant_stems(phrase)
        if not wanted:
            continue
        for tokens in all_sentences:
            stems = [stem(t) for t in tokens]
            if not wanted.issubset(set(stems)):
                continue
            first = min(i for i, s in enumerate(stems) if s in wanted)
            window = tokens[max(0, first - 2):first]
            if any(w in NEGATION_TOKENS for w in window):
                continue
            hits.append(phrase)
            break
    return hits


def substring_matches(keywords: set[str], text: str) -> set[str]:
    """Keywords (possibly multi-word) that appear in text, verbatim or via
    a known alias (see SYNONYMS) — "kubernetes" matches text containing
    only "k8s", and vice versa.

    Matching is word-boundary-based, not naive substring: "java" does not
    match text that only says "javascript", and a short alias like "ts"
    does not match inside "tests" or "posts".
    """
    lowered = text.lower()
    hits = set()
    for k in keywords:
        if not k:
            continue
        for variant in canonical_terms(k):
            if re.search(rf"\b{re.escape(variant)}\b", lowered):
                hits.add(k)
                break
    return hits


def uncovered_terms(terms: list[str], covered_by: set[str]) -> dict[str, int]:
    """Posting terms with no echo in the covered set, with their counts.

    A term appearing as a whole word inside a covered phrase is not a gap
    ("backend" is covered by "senior backend engineer"; "seattle" by
    "seattle, wa") — but a bare substring is ("java" is NOT covered by
    "javascript"). A bigram is dropped when either of its words is
    covered: it carries no information beyond its uncovered half, which
    is already reported on its own.
    """
    from collections import Counter

    counts = Counter(terms)
    cache: dict[str, bool] = {}

    def word_covered(term: str) -> bool:
        if term not in cache:
            variants = canonical_terms(term)
            if variants & covered_by:
                cache[term] = True
            else:
                patterns = [re.compile(rf"\b{re.escape(v)}\b") for v in variants]
                cache[term] = any(p.search(c) for p in patterns for c in covered_by)
        return cache[term]

    gaps: dict[str, int] = {}
    for term, count in counts.items():
        parts = term.split(" ")
        if word_covered(term) or any(word_covered(p) for p in parts):
            continue
        gaps[term] = count
    return gaps


def read_posting(arg_path: str | None) -> str:
    if arg_path:
        return Path(arg_path).read_text()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    sys.exit("No posting text given. Pass --posting <file> or pipe text on stdin.")
