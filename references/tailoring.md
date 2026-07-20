# Tailoring: selection by default, rewording only on request

A record is a fixed thing. What changes, town to town, is which parts of
it you show first and in what light. That's tailoring.

This skill has **two modes**, and they are not the same risk level.
**Selection is the default** — every time. **Rewording is opt-in** — only
when the user explicitly asks for it, for a specific bullet, in that
conversation. Never slide from one into the other without being asked.

## Select mode (default): pick, don't write

Given a posting, pick the existing bullets from `profile.yaml`'s master
bank most relevant to it — **verbatim, unchanged, per role** — and
recommend which of the profile's real skills to surface first in the
skills section. Nothing gets reworded, nothing gets reformatted. Run
`${CLAUDE_PLUGIN_ROOT}/scripts/select_bullets.py`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/select_bullets.py" --posting <path-or-heredoc> --profile profile.yaml --max-per-role 3
```

This is the mode to reach for whenever the user has an actual resume
document (Word, Google Doc, plain text, whatever) that they maintain
themselves. Hand them: which bullets to include per role, in what order,
and which skills to lead with — they paste it into their own formatting.
This plugin doesn't touch the document itself; it decides *content*, the
user keeps *form*.

What "pick" means precisely:

- **Select** which of a role's bullets go in this version, based on
  relevance to the posting (tag overlap, wording overlap, and known
  aliases — see `${CLAUDE_PLUGIN_ROOT}/references/ats.md`).
- **Order** the kept bullets within a role by the order they already
  appear in `profile.yaml`, not by score — don't silently promote a minor
  bullet above a major one just because it happens to match more words.
- **Mark** which skills-section entries the posting wants, using the
  profile's own wording — never the posting's wording, even for a known
  alias (profile says "PostgreSQL," posting says "Postgres" → mark
  PostgreSQL as relevant, don't relabel it "Postgres"). Say the alias was
  noticed; let the user decide if they want to match the posting's exact
  phrasing themselves.
- **Never** touch the words inside a bullet. Not a synonym swap, not a
  tense change, not combining two bullets into one. If a bullet doesn't
  say what the posting wants to hear, that's what `ats-check` is for —
  it's a gap, not a rewording opportunity.

## Reword mode (opt-in): only when asked, only what's asked

If the user explicitly asks to rewrite a bullet's *language* — "reword
this to match their terminology," "make bullet 3 punchier" — that's a
different, narrower action:

- Change *emphasis and language only*, never *content*. The reworded
  bullet must describe the exact same underlying fact as the original.
- **Reword** a bullet to use the posting's terminology, as long as the
  underlying fact holds ("message queue" → "event streaming pipeline" is
  fine if that's what it actually was; "helped with" → "led" is not fine
  unless the profile already says "led"). Don't call yourself the one who
  drew first if you were riding backup.
- **Recombine** two related bullets into one only if the user asked for
  that specifically, and nothing in the merge is invented.
- Show the before/after side by side — never replace the original
  silently, and never write the reworded version back into
  `profile.yaml` itself. `profile.yaml` stays in the user's own original
  words; reworded text lives only in the output for this one posting.

## The rule (applies to both modes)

Every word that leaves either mode must be traceable to `profile.yaml`.
If a posting wants something with no match, say so — don't paper over it
in either direction:

> "The posting wants Kubernetes experience — nothing in your profile
> mentions it. I won't add it; you'll need to speak to it separately, or
> add it to profile.yaml yourself if it's real."

Never do, in either mode:

- Invent or round up metrics. If `metrics: false` on a bullet, no number
  gets added — reworded or not. If `metrics: true`, the number doesn't
  change.
- Add a title, employer, date range, or degree that isn't in the profile.
- Claim ownership ("built", "led", "architected") of something the
  profile describes as a contribution ("contributed to", "helped").
- Add a skill or technology the profile doesn't list, even if it's
  "probably" true given the rest of the record.

## Workflow

1. Ask (or infer from context) whether this is a select-mode or
   reword-mode request — default to select unless the user has clearly
   asked for rewording.
2. Read the posting and the relevant `profile.yaml` sections (`skills` +
   `experience`, sometimes `projects`).
3. Select mode: run `select_bullets.py`, present its output as-is.
   Reword mode: draft the reworded bullet(s), show before/after.
4. List anything the posting asks for that has no match in
   `profile.yaml` — that's `ats-check`'s job in more depth, but flag it
   here too so it doesn't get quietly buried either way.
