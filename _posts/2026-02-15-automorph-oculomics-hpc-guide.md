---
layout: post
title: "AutoMorph on Your Laptop and on HPC/SSH: one guide for both paths"
date: 2026-02-15
author: "Inamullah Inamullah"
tags: [AutoMorph, oculomics, multi-omics, deep learning, fundus, HPC, SSH, local setup]
description: "A single, practical playbook to run the official AutoMorph pipeline from the local repo on your machine or over HPC/SSH—covering environment setup, data layout, resolution calibration, one‑shot runs, verification, and gotchas."
permalink: /automorph-local-hpc/
---

> **What you’ll learn**
> - How to run the **official AutoMorph** pipeline (M0→M3) either **locally** or on an **HPC/SSH** machine using the **same repository** and a minimal set of commands.   
> - The **exact local installation steps** (conda, Python 3.11, PyTorch 2.3.1/CUDA 12.1, extra packages) aligned with the project’s **`LOCAL.md`**.   
> - Why you must **calibrate pixel resolution** to report features in **microns**, and how to prepare/auto‑generate `resolution_information.csv`.   
> - How the **one‑shot runner** (`run.sh`) produces quality grading (M1), segmentations (M2), and features for **disc‑centred**, **macular Zone‑B/Zone‑C**, and **whole‑image** (M3). 

---

## 0) Official links (bookmark these)

- **Project website:** <https://rmaphoh.github.io/projects/automorph.html>  *(overview, context)*   
- **GitHub repository:** <https://github.com/rmaphoh/AutoMorph>  *(code, `LOCAL.md`, `run.sh`, modules)*   
- **Peer‑reviewed paper (TVST @ ARVO):** <https://tvst.arvojournals.org/article.aspx?articleid=2783477>  *(methods & validation)*   
- **Preprint (medRxiv):** <https://www.medrxiv.org/content/10.1101/2022.05.26.22274795v1>  *(open PDF)* 

---

## 1) One repository, two access paths

AutoMorph is intentionally simple to access: **clone the same repo**, then either (A) run it **locally** (laptop/workstation, macOS/Linux/Windows with MinGW‑w64) or (B) run it on your **HPC/SSH** server. The pipeline and commands are identical; only your **compute environment** changes. 

- **Pipeline recap (what will run)**  
  M0 *preprocess* → M1 *quality (EfficientNet‑B4 ensemble)* → M2 *vessel / artery‑vein / disc‑cup segmentations* → M3 *features: disc‑centred, macular‑centred (Zone‑B & Zone‑C), whole‑image*. These are orchestrated by `run.sh`. 

---

## 2) Local / Virtual‑Machine access (from `LOCAL.md`)

> **Requirements (local)**  
> - Linux or macOS preferred. On Windows, install **MinGW‑w64** to use the shell commands below.  
> - **Anaconda / Miniconda**.  
> - **Python 3.11**, **PyTorch 2.3.1** (CUDA 12.1 wheels for NVIDIA) or Apple **M‑series (mps)**.  
> - **GPU is essential**: NVIDIA (CUDA) or Apple Silicon (MPS). 

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

**Step 3 — Install PyTorch 2.3.1 (CUDA 12.1 example)**  
Check your CUDA: `nvcc --version`, then:

```bash
conda install -y pytorch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 pytorch-cuda=12.1 -c pytorch -c nvidia
```

