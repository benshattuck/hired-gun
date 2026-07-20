---
name: interview-prep
description: >
  Preps the user for an interview for a specific posting: likely
  questions drawn from the posting and role seniority, with STAR-style
  ("Situation/Task/Action/Result") talking points grounded strictly in
  real profile.yaml bullets — never invented scenarios or outcomes. Use
  when the user says things like "help me prep for this interview",
  "what questions might they ask", "help me practice talking about this
  experience", or "I have an interview for this role."
---

# Interview Prep

Read `${CLAUDE_PLUGIN_ROOT}/references/interview-prep.md` first — it has
the full method for generating questions and building STAR talking
points without fabricating.

If `profile.yaml` doesn't exist yet, hand off to `onboard` first. If a
gap-check hasn't run yet for this posting, running `ats-check` first
often sharpens the question list — gaps are exactly what's likely to get
asked about directly.

## What to do

1. Generate a short list of likely questions from the posting's stated
   responsibilities, the role's seniority level, and any gaps `ats-check`
   would surface.
2. For each, build a STAR-style talking point sourced from a **specific,
   named bullet** in `profile.yaml` — cite which bullet/role it comes
   from so the user can see the grounding, not just take the output on
   faith.
3. Where the profile has nothing to back up a likely question, say so
   plainly and suggest how the user might honestly address it (a related
   but different experience, or straightforward "I haven't done that
   specifically, here's how I'd approach learning it") — never invent
   the missing experience.
4. If the user adds detail live in conversation ("actually the team was
   12 people, and here's what happened next"), that's their material to
   use — incorporate it, but note it's not something to silently fold
   into `profile.yaml` unless they ask for that separately via `onboard`.

## What this skill never does

Same invariant as everywhere else: no invented scenarios, numbers, or
outcomes, and no coaching the user to overstate ownership beyond what
`profile.yaml` supports. Full rule in
`${CLAUDE_PLUGIN_ROOT}/references/constraints.md`.
