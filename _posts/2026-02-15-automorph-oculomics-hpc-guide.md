---
layout: post
title: "AutoMorph from Local Repo to HPC/SSH: one definitive guide"
date: 2026-02-15
author: "Inamullah Inamullah"
tags: [AutoMorph, oculomics, deep learning, fundus, pipeline, HPC, SSH, local setup]
description: "A detailed, reproducible guide to run the official AutoMorph pipeline locally or on HPC/SSH, with validated setup steps, resolution calibration, outputs, quality controls, and publication-ready reporting."
permalink: /automorph-local-and-hpc/
---

> **Executive summary**
> - AutoMorph converts fundus photos into quantitative retinal phenotypes through a four-stage pipeline (M0-M3).
> - The same repository supports both local runs and HPC/SSH runs.
> - For reproducibility at scale, keep data outside code with `AUTOMORPH_DATA`, run `run.sh` once per job, and calibrate `resolution_information.csv` for micron-scale metrics.
> - This guide keeps only authoritative sources: official project page, repository (`LOCAL.md`, `run.sh`), TVST 2022 paper, and medRxiv preprint.

---

## 1) Definitions first: what this pipeline is for

- **Oculomics**: using retinal features as biomarkers for systemic biology and disease risk.
- **AutoMorph**: an end-to-end deep-learning pipeline for color fundus images, producing standardized image quality outputs, segmentation masks, and tabular vascular features.
- **Why this matters for research**: manual vascular annotation does not scale well across cohorts. AutoMorph enables consistent, automated phenotyping suitable for downstream statistical and machine learning analyses.

AutoMorph resources:
- Project page: <https://rmaphoh.github.io/projects/automorph.html>
- Repository: <https://github.com/rmaphoh/AutoMorph>

---

## 2) Pipeline anatomy (M0-M3)

AutoMorph executes four modules in sequence:

- **M0: Pre-processing**
  - Standardizes inputs before model inference.
  - Reduces variation from raw camera exports.

- **M1: Image quality grading**
  - Selects gradable images for downstream segmentation and feature extraction.
  - Outputs quality predictions and a `Good_quality` subset.

- **M2: Segmentation**
  - Produces three core segmentation outputs:
    - vessel binary map
    - artery/vein map
    - optic disc/cup map

- **M3: Feature extraction**
  - Generates regional vascular features for:
    - disc-centred region
    - macular-centred Zone B
    - macular-centred Zone C
    - whole image
  - Outputs CSV files suitable for analysis pipelines.

Peer-reviewed performance and validation details are in TVST 2022.

---

## 3) Local vs HPC/SSH: one codebase, different compute mode

Use the same GitHub repository in both modes.

- **Local mode** is best for setup validation, debugging, and smaller image batches.
- **HPC/SSH mode** is best for large datasets, long jobs, and reproducibility under shared infrastructure.

The module order is identical in both modes because both rely on the same orchestrator:
- `run.sh`: <https://github.com/rmaphoh/AutoMorph/blob/main/run.sh>

---

## 4) Local setup (aligned with official `LOCAL.md`)

Canonical instructions:
- `LOCAL.md`: <https://github.com/rmaphoh/AutoMorph/blob/main/LOCAL.md>

### 4.1 Create environment

```bash
conda update conda
conda create -n automorph python=3.11 -y
conda activate automorph
```

### 4.2 Clone repository

```bash
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph
```

### 4.3 Install PyTorch stack (example used in official local guidance)

