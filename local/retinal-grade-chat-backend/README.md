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

## Actual image uploads

POST /api/predict accepts raw JPG/PNG bytes (not multipart), maximum 10 MiB, minimum 128 pixels per dimension, maximum 30 megapixels. It returns HTTP 202 and a random prediction_id. Poll GET /api/predictions/{prediction_id} until ready or failed. POST /api/chat with question and prediction_id explains that server-held result; do not send a case_id too. Fixed example contexts remain available separately.

The upload worker runs the existing AutoMorph M0/M1/M2/M3 pipeline in an isolated temporary directory, computes the study's global X1 skeleton summaries, DR-XAI-style weak X2 evidence, Huang LCL 2048D X3 features using the EyePACS training transform (224px bicubic, ImageNet normalization), and X4 macular biomarkers, then invokes the hash-verified frozen ImagePredictor. It does not fit preprocessing or impute an entirely missing stream. Uploads must pass the study's strict complete X1–X4 policy. A 0.008 mm/pixel resolution is assumed, matching the study; this is not measured physical calibration.

The full research deployment must provide the original study artifacts and model repositories. Configure RETINAL_STUDY_ROOT, AUTOMORPH_ROOT, AUTOMORPH_PYTHON, RETINAL_RXG_ROOT, and HUANG_WEIGHTS if their locations differ from the current server defaults. Model files and third-party code are not bundled here. The study root must include frozen manifests, preprocessing/checkpoint hashes, preprocessors.joblib, the selected image checkpoint, and its scripts/dependencies. The existing automorph environment contains the compatible extraction dependencies.

Only one image job runs at a time. Temporary image and extraction files are removed after processing; result/probability sessions remain only in process memory for 30 minutes after completion. Session count is bounded to 20. Server restarts discard results. No upload or image filesystem route exists. Access logs are disabled in the documented launch command. The client holds the unguessable session identifier only in page memory. Do not submit identifiable images without permission. This is a research grader, not a clinical service. An audit found that the previous APTOS/Messidor extractor used 128px/Huang normalization while EyePACS training used 224px/ImageNet normalization. Uploads now match training; the previous cross-dataset scores require consistent reevaluation and are not performance estimates for this upload pipeline.
