---
layout: post
title: "AutoMorph from the Local Repo and on HPC/SSH — one definitive guide"
date: 2026-02-15
author: "Inamullah Inamullah"
tags: [AutoMorph, oculomics, deep learning, fundus, pipeline, HPC, SSH, local setup]
description: "Run the official AutoMorph pipeline (M0→M3) from the local repository or on HPC/SSH — using the exact LOCAL.md steps, correct links, resolution calibration, one‑shot runs, verification, and gotchas."
permalink: /automorph-local-and-hpc/
---

> **What you’ll get here**
> - The **exact local setup** copied from the project’s **`LOCAL.md`** (conda, Python 3.11, PyTorch 2.3.1/CUDA 12.1, extra packages).   
> - A clean **HPC/SSH** pattern that keeps images/results outside the repo via **`AUTOMORPH_DATA`**, as supported by the official code.   
> - How and why to create **`resolution_information.csv`** so calibre/width and disc/cup metrics are in **microns**, using the repo’s helper.   
> - What the runner **`run.sh`** actually does — **M0→M3**, **cleans `Results/` at start**, then calls zone & whole‑image feature scripts. (Direct link to the runner.)   
> - Authoritative links (project page, GitHub, TVST paper, preprint) for methods and citations. 

---

## 1) Quick context — what AutoMorph is and why it matters

**AutoMorph** is an open, modular deep‑learning pipeline for color fundus photographs:  
- **M0**: pre‑processing  
- **M1**: image quality grading (EfficientNet‑B4 ensemble)  
- **M2**: binary vessel, artery/vein, and optic disc/cup segmentation  
- **M3**: vascular feature measurement (disc‑centred, **macular Zone‑B & Zone‑C**, and **whole‑image**).  

The peer‑reviewed **TVST (ARVO) 2022** paper documents both design and external validation; the **project page** and **GitHub** are the canonical sources for code and usage. 

---

## 2) Choose your path: **local** vs **HPC/SSH**

You always use the **same** official repository. For quick experiments or small batches, do a **local** install; for larger datasets, use **HPC/SSH** with `AUTOMORPH_DATA` so your images/results live outside the repo (safer for quotas & permissions). Both modes are supported by the official code/docs. 

---

## 3) Local / Virtual‑Machine setup (from `LOCAL.md`)

> These steps are reproduced directly from the official **LOCAL.md**. If the maintainers update anything, **defer to the current LOCAL.md**:  
> `https://github.com/rmaphoh/AutoMorph/blob/main/LOCAL.md` 

**Requirements (local)**  
- Linux or macOS preferred. On Windows, install **MinGW‑w64** to use the shell commands.  
- **Anaconda/Miniconda**.  
- **python=3.11, torch=2.3**.  
- **GPU is essential** — NVIDIA (CUDA) or Apple M‑series (**mps**). 

**Step 1 — Create the environment**
```bash
conda update conda
conda create -n automorph python=3.11 -y
````

**Step 2 — Activate and clone**

```bash
conda activate automorph
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph
```

**Step 3 — Install PyTorch 2.3.1 (CUDA 12.1 example from LOCAL.md)**  
(Check your CUDA with `nvcc --version`.)

```bash
conda install pytorch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

**Step 4 — Install remaining packages**

```bash
pip install --ignore-installed certifi
pip install -r requirement.txt
pip install efficientnet_pytorch==0.7.1 --no-deps
```

**Run (local mode)**

*   Put your fundus images in the repo’s **`images/`** folder.
*   Prepare **`resolution_information.csv`** (pixel size per image) for your dataset (see §5 to generate one quickly).
*   Launch:

```bash
sh run.sh
```

