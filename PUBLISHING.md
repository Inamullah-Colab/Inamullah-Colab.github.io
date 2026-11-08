# Blog and Scholarships

Public index: https://inamullah-colab.github.io/blog/
Publisher tools: https://inamullah-colab.github.io/publisher/

The index automatically includes published Jekyll posts. Existing post URLs are preserved. New posts use `layout: hub-article`, an explicit `permalink`, a `description` and `hub_category` (Scholarships, Research careers, Science & learning, Research methods). The browser tool creates a draft in GitHub's authenticated file editor. Replace all prompts, verify sources and deadlines, then change `published: false` to `true` and commit to master. A draft committed with false is still visible in the public source repository; never put private material there.

The existing GitHub Pages workflow builds and deploys after a master commit. The owner-supplied AdSense script is installed through `_includes/adsense-verification.html`, inside both shared page headers. `_data/adsense.yml` contains the public publisher ID and mode: `code` loads the script, `verification` emits the meta tag only, and `off` disables both. The matching seller entry is generated at `/ads.txt`. Google site approval, Auto ads configuration and Google consent messaging are managed in the owner’s AdSense account; installing the script does not confirm these are complete.

Visitor metrics are stored separately by the author’s Sites service. Its collector has no secret in the browser: the endpoint is public; reports require the owner's ChatGPT sign-in. The client respects consent and GPC/DNT, sends paths without queries and referrer origins only, and does not count unique people. The owner dashboard explains limitations. Direct article links remain on this GitHub website; application links go to the external organisation.
