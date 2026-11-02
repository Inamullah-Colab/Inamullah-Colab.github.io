---
title: "Retinal Grade Explorer: image grading and live LLM explanations"
excerpt: "Upload a retinal JPG/PNG for X1–X4 extraction, ResNet-152 grading, probabilities and live Qwen explanations. Research demonstration."
collection: portfolio
---

[Open the retinal image grading demo](/retinal-grade-chat/)

Upload a retinal photograph to run the original X1–X4 extractors and frozen ResNet-152 grader. The page displays all five class probabilities and a live Qwen explanation tied to the server-held prediction. Optional examples are illustrative.

This is a research model requiring clinical review. Historical external evaluation used different X3 preprocessing from training, so those scores are not performance estimates for this training-aligned upload pipeline. Consistent reevaluation is needed. No treatment decisions or patient history are included. The temporary HTTPS backend requires the existing research server to remain running.
