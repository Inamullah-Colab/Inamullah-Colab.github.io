---
layout: post
title: "AutoMorph for Oculomics on HPC: from Clear Problem → Proven Technique → Reproducible Solution"
date: 2026-02-15
author: "Inamullah Inamullah"
tags: [oculomics, multi-omics, deep learning, AutoMorph, fundus, segmentation, pipeline, HPC]
description: "A structured, research‑grade blog post that first defines the field, motivates the problem, explains the technique (AutoMorph), and then delivers a clean, reproducible HPC workflow with zone‑based macular, disc‑centred, and whole‑image features."
permalink: /automorph-oculomics-hpc-guide/
---

> **Executive summary (short form)**  
> **What**: AutoMorph is a validated, open pipeline that turns color fundus photographs into **quantitative retinal vascular features**—calibre (CRAE/CRVE/AVR), tortuosity, fractal dimension, vessel density, disc/cup metrics—ready for **multi‑omics** and **multi‑modal** modelling.   
> **Why now**: Oculomics—using ocular imaging as a window into systemic health—has accelerated with AI and biobank‑scale datasets; robust, automated pipelines are essential for reproducible phenotyping across cohorts.   
> **How (HPC quick start)**: keep data outside the repo (`AUTOMORPH_DATA`), generate pixel spacing for **micron** units, and run the **one‑shot** orchestrator `run.sh` (M0→M3). This produces quality‑filtered images (M1), three segmentations (M2), and features for **disc‑centred**, **macular‑centred Zone B & C**, and **whole‑image** (M3). 

---

## 1) Definitions first — the vocabulary we’ll use

- **Oculomics**: the use of ocular (retinal) biomarkers—derived from images and other modalities—to infer systemic health and disease risk (cardiometabolic, neurodegenerative, renal, environmental exposures, etc.). The retina is uniquely accessible, vascularized CNS tissue; AI makes its signals scalable and clinically meaningful.   
- **Multi‑omics / multi‑modal modelling**: linking genotypes, transcriptomics, metabolomics/lipidomics, clinical measurements, and imaging traits (here: retinal features) with statistical learning/AI to discover mechanisms and predict outcomes. Recent frameworks advocate “healthcare‑from‑the‑eye,” integrating oculomics with EHR/omics for proactive care.   
- **AutoMorph**: an open, modular deep‑learning pipeline (M0–M3) for fundus images. It standardizes images, grades quality, segments vessels/A‑V/disc‑cup, and quantifies vascular morphology (disc‑centred, **macular‑centred Zone B & Zone C**, whole‑image). The peer‑reviewed TVST 2022 paper details external validation. 

---

## 2) Motivation — the problems we must solve (and why they matter)

1. **Manual, inconsistent vascular measurements don’t scale**  
   Multi‑omics studies require *thousands–millions* of consistent phenotypes. Manual tracing is slow and observer‑dependent, which limits discovery and replication. A validated, automated pipeline enables population‑scale studies and cross‑site reproducibility.   

2. **We need *micron‑level* calibration for vascular biology**  
   Vessel calibre, disc/cup size, and width must be in **microns**, not pixels, for biological interpretation and cross‑device comparability. AutoMorph formalizes this through a resolution CSV or a documented constant spacing when DICOM data aren’t available.   

3. **Zone‑aware macular analysis captures spatial biology**  
   Macular **Zone B** (inner annulus around the fovea) and **Zone C** (outer annulus) reflect distinct vascular organization; comparing both helps study perfusion gradients, early microvascular remodeling, and disease‑specific signatures for multimodal models. AutoMorph natively computes both.   

4. **Bridging to multi‑omics and environmental health**  
   Survey and roadmap papers emphasize that retinal biomarkers integrate with genomics, metabolomics, and exposomics to improve both prediction and mechanism discovery; this *requires* standardized, high‑quality features at scale—AutoMorph’s raison d’être. 

---

## 3) Technique — the AutoMorph design (what it is, scientifically and technically)

**Pipeline (M0→M3)**  
- **M0**: pre‑processing (standardization).  
- **M1**: quality grading via an EfficientNet‑B4 ensemble (EyePACS‑Q style) → *produces* `Results/M1/Good_quality/` (the set used by downstream modules). Performance in the TVST paper: F1 ≈ 0.86 on EyePACS‑Q.   
- **M2**: three segmentation stacks → binary vessel, artery/vein classification, and optic disc/cup. Disc segmentation reaches F1 ≈ 0.94 in IDRiD; vessel segmentation generalizes across external datasets.   
- **M3**: quantitative features  
  - **Disc‑centred** (CDR, rim metrics, calibre/tortuosity/fractal geometry, density)  
  - **Macular‑centred Zone B** and **Zone C**  
  - **Whole‑image** morphology  
  The official runner calls the exact scripts for all zones and regions. 

