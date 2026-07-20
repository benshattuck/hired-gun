---
name: pipeline-tracker
description: >
  Logs job applications to a pipeline.md tracking table and surfaces
  overdue follow-ups. Use when the user says things like "log this
  application", "add this to my pipeline", "what's overdue", "what do I
  need to follow up on", or "update the status on <company>."
---

# Pipeline Tracker

If `pipeline.md` doesn't exist yet, create it from
`${CLAUDE_PLUGIN_ROOT}/templates/pipeline.example.md` in the user's
working directory.

**Log:** append a row — company, role, date applied, status, fit score
(if `job-match-score` has run for this posting), link, next action,
follow-up date. Status values: `researching` · `applied` · `screening` ·
`interviewing` · `offer` · `rejected` · `withdrawn`.

**Update:** when the user reports a status change (interview scheduled,
rejection, offer), edit that row in place rather than appending a new
one for the same application.

**"What's overdue":** scan the Follow-up column for dates already past
where the Status hasn't moved since. List them plainly — company, role,
how overdue, and what the Next Action says.

This file is the one place `job-search-automation` also writes to (new
postings it finds get logged as `researching`) — see that skill for how
the two connect.
