# Blog and Scholarships

Public index: https://inamullah-colab.github.io/knowledge/
Blog filter: https://inamullah-colab.github.io/knowledge/?section=Blog

`/blog/`, `/year-archive/`, `/categories/` and `/tags/` are compatibility redirects, not separate catalogues. Individual article URLs are unchanged. The shared navigation lives in `_data/navigation.yml` and `_includes/site-header.html`.
Publisher tools: https://inamullah-colab.github.io/publisher/

The reader combines published studio articles with Jekyll posts from `/hub-feed.json`. Existing post URLs are preserved. New posts use `layout: hub-article`, an explicit `permalink`, a `description` and `hub_category` (Scholarships, Research careers, Science & learning, Research methods). The browser tool creates a draft in GitHub's authenticated file editor. Replace all prompts, verify sources and deadlines, then change `published: false` to `true` and commit to master. A draft committed with false is still visible in the public source repository; never put private material there.

The existing GitHub Pages workflow builds and deploys after a master commit. The owner-supplied AdSense script is installed through `_includes/adsense-verification.html`, inside both shared page headers. `_data/adsense.yml` contains the public publisher ID and mode: `code` loads the script, `verification` emits the meta tag only, and `off` disables both. The matching seller entry is generated at `/ads.txt`. Google site approval, Auto ads configuration and Google consent messaging are managed in the owner’s AdSense account; installing the script does not confirm these are complete.

Visitor metrics are stored separately by the author’s Sites service. Its collector has no secret in the browser: the endpoint is public; reports require the owner's ChatGPT sign-in. The client respects consent and GPC/DNT, sends paths without queries and referrer origins only, and does not count unique people. The owner dashboard explains limitations. Direct article links remain on this GitHub website; application links go to the external organisation.


The redesigned public reader is https://inamullah-colab.github.io/knowledge/. Knowledge & Opportunity navigation links point there. It is hosted on GitHub Pages and stays on the GitHub address for reading, filtering, article pages, community browsing, support and privacy. The reader fetches only published material from the existing owner-controlled publishing service. New articles appear without manually copying posts into GitHub. Publishing and contribution authentication remain in the separate secure workspace.

Reader build source is maintained in the Knowledge & Opportunity repository under `github/`, alongside the shared design. Run `node scripts/build-github-reader.mjs` there, then replace this repository’s `knowledge/` assets and HTML from `github-dist/`. Preserve the folder paths. Its AdSense snippet uses the same publisher ID as this repository; Google approval remains managed in AdSense.

Keep the shared header include, `site-structure.css` and both `portfolio-navigation.js` and `reader-navigation.js` in every `knowledge/**/index.html` when refreshing reader assets. Main profile pages use `portfolio-page`; Publications is the full paper catalogue, About me is the personal story, CV is the professional record, and Resources is a reference shelf. Avoid copying those full sections back onto the homepage. Private workspace links belong in Owner tools.

Country flags use locally hosted SVGs in `assets/flags/` (MIT licence included). Keep `visitor-counter.css` and `country-flags.js` in the shared statistics include and all reader HTML entrypoints when refreshing the reader build. It decorates real country counts; unknown locations remain unflagged. Statistics count consented page views, not unique people.
