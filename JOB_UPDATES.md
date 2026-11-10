# University vacancy updates

The public Jobs catalogue is https://inamullah-colab.github.io/knowledge/?section=Jobs. This maintained collection has three stable pages:

- /jobs/university-research-roles/
- /jobs/university-teaching-roles/
- /jobs/university-professional-technical-roles/

Source data: `_data/university_jobs.json`. Pages render `_includes/university-job-list.html`. Update the existing registry and pages; do not create another dated roundup on each run. Initial review: 10 November 2026, 21 distinct vacancies (6 research, 9 teaching, 6 professional/technical), compared with 482 existing vacancy/link entries. None of this initial batch duplicated an existing vacancy.

## Research and verification

Use https://www.jobs.ac.uk/ for discovery. Its terms at https://www.jobs.ac.uk/legal/terms-and-conditions restrict reproduction of site material; there is no recorded syndication permission. Do not scrape or reproduce its vacancy database or advert text. Find the employer's actual advert, read it, then write a short original summary of factual role details with an official link. Do not treat an index/search snippet as proof an application is still open. Do not bypass access controls. This is a curated selection, not an exhaustive jobs.ac.uk mirror.

Read every existing record's official advert to check status, deadline and changed details. A failed retrieval does not prove closure: retain the prior verification date, mark `unverified`, and report the blocker. Mark explicitly closed adverts `closed`; do not invent a closing date. Deadlines passed in UK time are labelled by the reader automatically. Preserve closed records as history; do not erase their evidence. Reopened adverts require fresh verification. No fabricated salaries, qualifications, sponsorship or eligibility promises.

Compare newly found roles against this registry, all other `_posts` job articles and the public publishing feed at https://knowledge-opportunity-inam.boxywatermelon2.chatgpt.site/api/reader (articles[].jobRoundup.items). Exclude the three generated collection pages when constructing the external existing-listings index. Deduplicate by canonical employer advert URL, then employer + vacancy reference. Strip tracking parameters but preserve identifiers such as JobId/ref; identical generic titles at different employers are not duplicates. Update a matching vacancy in place. Assign each role one primary group: research, teaching or professional. Lecturers/professors belong in teaching even when research is part of the job.

Each record must have a stable id, employer reference, title, employer, location, role_type, summary, eligibility, official url, discovery_url, group, closing_date, checked_at and status. Retain precise employer deadlines; disclose meaningful conflicting dates in editor_note. Avoid unverified roles without a reliable opening/deadline status. Keep summaries concise, with only necessary facts from each source.

## Publication

Use the connected GitHub writer for `Inamullah-Colab/Inamullah-Colab.github.io`, branch `master`. Fetch the latest branch before editing, preserve unrelated changes, and update the reference using an expected-SHA lease. Public content is authorised by the user's weekly update request. The existing GitHub Pages workflow publishes pushes. No account credentials belong in source or public records.

Run `python scripts/check-university-jobs.py`, optionally passing a JSON file of the existing external listings with url/employer/reference fields. Run `node scripts/test-university-jobs.mjs` if changing deadline behaviour. Confirm the GitHub Pages deployment succeeds and read back the generated pages. Keep the active reader bundle, feed-version meta and no-store fetch behaviour intact. Report the numbers added, updated, closed, skipped as duplicate and unverifiable, with the Jobs link. Never describe a failed or pending deployment as published.

The weekly scheduled review uses these instructions and the connected GitHub tools. Scheduling a task confirms the schedule, not a completed future run. Report source, tool or authorisation failures instead of claiming an update occurred.
