---
name: job-match-score
description: >
  Scores how well a pasted or described job posting fits the user's
  profile.yaml and criteria.yaml — a 0-100 fit score with a one-line
  rationale, run via a deterministic, auditable heuristic (no black box).
  Use when the user pastes a posting and asks things like "does this fit
  me", "should I apply to this", "how good a match is this job", "score
  this posting", or "rate this against my criteria."
---

# Job Match Score

The user pastes a wanted poster. Run
`${CLAUDE_PLUGIN_ROOT}/scripts/score_fit.py` against their `profile.yaml`
+ `criteria.yaml`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/score_fit.py" --posting <path-or-heredoc> --profile profile.yaml --criteria criteria.yaml
```

If `profile.yaml` or `criteria.yaml` don't exist yet, hand off to the
`onboard` skill first — don't guess at either file's contents.

Report the 0–100 score and **one line** of rationale — the strongest
reason it fits, the biggest reason it doesn't, and any dealbreaker hit by
name. If the script can't run (no Python, missing PyYAML), work the same
method by hand rather than skipping straight to a gut-feel number — the
full method is in `${CLAUDE_PLUGIN_ROOT}/references/ats.md`, and it's
designed to be reproducible without the script.

A low score isn't necessarily a "don't apply" — surface it, then let the
user decide. If they want to close the gap, point them at `ats-check` for
the keyword diff or `tailor-resume` to see if reordering existing bullets
helps.
