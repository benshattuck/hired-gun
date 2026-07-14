# Keyword-gap analysis method

This is the method `scripts/score_fit.py` and `scripts/gap_report.py`
work by, written out so you can run it by hand when the scripts aren't
handy, and so it's easy to check a man's math.

It is deliberately a **heuristic keyword matcher**, not an oracle and not
an ML model. It's meant to be fast, plain, and auditable — you should
always be able to see exactly why a score came out the way it did. No
gunslinger worth hiring keeps his reasoning in a locked drawer.

## Step 1: read the poster

From the pasted posting text:
1. Lowercase everything.
2. Strip punctuation, split on whitespace.
3. Drop English stopwords and generic filler ("responsibilities",
   "team", "environment", "strong", "excellent" — see `STOPWORDS` in
   `scripts/_common.py`).
4. Keep tokens of length ≥ 3, plus adjacent-word bigrams ("machine
   learning", "on call") since a lot of the signal is in two-word terms.
5. Also do a direct substring search for every phrase in the candidate's
   own `skills` + bullet `tags` (from `profile.yaml`) against the raw
   posting text — this catches multi-word skills a naive tokenizer would
   split apart ("event-driven architecture").

## Step 2: check the ledger

Flatten `profile.yaml`'s `skills.*` lists and every experience bullet's
`tags` into one lowercase set. This is the candidate's known trade — what
he can actually do, not what he claims at the bar.

## Step 3: match and diff

- **Matched** = posting terms found in the profile's keyword set (or vice
  versa via the substring pass in step 1.5).
- **Gap** = posting terms with no match — these are what `gap_report.py`
  prints, ranked by how often they show up in the posting (frequency is a
  weak but free proxy for how much the outfit cares).
- **Coverage** = `len(matched) / len(posting_terms)`, the fraction of the
  posting's vocabulary the profile already speaks.

## Step 4: score components (`score_fit.py`)

The 0–100 score is a sum of capped components, not a black box you take
on faith:

| Component | Max points | Signal |
|---|---|---|
| Keyword coverage | 60 | `coverage` from Step 3, scaled |
| Title/seniority match | 20 | any of `criteria.roles.titles` / `seniority` found in the posting |
| Location fit | 20 | posting's stated mode (remote/hybrid/onsite) and city against `criteria.location` |
| Dealbreaker penalty | floors the score | any phrase in `criteria.dealbreakers` clearly matched in the posting text |

The rationale line is generated from whichever component moved the score
most, plus the single biggest gap term — e.g. *"78/100 — strong keyword
overlap (Python, event-driven, payments) and remote-first, but posting
wants Kubernetes which isn't in your profile."*

## Known limitations (good first contributions)

- Pure keyword matching misses synonyms the tokenizer doesn't know about
  ("k8s" vs "Kubernetes"). A small synonym map would help — see
  `CONTRIBUTING.md`.
- Bigram extraction is naive; it doesn't understand phrase boundaries.
- Location parsing is a simple string search, not a geocoder — city
  matches must appear roughly as written in `criteria.yaml`.
- No language other than English is supported by the stopword list yet.
