# Hired Gun

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Agent Skill](https://img.shields.io/badge/Claude-Agent%20Skill-b8860b.svg)](https://code.claude.com/docs/en/claude-code-on-the-web)

*An Agent Skill for working the job-search frontier — grounded entirely
in a record you keep yourself.*

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

That's what this is. Below the frontier talk, it's an
[Agent Skill](https://code.claude.com/docs/en/claude-code-on-the-web):
fit scoring, resume tailoring, keyword-gap analysis, outreach drafting,
and application tracking, all running against flat files that live on
your machine, under your name, in your control.

## The job

1. **Make your mark** — parse your resume into `profile.yaml`, once.
2. **Read the poster** — paste a job posting, get a 0–100 fit score with
   one straight line of why.
3. **Load the right rounds** — rewrite your bullets to speak the
   posting's language, grounded strictly in `profile.yaml`. Nothing
   invented, not once.
4. **Count the saddlebags** — see which terms a posting wants that you
   don't have on record.
5. **Send word ahead** — draft a recruiter/hiring-manager message or
   cover note, under 120 words, ready for you to read over and send
   yourself.
6. **Keep the trail log** — log applications to `pipeline.md`, get
   nudged when a follow-up's gone quiet too long.

## The code

A hired gun works to a code, or they're just somebody with a gun. This
one's non-negotiable — it's written into [`SKILL.md`](SKILL.md) itself,
not just this README:

- **Never fabricate.** No invented experience, dates, titles, employers,
  or numbers. If a claim isn't in `profile.yaml`, it doesn't go in the
  draft — the gap gets flagged instead.
- **Draft only.** Nothing gets sent, submitted, or posted without you
  pulling the trigger yourself. Every workflow here ends in a draft, not
  an action.
- **No riding through fences.** No scraping that violates a board's
  Terms of Service. Paste the posting, or point this at an official
  API/feed. If neither exists, it says so instead of jumping the wire.
- **No telemetry.** Nothing calls home. Your record stays in your files.

## Strapping it on

Drop this repo into your skills folder:

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

## First ride (60 seconds)

1. Start a Claude session anywhere and say:
   > "Set up the hired-gun skill — here's my resume: [paste it]"

   Claude reads `SKILL.md`, builds `profile.yaml` from your resume and
   `criteria.yaml` from a few direct questions (pay floor, range you'll
   ride, dealbreakers), using `templates/*.example.yaml` as the pattern.

2. Find a posting and paste it in:
   > "Does this fit me?" [paste posting]

   Claude runs `scripts/score_fit.py` and hands you a score plus a
   one-line rationale — no ceremony.

3. If it's worth the ride:
   > "Tailor my resume for this" → grounded bullet rewrites, gaps flagged.
   > "What am I missing?" → `scripts/gap_report.py`'s keyword diff.
   > "Draft a note to the recruiter" → short, specific, ready to send.
   > "Log this in my pipeline" → a row appended to `pipeline.md`.

## A job worked, start to finish

**You:**
> Set up hired-gun. Here's my resume: [pastes a resume for a backend
> engineer, 6 years, mostly Python/AWS/payments work]

**Claude:** transcribes it into `profile.yaml` — your own wording, bullet
for bullet, nothing embellished — then asks a handful of direct
questions to fill in `criteria.yaml` (comp floor? remote/hybrid/onsite?
any lines you won't cross?), and confirms both files are saved.

**You:**
> Does this fit me? [pastes a "Senior Backend Engineer, remote, payments
> team, Python/Kafka/Postgres, Kubernetes a plus" posting]

**Claude:**
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

**You:** "What am I missing, and tailor my top 3 bullets for this."

**Claude:** runs the gap report (`kubernetes` isn't on record — flagged,
not faked), then rewrites three `profile.yaml` bullets to bring the
payments/event-driven/Kafka overlap up front, showing a before/after so
nothing sneaks past you unreviewed.

**You:** "Draft a note to whoever's hiring for this, and log it as
applied."

**Claude:** drafts a sub-120-word note that names the specific team and
one real, matching accomplishment — yours to send — and appends a row to
`pipeline.md` with today's date and a follow-up marker a week out.

## What's in the saddlebags

```
hired-gun/
  SKILL.md              # the code, and the workflow routing Claude follows
  templates/
    profile.example.yaml    # schema for your record
    criteria.example.yaml   # schema for your terms
    pipeline.example.md     # schema for your trail log
  references/
    tailoring.md         # how to rewrite bullets without inventing a scar
    outreach.md          # message patterns for recruiters / hiring managers
    ats.md               # the keyword-gap method, laid out in full
  scripts/
    score_fit.py         # posting vs. record → 0-100 + rationale
    gap_report.py        # posting vs. record → what's missing
  tests/
    test_scoring.py      # regression suite for the matching heuristics
  README.md
  CONTRIBUTING.md
  LICENSE                # MIT
```

See [`SKILL.md`](SKILL.md) for the full workflow routing Claude follows,
and [`references/`](references/) for the detailed method docs.

## Why we don't ride with a posse

It'd be tempting to have this thing go crawl the boards itself — pull
every posting in the territory, sort them, hand you a list. Don't believe
anyone who tells you that's simple. Board layouts change without notice,
scraping HTML in defiance of a site's Terms of Service is a fast way to
get your access revoked (or worse), and a crawler is the first thing in
any tool like this to rot the moment a site redesigns its listing page.

A skill that does tailoring, gap analysis, outreach, and tracking
exceptionally well — and lets you paste the poster yourself — stays
useful longer, breaks less, and is a lot easier for the next contributor
to reason about than one that's also secretly maintaining a scraper
army. So that's the trade this repo makes, on purpose: no discovery, no
crawling. You bring the posting. This does the rest.

## Deputize yourself

Board integrations (official APIs/feeds only), role-specific tailoring
guides, and sharper keyword matching are all wanted. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) before you ride out.

## The fine print

MIT — see [`LICENSE`](LICENSE). Take it, use it, fork it, sell your own
services around it. Just don't tell anyone it phones home, because it
doesn't.
