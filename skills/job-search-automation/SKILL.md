---
name: job-search-automation
description: >
  Scans a small, curated set of official job APIs/feeds (see
  sources.yaml and references/boards.md) for postings matching the
  user's criteria.yaml, scores them, and reports a ranked digest —
  designed to be run on demand or on a daily schedule. Use when the user
  asks things like "find me jobs today", "run my job search", "what's
  new that matches my criteria", or "set up a daily job search." Never
  scrapes a board's search-results pages and never applies to anything —
  it only finds and scores, always as a report for the user to act on.
---

# Job Search Automation

This is the one skill in the plugin that makes outbound network
requests. It only fetches the specific official endpoints documented in
`${CLAUDE_PLUGIN_ROOT}/references/boards.md`, never a general web search
or a board's own search-results HTML. Full rule in
`${CLAUDE_PLUGIN_ROOT}/references/constraints.md`.

## First run: set up sources

If `sources.yaml` doesn't exist, walk the user through
`${CLAUDE_PLUGIN_ROOT}/templates/sources.example.yaml` — which companies
on Greenhouse/Lever to watch, whether to include RemoteOK, We Work
Remotely categories, HN's monthly thread, USAJobs. Start small; it's easy
to add more sources later. If `profile.yaml`/`criteria.yaml` don't exist
either, hand off to `onboard` first.

## Running a scan

Delegate the fetch-and-score work to the `job-scout` agent rather than
doing it inline — it's a repetitive, tool-heavy task that runs fine on a
lighter model, and keeps a dozen raw API responses out of the main
conversation's context. `job-scout` reports back a ranked digest.

Present the digest to the user plainly: top matches first, with score
and one-line rationale each, any dealbreaker hits called out separately.
Ask if they want any of them logged to `pipeline.md` (usually yes for
anything above a score the user considers worth pursuing) — `job-scout`
may have already appended new ones as `researching`; confirm rather than
duplicating.

## Setting up a daily run

The scan itself is the same either way; only the trigger differs by
environment:

**Claude Code Remote / Cowork sessions**: this environment can schedule
a recurring Routine that fires a prompt into a session daily. Set one up
with a prompt like *"Run job-search-automation's scan and report the
digest"* — but only in a session/environment where `profile.yaml`,
`criteria.yaml`, and `sources.yaml` actually live; a routine that fires
into a fresh environment with no data to read isn't useful. If the user's
data lives in a private location, make sure the routine fires into a
session that can reach it, not a public repo.

**Local Claude Code CLI**: a cron entry invoking Claude non-interactively
from the directory holding the user's data files, e.g.:

```cron
0 8 * * * cd ~/job-search && claude -p "Run job-search-automation's scan and report the digest" >> ~/job-search/digest.log 2>&1
```

Either way, this plugin never sets up the schedule itself — scheduling is
a host-environment capability, not something a skill can create on its
own. Walk the user through whichever path matches where they're running
Claude, and confirm the schedule is actually reaching their real data
files before calling it done.

## What this skill never does

- Never applies to anything, never submits a form, never sends outreach —
  it finds and scores, nothing more.
- Never fetches outside the documented endpoints in `references/boards.md`.
- Never runs a browser-automation MCP tool unattended in a loop; that
  path (see `references/boards.md`) is for an explicit, human-present or
  human-requested run, not silent daily automation.
