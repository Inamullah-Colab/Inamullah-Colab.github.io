---
permalink: /
title: "About Me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I am **Inamullah**, a PhD student in Computer Science at the [School of Electronics and Computer Science](https://www.southampton.ac.uk/about/faculties-schools-departments/school-of-electronics-and-computer-science), [University of Southampton](https://www.southampton.ac.uk/). My research investigates how the **retinal microvasculature can serve as a non-invasive marker of systemic biological processes**, and how information captured in the eye relates to complex interactions spanning molecular, genetic, and clinical domains.

The retina offers a uniquely accessible view of human vascular and neurological systems. Beyond its local anatomy, retinal vascular patterns encode signals associated with cardiometabolic regulation, neurovascular health, and developmental processes. My work focuses on extracting and analysing fine-grained vascular traits, such as vessel calibre, tortuosity, density, and fractal geometry, and on examining how these features relate to **clinical phenotypes, molecular profiles, and genetic variation**.

A key objective of my research is not merely to identify statistical relationships, but to **understand the biological structure and mechanisms underlying them**. To achieve this, we develop and apply **mathematical and statistical methodologies** capable of modelling latent structures, mediated pathways, and confounding effects inherent in high-dimensional biomedical data. These approaches include multivariate statistical analysis, causal and mediation modelling, network-based representations, and interpretable machine learning frameworks designed to separate direct effects from indirect or shared influences.

By integrating retinal imaging with clinical measurements, lipidomic profiles, and genetic data, my research explores how information propagates across biological scales, from molecular regulation and genetic predisposition to vascular morphology and observable disease risk. This integrative perspective enables the study of **biological pathways, regulatory interactions, and cross-modal dependencies**, rather than analysing each data source in isolation.

This work aligns closely with the emerging field of **oculomics**, which leverages ocular biomarkers derived from advanced imaging to infer systemic health and disease. My broader research interests include multimodal data integration, explainable and trustworthy AI for healthcare, and the development of computational methods that prioritise interpretability, robustness, and translational relevance.

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

## Academic Background and Motivation

My academic path has evolved through a combination of interdisciplinary training, professional experience, and personal motivation, ultimately converging on medically oriented computational research.

Before beginning my doctoral studies, I completed a **Master’s degree in Computer Science**, with a major focus on **artificial intelligence for medical imaging**. During this programme, I developed practical experience in image analysis, computational modelling, and data-driven methods applied to biomedical problems. This stage of my training played a formative role in connecting my technical background to healthcare-focused research questions.

Prior to this, I earned a **Bachelor’s degree with a combined emphasis on physics, mathematics, and computer science**, providing a strong foundation in analytical reasoning, mathematical formulation, and algorithmic thinking. Earlier still, I completed a **three-year diploma in civil engineering** and subsequently accumulated **over twelve years of professional experience** in this field. This early exposure to engineering practice fostered a pragmatic mindset, systems-level thinking, and an appreciation for real-world constraints, qualities that continue to influence my research approach.

Beyond formal education, my motivation to work on health-related problems is deeply rooted in personal experience. I come from **Bajaur Agency**, a remote tribal region in Pakistan near the Pakistan–Afghanistan border, where access to basic healthcare infrastructure, medical services, and medication has historically been limited. Growing up in such an environment shaped my early awareness of health inequities and instilled a strong desire to contribute, in whatever capacity possible, to improving healthcare outcomes.

Although unstable circumstances prevented me from pursuing a conventional medical career, this aspiration did not diminish. Instead, it evolved. Over time, I recognized that **computational science, engineering, and data-centric methodologies** offer powerful alternatives to support medical research and healthcare delivery. This realisation guided my gradual integration of physics, mathematics, computer science, engineering, and medical imaging into a unified research trajectory.

My current PhD work represents the synthesis of these experiences. By combining retinal imaging with clinical, molecular, and genetic data, and employing mathematical, statistical, and interpretable machine learning techniques to model complex biological relationships, my research aims to generate mechanistic insights from non-invasive data sources. This intersection, between technical rigor and medical relevance, closely reflects both my intellectual interests and long-term goals.

---

## Research Keywords

**Artificial Intelligence**, **Machine Learning**, **Interpretable Models**, **Causal and Mediation Analysis**, **Graphical and Network Models**, **Bayesian Methods**, **Mathematical Modelling**, **Medical Imaging**, **Retinal Microvasculature**, **Oculomics**, **Multi-Omics Integration**, **Genetic Variation**, **Clinical Phenotyping**, **Systemic Disease**, **Biomarker Discovery**, **Precision Medicine**

---

## Recent Publications

{% assign recent_publications = site.data.publications | sort: "date" | reverse %}
{% assign featured_publication = recent_publications | where: "citation_key", "retisem_ssrn_2026" | first %}

{% if featured_publication %}
  {% assign featured_citation = site.data.citations.papers[featured_publication.citation_key] %}
  <article class="pub-feature-card">
    <div class="pub-feature-media">
      <img src="{{ featured_publication.image }}" alt="{{ featured_publication.title }}">
    </div>
    <div class="pub-feature-body">
      <p class="pub-kicker">Featured Paper</p>
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
  {% for publication in recent_publications limit:3 %}
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

