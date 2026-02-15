---

title: "Publications"
permalink: /publications/
layout: single
author_profile: true
---
<link rel="stylesheet" href="/assets/css/custom-publications.css">

<h1 style="
  text-align:center;
  margin-top:0.5em;
  margin-bottom:1.2em;
  letter-spacing:0.5px;
">
</h1>

<p style="text-align:center; max-width:900px; margin:0 auto 2em auto; opacity:0.9;">
  Peer-reviewed journal articles and conference contributions at the intersection of
  retinal imaging, artificial intelligence, oculomics, and systemic health are listed below. 
</p>

<div class="pub-stats-wrap" data-total-cites="{{ site.data.citations.total | default: 37 }}">
  <div class="pub-stat-card">
    <div class="pub-stat-label">Total citations</div>
    <div class="pub-stat-value" id="pub-total-citations">0</div>
  </div>
  <div class="pub-stat-card">
    <div class="pub-stat-label">Papers tracked</div>
    <div class="pub-stat-value" id="pub-paper-count">0</div>
  </div>
  <div class="pub-stat-card">
    <div class="pub-stat-label">Citation snapshot</div>
    <div class="pub-stat-value" id="pub-cite-updated">Today</div>
  </div>
</div>

<!-- Set each paper citation count in data-cites -->

<div class="pub-card" data-cites="{{ site.data.citations.papers.biomimetics_2023.count | default: 0 }}">
  <div class="pub-img-wrap">
    <img class="pub-img floaty" src="/images/biomimetics-2023.png" alt="Biomimetics 2023">
  </div>
  <div>
    <div class="pub-title">
      <strong>Data Diversity in Convolutional Neural Network Based Ensemble Model for Diabetic Retinopathy</strong>
    </div>
    <div class="pub-meta"><em>Biomimetics (MDPI)</em>, 2023</div>
    <div class="pub-links" style="margin-top:8px;">
      <a href="https://www.mdpi.com/2313-7673/8/2/187">Journal</a>
    </div>
    <div class="pub-cite-chip">Citations: <strong>0</strong></div>
    <p class="pub-sum">
      This study systematically analyses how ensemble diversity mitigates data scarcity in medical
      imaging, offering insights into model generalisation under real-world clinical constraints.
    </p>
  </div>
</div>

<hr>

<div class="pub-card" data-cites="{{ site.data.citations.papers.imu_2024.count | default: 0 }}">
  <div class="pub-img-wrap">
    <img class="pub-img floaty" src="/images/imu-2024.png" alt="Informatics in Medicine Unlocked 2024">
  </div>
  <div>
    <div class="pub-title">
      <strong>Deciphering the Impact of Diversity in CNN-Based Ensembles on Overcoming Data Imbalance and Scarcity</strong>
    </div>
    <div class="pub-meta"><em>Informatics in Medicine Unlocked (Elsevier)</em>, 2024</div>
    <div class="pub-links" style="margin-top:8px;">
      <a href="https://www.sciencedirect.com/science/article/pii/S2352914824001138">Journal</a>
    </div>
    <div class="pub-cite-chip">Citations: <strong>0</strong></div>
    <p class="pub-sum">
      This work demonstrates how architectural and data-level diversity in CNN-based ensemble models
      improves robustness when medical imaging datasets are imbalanced or limited, using diabetic
      Retinopathy as a case study.
    </p>
  </div>
</div>

<hr>

<div class="pub-card" data-cites="{{ site.data.citations.papers.jpmhd_2025.count | default: 0 }}">
  <div class="pub-img-wrap">
    <img class="pub-img floaty" src="/images/jpmhd-2025.png" alt="Oculomics Survey 2025">
  </div>
  <div>
    <div class="pub-title">
      <strong>The Eye as a Window to Systemic Health: A Survey of Retinal Imaging from Classical Techniques to Oculomics</strong>
    </div>
    <div class="pub-meta"><em>The Journal of Precision Medicine: Health and Disease</em>, 2025</div>
    <div class="pub-links" style="margin-top:8px;">
      <a href="https://www.sciencedirect.com/science/article/pii/S305063282500023X">Journal</a>
    </div>
    <div class="pub-cite-chip">Citations: <strong>0</strong></div>
    <p class="pub-sum">
      A comprehensive survey tracing the evolution of retinal imaging toward oculomics, highlighting
      how retinal biomarkers can reveal systemic, cardiovascular, and metabolic health.
    </p>
  </div>
</div>

<hr>

<div class="pub-card" data-cites="{{ site.data.citations.papers.micad_2025.count | default: 0 }}">
  <div class="pub-img-wrap">
    <img class="pub-img floaty" src="/images/micad-2025.png" alt="MICAD 2025">
  </div>
  <div>
    <div class="pub-title">
      <strong>Retinal Lipidomics Associations as Candidate Biomarkers for Cardiovascular Health</strong>
    </div>
    <div class="pub-meta"><em>MICAD Proceedings</em>, 2025 — Oral Presentation</div>
    <div class="pub-links" style="margin-top:8px;">
      <a href="https://arxiv.org/abs/2508.03538">arXiv</a>
    </div>
    <div class="pub-cite-chip">Citations: <strong>0</strong></div>
    <p class="pub-sum">
      This conference paper explores associations between retinal microvascular traits and lipidomic
      profiles, identifying candidate non-invasive biomarkers for cardiovascular risk.
    </p>
  </div>
</div>

<hr>

<div class="pub-card" data-cites="{{ site.data.citations.papers.scirep_preprint_2025.count | default: 0 }}">
  <div class="pub-img-wrap">
    <img class="pub-img floaty" src="/images/scirep-2025.png" alt="Scientific Reports submission">
  </div>
  <div>
    <div class="pub-title">
      <strong>Integrated Oculomics and Lipidomics Reveal Microvascular Metabolic Signatures Associated with Cardiovascular Health</strong>
    </div>
    <div class="pub-meta"><em>Under Review — Scientific Reports (Nature Portfolio)</em></div>
    <div class="pub-links" style="margin-top:8px;">
      <a href="https://arxiv.org/abs/2507.12663">arXiv</a>
    </div>
    <div class="pub-cite-chip">Citations: <strong>0</strong></div>
    <p class="pub-sum">
      This study integrates retinal imaging with lipidomic profiles in a healthy cohort, revealing
      microvascular-metabolic signatures linked to cardiovascular health and systemic regulation.
    </p>
  </div>
</div>

<script>
  (function () {
    var statsWrap = document.querySelector('.pub-stats-wrap');
    var cards = document.querySelectorAll('.pub-card[data-cites]');
    var total = 0;
    cards.forEach(function (card) {
      var cites = parseInt(card.getAttribute('data-cites') || '0', 10);
      if (isNaN(cites)) cites = 0;
      total += cites;
      var strong = card.querySelector('.pub-cite-chip strong');
      if (strong) strong.textContent = cites.toLocaleString();
    });

    var totalEl = document.getElementById('pub-total-citations');
    var countEl = document.getElementById('pub-paper-count');
    var dateEl = document.getElementById('pub-cite-updated');

    var manualTotal = statsWrap ? parseInt(statsWrap.getAttribute('data-total-cites') || '', 10) : NaN;
    if (totalEl) totalEl.textContent = (isNaN(manualTotal) ? total : manualTotal).toLocaleString();
    if (countEl) countEl.textContent = cards.length.toString();
    if (dateEl) {
      var d = new Date();
      dateEl.textContent = d.toLocaleDateString();
    }
  })();
</script>