```bash
conda install pytorch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

### 4.4 Install remaining requirements

```bash
pip install --ignore-installed certifi
pip install -r requirement.txt
pip install efficientnet_pytorch==0.7.1 --no-deps
```

### 4.5 Prepare data and run

- Put fundus images in `images/`.
- Ensure `resolution_information.csv` is present (see Section 6).
- Run the full pipeline:

```bash
sh run.sh
```

---

## 5) HPC/SSH setup (recommended for large-scale runs)

### 5.1 Environment and repository

```bash
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph
conda create -n automorph python=3.11 -y
conda activate automorph
pip install -r requirement.txt
```

Install PyTorch packages compatible with your cluster GPU/CUDA policy.

### 5.2 Keep code and data separate

```bash
mkdir -p $HOME/retina_all/images
export AUTOMORPH_DATA=$HOME/retina_all
```

Place input images under:

```bash
$AUTOMORPH_DATA/images
```

Why this is important:
- avoids writing heavy outputs into the code tree
- simplifies permissions and quota handling
- improves run-to-run reproducibility

### 5.3 Generate or provide pixel resolution file

```bash
python generate_resolution.py 0.008
```

This creates `resolution_information.csv` for width/calibre calibration in physical units.

### 5.4 Run detached over SSH

```bash
nohup bash run.sh > "$AUTOMORPH_DATA/automorph_run_$(date +%F_%H%M).log" 2>&1 & disown
tail -f "$AUTOMORPH_DATA"/automorph_run_*.log
```

Operational note:
- `run.sh` cleans `Results/` at job start by design.
- Do not launch multiple `run.sh` jobs against the same data root at the same time.

---

## 6) Resolution calibration: why micron units matter

Many vascular metrics are only biologically comparable when pixel spacing is known.

- File contract: `resolution_information.csv`
- Helper script: `generate_resolution.py`

If per-image metadata are unavailable, a documented constant (for your camera/device context) can be used temporarily. For publication-quality analyses, prefer device-specific spacing whenever available.

---

## 7) Output map and verification checklist

### 7.1 Expected output tree (HPC mode)

```text
$AUTOMORPH_DATA/
├── images/
├── resolution_information.csv
└── Results/
    ├── M1/
    │   ├── results_ensemble.csv
    │   └── Good_quality/
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
```

### 7.2 Practical checks

```bash
# how many images passed quality grading?
ls -1 "$AUTOMORPH_DATA/Results/M1/Good_quality" | wc -l

# were M2 masks generated?
find "$AUTOMORPH_DATA/Results/M2" -maxdepth 2 -type f | head -n 20

# are M3 feature tables present?
find "$AUTOMORPH_DATA/Results/M3" -maxdepth 2 -type f -name '*.csv' | sort
```

### 7.3 Provenance checklist for reproducibility

Record these fields with each run:
- AutoMorph commit hash and run date
- Python, PyTorch, CUDA versions
- GPU model and driver info
- `AUTOMORPH_DATA` path
- pixel spacing strategy (`resolution_information.csv` source)
- total input image count and M1 gradable count

---

## 8) Common failure modes and fixes

- **Issue: `Results/` unexpectedly overwritten**
  - Cause: another `run.sh` started while a job was active.
  - Fix: one orchestrated run per data root; stage-specific reruns should be planned explicitly.

- **Issue: only a tiny dataset processed**
  - Cause: `AUTOMORPH_DATA` not exported in current shell/session.
  - Fix: export and verify path (`echo $AUTOMORPH_DATA`) before running.

- **Issue: implausible calibre/width values**
  - Cause: missing/incorrect spacing in `resolution_information.csv`.
  - Fix: regenerate or replace spacing values with correct device-specific information.

- **Issue: package/GPU mismatch**
  - Cause: PyTorch/CUDA incompatibility.
  - Fix: align installed packages with cluster CUDA and verify import/runtime before full run.

---

## 9) Publication-ready methods text

> We used AutoMorph to extract retinal vascular phenotypes from color fundus photographs. The official pipeline orchestrator (`run.sh`) was executed from M0 to M3, including preprocessing, quality grading, vessel/artery-vein/disc-cup segmentation, and feature extraction for disc-centred, macular Zone B, macular Zone C, and whole-image regions. Pixel resolution was provided through `resolution_information.csv` (generated with `generate_resolution.py` when per-image metadata were unavailable), enabling width and calibre interpretation in physical units.

---

## 10) Authoritative references

- AutoMorph project page: <https://rmaphoh.github.io/projects/automorph.html>
- AutoMorph GitHub repository: <https://github.com/rmaphoh/AutoMorph>
- Local setup guide (`LOCAL.md`): <https://github.com/rmaphoh/AutoMorph/blob/main/LOCAL.md>
- Pipeline runner (`run.sh`): <https://github.com/rmaphoh/AutoMorph/blob/main/run.sh>
- TVST 2022 paper (peer-reviewed): <https://tvst.arvojournals.org/article.aspx?articleid=2783477>
- medRxiv preprint: <https://www.medrxiv.org/content/10.1101/2022.05.26.22274795v1>
