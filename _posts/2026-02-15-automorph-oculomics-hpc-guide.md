---
layout: post
title: "AutoMorph from Local Repo to HPC/SSH: one definitive guide"
date: 2026-02-15
author: "Inamullah Inamullah"
tags: [AutoMorph, oculomics, deep learning, fundus, pipeline, HPC, SSH, local setup]
description: "A detailed, reproducible guide to run the official AutoMorph pipeline locally or on HPC/SSH, with validated setup steps, resolution calibration, outputs, quality controls, and publication-ready reporting."
permalink: /automorph-local-and-hpc/
---

<style>
.automorph-page {
  --bg1: #f0f9ff;
  --bg2: #f7fee7;
  --ink: #0f172a;
  --muted: #334155;
  --primary: #0ea5e9;
  --secondary: #22c55e;
  --card: #ffffff;
  --ring: rgba(14, 165, 233, 0.18);
  color: var(--ink);
  font-family: "Segoe UI", "Trebuchet MS", Helvetica, Arial, sans-serif;
}

.automorph-hero {
  background: linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%);
  color: #ffffff;
  border-radius: 18px;
  padding: 28px;
  box-shadow: 0 12px 30px rgba(2, 132, 199, 0.22);
  margin: 12px 0 22px 0;
}

.automorph-hero h1 {
  margin: 0 0 10px 0;
  line-height: 1.2;
  font-size: clamp(1.4rem, 2.2vw, 2rem);
}

.automorph-hero p {
  margin: 8px 0 0 0;
  opacity: 0.98;
}

.automorph-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  margin: 16px 0 22px 0;
}

.automorph-chip {
  background: #ecfeff;
  border: 1px solid #bae6fd;
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 0.93rem;
  color: #075985;
}

.automorph-section {
  background: linear-gradient(180deg, var(--card), #f8fafc);
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
  box-shadow: 0 3px 14px rgba(15, 23, 42, 0.06);
}

.automorph-section h2 {
  margin-top: 0;
  border-left: 5px solid var(--primary);
  padding-left: 10px;
}

.automorph-callout {
  border-left: 5px solid var(--secondary);
  background: #f0fdf4;
  border-radius: 10px;
  padding: 12px 14px;
  margin: 10px 0;
  color: #14532d;
}

.automorph-page ul {
  margin-top: 8px;
}

.automorph-page pre {
  background: #0b1020;
  color: #dbeafe;
  border-radius: 12px;
  padding: 12px;
  overflow-x: auto;
  border: 1px solid #1e293b;
  box-shadow: inset 0 0 0 1px rgba(148, 163, 184, 0.12);
}

.automorph-page code {
  font-family: Consolas, "Courier New", monospace;
}

.automorph-page pre code {
  color: #f8fafc !important;
  opacity: 1;
}

.automorph-kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  margin: 12px 0 0 0;
}

.automorph-kpi {
  background: #ffffff;
  border: 1px solid #d1fae5;
  border-radius: 10px;
  padding: 10px;
}

.automorph-kpi b {
  display: block;
  font-size: 1.05rem;
  color: #065f46;
}

.automorph-refs a {
  word-break: break-word;
}
</style>

<div class="automorph-page">
  <section class="automorph-hero">
    <h1>AutoMorph from Local Repo to HPC/SSH</h1>
    <p>One reproducible, publication-ready workflow for running the official M0-M3 pipeline at small or large scale.</p>
  </section>

  <div class="automorph-grid">
    <div class="automorph-chip"><b>Local path:</b> quick setup, debugging, smaller batches</div>
    <div class="automorph-chip"><b>HPC path:</b> scalable runs, cleaner data separation, long jobs</div>
    <div class="automorph-chip"><b>Calibration:</b> use <code>resolution_information.csv</code> for micron units</div>
    <div class="automorph-chip"><b>Orchestration:</b> <code>run.sh</code> executes M0 to M3 in fixed order</div>
  </div>

  <section class="automorph-section">
    <h2>1) What AutoMorph does</h2>
    <p><b>AutoMorph</b> is an open pipeline for color fundus photographs that generates quantitative retinal phenotypes.</p>
    <ul>
      <li><b>M0</b>: preprocessing</li>
      <li><b>M1</b>: image quality grading</li>
      <li><b>M2</b>: vessel, artery-vein, and disc-cup segmentation</li>
      <li><b>M3</b>: feature extraction for disc-centred, macular Zone B/C, and whole-image regions</li>
    </ul>
    <div class="automorph-kpis">
      <div class="automorph-kpi"><b>M0</b>Input standardization</div>
      <div class="automorph-kpi"><b>M1</b>Gradable subset</div>
      <div class="automorph-kpi"><b>M2</b>Segmentation masks</div>
      <div class="automorph-kpi"><b>M3</b>CSV phenotypes</div>
    </div>
  </section>

  <section class="automorph-section">
    <h2>2) Local setup (official pattern)</h2>
    <p>Use the maintainer guide: <a href="https://github.com/rmaphoh/AutoMorph/blob/main/LOCAL.md">LOCAL.md</a>.</p>
    <pre><code class="language-bash">conda update conda
