---
name: ats-check
description: >
  Diffs a job posting's keywords against the user's profile.yaml to show
  what an ATS (applicant tracking system) keyword scan would flag as
  covered vs. missing. Use when the user asks things like "what am I
  missing for this role", "will this pass an ATS scan", "keyword gap
  check", "what skills should I highlight for this posting."
---

# ATS Check

Run `${CLAUDE_PLUGIN_ROOT}/scripts/gap_report.py` against the posting and
the user's `profile.yaml`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gap_report.py" --posting <path-or-heredoc> --profile profile.yaml --top 15
```

If `profile.yaml` doesn't exist yet, hand off to the `onboard` skill
first.

Present the result short and plain: **covered** (already in the profile,
confirmation only), **missing** (terms the posting uses that the profile
doesn't — these are what an ATS keyword scan would likely dock points
for). Method in full at `${CLAUDE_PLUGIN_ROOT}/references/ats.md`.

A gap is information, not a verdict:

- If it's a real, true skill — tell the user to add it to `profile.yaml`
  themselves (with real, provable specifics), then re-run the check. Never
  add it on their behalf; that's how a resume starts saying things that
  aren't true. See `${CLAUDE_PLUGIN_ROOT}/references/constraints.md`.
- If it's a skill the profile already has under a different name (their
  tag says "k8s," the posting says "Kubernetes"), that's a `tailor-resume`
  job — surfacing the *exact term the posting used*, for a skill that's
  already real, is exactly what tailoring is for.
- If it's not real at all, say so plainly. A gap that stays a gap is a
  more useful answer than a resume that quietly stops being true.
