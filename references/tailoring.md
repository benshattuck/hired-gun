# Tailoring bullets without fabricating

A man's record is a fixed thing. What changes, town to town, is which
parts of it you show first and in what light. That's tailoring. It is not
the art of putting a scar on a man who never fought — it's the art of
turning him toward the light so the scar he does have shows.

The goal is to change *emphasis and language*, never *content*. A
tailored resume should describe the exact same set of facts as
`profile.yaml` — just in the words and order that make the match to a
specific posting plain to a recruiter skimming it at a hundred yards.

## The rule

Every tailored bullet must be traceable to one or more entries in
`profile.yaml` — an experience bullet, a skill, a project, a note. If you
can't point to the source, don't write it. Say so instead:

> "The posting wants Kubernetes experience — nothing in your profile
> mentions it. I won't add it; you'll need to speak to it separately or
> we skip that requirement."

## What tailoring is allowed to do

- **Reorder** bullets so the most relevant ones for this posting ride up
  front within each role.
- **Reword** a bullet to use the posting's terminology, as long as the
  underlying fact holds ("message queue" → "event streaming pipeline" is
  fine if that's what it actually was; "helped with" → "led" is not fine
  unless the profile already says "led"). Don't call yourself the man who
  drew first if you were riding backup.
- **Recombine** two related bullets into one if it reads cleaner, as long
  as nothing in the merge is invented.
- **Cut** bullets irrelevant to this posting (the profile always keeps the
  full record; a tailored resume doesn't need every line of it).
- **Surface** an existing skill or note that wasn't in the original bullet
  wording but sits elsewhere in `profile.yaml`, if it's genuinely
  relevant to the job at hand.

## What tailoring must never do

- Invent or round up metrics. If `metrics: false` on a bullet, don't add a
  number to it. If `metrics: true`, don't change the number.
- Add a title, employer, date range, or degree that isn't in the profile.
- Claim ownership ("built", "led", "architected") of something the
  profile describes as a contribution ("contributed to", "helped"). Match
  the verb's level of ownership to the source.
- Add a skill or technology the profile doesn't list, even if it's
  "probably" true given the rest of the record. Ask the user instead of
  guessing — they can add it to `profile.yaml` if it's real.

## Workflow

1. Read the posting and the relevant `profile.yaml` sections (usually
   `experience` + `skills`, sometimes `projects`).
2. For each posting requirement, find the closest matching bullet(s) via
   `tags` and text.
3. Draft the tailored version, reusing `references/ats.md`'s vocabulary
   where it's a genuine match.
4. List anything the posting asks for that has no match — that's the gap
   report's job (see `references/ats.md`), but flag it here too so it
   doesn't get quietly buried.
5. Show the user a before/after view so they can see exactly what
   changed and why, not just take delivery of the final draft sight
   unseen.
