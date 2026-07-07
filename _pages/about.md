---
permalink: /
title: "About"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

<section class="site-hero">
  <div class="site-hero__content">
    <p class="site-hero__kicker">Oculomics • Interpretable AI • Biomedical Data Integration</p>
    <h1 class="site-hero__title">Retinal Biomarkers for Systemic Health, Modeled with Interpretable and Causal AI</h1>
    <p class="site-hero__lead">
      I study how retinal microvascular structure can serve as a non-invasive marker of systemic biology, linking imaging, lipidomics, genetics, and clinical data through interpretable machine learning and pathway-aware modelling.
    </p>
    <div class="site-hero__actions">
      <a href="/publications/" class="btn btn--primary">View Publications</a>
      <a href="/cv/" class="btn btn--inverse">Open CV</a>
    </div>
  </div>
  <div class="site-hero__stats">
    <div class="site-hero__stat">
      <span class="site-hero__stat-value">51</span>
      <span class="site-hero__stat-label">Google Scholar Citations</span>
    </div>
    <div class="site-hero__stat">
      <span class="site-hero__stat-value">AI + Retina</span>
      <span class="site-hero__stat-label">Core Research Direction</span>
    </div>
    <div class="site-hero__stat">
      <span class="site-hero__stat-value">Southampton</span>
      <span class="site-hero__stat-label">PhD Base</span>
    </div>
  </div>
</section>

