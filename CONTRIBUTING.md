# Deputizing

This outfit runs small on purpose: tailoring, gap analysis, outreach, and
tracking, done right, for one rider at a time, with no server and no wire
back to anybody. The contributions worth having extend that reach without
loosening those terms — read [`SKILL.md`](SKILL.md) for the code before
you propose a change to it.

## Good first jobs

- **Board integrations** — a reference doc (`references/boards/*.md`)
  showing how to pull postings from a specific board's *official* API or
  RSS feed, and how to hand the result to the skill as pasted text.
  Scraping HTML against a site's Terms of Service will not be merged —
  see "What doesn't ride" below.
- **Role-specific tailoring guides** — `references/tailoring-<field>.md`
  for trades with different resume conventions than software engineering
  (academic CVs, sales, design portfolios with visual samples). Follow
  the shape of `references/tailoring.md`: what's allowed to change, what
  must never change, grounded in a profile.yaml-like source.
- **Better keyword matching** — `scripts/_common.py`'s tokenizer is
  deliberately plain (see "Known limitations" in `references/ats.md`). A
  synonym map (`k8s` ↔ `Kubernetes`), stemming, or smarter bigram
  extraction are all welcome, as long as the method stays something you
  can explain to a stranger over a campfire — no opaque ML scoring that
  can't produce a one-line rationale.
- **Localization** — the stopword list in `scripts/_common.py` and the
  outreach patterns in `references/outreach.md` only speak English.
- **Tests** — `scripts/` currently has none beyond manual runs. Small,
  dependency-free tests (stdlib `unittest`, fixture posting text) are
  wanted.

## What doesn't ride

- Scraping that violates a job board's Terms of Service. If a board has
  no official API or feed, the answer is "the user pastes the posting,"
  not a scraper riding around the front gate.
- Anything that sends, applies, or posts on the user's behalf without an
  explicit review step. Every workflow in this skill ends in a draft.
- Telemetry, analytics, or network calls of any kind from `scripts/`.
  They work fully offline, off local files, full stop.
- Hardcoded personal data, sample resumes with real people's information,
  or anything that turns this into a hosted or multi-user service. It
  stays a one-rider, local-files skill.

## Working the code

The scripts are stdlib + PyYAML, no build step, no forge required:

```bash
pip install pyyaml
python3 scripts/score_fit.py --posting some_posting.txt --profile templates/profile.example.yaml --criteria templates/criteria.example.yaml
python3 scripts/gap_report.py --posting some_posting.txt --profile templates/profile.example.yaml
```

When you change scoring or gap logic, update `references/ats.md` to
match. The method doc and the code should never drift apart — that's
what keeps the score something a rider can check, not a black box he has
to trust on faith.

## Riding in with a change

- Keep `SKILL.md` under ~200 lines. If your change needs more room than
  that to explain, it belongs in a new or existing file under
  `references/`.
- One concern per pull request. A board integration and a tailoring
  guide are two PRs, not one saddled together.
- Say what you tested by hand — there's no CI riding shotgun here yet.
