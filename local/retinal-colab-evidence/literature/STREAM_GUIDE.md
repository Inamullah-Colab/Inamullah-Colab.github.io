# What each evidence stream means

| Stream | Actual frozen-model input | Display and permitted interpretation |
|---|---|---|
| X1 | 16 skeleton summaries | Vessel maps, skeleton occupancy, connected components, endpoint and junction pixels. Supplementary 8-neighbor skeleton length is in processed pixels, not physical millimeters. |
| X2 | 190 weak proxy features | Five heuristic channels and their statistics. A separate true Grad-CAM is generated from the actual grading model image branch. It does not replace X2 or confirm lesions. |
| X3 | 2048 raw Huang lesion-contrastive encoder features | Embedding components and norm. A lesion-trained encoder is not the separate lesion detector; no lesion boxes/counts are available in this release. |
| X4 | 72 AutoMorph biomarkers | Whole-region, artery/vein and zone B/C descriptors: density, fractal complexity, tortuosity/curvature, width, caliber and cup/disc measures. No clinical thresholds are invented. |

The chatbot uses the current image's measured values and a small curated reference library. The LLM chooses explanation details; measurements and references are rendered from trusted facts. Papers explain methods and general limitations, not diagnoses for an uploaded image. No history or medication advice is inferred. Grad-CAM describes the image branch conditional on supplied tabular streams; it does not quantify causal contributions of X1–X4.

The grading checkpoint is frozen. The upload X3 transform matches EyePACS training (224px bicubic/ImageNet normalization). Historical APTOS/Messidor features used a different transform; those scores require consistent reevaluation. The assumed 0.008 mm/pixel is not measured physical calibration.

References are stored in references.json with original paper links. No article text or patient data is bundled.
