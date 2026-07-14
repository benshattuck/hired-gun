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
    "the", "and", "for", "with", "you", "your", "our", "are", "will",
    "have", "has", "this", "that", "from", "who", "what", "when", "where",
    "why", "how", "all", "any", "can", "who", "team", "role", "work",
    "working", "years", "year", "strong", "excellent", "ability", "able",
    "including", "etc", "such", "into", "using", "use", "used", "per",
    "environment", "responsibilities", "requirements", "qualifications",
    "about", "join", "company", "we", "us", "our", "job", "description",
    "preferred", "required", "plus", "a", "an", "of", "in", "on", "to",
    "is", "as", "or", "be", "at", "by", "it", "its", "their", "they",
    "these", "those", "other", "more", "most", "than", "not", "but",
}


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


_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+.#-]*")


def posting_terms(text: str) -> list[str]:
    """Tokenize posting text into significant unigrams + bigrams."""
    words = [w for w in _TOKEN_RE.findall(text.lower()) if len(w) >= 3]
    words = [w for w in words if w not in STOPWORDS]
    bigrams = [f"{a} {b}" for a, b in zip(words, words[1:])]
    return words + bigrams


def substring_matches(keywords: set[str], text: str) -> set[str]:
    """Keywords (possibly multi-word) that appear verbatim in text."""
    lowered = text.lower()
    return {k for k in keywords if k and k in lowered}


def read_posting(arg_path: str | None) -> str:
    if arg_path:
        return Path(arg_path).read_text()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    sys.exit("No posting text given. Pass --posting <file> or pipe text on stdin.")
