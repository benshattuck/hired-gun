---
name: tailor-resume
description: >
  Tailors a resume to a specific job posting by selecting the best
  existing bullets from profile.yaml's master bank — verbatim, no
  rewording, no reformatting — and surfaces which real skills to lead
  with in the skills section. Rewording a bullet's language only happens
  if explicitly requested. Use when the user asks to "tailor my resume
  for this job", "pick the best bullets for this posting", "update my
  skills section for this role", or "customize my resume for this
  posting."
---

# Tailor Resume

**Default behavior is selection, not rewriting.** Read
`${CLAUDE_PLUGIN_ROOT}/references/tailoring.md` before doing anything —
it defines exactly what "select mode" and the opt-in "reword mode" each
allow and forbid.

If `profile.yaml` doesn't exist yet, hand off to `onboard` first —
tailoring has nothing to select from without it.

## What to do

1. Run `${CLAUDE_PLUGIN_ROOT}/scripts/select_bullets.py` against the
   posting and `profile.yaml`:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/select_bullets.py" --posting <path-or-heredoc> --profile profile.yaml --max-per-role 3
   ```

2. Present its output plainly: which bullets it picked per role
   (verbatim — don't touch a single word), which skills-section entries
   are relevant to this posting (marked, not relabeled), and which
   bullets it left out this time (still true, still on record).
3. If the user then asks to *reword* something — different from
   selecting — that's the opt-in mode in `references/tailoring.md`. Do
   it only for the specific bullet(s) they name, show a before/after, and
   never write the reworded version back into `profile.yaml`.
4. If the posting wants something with no bullet or skill to back it up,
   say so directly. Point at `ats-check` for the full keyword-gap
   picture, or `onboard` if the user says it's real and just missing from
   `profile.yaml`.

## What this skill never does

- Never edits `profile.yaml` — it only reads from it. The master bank
  changes only through `onboard`, by the user's own hand.
- Never invents a bullet, a metric, or a skill. Full rule in
  `${CLAUDE_PLUGIN_ROOT}/references/constraints.md`.
- Never touches an actual resume *file* (Word doc, PDF, etc.) directly —
  it hands back content for the user to place into whatever document
  they already maintain, so their formatting is never at risk.
