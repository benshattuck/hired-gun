---
name: outreach
description: >
  Drafts a recruiter or hiring-manager message, referral request, or cover
  note grounded in the user's profile.yaml — under 120 words, specific,
  draft only, never sent automatically. Use when the user asks to "draft a
  note to the recruiter", "write a cover letter for this", "message the
  hiring manager", or "help me reach out about this role."
---

# Outreach

Read `${CLAUDE_PLUGIN_ROOT}/references/outreach.md` first — it has the
exact structure for cold recruiter messages, referral requests, cover
notes, and follow-ups.

Every specific claim in the draft must trace to `profile.yaml`, same
grounding rule as everywhere else — see
`${CLAUDE_PLUGIN_ROOT}/references/constraints.md`. If `profile.yaml`
doesn't exist yet, hand off to `onboard` first.

**Draft only.** Put the text in the chat or a file. Never send an email,
submit a form, or post a message on the user's behalf — the rider reads
it, the rider sends it. If asked to "send" it, say plainly that you draft
and they send, and hand over the text.

If a match score or gap check hasn't happened yet for this posting,
mention that `job-match-score` or `ats-check` might sharpen what the
message leads with — but don't block the draft on it.
