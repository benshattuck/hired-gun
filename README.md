# Hired Gun

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-b8860b.svg)](https://code.claude.com/docs/en/plugins)

*A Claude Code plugin for working the job-search frontier — grounded
entirely in a record you keep yourself.*

---

*The territory doesn't care what you did back east. Out here you're
worth what's in your ledger and what you can prove on the day. There's
no sheriff grading your resume against some rubric nailed to the wall of
the county office — there's a poster on a wall, and there's you, and
there's the gap between the two, and somebody's got to measure it
straight.*

*That's the job. Not to talk you up. Not to invent a scar you never
earned so the poster likes you better. To read the wanted notice, read
your record, and tell you plain whether the two make a fit — and if they
don't, exactly what's missing, so you can go get it or ride on.*

That's what this is. Below the frontier talk, it's a
[Claude Code plugin](https://code.claude.com/docs/en/plugins): eight
skills and one subagent, all running against flat files that live on
your machine, under your name, in your control.

## The outfit — eight skills, one subagent

Each is namespaced `hired-gun:<name>` once installed, and each loads on
its own — pick whichever one matches what you're doing, no need to work
through them in order:

| Skill | What it does |
|---|---|
| `onboard` | Parses a pasted resume into `profile.yaml` (the master bank every other skill reads from) and walks through `criteria.yaml`. One-time setup, revisited whenever your record or terms change. |
| `job-match-score` | Scores a pasted posting against `profile.yaml` + `criteria.yaml`, 0–100, with a one-line rationale — deterministic and auditable, not a black box. |
| `ats-check` | Diffs a posting's keywords against `profile.yaml` to show what an ATS scan would flag as covered vs. missing. |
| `tailor-resume` | Selects the best-fitting bullets from your master bank for a posting — **verbatim, no rewording, no reformatting** — and marks which real skills to lead with. Rewording is opt-in only, on request. |
| `interview-prep` | Likely questions for a posting, with STAR-style talking points sourced from real bullets — never an invented scenario. |
| `outreach` | Drafts a recruiter/hiring-manager message or cover note, under 120 words, draft only. |
| `pipeline-tracker` | Logs applications to `pipeline.md`, surfaces overdue follow-ups. |
| `job-search-automation` | Scans a small, curated set of official job APIs/feeds for postings matching your criteria and reports a ranked digest — runnable on demand or on a daily schedule. |

Plus **`job-scout`**, a subagent `job-search-automation` delegates the
actual fetching-and-scoring to. It runs on a lighter model (`haiku`) —
repetitive, tool-heavy work doesn't need the same model as tailoring or
interview coaching, and isolating it keeps a dozen raw API responses out
of your main conversation.

## The code

A hired gun works to a code, or they're just somebody with a gun. This
one's non-negotiable — the canonical version lives in
[`references/constraints.md`](references/constraints.md), and every
skill restates the piece that's load-bearing for it:

- **Never fabricate.** No invented experience, dates, titles, employers,
  or numbers. If a claim isn't in `profile.yaml`, it doesn't go in the
  output — the gap gets flagged instead.
- **Draft only.** Nothing gets sent, submitted, applied to, or posted
  without you pulling the trigger yourself — including
  `job-search-automation`, which finds and scores but never applies.
- **No riding through fences.** No scraping that violates a board's
  Terms of Service. `job-search-automation` works from a named list of
  official APIs/feeds (see [`references/boards.md`](references/boards.md)),
  a browser-automation MCP tool acting as your own session, or postings
  you paste directly.
- **No telemetry.** Nothing calls home, except the outbound fetches
  `job-search-automation` makes to the sources you configured — never
  anywhere else.

## Strapping it on

Drop this repo into your skills folder — Claude Code auto-loads any
folder there with a `.claude-plugin/plugin.json` as a plugin:

```bash
git clone https://github.com/benshattuck/hired-gun ~/.claude/skills/hired-gun
```

Or copy it into an existing skills checkout:

```bash
cp -r hired-gun ~/.claude/skills/hired-gun
```

The scripts need one thing on your belt:

```bash
pip install pyyaml
```

Restart Claude Code (or run `/reload-plugins`) and you should see it
listed as `hired-gun@skills-dir`.

## First ride (60 seconds)

1. Start a Claude Code session anywhere and say:
   > "Set up hired-gun — here's my resume: [paste it]"

   `onboard` builds `profile.yaml` from your resume — every bullet you've
   got, not just the ones that fit one page — and `criteria.yaml` from a
   few direct questions (pay floor, range you'll ride, dealbreakers).

2. Find a posting and paste it in:
   > "Does this fit me?" [paste posting]

   `job-match-score` hands you a score plus a one-line rationale — no
   ceremony.

3. If it's worth the ride:
   > "Tailor my resume for this" → best-fit bullets picked, verbatim.
   > "What am I missing?" → `ats-check`'s keyword diff.
   > "Help me prep for the interview" → `interview-prep`'s STAR talking points.
   > "Draft a note to the recruiter" → `outreach`, short and specific.
   > "Log this in my pipeline" → `pipeline-tracker` appends a row.
   > "Find me jobs today" → `job-search-automation` runs a scan.

## A job worked, start to finish

**You:**
> Set up hired-gun. Here's my resume: [pastes a resume for a backend
> engineer, 6 years, mostly Python/AWS/payments work]

**Claude (`onboard`):** transcribes it into `profile.yaml` — your own
wording, every bullet, nothing embellished — then asks a handful of
direct questions to fill in `criteria.yaml`, and confirms both files are
saved.

**You:**
> Does this fit me? [pastes a "Senior Backend Engineer, remote, payments
> team, Python/Kafka/Postgres, Kubernetes a plus" posting]

**Claude (`job-match-score`):**
```
Fit score: 81/100
  keyword coverage: 41/60 (10 matched terms)
  title/seniority match: 20/20 (Senior Backend Engineer, senior)
  location fit: 20/20 (posting mentions 'remote')
  nice-to-have bonus: +0 (none)

Rationale: 81/100 — strongest signal is title match (Senior Backend
Engineer, senior); biggest gap: posting wants 'kubernetes', not in
your profile
```

**You:** "What am I missing, and pick my best bullets for this."

**Claude (`ats-check`, then `tailor-resume`):** runs the gap report
(`kubernetes` isn't on record — flagged, not faked), then selects three
existing `profile.yaml` bullets per role that best match the posting —
unchanged, word for word — and marks Python/Kafka/PostgreSQL as the
skills to lead with.

**You:** "Help me prep, and draft a note to whoever's hiring for this."

**Claude (`interview-prep`, then `outreach`):** builds STAR talking
points for likely questions, each cited back to a specific bullet, then
drafts a sub-120-word note naming the specific team and one real
accomplishment — yours to send.

**You:** "Log it as applied, and find me more like this."

**Claude (`pipeline-tracker`, then `job-search-automation`):** appends a
row with today's date and a follow-up marker a week out, then hands the
scan off to `job-scout`, which checks your configured feeds and reports
back a ranked digest of new matches.

## What's in the saddlebags

```
hired-gun/
  .claude-plugin/
    plugin.json           # plugin manifest
  skills/
    onboard/SKILL.md
    job-match-score/SKILL.md
    ats-check/SKILL.md
    tailor-resume/SKILL.md
    interview-prep/SKILL.md
    outreach/SKILL.md
    pipeline-tracker/SKILL.md
    job-search-automation/SKILL.md
  agents/
    job-scout.md           # lighter-model subagent for feed scanning
  templates/
    profile.example.yaml    # schema for your master bank
    criteria.example.yaml   # schema for your terms
    pipeline.example.md     # schema for your trail log
    sources.example.yaml    # schema for job-search-automation's feed list
  references/
    constraints.md       # the canonical hard rules every skill answers to
    tailoring.md          # select-mode vs. opt-in reword-mode rules
    outreach.md           # message patterns for recruiters / hiring managers
    ats.md                # the keyword-gap method, laid out in full
    interview-prep.md     # STAR method without fabricating
    boards.md             # curated official job feeds/APIs
  scripts/
    score_fit.py          # posting vs. record → 0-100 + rationale
    gap_report.py          # posting vs. record → what's missing
    select_bullets.py      # posting vs. record → verbatim bullet picks
    _common.py             # shared matching logic (tokenizer, synonyms, negation)
  tests/
    test_scoring.py        # regression suite for the matching heuristics
  README.md
  CONTRIBUTING.md
  LICENSE                  # MIT
```

## Why job-search-automation doesn't crawl the boards

It'd be tempting to have this scan every board in the territory and hand
you a list. Don't believe anyone who tells you that's simple. Board
layouts change without notice, scraping HTML in defiance of a site's
Terms of Service is a fast way to get your access revoked (or worse), and
a general crawler is the first thing in any tool like this to rot.

So `job-search-automation` works from a short, named list of official
APIs/feeds instead — see [`references/boards.md`](references/boards.md)
for exactly which ones and why each is on the list. There's no
legitimate path to LinkedIn- or Indeed-breadth coverage without either a
paid enterprise API or a browser-automation tool acting as your own
logged-in session (also documented there). If a board you want has
neither, the honest answer is that it isn't covered yet.

## Deputize yourself

Board integrations (official APIs/feeds only), role-specific tailoring
guides, and sharper keyword matching are all wanted. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) before you ride out.

## The fine print

MIT — see [`LICENSE`](LICENSE). Take it, use it, fork it, sell your own
services around it. Just don't tell anyone it phones home, because it
doesn't — except for the one skill that fetches the feeds you told it to.
