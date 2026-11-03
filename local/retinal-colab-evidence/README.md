# Retinal Colab Evidence Explorer

Separate, retrievable research package for free interactive Colab sessions. It runs the actual frozen ResNet152/X1–X4 grader, displays nine structure/evidence/attribution panels, exposes measured values, and provides a local Qwen chatbot grounded in the report and cited methods literature.

## Start

1. Download artifacts/retinal_models_v1.tar.gz from the project workspace and place it in your own Google Drive. The large inference-only bundle stays outside GitHub; no datasets, original retinal photographs, credentials or patient records are included.
2. Open notebooks/Retinal_Evidence_Explorer_v3.ipynb in Colab, choose a GPU runtime, and run the setup cells. Set BUNDLE_PATH to your Drive file. The notebook verifies checksums and installs an isolated Python3.11 model environment.
3. Upload a retinal JPG/PNG, run analysis, inspect overlays/tables and ask questions in the notebook chat. The first environment/model download and each AutoMorph analysis can take several minutes. Free GPU availability and runtime limits apply. No public API, tunnel or external website hosting is started.
4. Download your report or explicitly copy it to Drive. Reports and input images stay in your notebook runtime until the cleanup cell or runtime termination; they are not automatically uploaded to GitHub or this research server.

The model bundle must be supplied to each user who runs the notebook. This is not a self-contained weights download from GitHub. Code is stored at local/retinal-colab-evidence in the GitHub Pages repository and the website links directly to the notebook.

## Folder contents

- app/: portable extraction, hash-verified grader, Grad-CAM, measured evidence, citations and local chat.
- notebooks/: interactive notebook, no public server.
- literature/: stream guide and original references.
- scripts/: reproducible bundle builder and verification.
- artifacts/: local model bundle, checksums and manifest (large weights excluded from GitHub).
- reports/: local QA reports, not publicly committed.
- tests/: contract and evidence checks.

## Scientific boundaries

See literature/STREAM_GUIDE.md. X2 is weak proxy evidence. X3 is a lesion-trained encoder, not a lesion detector. We do not invent lesion counts or normal ranges. The model is not clinically validated, and historical external scores need reevaluation after the X3 preprocessing audit. Upstream AutoMorph and model licenses are retained in the inference bundle; do not assume redistribution rights for third-party weights. Share artifacts only as permitted by their upstream terms.

## Normal no-grade outcomes

Version 2 stops immediately after a quality-model rejection and returns status quality_rejected with no grade or disease probabilities. If required measurements are incomplete, status feature_incomplete retains available X1/X4 values and lists missing measurements. Display, chat and download cells handle both statuses without raising a traceback. A quality-model decision is not proof of clinical ungradability. Grading remains conditional on accepted quality and complete model inputs; no values are fabricated. The existing model bundle is unchanged.

## Question-specific knowledge (v3)

See literature/KNOWLEDGE_LIBRARY.md and app/knowledge_base.json. The assistant retrieves 26 cited ophthalmology/oculomics topics, focuses on the metric asked about, labels each user question, and handles short follow-ups. This expands inference-time knowledge; it does not fine-tune Qwen or add systemic diagnostic capabilities. The model bundle is unchanged.
