# Interview prep method

Same invariant as everywhere else in this plugin: every talking point
traces to `profile.yaml`. An interview room is the worst possible place
for a fabricated story to surface — a hiring manager asking one follow-up
question is all it takes to unravel a made-up detail, and it costs more
than the gap ever would have.

## What to generate

**1. Likely questions**, pulled from three sources:

- **The posting itself** — its stated responsibilities and requirements
  translate fairly directly into "tell me about a time you..." and "how
  would you approach..." questions. A posting emphasizing on-call and
  reliability will ask about incidents; one emphasizing mentorship will
  ask about growing junior engineers.
- **Role/seniority conventions** — a staff/senior posting skews toward
  ownership, tradeoffs, and influence-without-authority questions more
  than an entry-level one does. Use judgment, not a fixed script.
- **Gaps from `ats-check`** — if the posting wants something the profile
  doesn't clearly have, that gap is *likely to come up as a direct
  question*. Surface it here too, framed as "worth having an honest
  answer ready for," not as something to paper over.

**2. Talking points, in STAR shape** (Situation, Task, Action, Result),
one per likely question, each built from a *specific, named bullet* in
`profile.yaml`:

- **Situation/Task**: the context already implied by the bullet and the
  role/company/dates around it. Don't invent scale, stakes, or team size
  that isn't in the bullet or that the user hasn't confirmed out loud.
- **Action**: expand the bullet's verb into what was actually done, using
  only what's in `profile.yaml` plus whatever the user adds live in
  conversation. If the user adds detail, that's fine — it's now something
  they said, not something invented. Note the distinction: material this
  skill generates must trace to `profile.yaml`; material the *user*
  supplies live is theirs to add.
- **Result**: use the bullet's own metric if `metrics: true`. If
  `metrics: false`, don't invent one — coach the user to describe the
  qualitative outcome instead, or ask them if they remember a number that
  never made it into `profile.yaml` (if so, that belongs added to
  `profile.yaml` via `onboard`, not just used here once).

## What this must never do

- Never invent a scenario, a number, or an outcome not in `profile.yaml`
  and not stated by the user in this conversation.
- Never coach the user to claim ownership the profile doesn't support
  ("I led the migration" when the bullet says "contributed to").
- Never promise the user a question will or won't be asked — these are
  informed guesses, not certainties. Say so.

## Format

Keep it scannable: group by likely question, one STAR talking point each,
2-4 sentences per section. This is prep material for the user to
internalize and speak in their own words in the room — not a script to
read verbatim, and definitely not something to hand the interviewer.