conda create -n automorph python=3.11 -y
conda activate automorph
git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph

conda install pytorch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
pip install --ignore-installed certifi
pip install -r requirement.txt
pip install efficientnet_pytorch==0.7.1 --no-deps</code></pre>
    <p>Place images in <code>images/</code>, provide <code>resolution_information.csv</code>, then run:</p>
    <pre><code class="language-bash">sh run.sh</code></pre>
  </section>

  <section class="automorph-section">
    <h2>3) HPC/SSH setup (recommended for scale)</h2>
    <pre><code class="language-bash">git clone https://github.com/rmaphoh/AutoMorph.git
cd AutoMorph
conda create -n automorph python=3.11 -y
conda activate automorph
pip install -r requirement.txt</code></pre>

    <p>Keep data outside the repository:</p>
    <pre><code class="language-bash">mkdir -p $HOME/retina_all/images
export AUTOMORPH_DATA=$HOME/retina_all</code></pre>

    <p>Generate spacing file for micron calibration:</p>
    <pre><code class="language-bash">python generate_resolution.py 0.008</code></pre>

    <p>Run detached over SSH:</p>
    <pre><code class="language-bash">nohup bash run.sh &gt; "$AUTOMORPH_DATA/automorph_run_$(date +%F_%H%M).log" 2&gt;&amp;1 &amp; disown
tail -f "$AUTOMORPH_DATA"/automorph_run_*.log</code></pre>

    <div class="automorph-callout">
      <b>Important:</b> <code>run.sh</code> cleans <code>Results/</code> at start. Run one job per data root at a time.
    </div>
  </section>

  <section class="automorph-section">
    <h2>4) Expected outputs and verification</h2>
    <pre><code class="language-text">$AUTOMORPH_DATA/
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
        └── Whole_image/*.csv</code></pre>

    <pre><code class="language-bash">ls -1 "$AUTOMORPH_DATA/Results/M1/Good_quality" | wc -l
find "$AUTOMORPH_DATA/Results/M2" -maxdepth 2 -type f | head -n 20
find "$AUTOMORPH_DATA/Results/M3" -maxdepth 2 -type f -name '*.csv' | sort</code></pre>
  </section>

  <section class="automorph-section">
    <h2>5) Reproducibility checklist</h2>
    <ul>
      <li>AutoMorph commit hash and run date</li>
      <li>Python, PyTorch, CUDA versions</li>
      <li>GPU model and driver details</li>
      <li><code>AUTOMORPH_DATA</code> path used at runtime</li>
      <li>Resolution source used in <code>resolution_information.csv</code></li>
      <li>Total input images and M1 gradable count</li>
    </ul>
  </section>

  <section class="automorph-section">
    <h2>6) Copy-ready methods text</h2>
    <div class="automorph-callout">
      We used AutoMorph to extract retinal vascular phenotypes from color fundus images. The official <code>run.sh</code> orchestrator was executed from M0 to M3 (preprocessing, quality grading, vessel/artery-vein/disc-cup segmentation, and feature extraction for disc-centred, macular Zone B, macular Zone C, and whole-image regions). Pixel resolution was provided through <code>resolution_information.csv</code>, generated with <code>generate_resolution.py</code> when per-image metadata were unavailable.
    </div>
  </section>

  <section class="automorph-section automorph-refs">
    <h2>7) Authoritative references</h2>
    <ul>
      <li>AutoMorph project page: <a href="https://rmaphoh.github.io/projects/automorph.html">https://rmaphoh.github.io/projects/automorph.html</a></li>
      <li>AutoMorph GitHub repository: <a href="https://github.com/rmaphoh/AutoMorph">https://github.com/rmaphoh/AutoMorph</a></li>
      <li>Local setup guide (<code>LOCAL.md</code>): <a href="https://github.com/rmaphoh/AutoMorph/blob/main/LOCAL.md">https://github.com/rmaphoh/AutoMorph/blob/main/LOCAL.md</a></li>
      <li>Pipeline runner (<code>run.sh</code>): <a href="https://github.com/rmaphoh/AutoMorph/blob/main/run.sh">https://github.com/rmaphoh/AutoMorph/blob/main/run.sh</a></li>
      <li>TVST 2022 paper: <a href="https://tvst.arvojournals.org/article.aspx?articleid=2783477">https://tvst.arvojournals.org/article.aspx?articleid=2783477</a></li>
      <li>medRxiv preprint: <a href="https://www.medrxiv.org/content/10.1101/2022.05.26.22274795v1">https://www.medrxiv.org/content/10.1101/2022.05.26.22274795v1</a></li>
    </ul>
  </section>
</div>
