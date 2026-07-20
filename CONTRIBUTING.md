# Deputizing

This is a Claude Code plugin, eight skills and one subagent, run for one
rider at a time, with no server and no wire back to anybody except the
sources `job-search-automation` is explicitly told to fetch. The
contributions worth having extend that reach without loosening those
terms — read [`references/constraints.md`](references/constraints.md)
for the code before you propose a change to any skill.

## Good first jobs

- **Board integrations** — extend
  [`references/boards.md`](references/boards.md) with another *official*
  API or feed, and add it to
  [`templates/sources.example.yaml`](templates/sources.example.yaml)'s
  schema. Scraping HTML against a site's Terms of Service will not be
  merged — see "What doesn't ride" below.
- **Role-specific tailoring guides** — `references/tailoring-<field>.md`
  for trades with different resume conventions than software engineering
  (academic CVs, sales, design portfolios with visual samples). Follow
  the shape of `references/tailoring.md`: select-mode first, reword-mode
  opt-in only, grounded in a profile.yaml-like source.
- **Better keyword matching** — `scripts/_common.py`'s tokenizer and
  `SYNONYMS` alias table are deliberately small (see "Known limitations"
  in `references/ats.md`). Extending the alias table, smarter stemming,
  or better bigram extraction are all welcome, as long as the method
  stays something you can explain to a stranger over a campfire — no
  opaque ML scoring that can't produce a one-line rationale.
- **Localization** — the stopword list in `scripts/_common.py` and the
  outreach patterns in `references/outreach.md` only speak English.
- **Tests** — a stdlib `unittest` suite lives in `tests/`; run it with
  `python3 -m unittest discover -s tests` from the repo root. Every case
  maps to a real bug or a design promise. Add one whenever you change the
  matching logic in `scripts/`.

## What doesn't ride

- Scraping that violates a job board's Terms of Service. If a board has
  no official API or feed, the answer is "the user pastes the posting,"
  not a scraper riding around the front gate — see `references/boards.md`
  for what's already covered and why.
- Anything that sends, applies, or posts on the user's behalf without an
  explicit review step. Every skill in this plugin ends in a draft or a
  report — including `job-search-automation`, which finds and scores but
  never applies.
- Telemetry, analytics, or network calls from anywhere except
  `job-search-automation`'s documented, opt-in fetches. Every other
  script works fully offline, off local files, full stop.
- Hardcoded personal data, sample resumes with real people's information,
  or anything that turns this into a hosted or multi-user service. It
  stays a one-rider, local-files plugin.

## Working the code

The scripts are stdlib + PyYAML, no build step, no forge required:

```bash
pip install pyyaml
python3 scripts/score_fit.py --posting some_posting.txt --profile templates/profile.example.yaml --criteria templates/criteria.example.yaml
python3 scripts/gap_report.py --posting some_posting.txt --profile templates/profile.example.yaml
python3 scripts/select_bullets.py --posting some_posting.txt --profile templates/profile.example.yaml
python3 -m unittest discover -s tests
```

When you change scoring or gap logic, update `references/ats.md` in the
same pull request. The method doc and the code should never drift apart —
that's what keeps the score something a rider can check, not a black box
they have to trust on faith.

To test the plugin as Claude Code actually loads it (not just the raw
scripts):

```bash
claude plugin validate . --strict
claude --plugin-dir . -p "list the skills and agents this plugin provides"
```

## Adding a new skill

- One skill, one job. If you're tempted to add a second unrelated
  workflow to an existing `SKILL.md`, it's a new skill under `skills/`
  instead.
- Keep each `SKILL.md` under ~150 lines. Route detail to a `references/`
  file rather than growing the skill file itself.
- Restate whichever piece of `references/constraints.md` is load-bearing
  for that skill (never-fabricate for anything touching `profile.yaml`,
  draft-only for anything producing outreach, no-riding-through-fences
  for anything that fetches network data) — don't make the reader hunt
  for it in a separate file for the invariant that matters most.
- If the skill needs a heavier or lighter model for a specific sub-task
  (batch/mechanical work vs. nuanced grounded writing), consider a
  dedicated subagent under `agents/` with its own `model` field, the way
  `job-search-automation` delegates to `job-scout` — rather than forcing
  one model choice on the whole conversation.

## Riding in with a change

- One concern per pull request. A board integration and a tailoring
  guide are two PRs, not one saddled together.
- Say what you tested by hand — there's no CI riding shotgun here yet.
