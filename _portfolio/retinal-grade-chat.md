---
title: "RetinalInsight: contextual DR grading"
excerpt: "Inspect X1–X4 vessel structures, weak evidence, Grad-CAM and biomarkers, or run the interactive Colab notebook."
collection: portfolio
---

[Open the retinal evidence website](/retinal-grade-chat/)

[Open the free interactive Colab notebook](https://colab.research.google.com/github/Inamullah-Colab/Inamullah-Colab.github.io/blob/master/local/retinal-colab-evidence/notebooks/Retinal_Evidence_Explorer_v3.ipynb)

Actual image predictions are accompanied by vessel skeleton overlays, all 72 X4 biomarkers, weak X2 evidence maps, a separate true Grad-CAM, and summaries of the lesion-trained X3 representation. A local Qwen assistant explains measured results with primary literature citations. X3 is an encoder; lesion boxes and counts are unavailable.

[View the standalone source repository](https://github.com/Inamullah-Colab/retinalinsight-dr-grading). Source includes the dashboard, Colab runtime, method documentation and citations. Colab requires the supplied model bundle in the user's Drive and starts no public server. The website backend still requires the existing server and temporary tunnel. Historical external scores require consistent X3 preprocessing reevaluation. This is research software requiring clinical review.


Acknowledgements: [AutoMorph, Zhou et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9290317/), [lesion-based contrastive learning, Yijin Huang, Li Lin et al.](https://arxiv.org/abs/2107.08274), and [Grad-CAM, Selvaraju et al.](https://arxiv.org/abs/1610.02391). New X2 evidence maps use five distinct channel colours with fixed scales; these remain weak proxies rather than confirmed lesion detections.