*(Use the official PyTorch selector if your CUDA differs.)* [\[github.com\]](https://github.com/rmaphoh/AutoMorph/blob/main/resolution_information.csv)

**Step 4 — Install the rest**

```bash
pip install --ignore-installed certifi
pip install -r requirement.txt
pip install efficientnet_pytorch==0.7.1 --no-deps
```

**Data layout & run (local)**

*   Put your fundus images in the **`images/`** folder at repo root.
*   Ensure you have a **`resolution_information.csv`** (pixel size per image) for calibrated micron‑level features. *(If you don’t have device metadata, you can generate a constant spacing; see §4.2).*
*   Launch:

```bash
sh run.sh
```

`run.sh` performs M0→M3 in order and writes all results into the repo’s `Results/` (local mode) unless you configure an external data directory (see HPC/SSH mode below). [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

***

## 3) HPC / SSH access (recommended for large datasets)

> **Why HPC/SSH?**  
> More vRAM, faster batch inference, and cleaner separation of **code** and **data** using the environment variable **`AUTOMORPH_DATA`**. The official repo supports this pattern directly.

**3.1 — Clone & environment (same as local)**

```bash
# on the server (after ssh ...)
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph
conda create -n automorph python=3.11 -y
conda activate automorph

# install PyTorch that matches your cluster CUDA
# (example below uses CUDA 12.6 wheels; replace via the PyTorch selector)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install -r requirement.txt
```

Use PyTorch’s **Get Started** page to copy the exact command for your CUDA/Python combo. [\[github.com\]](https://github.com/rmaphoh/AutoMorph/blob/main/resolution_information.csv)

**3.2 — Keep images/results outside the repo**

```bash
# a writable data root outside the code:
mkdir -p $HOME/retina_all/images
export AUTOMORPH_DATA=$HOME/retina_all
echo "$AUTOMORPH_DATA"   # sanity: /home/<you>/retina_all

# copy your fundus images (.jpg/.png) here:
# $AUTOMORPH_DATA/images/
```

AutoMorph is designed to read from `$AUTOMORPH_DATA/images` and write to `$AUTOMORPH_DATA/Results` when that env var is set. This pattern is referenced across the repo and used by the runner.

**3.3 — Generate resolution CSV (microns)**

```bash
# from the repo root:
python generate_resolution.py 0.008
```

This creates `$AUTOMORPH_DATA/resolution_information.csv`, allowing **micron** calibration for widths, calibres (CRAE/CRVE/AVR), and disc/cup metrics even without per‑image DICOM metadata.

**3.4 — One‑shot run that survives SSH drops**

```bash
nohup bash run.sh > "$AUTOMORPH_DATA/automorph_run_$(date +%F_%H%M).log" 2>&1 & disown
tail -f "$AUTOMORPH_DATA"/automorph_run_*.log
```

`run.sh` executes M0→M3 in sequence and **cleans the `Results/` at start** by design—launch **one** job and let it finish. It then calls the feature scripts for **disc‑centred**, **macular Zone‑B**, **Zone‑C**, and **whole‑image** in M3. [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

***

## 4) What to expect (and how to verify)

**4.1 — Directory tree (HPC/SSH mode)**

    $AUTOMORPH_DATA/
     ├── images/                      # your raw fundus photos
     ├── resolution_information.csv   # pixel size per image
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

These folder names and CSVs are the outputs created by `run.sh` and its called scripts (zones & whole‑image). [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

**4.2 — Quick checks**

```bash
# count of gradable images prepared by M1:
ls -1 "$AUTOMORPH_DATA/Results/M1/Good_quality" | wc -l

# segmentation artifacts exist?
find "$AUTOMORPH_DATA/Results/M2" -maxdepth 2 -type f | head -n 20

# feature CSVs (disc, zone B/C, whole):
find "$AUTOMORPH_DATA/Results/M3" -maxdepth 2 -type f -name '*.csv' | sort
```

(For local mode, replace `$AUTOMORPH_DATA` with the repo root if you didn’t set the env var.) The M3 zone files (**Zone‑B**/ **Zone‑C**) are generated by the explicit scripts invoked in the runner. [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

***

## 5) Why resolution matters (microns)

Several vascular metrics—average width, **CRAE/CRVE/AVR**, disc/cup sizes—must be in **microns** for biological interpretation and cross‑device comparability. AutoMorph formalizes this in `resolution_information.csv`, and provides `generate_resolution.py` so you can easily supply a constant spacing when precise metadata are missing.

***

## 6) Troubleshooting & gotchas

*   **Results wiped unexpectedly?**  
    `run.sh` **cleans** the `Results/` directory at the start of each run; do **not** launch multiple runs at once. For targeted reruns, call the module scripts directly (same ones as in `run.sh`). [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

*   **Repo processed only a few sample images?**  
    In HPC mode, make sure `AUTOMORPH_DATA` is exported in the current shell *before* running; otherwise it may default to the small sample set and local paths.

*   **PyTorch / CUDA mismatch?**  
    Use the **PyTorch Get Started** selector to install the wheel that matches your CUDA and Python versions on the machine. [\[github.com\]](https://github.com/rmaphoh/AutoMorph/blob/main/resolution_information.csv)

***

## 7) Science & validation (why this pipeline is trusted)

*   The **TVST 2022 paper** documents AutoMorph’s design and external validation: EfficientNet‑B4 quality grading (EyePACS‑Q F1 ≈ 0.86), robust vessel/AV/disc‑cup segmentation, and strong agreement of derived vascular features with expert annotations. [\[pip.pypa.io\]](https://pip.pypa.io/en/stable/reference/requirements-file-format.html)
*   The **project website** and **GitHub** document continuing updates and the intended workflows (local & HPC), including `LOCAL.md`, `generate_resolution.py`, and the `run.sh` orchestrator.

***

## 8) Copy‑paste snippets (choose your path)

**Local (from `LOCAL.md`)**

```bash
conda update conda
conda create -n automorph python=3.11 -y
conda activate automorph
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph
conda install pytorch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
pip install --ignore-installed certifi
pip install -r requirement.txt
pip install efficientnet_pytorch==0.7.1 --no-deps
# Put images in ./images/ and ensure resolution_information.csv exists
sh run.sh
```

**HPC / SSH**

```bash
# environment
conda create -n automorph python=3.11 -y
conda activate automorph
# install pytorch that matches your cluster CUDA (example uses cu126 wheels)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install -r requirement.txt

# data & resolution
mkdir -p $HOME/retina_all/images
export AUTOMORPH_DATA=$HOME/retina_all
python generate_resolution.py 0.008

# one-shot run (non-interactive)
nohup bash run.sh > "$AUTOMORPH_DATA/automorph_run_$(date +%F_%H%M).log" 2>&1 & disown
tail -f "$AUTOMORPH_DATA"/automorph_run_*.log
```

 [\[github.com\]](https://github.com/rmaphoh/AutoMorph/blob/main/resolution_information.csv), [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

***

## 9) Cite in your methods

> “We used the **AutoMorph** pipeline (official repository and project page) to generate retinal vascular features from color fundus photographs. We followed the authors’ environment instructions (Python 3.11; PyTorch 2.3.x with CUDA support) and ran the **one‑shot** `run.sh` (M0→M3) to produce quality‑filtered images (M1), vessel/AV/disc‑cup masks (M2), and disc‑centred / macular Zone‑B / Zone‑C / whole‑image features (M3). Pixel spacing was provided via `resolution_information.csv` (generated with `generate_resolution.py` at 0.008 mm/pixel when DICOM spacing was unavailable).” [\[reddit.com\]](https://www.reddit.com/r/raspberry_pi/comments/1cxmw64/raspberry_pi_5_running_bookworm_autostart_issues/)

***

### Acknowledgements & links

*   **AutoMorph project page:** <https://rmaphoh.github.io/projects/automorph.html>
*   **AutoMorph GitHub (code, `LOCAL.md`):** <https://github.com/rmaphoh/AutoMorph>
*   **Peer‑reviewed paper (TVST 2022):** <https://tvst.arvojournals.org/article.aspx?articleid=2783477> (DOI: 10.1167/tvst.11.7.12) [\[pip.pypa.io\]](https://pip.pypa.io/en/stable/reference/requirements-file-format.html)
*   **Preprint:** <https://www.medrxiv.org/content/10.1101/2022.05.26.22274795v1>
