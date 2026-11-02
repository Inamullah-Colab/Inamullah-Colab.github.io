# Retinal grade chat backend

The live sample uses FastAPI on the existing server, exposed through a temporary Cloudflare Quick Tunnel. It runs Qwen2.5-1.5B-Instruct locally. No model API key is needed. The URL changes if the tunnel restarts; this is a demonstration, with no uptime guarantee.

Install requirements in a virtual environment. Set MODEL_PATH to a local copy of the pinned model, or leave it unset to download the pinned model. Run from this directory:

```sh
uvicorn api:app --host 127.0.0.1 --port 7867 --no-access-log
cloudflared tunnel --url http://127.0.0.1:7867 --protocol http2 --no-autoupdate
```

Set ALLOWED_ORIGINS to your GitHub Pages origin. Update web/config.js with the HTTPS backend URL and transport fastapi. For permanent hosting, deploy this same API on a persistent server with HTTPS and a stable hostname.

GET /health reports readiness. POST /api/chat accepts only question and case_id (grade-0 through grade-4). Ten requests per minute globally and one inference at a time bound demo usage. Illustrative contexts are fixed; user-supplied probabilities and grades are rejected. No images, history or medication decisions are accepted. Generated text is constrained to supplied facts and cited grade definitions.

The alternative Gradio entry point app.py is retained for compatible hosts. Model weights and retinal datasets are not part of this source package. Qwen weights retain their upstream license.
