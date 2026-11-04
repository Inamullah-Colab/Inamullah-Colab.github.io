# Optional OpenAI research assistant

Status: implemented, **disabled by default**. The deployed server currently has no OpenAI API key or funded API access. Local Qwen remains the default. No real OpenAI request has been made during implementation; provider behavior was tested with mocked HTTP responses.

## What it does

- Uses the OpenAI Responses API from the backend. No key or OpenAI call is placed in GitHub Pages JavaScript.
- Supplies the current server-held grade, probabilities and numerical X1/X2/X4 measurements. X3 is explicitly an encoder, not verified lesion detections.
- Does not send retinal images, evidence PNGs, filesystem paths or patient records. The question, up to two previous questions, report values and selected library facts are sent in OpenAI mode. Users should avoid typing identifying information.
- Retrieves up to three relevant topics from the existing cited library. Web search is restricted to PubMed/PMC, NEI, NICE, AAO, WHO, CDC, NIDDK and ClinicalTrials.gov. This is not access to every database or paywalled full text.
- Can use up to two pre-existing OpenAI vector stores for an authorized paper/guideline library. This setup does not upload papers or create billable storage automatically.
- Renders provider-supplied web citations as clickable inline links and lists document source names.
- Grounds the explanation in the report while instructing the model to distinguish image findings, population associations, clinical relevance and uncertainty. Prompt instructions do not guarantee medical correctness. Clinical review and representative evaluation are required before clinical use.

## Enable later, only with funded API access

On the backend host, use a private shell/session. Do not put a key in a notebook shared with others, the repository, web/config.js, URLs, or chat.

```bash
read -rs -p 'OpenAI API key: ' OPENAI_API_KEY
export OPENAI_API_KEY
export RETINAL_OPENAI_ENABLED=1
export RETINAL_OPENAI_MODEL='YOUR_RESPONSES_MODEL_WITH_WEB_SEARCH_SUPPORT'
export RETINAL_OPENAI_DAILY_CALLS=20
export RETINAL_OPENAI_USAGE_DB="$HOME/.local/state/retinalinsight/openai-usage.sqlite3"
# Optional: IDs of an existing authorized paper library (otherwise leave unset).
# export RETINAL_OPENAI_VECTOR_STORES='vs_...'
```

Select a model available to your API project that supports Responses API web search. The integration deliberately has no silently selected paid model. Restart the single API process with these environment variables. Use the existing environment and documented Uvicorn launch command. A live restart discards in-memory image sessions, so wait for active image jobs to finish first.

GET /health exposes only availability, model name and supported search modes, never credentials. The website enables the OpenAI selector only when the backend reports it configured. To disable, set RETINAL_OPENAI_ENABLED=0 and restart. A configured key alone does not enable paid requests. Local requests never silently switch to OpenAI.

## Usage and failure behavior

Default: 20 provider requests per UTC day, at most two simultaneous requests, at most two tool calls and 1,400 output tokens per request. A SQLite reservation is committed **before** contacting OpenAI and persists across server restarts. Failed and interrupted calls also count; the application does not retry them automatically. Questions or images are not stored in that database.

This is a request allowance, not a guaranteed dollar ceiling. Input tokens, model choice, search calls and optional vector-store storage affect charges. Configure additional project spending controls with OpenAI and monitor actual usage. Never delete the usage database to reset an allowance unintentionally.

Missing credentials, disabled mode or a zero allowance produce a clear 503 without contacting OpenAI. A reached allowance produces 429. Provider failures produce a sanitized error; the user can select local mode. There is no hidden paid fallback or silent substitution of a local answer.

## Verification and activation checklist

The automated tests cover: no-key/no-network behavior; report privacy allowlist; request context; citation parsing; incomplete answers; sanitized errors; restart-persistent and concurrent usage limits. Browser tests cover availability gating and safe inline citation rendering using simulated provider responses. These do not validate clinical accuracy or actual account/model/tool compatibility. After configuring an account, run a small controlled evaluation before making OpenAI available publicly: include grading explanations, X1–X4 queries, ocular conditions, systemic associations, unsupported diagnoses, fabricated-lesion requests, prompt injection and citation accuracy. Live activation and these account-dependent checks remain pending.

Official references:
- https://developers.openai.com/api/docs/guides/tools-web-search
- https://developers.openai.com/api/docs/guides/tools-file-search
- https://developers.openai.com/api/docs/pricing