The runner’s logic/order is defined here (official):  
`https://github.com/rmaphoh/AutoMorph/blob/main/run.sh` (M0→M3, cleans `Results/` at start, then calls zone/whole‑image feature scripts). [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

***

## 4) HPC / SSH setup (same repo, cluster‑friendly)

The repo supports a **data‑outside‑code** pattern via **`AUTOMORPH_DATA`** so images and results live in a writable area outside the repository. This is standard for HPC and also used in the AutoMorph tooling.

**4.1 — Clone & environment**

```bash
# after ssh:
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph

conda create -n automorph python=3.11 -y
conda activate automorph

# install torch/torchvision appropriate for your cluster CUDA (use your site-standard)
pip install -r requirement.txt
```

(Use the same versions as your local test or those from `LOCAL.md` to keep environments consistent.)

**4.2 — Keep images/results outside the repo**

```bash
mkdir -p $HOME/retina_all/images
export AUTOMORPH_DATA=$HOME/retina_all
# copy .jpg/.png fundus images into $AUTOMORPH_DATA/images/
```

When `AUTOMORPH_DATA` is set, the pipeline reads from `$AUTOMORPH_DATA/images` and writes to `$AUTOMORPH_DATA/Results`, as designed in the official code.

**4.3 — One‑shot run that survives disconnects**

```bash
# (generate resolution CSV first — see §5)
nohup bash run.sh > "$AUTOMORPH_DATA/automorph_run_$(date +%F_%H%M).log" 2>&1 & disown
tail -f "$AUTOMORPH_DATA"/automorph_run_*.log
```

`run.sh` performs M0→M3, **deletes the `Results/` folder at the start (by design)**, and invokes feature scripts for **disc‑centred**, **macular Zone‑B/Zone‑C**, and **whole‑image**. See the runner for the exact order and commands. [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

***

## 5) Calibrate features in **microns** with `resolution_information.csv`

Many vascular features (vessel width, **CRAE/CRVE/AVR**, disc/cup) require **micron‑scale** calibration, not pixels. The official repo ships both the **file contract** and a **helper**:

*   **File**: `resolution_information.csv` → pixel size per image.
*   **Helper**: `generate_resolution.py` to create the CSV (e.g., a constant spacing when per‑image DICOM metadata are unavailable).

Run from the repo root, optionally using a constant like `0.008` **mm/pixel** (adjust for your camera):

```bash
python generate_resolution.py 0.008
```

This will write the CSV in your active data location (under `AUTOMORPH_DATA` if set). Both the file and helper are part of the official repository.

***

## 6) What success looks like — folder map and quick checks

**6.1 — Expected tree (HPC/SSH)**

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

This structure (and the feature CSVs) reflects what the **official runner** executes (zones & whole‑image scripts). [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

**6.2 — Sanity checks**

```bash
# how many gradable images were prepared by M1?
ls -1 "$AUTOMORPH_DATA/Results/M1/Good_quality" | wc -l

# segmentation artifacts exist?
find "$AUTOMORPH_DATA/Results/M2" -maxdepth 2 -type f | head -n 20

# feature CSVs (disc, zone B/C, whole)
find "$AUTOMORPH_DATA/Results/M3" -maxdepth 2 -type f -name '*.csv' | sort
```

***

## 7) Gotchas (so you don’t lose a day)

*   **Don’t launch multiple `run.sh` in parallel**: the runner **cleans** `Results/` at the start by design. If you need to re‑run a single stage, call the same module scripts `run.sh` uses (see the file for exact commands). [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)
*   **Remember `AUTOMORPH_DATA` on HPC**: if you forget to export it, the pipeline may fall back to local paths and process only a tiny sample. The external data‑dir pattern is supported in the repo to keep your code tree clean.
*   **Use the official docs for local installs**: the definitive local instructions are maintained in **`LOCAL.md`**. Always check that file for version bumps or flags.

***

## 8) Methods blurb you can paste into papers

> We used **AutoMorph** (official repository and project page) to compute retinal vascular features from color fundus photographs. We followed the authors’ instructions (Python 3.11, PyTorch 2.3.1/CUDA 12.1) and ran the **one‑shot** `run.sh` (M0→M3) to produce quality‑filtered images (M1), vessel/AV/disc‑cup masks (M2), and disc‑centred / **macular Zone‑B** / **Zone‑C** / **whole‑image** features (M3). Pixel spacing was provided via `resolution_information.csv` (generated with `generate_resolution.py` when DICOM spacing was unavailable). We cite the project website, GitHub, and the **TVST 2022** paper. [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/), [\[pip.pypa.io\]](https://pip.pypa.io/en/stable/reference/requirements-file-format.html)

***

## 9) Authoritative links

*   **AutoMorph project page (official):** <https://rmaphoh.github.io/projects/automorph.html>
*   **AutoMorph GitHub repository:** <https://github.com/rmaphoh/AutoMorph>  (code, `LOCAL.md`, `run.sh`)
*   **Runner (exact module order & cleaning behavior):** <https://github.com/rmaphoh/AutoMorph/blob/main/run.sh> [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)
*   **Local installation guide:** <https://github.com/rmaphoh/AutoMorph/blob/main/LOCAL.md>
*   **Peer‑reviewed paper (TVST 2022 @ ARVO):** <https://tvst.arvojournals.org/article.aspx?articleid=2783477>  (DOI: 10.1167/tvst.11.7.12) [\[pip.pypa.io\]](https://pip.pypa.io/en/stable/reference/requirements-file-format.html)
*   **Preprint (medRxiv):** <https://www.medrxiv.org/content/10.1101/2022.05.26.22274795v1>
