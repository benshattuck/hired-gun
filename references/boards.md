# Curated job sources for job-search-automation

`job-search-automation` never scrapes. It works from three kinds of
source, in order of preference, all consistent with
`references/constraints.md`'s "no riding through fences" rule:

1. **Official public APIs/feeds** — the list below. Small and curated on
   purpose; it grows by someone adding a source they've verified is
   public and ToS-clean, not by pointing this at arbitrary sites.
2. **A browser-automation MCP tool acting as the user's own logged-in
   session** — if the user has one configured (e.g. a Playwright-based
   browser connector), Claude can drive an interactive search on a site
   like LinkedIn or Indeed *as the user*, the same way the user would
   click around themselves. This is meaningfully different from an
   unattended scraper hitting the site at scale: it's assisted browsing,
   rate-limited by being a real interactive session, and subject to
   whatever the user already agreed to by having an account. Still: don't
   automate around a site's explicit bot-detection or rate limits, and
   don't run this unattended in a loop — a human should be present or
   have explicitly asked for this specific run.
3. **Postings the user pastes directly** — always available, works for
   any board, zero ambiguity about consent.

There is no legitimate path in this plugin to LinkedIn- or
Indeed-breadth automated coverage without one of the above. If a user
asks for a board with none of the three, say that plainly instead of
finding a workaround.

## Official sources

### Greenhouse job board API

Many companies that use Greenhouse for hiring expose a public, unauthenticated
JSON API for their own postings:

```
https://boards-api.greenhouse.io/v1/boards/{company-token}/jobs
```

`{company-token}` is the slug in the company's own Greenhouse job board URL
(e.g. `boards.greenhouse.io/stripe` → token `stripe`). Add each company the
user wants watched to `sources.yaml`'s `greenhouse_companies` list. Append
`?content=true` to include full descriptions.

### Lever postings API

Same idea, for companies on Lever:

```
https://api.lever.co/v0/postings/{company-token}?mode=json
```

Add tokens to `sources.yaml`'s `lever_companies`.

### RemoteOK API

A public, documented JSON feed of remote postings across companies:

```
https://remoteok.com/api
```

No auth. Set `remoteok: true` in `sources.yaml`. Filter results by
keyword/criteria after fetching — the feed itself isn't filterable.

### We Work Remotely RSS

Category-based RSS feeds, e.g.:

```
https://weworkremotely.com/categories/remote-programming-jobs.rss
```

See the site for other category slugs. Add the categories the user wants
to `sources.yaml`'s `weworkremotely_categories`.

### Hacker News "Who is hiring?" (monthly thread)

HN's official Firebase API and Algolia search API are both public. Find
the current month's thread via Algolia:

```
https://hn.algolia.com/api/v1/search_by_date?query=%22Who%20is%20hiring%22&tags=story&hitsPerPage=1
```

Then fetch its top-level comments via the Firebase item API
(`https://hacker-news.firebaseio.com/v0/item/{id}.json`). Set
`hn_who_is_hiring: true` in `sources.yaml`. This one is noisier than the
others — comments are freeform text, not structured postings — so
scoring quality here is lower; treat hits as leads to read, not a clean
match list.

### USAJobs API (U.S. federal roles)

Official API for federal government postings, requires a free API key
(https://developer.usajobs.gov/apirequest/). Set `usajobs.enabled: true`
and `usajobs.keywords` in `sources.yaml`; the user supplies their own API
key as an environment variable, never committed to `sources.yaml`.

## Explicitly not covered

LinkedIn and Indeed's general job search are not on this list — both
restrict programmatic access to paid enterprise partners, and there's no
public, ToS-clean API for general search. Use the browser-MCP path above
if the user wants either covered, or paste postings directly.
