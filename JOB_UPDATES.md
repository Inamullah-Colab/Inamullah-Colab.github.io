# University vacancy updates

Public catalogue: https://inamullah-colab.github.io/knowledge/?section=Jobs

The user wants the established Cambridge/Oxford/Southampton format: one employer and one subject or role family per post, using the existing searchable JobRoundup component. Do not replace these with generic multi-university research/teaching/support pages. Current additions: 93 distinct vacancies in 29 employer/role collections, reviewed 10 November 2026. Bath has 28, Leeds 30 and Manchester 27; eight further roles cover seven other universities. This is a curated selection, not an exhaustive vacancy census.

## Data and stable pages

- Edit `_data/university_jobs.json` as the source of truth.
- Run `python scripts/build-university-job-articles.py` to regenerate `_data/university_job_articles.json`.
- `hub-feed.json` exposes these as `jobArticles`. The reader displays the same article layout, role search, salary/reference fields, official links and seven-day red deadline indicators as existing university posts.
- Stable URLs use `/knowledge/articles/?post=university-<employer>-<collection_group>`, e.g. `university-bath-computing`. Update these in place; do not create another dated collection each week.
- The three old `/jobs/university-…-roles/` URLs are compatibility redirects, hidden from the catalogue using `hub_hidden: true`.

Each vacancy needs a stable id, title, employer, location, reference, role_type, salary, summary, eligibility, official url, discovery_url where known, group, collection_group, closing_date, checked_at and status. Preserve department, closing_time and material editor_note fields when available. `group` is research/teaching/professional; `collection_group` is academic/computing/health/engineering/social/professional/technical. Each vacancy belongs to exactly one collection. Lecturers/professors are academic; IT and data roles may be computing regardless of research/professional contract. Add stable employer slugs to the generator when expanding to another university. The two Leeds EAP adverts AHCLC1246 and AHCLC1247 are distinct references, not duplicates.

## Discovery and verification

Use https://www.jobs.ac.uk/ for discovery, then read individual official employer adverts and write concise original summaries. Its terms at https://www.jobs.ac.uk/legal/terms-and-conditions restrict republication; no syndication permission is recorded. Do not scrape/copy its advert database or descriptions. Do not treat indexed snippets as proof of an open application or bypass access controls. Exclude staff-only or otherwise inaccessible restricted roles from the public external-applicant collection.

Recheck every current official advert. A failed retrieval does not prove closure: preserve the last checked_at, mark `unverified`, and report the blocker. Mark explicitly closed adverts `closed`; preserve them as history. The UI also marks elapsed deadlines automatically in UK time. Preserve exact advertised closing dates/times; do not infer a precise time from ambiguous “midnight”. Keep important conflicts in editor_note. Never invent eligibility, salaries, sponsorship or availability. Detailed eligibility is in the employer’s full person specification; summaries are selective.

Deduplicate against this registry, other `_posts` job articles and the public publishing feed at https://knowledge-opportunity-inam.boxywatermelon2.chatgpt.site/api/reader (`articles[].jobRoundup.items`). Exclude managed ids starting `university-` when constructing the external comparison index. Compare canonical employer URLs (remove tracking but retain JobId/ref) and employer + vacancy reference. Do not merge different references simply because titles match. Update existing matches rather than creating duplicate cards.

## Validation and publication

Run `python scripts/check-university-jobs.py [optional-external-index.json]`, then the generator. It validates all source records before building. Confirm every registry vacancy appears once in the generated collections and each collection has one employer. The Sites source includes `scripts/test-managed-jobs.ts` for reader integration and deadline regression tests; run it with `node --import tsx scripts/test-managed-jobs.ts <absolute-generated-articles-json>` after reader changes.

Use the connected GitHub writer for `Inamullah-Colab/Inamullah-Colab.github.io`, branch `master`. Fetch latest changes, preserve unrelated files and move the branch with an expected-SHA lease. Public publication is authorised. The GitHub Pages workflow deploys pushes. Confirm deployment succeeds and read back a representative public article, including search, deadline filters and official links. Report added/updated/closed/duplicate/unverified counts with the Jobs link. Do not describe a failed or pending deployment as published.

Routine data updates need only the two JSON files. Do not alter the active reader assets, feed-version meta, no-store behaviour, navigation, advertisements or all-time visitor statistics. The original Sites source also reads this feed; keep that integration intact. No credentials belong in public files.

The existing weekly task performs this review. Preserve its schedule; do not create a duplicate task. Report source, tool or authorisation failures rather than claiming an update happened.
