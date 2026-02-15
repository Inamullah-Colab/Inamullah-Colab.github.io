---
layout: post
title: "AutoMorph from Local Repo to HPC/SSH: one definitive guide"
date: 2026-02-15
author: "Inamullah Inamullah"
tags: [AutoMorph, oculomics, deep learning, fundus, pipeline, HPC, SSH, local setup]
description: "A single, detailed guide to run the official AutoMorph pipeline locally or on HPC/SSH, with clean setup steps, valid references, resolution calibration, and reproducible outputs."
permalink: /automorph-local-and-hpc/
---

> **What this guide gives you**
> - A single workflow for both **local** and **HPC/SSH** execution using the same AutoMorph repository.
> - Local setup aligned with official `LOCAL.md` guidance.
> - Reproducible data handling with `AUTOMORPH_DATA`.
> - Correct micron-scale calibration using `resolution_information.csv` and `generate_resolution.py`.
> - Only authoritative references: project page, GitHub repo/docs, TVST 2022 paper, and medRxiv preprint.

---

## 1) What AutoMorph does

**AutoMorph** is an open, modular deep-learning pipeline for retinal fundus photos:
- **M0**: preprocessing
- **M1**: image quality grading
- **M2**: vessel / artery-vein / optic disc-cup segmentation
- **M3**: vascular feature extraction (disc-centred, macular Zone B/C, whole-image)

For methods and validation, use the peer-reviewed TVST paper and official project resources.

---

## 2) One repository, two execution paths

Use the same codebase in both cases:
- **Local** (laptop/workstation): best for development and smaller batches.
- **HPC/SSH**: best for large datasets and long runs.

Pipeline logic remains the same; only compute environment changes.

---

## 3) Local setup (official pattern)

Follow the maintainer guide:
- `LOCAL.md`: <https://github.com/rmaphoh/AutoMorph/blob/main/LOCAL.md>

Typical local setup:

```bash
conda update conda
conda create -n automorph python=3.11 -y
conda activate automorph
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph
```

Install PyTorch matching your hardware/CUDA (example from project guidance):

```bash
conda install pytorch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

Install remaining dependencies:

```bash
pip install --ignore-installed certifi
pip install -r requirement.txt
pip install efficientnet_pytorch==0.7.1 --no-deps
```

Put input fundus images in `images/`, ensure `resolution_information.csv` exists, then run:

```bash
sh run.sh
```

Runner reference:
- `run.sh`: <https://github.com/rmaphoh/AutoMorph/blob/main/run.sh>

---

## 4) HPC/SSH setup (recommended for scale)

### 4.1 Clone and create environment

```bash
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph
conda create -n automorph python=3.11 -y
conda activate automorph
pip install -r requirement.txt
```

If using GPU nodes, install PyTorch to match cluster CUDA.

### 4.2 Keep data outside the repo

```bash
mkdir -p $HOME/retina_all/images
export AUTOMORPH_DATA=$HOME/retina_all
```

Place images in `$AUTOMORPH_DATA/images`.

### 4.3 Create resolution CSV (microns)

```bash
python generate_resolution.py 0.008
```

This creates `resolution_information.csv` for calibrated width/calibre measurements.

### 4.4 Run safely over SSH

```bash
nohup bash run.sh > "$AUTOMORPH_DATA/automorph_run_$(date +%F_%H%M).log" 2>&1 & disown
tail -f "$AUTOMORPH_DATA"/automorph_run_*.log
```

Important: `run.sh` cleans `Results/` at start, so do not launch multiple runs in parallel.

---

## 5) Expected outputs

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

Quick checks:

```bash
ls -1 "$AUTOMORPH_DATA/Results/M1/Good_quality" | wc -l
find "$AUTOMORPH_DATA/Results/M2" -maxdepth 2 -type f | head -n 20
find "$AUTOMORPH_DATA/Results/M3" -maxdepth 2 -type f -name '*.csv' | sort
```

---

## 6) Common pitfalls

- `run.sh` is not parallel-safe for multiple concurrent runs (it clears `Results/` first).
- Forgetting `AUTOMORPH_DATA` in HPC sessions can lead to wrong input/output paths.
- Missing or incorrect pixel spacing reduces biological interpretability of calibre/width metrics.

---

## 7) Methods text (copy-ready)

> We used AutoMorph to extract retinal vascular phenotypes from color fundus images. The official `run.sh` workflow was executed from M0 to M3 (preprocessing, quality grading, vessel/AV/disc-cup segmentation, and feature extraction for disc-centred, macular Zone B/C, and whole-image regions). Pixel spacing was provided using `resolution_information.csv` generated with `generate_resolution.py` when per-image metadata were unavailable.

---

## 8) Authoritative references

- AutoMorph project page: <https://rmaphoh.github.io/projects/automorph.html>
- AutoMorph GitHub repository: <https://github.com/rmaphoh/AutoMorph>
- Local installation guide (`LOCAL.md`): <https://github.com/rmaphoh/AutoMorph/blob/main/LOCAL.md>
- Pipeline runner (`run.sh`): <https://github.com/rmaphoh/AutoMorph/blob/main/run.sh>
- TVST 2022 paper (peer-reviewed): <https://tvst.arvojournals.org/article.aspx?articleid=2783477>
- medRxiv preprint: <https://www.medrxiv.org/content/10.1101/2022.05.26.22274795v1>
