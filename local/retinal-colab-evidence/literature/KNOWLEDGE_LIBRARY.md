# Ophthalmology and oculomics knowledge library

The source of truth is app/knowledge_base.json: 26 curated, cited topics with review dates and explicit scope boundaries. Coverage includes DR, macular edema, glaucoma, AMD, cataract, dry eye, refraction, vein occlusion, detachment, systemic diabetes/blood-pressure context, cardiovascular/kidney research, foundation models, oculomics and vessel-feature methods. It is a limited educational library, not all ophthalmology or a clinically validated diagnostic knowledge base.

## How answers are made

Character-based retrieval and exact topic aliases find relevant source cards. The local Qwen model selects whitelisted fact identifiers. Only reviewed source statements are rendered; arbitrary model-generated medical claims and identifiers are rejected. The current image report supplies metric values without changing them. Method boundaries remain attached to each topic. Specific questions do not repeat the full four-stream introduction. Short follow-ups can use the last question for retrieval context.

## What has not been trained

No new fine-tuning, image retraining, or systemic disease head was added. Retrieval makes curated knowledge available at inference time. Cardiovascular, kidney and neurological research associations do not establish individual diagnoses from this DR model. Medication and patient-record workflows remain outside scope.

## Updating the library

Add a unique topic ID, clear keywords, short factual statements, a supporting primary/official source URL, reviewed date and deployment-specific boundary. Run tests/test_knowledge.py and actual-model development checks. Do not paste full copyrighted papers, patient data, or unsupported clinical cutoffs. Review source changes periodically. No external requests or patient uploads occur during retrieval; the library and model run locally.

## Validation

Development tests check topic relevance, unrelated-question abstention, exact measurement preservation, short follow-up resolution, whitelist enforcement and systemic-diagnosis limitations. These tests are not clinical validation. Broader evaluation and expert review remain necessary before clinical use.
