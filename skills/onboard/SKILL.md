---
name: onboard
description: >
  Sets up a rider's job-search records for the first time: parses a pasted
  resume into profile.yaml (the master bank every other hired-gun skill
  reads from) and walks through criteria.yaml (target roles, comp floor,
  location, dealbreakers). Use when profile.yaml doesn't exist yet in the
  working directory, or when the user says things like "set up hired-gun",
  "here's my resume", "help me start a job search", or "my resume/criteria
  changed, update it." Do not use once profile.yaml already exists and is
  current — route to the specific skill (job-match-score, tailor-resume,
  ats-check, interview-prep, job-search-automation) the user actually wants.
---

# Onboard

If `profile.yaml` doesn't exist yet, the rider hasn't got a record on
file. Open one:

1. Ask the user to paste their resume (text or file).
2. Map it into `${CLAUDE_PLUGIN_ROOT}/templates/profile.example.yaml`'s
   structure and save as `profile.yaml` in the user's working directory.
   **Put in every bullet you're given, not just the ones that would fit
   on one page** — `profile.yaml` is the master bank the `tailor-resume`
   skill selects from, not a resume itself. Keep the user's original
   wording; you're a scribe here, not a novelist.
3. Walk them through `${CLAUDE_PLUGIN_ROOT}/templates/criteria.example.yaml`
   → save as `criteria.yaml`. Ask straight for the pay floor, the range
   they'll ride, and the dealbreakers. Don't guess at another rider's
   terms.
4. Create `pipeline.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/pipeline.example.md` if they want a
   trail log (see the `pipeline-tracker` skill).

Re-open the record (or edit it) whenever the user says their resume or
terms changed. A stale ledger gets people shot at in this line of work —
every other skill in this plugin trusts what's in these two files.

**Never fabricate** while transcribing: preserve wording, don't round up
metrics, don't add a skill the resume didn't mention. Full rules in
`${CLAUDE_PLUGIN_ROOT}/references/constraints.md`.
