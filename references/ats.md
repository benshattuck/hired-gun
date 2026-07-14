# Keyword-gap analysis method

This is the method `scripts/score_fit.py` and `scripts/gap_report.py`
work by, written out so you can run it by hand when the scripts aren't
handy, and so anyone can check the math.

It is deliberately a **heuristic keyword matcher**, not an oracle and not
an ML model. It's meant to be fast, plain, and auditable — you should
always be able to see exactly why a score came out the way it did. No
gunslinger worth hiring keeps their reasoning in a locked drawer.

**Keep this file and the scripts in lockstep.** If you change the code,
change this doc in the same pull request — the whole point of a method
doc is that it's true.

## Step 1: read the poster

From the pasted posting text (`sentence_tokens` + `posting_terms` in
`scripts/_common.py`):
1. Lowercase everything, and treat hyphens as spaces — "on-call" and
   "on call" are the same thing said two ways.
2. Split into sentences and clauses (on `.`, `!`, `?`, `;`, `:`, and
   newlines). Everything downstream is sentence-scoped.
3. Tokenize each sentence, stripping trailing periods so "Kafka." matches
   "kafka" (internal dots survive for "node.js"; `+` and `#` survive for
   c++ and c#).
4. Drop English stopwords, generic posting filler ("responsibilities",
   "excellent", "candidate"), and spelled-out numbers — see `STOPWORDS`.
5. Keep tokens of length ≥ 3, plus adjacent-word bigrams **within a
   sentence** ("machine learning", "error budget"). Bigrams never cross a
   sentence boundary — "…Kafka. Kubernetes…" must not mint the phantom
   skill "kafka kubernetes".
6. Also do a direct substring search for every phrase in the candidate's
   own `skills` + bullet `tags` (from `profile.yaml`) against the raw
   posting text — this catches multi-word skills a tokenizer would split
   apart ("event-driven architecture").

## Step 2: check the ledger

Flatten `profile.yaml`'s `skills.*` lists and every experience bullet's
`tags` into one lowercase set. This is the candidate's known trade — what
they can actually do, not what anyone claims at the bar.

## Step 3: match and diff

- **Matched** = posting terms found in the profile's keyword set (or vice
  versa via the substring pass in step 1.6).
- **Gap** = posting terms with no match, after two noise filters
  (`uncovered_terms`): a term appearing as a whole word inside a matched
  keyword isn't a gap ("backend" is covered by "senior backend engineer" —
  though "java" is *not* covered by "javascript"), and a bigram is
  dropped when either of its words is covered, since its uncovered half
  is already reported alone. What survives is ranked by how often the
  posting says it — frequency is a weak but free proxy for how much the
  outfit cares.
- **Coverage** = `len(matched) / len(posting_terms)`, the fraction of the
  posting's vocabulary the profile already speaks.

## Step 4: criteria phrases — dealbreakers and nice-to-haves

Dealbreakers and nice-to-haves in `criteria.yaml` are matched by the same
rule (`phrase_hits`):

1. Reduce the criteria phrase to its **significant word-stems** — words
   of 4+ letters, minus stopwords, run through a crude suffix-stripping
   stemmer so "requires", "required", and "require" all land on one stem.
2. A phrase hits when every significant stem appears in a **single
   sentence** of the posting…
3. …unless a negation token ("no", "not", "never", "without", "don't")
   sits within the two tokens just before the first matched word. So *"no
   on-call heavier than one week per month"* reads as a promise kept,
   while *"we don't sugarcoat it: on-call is heavier…"* — negation in a
   different clause — is still flagged.

Write criteria phrases short and concrete ("small team", "error budget",
"requires security clearance"); every extra word is another word the
posting must contain before the phrase can hit.

## Step 5: score components (`score_fit.py`)

The 0–100 score is a sum of capped components, not a black box you take
on faith:

| Component | Points | Signal |
|---|---|---|
| Keyword coverage | up to 60 | `coverage` from Step 3, scaled (~40% coverage → full marks) |
| Title/seniority match | 20 or 0 | any of `criteria.roles.titles` / `seniority` found in the posting |
| Location fit | up to 20 | posting's stated mode (remote/hybrid/onsite), or 15 for a city match, against `criteria.location` |
| Nice-to-have bonus | +2 each, max +6 | phrases from `criteria.nice_to_haves` the posting affirmatively states |
| Dealbreaker penalty | floors the score at 20 | any `criteria.dealbreakers` phrase the posting affirmatively states |

The rationale line names the strongest component and the single biggest
gap — the most-mentioned uncovered term, excluding things the criteria
already say you *want* (a posting saying "remote" answers your location
preference; it isn't a skill gap). Ties break toward single words, then
longer ones, so "kubernetes" beats both "month" and a leftover bigram.
E.g.:

> *81/100 — strongest signal is title match (Senior Backend Engineer,
> senior); biggest gap: posting wants 'kubernetes', not in your profile*

## Known limitations (good first contributions)

- Stemming is crude suffix-stripping, and there's no synonym map — "k8s"
  and "Kubernetes" still don't match. A small synonym table would help;
  see `CONTRIBUTING.md`.
- Bigram extraction is naive within a sentence; it doesn't understand
  phrase boundaries.
- Location parsing is a simple string search, not a geocoder — city
  matches must appear roughly as written in `criteria.yaml`.
- The negation window is two tokens; unusual phrasing can slip past it in
  either direction.
- No language other than English is supported by the stopword list yet.

Regression tests for the behaviors above live in `tests/test_scoring.py` —
run `python3 -m unittest discover -s tests` from the repo root, and add a
case whenever you change the matching logic.
