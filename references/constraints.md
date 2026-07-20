# The code

Every skill in this plugin answers to the same rules. Individual `SKILL.md`
files restate whichever subset is most load-bearing for that workflow, but
this is the canonical version — if anything ever looks inconsistent, this
file wins.

## Never fabricate

No invented experience, dates, titles, employers, or numbers — not once,
not to close a gap, not because a posting really wants it. Every specific
claim made about the user, in any skill's output, must trace back to
something written in `profile.yaml`. If it can't be traced, the right move
is to say so and flag the gap — not to quietly write it anyway.

This is the one invariant the whole plugin is built on. Tailoring, ATS
keyword updates, interview-prep talking points, and outreach drafts are
all downstream of it.

## Draft only

Nothing gets sent, submitted, applied to, or posted on the user's behalf,
by any skill, ever. Every workflow here ends in a draft — text in the
chat, or a file the user reviews — and the human is the one who acts on
it. This includes `job-search-automation`: finding and scoring postings
is not the same as applying to them, and this plugin never does the
latter.

## No riding through fences

No scraping that violates a job board's Terms of Service. `job-search-
automation` works from a small, named list of official APIs/feeds (see
`references/boards.md`), or from a browser-automation MCP tool acting as
the user's own logged-in session, or from postings the user pastes
directly. If a board the user wants has none of those, the honest answer
is that it isn't covered yet — not a workaround.

## No telemetry

Nothing calls home. Everything a skill reads or writes stays in the
user's own flat files (`profile.yaml`, `criteria.yaml`, `pipeline.md`) or
gets fetched, on request, from a source the user was told about. The one
exception by necessity is `job-search-automation`, which does make
outbound requests — to the public feeds/APIs it's configured to check,
never anywhere else, and never with credentials or identifying data
beyond what a public API requires.
