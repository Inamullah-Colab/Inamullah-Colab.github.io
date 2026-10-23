# Portfolio draft

This local redesign positions Inam Ullah Khan for academic research and industry
roles in machine learning, medical imaging, and biomedical data science.

## Changes

- A dedicated, responsive homepage with a short introduction and existing portrait.
- Three featured research projects, selected publications, methods, teaching, and contact links.
- The original background narrative is retained at `/background/`.
- Research and About links are added to the existing site's navigation.
- The rest of the AcademicPages site continues to use its existing layouts.

Content uses the repository's existing research descriptions and publication statuses.
The selected homepage publication entries are curated in `_includes/portfolio-home.html`;
update them when publication status changes. No project metrics, employment dates,
graduation date, or code release claims have been invented.

## Review

Run `python scripts/prepare_portfolio_preview.py` from the repository root. Open
`local/portfolio-preview/portfolio-draft.html` for a self-contained homepage preview.
Its links to other pages point to the live site; the new Background page will only
be available after deployment. For a complete preview, use `bundle exec jekyll serve`.

Checks passed for HTML structure, homepage anchors, internal route targets, image
alternative text, asset HTTP responses, and Git whitespace. Responsive styles cover
900px and 620px breakpoints, keyboard focus, and reduced-motion preferences.
Full Jekyll build and visual browser checks remain unverified: Ruby/Bundler and a
connected browser were unavailable in this environment.

## Daily emails

The daily 06:00 UTC schedule has been removed from
`.github/workflows/update-citations.yml` at the user's request. Manual runs and
runs triggered by updater code changes remain available. Existing citation counts
are preserved. The email subject or Actions run history is still needed to confirm
whether this workflow caused the daily emails. Account notification settings were
not changed.

The citation schedule removal was pushed to `master` in commit `e7064a1`.
The portfolio redesign is prepared for publication through the existing GitHub
Pages workflow. Verify the deployment result and live homepage after pushing.