I am **Inam Ullah**, a PhD student in Computer Science at the [School of Electronics and Computer Science](https://www.southampton.ac.uk/about/faculties-schools-departments/school-of-electronics-and-computer-science), [University of Southampton](https://www.southampton.ac.uk/). My research focuses on how **retinal microvascular structure can act as a non-invasive marker of systemic biology**, and how signals captured in the eye relate to molecular, genetic, and clinical processes.

The retina provides a uniquely accessible view of vascular and neurological health. My work studies fine-grained retinal traits, including vessel calibre, tortuosity, density, and fractal geometry, and examines how these features relate to **clinical phenotypes, lipidomic profiles, and genetic variation**.

A central aim of this research is not only to identify associations, but to **understand the biological structure and mechanisms underlying them**. To do that, I develop and apply **mathematical, statistical, and interpretable machine learning methods** for high-dimensional biomedical data, including causal and mediation modelling, pathway-aware representations, and network-based analysis.

By integrating retinal imaging with clinical, lipidomic, and genetic data, my research explores how information propagates across biological scales, from molecular regulation and inherited predisposition to vascular morphology and disease risk. This integrative perspective supports the study of **biological pathways, regulatory interactions, and cross-modal dependencies**, rather than treating each data source in isolation.

This work aligns closely with the emerging field of **oculomics**, which leverages ocular biomarkers derived from advanced imaging to infer systemic health and disease. My broader research interests include multimodal data integration, explainable and trustworthy AI for healthcare, and the development of computational methods that prioritise interpretability, robustness, and translational relevance.

---

## Research Focus

- **Oculomics and retinal biomarkers** for systemic cardiovascular, metabolic, and neurological health.
- **Interpretable machine learning** for biomedical imaging and multimodal health data.
- **Causal and mediation modelling** for pathway-level biological interpretation.
- **Multi-omics integration** linking retinal phenotypes with lipidomic, genetic, and clinical measurements.

---

## News & Updates

{% assign homepage_news = site.posts | sort: "date" | reverse %}

<article class="news-feature-card">
  <div class="news-feature-media">
    <img src="/images/Systemic_Health.png" alt="Illustration linking retinal imaging to systemic health">
  </div>
  <div class="news-feature-body">
    <p class="pub-kicker">Featured In The News</p>
    <h3 class="news-feature-title">Forbes: How Artificial Intelligence Makes Eye Exams a Gateway to Whole-Body Wellness</h3>
    <p class="news-feature-meta"><strong>November 5, 2025</strong> | Forbes</p>
    <p class="news-feature-summary">
      Forbes featured the broader idea at the center of our paper:
      <em>The Eye as a Window to Systemic Health: A Survey of Retinal Imaging from Classical Techniques to Oculomics</em>.
      The article emphasizes how AI-enabled eye exams can act as a gateway to whole-body wellness by revealing systemic cardiovascular, metabolic, and neurological signals from retinal imaging.
    </p>
    <div class="news-feature-links">
      <a href="https://www.forbes.com/sites/williamhaseltine/2025/11/05/how-artificial-intelligence-makes-eye-exams-a-gateway-to-whole-body-wellness/">Read Forbes article</a>
      <a href="https://www.sciencedirect.com/science/article/pii/S305063282500023X">View related paper</a>
    </div>
  </div>
</article>

<div class="news-grid">
  <article class="news-card">
    <p class="news-date">15 Jun 2026</p>
    <h3 class="news-title"><a href="/publications/">RetiSEM accepted at IJCAI 2026</a></h3>
    <p class="news-summary">RetiSEM: Generalising Causal Models for Fragmented Biomedical Data has been accepted for oral presentation at IJCAI 2026.</p>
    <p class="news-link"><a href="https://openreview.net/forum?id=Jaj6hWKcGz">View OpenReview</a></p>
  </article>
  {% for post in homepage_news limit:3 %}
    <article class="news-card">
      <p class="news-date">{{ post.date | date: "%d %b %Y" }}</p>
      <h3 class="news-title"><a href="{{ post.url }}">{{ post.title }}</a></h3>
      {% if post.description %}
        <p class="news-summary">{{ post.description }}</p>
      {% elsif post.excerpt %}
        <p class="news-summary">{{ post.excerpt | strip_html | strip_newlines | truncate: 180 }}</p>
      {% endif %}
      <p class="news-link"><a href="{{ post.url }}">Read update</a></p>
    </article>
  {% endfor %}
</div>

<p><a href="/year-archive/" class="btn btn--primary">View all updates</a></p>

---

## Background

My academic path has evolved through interdisciplinary training, professional experience, and a sustained interest in medically relevant computational research.

Before beginning my doctoral studies, I completed a **Master's degree in Computer Science**, with a strong focus on **artificial intelligence for medical imaging**. That training gave me practical experience in image analysis, computational modelling, and data-driven approaches to biomedical problems.

Prior to this, I earned a **Bachelor's degree** with combined emphasis on physics, mathematics, and computer science, which provided a strong foundation in analytical reasoning, mathematical formulation, and algorithmic thinking. Earlier, I also completed a **three-year diploma in civil engineering** and accumulated **more than twelve years of professional experience** in that field. That engineering background continues to shape my research through systems thinking, pragmatism, and attention to real-world constraints.

My motivation to work on health-related problems is also rooted in personal experience. I come from **Bajaur Agency**, a remote tribal region in Pakistan near the Pakistan-Afghanistan border, where access to healthcare infrastructure, medical services, and medication has historically been limited. Growing up in that environment shaped my awareness of health inequities and strengthened my commitment to medically relevant research.

Although circumstances prevented me from pursuing a conventional medical career, the motivation remained. Over time, I came to see **computational science, engineering, and data-centric methods** as powerful ways to contribute to medical research and healthcare delivery. That realization gradually brought together my interests in physics, mathematics, computer science, engineering, and medical imaging into a single research trajectory.

My current PhD work is the synthesis of these experiences. By combining retinal imaging with clinical, molecular, and genetic data, and by using mathematical, statistical, and interpretable machine learning methods to model complex biological relationships, I aim to generate mechanistic insight from non-invasive data sources.

---

## Research Keywords

**Artificial Intelligence**, **Machine Learning**, **Interpretable Models**, **Causal and Mediation Analysis**, **Graphical and Network Models**, **Bayesian Methods**, **Mathematical Modelling**, **Medical Imaging**, **Retinal Microvasculature**, **Oculomics**, **Multi-Omics Integration**, **Genetic Variation**, **Clinical Phenotyping**, **Systemic Disease**, **Biomarker Discovery**, **Precision Medicine**

---

## Recent Publications

{% assign recent_publications = site.data.publications | sort: "date" | reverse %}
{% assign featured_publication = recent_publications | where: "citation_key", "retisem_ssrn_2026" | first %}
{% assign listed_recent_publications = recent_publications | where_exp: "item", "item.citation_key != 'retisem_ssrn_2026'" %}

{% if featured_publication %}
  {% assign featured_citation = site.data.citations.papers[featured_publication.citation_key] %}
  <article class="pub-feature-card">
    <div class="pub-feature-media">
      <img src="{{ featured_publication.image }}" alt="{{ featured_publication.title }}">
    </div>
    <div class="pub-feature-body">
      <p class="pub-kicker">{% if featured_publication.type == "conferences" %}Featured Conference Paper{% else %}Featured Paper{% endif %}</p>
      <h3 class="pub-feature-title">{{ featured_publication.title }}</h3>
      <p class="pub-feature-meta">
        <strong>{{ featured_publication.year }}</strong>
        {% if featured_publication.status %} | {{ featured_publication.status }}{% endif %}
        | <em>{{ featured_publication.venue }}</em>
      </p>
      <p class="pub-feature-summary">{{ featured_publication.summary }}</p>
      <div class="pub-feature-footer">
        <div class="pub-links">
          {% for link in featured_publication.links %}
            <a href="{{ link.url }}">{{ link.label }}</a>
          {% endfor %}
        </div>
        <div class="pub-cite-chip">Citations: <strong>{{ featured_citation.count | default: 0 }}</strong></div>
      </div>
    </div>
  </article>
{% endif %}

<div class="pub-mini-grid">
  {% for publication in listed_recent_publications limit:3 %}
    {% assign citation_entry = site.data.citations.papers[publication.citation_key] %}
    <article class="pub-mini-card">
      <div class="pub-mini-topline">
        <span>{{ publication.year }}</span>
        {% if publication.status %}
          <span class="pub-badge">{{ publication.status }}</span>
        {% endif %}
      </div>
      <h3 class="pub-mini-title">{{ publication.title }}</h3>
      <p class="pub-mini-meta"><em>{{ publication.venue }}</em></p>
      <p class="pub-mini-summary">{{ publication.summary }}</p>
      <div class="pub-mini-footer">
        <div class="pub-links">
          {% for link in publication.links limit:1 %}
            <a href="{{ link.url }}">{{ link.label }}</a>
          {% endfor %}
        </div>
        <div class="pub-cite-chip">Citations: <strong>{{ citation_entry.count | default: 0 }}</strong></div>
      </div>
    </article>
  {% endfor %}
</div>

<p><a href="/publications/" class="btn btn--primary">View all publications</a></p>
