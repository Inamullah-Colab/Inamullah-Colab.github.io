---
title: "Retinal Evidence Explorer: morphology, grading and LLM explanations"
excerpt: "Inspect X1–X4 vessel structures, weak evidence, Grad-CAM and biomarkers, or run the interactive Colab notebook."
collection: portfolio
---

[Open the retinal evidence website](/retinal-grade-chat/)

[Open the free interactive Colab notebook](https://colab.research.google.com/github/Inamullah-Colab/Inamullah-Colab.github.io/blob/master/local/retinal-colab-evidence/notebooks/Retinal_Evidence_Explorer.ipynb)

Actual image predictions are accompanied by vessel skeleton overlays, all 72 X4 biomarkers, weak X2 evidence maps, a separate true Grad-CAM, and summaries of the lesion-trained X3 representation. A local Qwen assistant explains measured results with primary literature citations. X3 is an encoder; lesion boxes and counts are unavailable.

The separate source package is in local/retinal-colab-evidence. Colab requires the supplied model bundle in the user's Drive and starts no public server. The website backend still requires the existing server and temporary tunnel. Historical external scores require consistent X3 preprocessing reevaluation. This is research software requiring clinical review.