**Key implementation choices that matter**  
- **Reproducibility**: `run.sh` orchestrator with fixed module order and **clean‑start** behavior (it wipes `Results` at the start by design to avoid cross‑run contamination).   
- **Separation of concerns**: images and outputs live *outside* the repo via `AUTOMORPH_DATA`. This is ideal for HPC (permissions/quotas/modules).   
- **Micron calibration**: `generate_resolution.py` writes a resolution CSV; alternatively, a documented constant (e.g., 0.008 mm/pixel for relevant devices) ensures biological comparability across datasets.   
- **Open science**: code, scripts, and documentation are public, with a peer‑reviewed reference and continuing updates (e.g., Python 3.11 / PyTorch 2.x support). 

---

## 4) Solution — a clean, reproducible **HPC/SSH** workflow

### 4.1. Clone code and set up environment
```bash
# On your server
mkdir -p $HOME/src && cd $HOME/src
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph

# Conda env (use the PyTorch selector for your CUDA/Python)
conda create -n automorph python=3.11 -y
conda activate automorph
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install -r requirement.txt
```

Use the PyTorch “Get Started” page to pick the exact wheel for your cluster’s CUDA/Python; this page is the canonical source for installation combos. [\[ioflood.com\]](https://ioflood.com/blog/pip-install-requirements-txt/)

### 4.2. Keep data outside the code (critical on HPC)

```bash
mkdir -p $HOME/retina_all/images
export AUTOMORPH_DATA=$HOME/retina_all
# copy .jpg/.png fundus images into $AUTOMORPH_DATA/images/
```

AutoMorph is built to read from `$AUTOMORPH_DATA/images` and write results to `$AUTOMORPH_DATA/Results`—this is documented in the repo and respected by the runner. [\[stackoverflow.com\]](https://stackoverflow.com/questions/55052434/does-python-requirements-file-have-to-specify-version)

### 4.3. Generate pixel resolution (microns) for biological interpretability

```bash
cd ~/src/AutoMorph
python generate_resolution.py 0.008
```

This creates `resolution_information.csv`. If you have DICOM/FDA pixel spacing per image, you can populate the CSV accordingly; otherwise a documented constant is acceptable (as per maintainers). [\[github.com\]](https://github.com/rmaphoh/AutoMorph/blob/main/resolution_information.csv)

### 4.4. One‑shot pipeline (M0→M3) that survives disconnects

```bash
nohup bash run.sh > "$AUTOMORPH_DATA/automorph_run_$(date +%F_%H%M).log" 2>&1 & disown
tail -f "$AUTOMORPH_DATA"/automorph_run_*.log
```

`run.sh` performs: preprocess → quality grading & merge → vessel/AV/disc‑cup segmentation → **disc‑centred**, **macular Zone B & C**, **whole‑image** features. Note the deliberate **clean‑start** deletion of `Results` at the beginning of each run. [\[github.com\]](https://github.com/rmaphoh/)

### 4.5. Verify outputs (what “good” looks like)

```bash
# M1: quality CSV + list of gradable images used downstream
ls -lh "$AUTOMORPH_DATA/Results/M1/results_ensemble.csv"
ls -1  "$AUTOMORPH_DATA/Results/M1/Good_quality" | wc -l

# M2: segmentation artifacts
find "$AUTOMORPH_DATA/Results/M2" -maxdepth 2 -type f | head -n 20

# M3: features (disc-centred, macular Zone B/C, whole-image)
find "$AUTOMORPH_DATA/Results/M3" -maxdepth 2 -type f -name '*.csv' | sort
```

Zone‑based macular features derive from the official scripts `create_datasets_macular_centred_B.py` and `..._C.py`, called by the runner. [\[github.com\]](https://github.com/rmaphoh/)

***

## 5) Linking features to **multi‑omics** and **multi‑modal** models

With AutoMorph complete, you get **tabular CSVs** for each image—calibre (CRAE/CRVE), AVR, vessel width/density, tortuosity (distance, squared curvature), fractal dimension, disc/cup metrics—suitable for:

*   **Genomic/lipidomic association** (GWAS/MWAS) and **causal inference** (Mendelian Randomization) using retinal traits as mediators or endpoints. [\[github.com\]](https://github.com/rmaphoh/)
*   **Risk modelling** that fuses retinal features with clinical covariates and omics. Recent position papers outline how oculomics integrates into healthcare frameworks with EHR and social determinants to enable proactive care. [\[geeksforgeeks.org\]](https://www.geeksforgeeks.org/machine-learning/image-feature-extraction-using-python/)
*   **Exposome/precision environmental health** studies where retinal biomarkers act as sensitive, non‑invasive indicators of exposure‑related vascular/neural changes. [\[github.com\]](https://github.com/Effendy77/Retinal-Feature-Extract-CKD)

The AutoMorph paper provides peer‑reviewed performance and external validation, supporting downstream analyses at cohort scale. [\[geeksforgeeks.org\]](https://www.geeksforgeeks.org/machine-learning/image-feature-extraction-using-python/)

***

## 6) Pitfalls and guardrails

*   **Don’t parallelize `run.sh`**: each invocation **deletes** the `Results` tree at start. Use a single one‑shot for full runs; call module scripts directly for stage‑specific reruns (same ones used by the runner). [\[github.com\]](https://github.com/rmaphoh/)
*   **Always export `AUTOMORPH_DATA`** in the current shell. Otherwise the code may fall back to local sample paths and you’ll process only a tiny demo set. [\[stackoverflow.com\]](https://stackoverflow.com/questions/55052434/does-python-requirements-file-have-to-specify-version)
*   **Ensure microns**: if you skip the resolution CSV, some features lose biological interpretability and cross‑device comparability. Use `generate_resolution.py` or your own per‑image spacing. [\[github.com\]](https://github.com/rmaphoh/AutoMorph/blob/main/resolution_information.csv)
*   **Record provenance**: AutoMorph commit date, PyTorch/CUDA/Python versions, GPU/CPU, number of gradable images, and your pixel spacing assumption—this is critical for multi‑omics reproducibility. [\[github.com\]](https://github.com/rmaphoh/AutoMorph/blob/main/resolution_information.csv)

***

## 7) Folder map (after a successful run)

    $AUTOMORPH_DATA/
     ├── images/                      # your raw fundus photos
     └── Results/
         ├── M1/
         │   ├── results_ensemble.csv
         │   └── Good_quality/        # images that proceed to M2/M3
         ├── M2/
         │   ├── Vessel_binary/
         │   ├── Artery_vein/
         │   └── Disc_cup/
         └── M3/
             ├── Disc_centred/*.csv
             ├── Macular_centred/
             │   ├── Macular_Zone_B_Measurement.csv
             │   └── Macular_Zone_C_Measurement.csv
             └── Whole_image/*.csv

This structure is generated by the official `run.sh` sequence and the feature scripts it calls. [\[github.com\]](https://github.com/rmaphoh/)

***

## 8) Methods blurb you can paste into a paper

> We used **AutoMorph** (UCL/Moorfields; commit date matching our run) to compute retinal vascular features from color fundus photographs. The pipeline ran M0–M3 (pre‑processing → image quality → vessel/artery‑vein/disc‑cup segmentation → zone‑based and whole‑image features) using the official `run.sh` orchestrator. Data were organized outside the repository via `AUTOMORPH_DATA`. Pixel spacing was set using `generate_resolution.py` (0.008 mm/pixel) to report **micron‑scale** width and calibre metrics. Outputs included disc‑centred, **macular‑centred Zone B & C**, and whole‑image CSVs. AutoMorph performance and external validation are reported in the TVST 2022 paper. [\[github.com\]](https://github.com/rmaphoh/AutoMorph/blob/main/resolution_information.csv), [\[github.com\]](https://github.com/rmaphoh/), [\[geeksforgeeks.org\]](https://www.geeksforgeeks.org/machine-learning/image-feature-extraction-using-python/)

***

## References

*   **AutoMorph official repository & docs** — modules, environment notes, `generate_resolution.py`, runner. [\[github.com\]](https://github.com/rmaphoh/AutoMorph/blob/main/resolution_information.csv)
*   **`run.sh` (pipeline order & cleaning behaviour; Zone B/C scripts)**. [\[github.com\]](https://github.com/rmaphoh/)
*   **AutoMorph TVST paper (2022)** — validation and performance across datasets. [\[geeksforgeeks.org\]](https://www.geeksforgeeks.org/machine-learning/image-feature-extraction-using-python/)
*   **PyTorch “Get Started”** — select correct wheel for your CUDA/Python. [\[ioflood.com\]](https://ioflood.com/blog/pip-install-requirements-txt/)
*   **Oculomics + multi‑omics surveys & frameworks** — 2025 survey (arXiv/Elsevier DOI), exposomics roadmap (Oxford Academic), and 2026 “Healthcare‑from‑the‑Eye” framework. [\[github.com\]](https://github.com/rmaphoh/), [\[github.com\]](https://github.com/Effendy77/Retinal-Feature-Extract-CKD), [\[geeksforgeeks.org\]](https://www.geeksforgeeks.org/machine-learning/image-feature-extraction-using-python/)
