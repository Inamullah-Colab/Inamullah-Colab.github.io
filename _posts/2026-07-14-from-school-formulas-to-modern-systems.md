---
title: "From School Formulas to Modern Systems"
layout: post
date: 2026-07-14 12:00:00 +0000
last_modified_at: 2026-07-14 12:00:00 +0000
published: true
permalink: /posts/2026/07/from-school-formulas-to-modern-systems/
tags:
  - mathematics
  - trigonometry
  - physics
  - probability
  - vector-calculus
  - machine-learning
  - deep-learning
  - scientific-computing
excerpt: "A detailed reflection on how the formulas that once felt empty at school later became part of the practical language of modelling, proof, simulation, machine learning, and medical applications."
---

# From School Formulas to Modern Systems

There was a stage in school when I genuinely felt bored by mathematics and physics.

Not because the subjects were unimportant, but because I could not yet see what they were for.

A page filled with angles, trigonometric identities, derivatives, vector operators, and field equations can feel exhausting when all you see is symbolic pressure and no living context. At that age, it is easy to ask:

> Why am I spending so much time on this?  
> Where does this appear in practical life?

At the time, those questions felt reasonable to me. I could solve exercises, but I could not yet see a convincing bridge between formal mathematics and the real world.

What changed later was not the symbols. What changed was my perspective.

Once I moved into scientific computing, image analysis, quantitative modelling, and machine learning, I started to recognise that many of those old formulas were not isolated school tasks at all. They were compact descriptions of mechanisms:

- how geometry behaves,
- how signals repeat,
- how fields evolve,
- how nonlinear systems are approximated,
- how uncertainty is represented,
- how models learn from data,
- and how theory becomes something implementable.

That is the broader idea behind this post.

## The Diagram as a Map, Not Decoration

The figure below is meant to do more than look attractive. It is intended to summarise a chain of ideas that often appears fragmented when we first encounter it:

- trigonometric ratios and the unit circle,
- classical mathematical structure,
- physical modelling,
- probabilistic reasoning,
- machine learning and deep learning,
- language models and modern computational systems,
- and finally social and medical applications.

<div class="math-journey-figure">
  <img src="/images/math-from-school-to-modern-systems.svg" alt="Visual map linking the unit circle and trigonometric ratios to classical mathematics, physics, probability, machine learning, language models, and real-world applications.">
</div>

The point of the figure is not to claim that every modern system comes directly from one trigonometric identity. That would be shallow. The point is subtler: the same foundational mathematics keeps reappearing, often under different names, in more advanced computational settings.

## Why the Unit Circle Is More Important Than It First Appears

For many students, trigonometry begins as memorisation:

$$
\sin \theta, \qquad \cos \theta, \qquad \tan \theta.
$$

That is often where boredom begins as well. Without a geometric picture, these expressions can feel like arbitrary symbols.

But the unit circle changes the story.

The point at angle $\theta$ is

$$
(\cos \theta, \sin \theta).
$$

That single statement already explains:

- why cosine and sine are coordinates,
- why periodicity emerges naturally,
- why rotation matrices use those functions,
- why circular motion and wave behaviour are mathematically connected.

It also makes the classical identity

$$
\sin^2 \theta + \cos^2 \theta = 1
$$

look much less mysterious, because it is simply the unit-circle equation in disguise.

This is one of the first places where mathematics becomes more meaningful when moved from memorisation into structure.

## What the Triangle Ratios Really Give Us

The familiar right-triangle definitions

$$
\sin \theta = \frac{\text{opposite}}{\text{hypotenuse}}, \qquad
\cos \theta = \frac{\text{adjacent}}{\text{hypotenuse}}, \qquad
\tan \theta = \frac{\text{opposite}}{\text{adjacent}}
$$

are not just school exercises. They teach an important modelling habit: **ratios can preserve meaning under scale**.

That is already a scientific idea.

When a quantity is written as a ratio rather than a raw magnitude, it often becomes more stable, more transferable, and more interpretable. This is one reason trigonometric thinking survives into signal processing, coordinate systems, numerical geometry, and many imaging tasks.

In practical work, the same mental move happens again and again:

- use structure rather than raw values,
- represent behaviour in a normalised form,
- search for invariants that survive scaling, noise, or transformation.

## From Geometry to Physical Modelling

At a broader level, mathematical physics often begins by asking:

- what is changing,
- where is it changing,
- how fast is it changing,
- in which direction is it changing,
- and what constraints govern that change?

That leads naturally to ideas such as:

- scalar fields,
- vector fields,
- gradients,
- divergence,
- curl,
- Laplacians.

At school, these may appear as formal operations. Later, they become ways of describing very real phenomena:

- transport,
- flow,
- accumulation,
- diffusion,
- oscillation,
- potential,
- conservation.

The language becomes increasingly expressive. What once looked symbolic begins to function as a modelling grammar.

## Nonlinearity and the Need for Reduction

One of the hardest transitions in applied mathematics is realising that most important systems are not perfectly simple.

They are often nonlinear, unstable, coupled, noisy, or only partially observed.

This is where a deeper mathematical mindset becomes useful. Instead of asking for one perfect closed-form answer, we begin asking:

- Can the system be approximated locally?
- Can a nonlinear phenomenon be studied through linearisation?
- Can we separate dominant structure from noise?
- Can we control sensitivity?
- Can we transform the problem into a tractable form?

This is where reduction becomes central.

Reduction does not mean oversimplification. It means building a careful bridge from the full problem to an analysable one.

That same mindset appears in:

- local linear approximation,
- perturbation analysis,
- stability studies,
- numerical simulation,
- regularisation,
- probabilistic modelling.

Many systems that appear chaotic or entropic at first sight become partially understandable only because we learn how to represent them in a better mathematical language.

## Why Probability Enters the Story

Pure geometry and deterministic physics are powerful, but real data rarely arrive in clean exact form.

Measurements are noisy. Observations are incomplete. Biological systems vary. Sensors fail. Human behaviour is irregular. Real-world systems contain uncertainty by default.

That is why probability becomes unavoidable.

Probability gives us a disciplined language for:

- uncertainty,
- variability,
- inference,
- confidence,
- noise modelling,
- prediction under partial information.

This is not separate from the rest of mathematics. It is what allows structural mathematics to survive contact with imperfect reality.

In practice, many useful models stand at the intersection of:

- geometric structure,
- physical intuition,
- probabilistic uncertainty,
- computational approximation.

That intersection is where a large part of modern quantitative science actually lives.

## The Bridge to Machine Learning

Machine learning often appears modern and self-contained, but it is built from older mathematical layers.

At a minimum, it depends on:

- **linear algebra** for representation and transformation,
- **calculus** for gradients and optimisation,
- **probability** for uncertainty and statistical learning,
- **geometry** for similarity, embeddings, and structure,
- **approximation theory** for generalisation and expressive modelling.

Even deep learning, which is nonlinear overall, is still assembled from repeated linear maps plus nonlinear activation functions and optimised through gradient-based updates.

That is why I no longer see older mathematics as "before AI" knowledge. It is still inside AI.

## Deep Learning and Foundation Models

When people speak about deep learning, language models, or ChatGPT-style systems, the surface looks very different from school mathematics. The interface is fluent and conversational. The user does not see the mathematics directly.

But beneath that surface, the chain still holds:

- vectors,
- matrices,
- dot products,
- probabilistic outputs,
- optimisation,
- representation learning.

Language models extend this into large-scale sequence modelling, contextual embeddings, attention mechanisms, and token prediction, but they are still mathematical systems before they are interface systems.

This matters because it prevents us from mystifying the technology. We can admire the scale and sophistication without forgetting that structure, approximation, and optimisation still govern the result.

## Why This Matters in Social and Medical Settings

For me, the most meaningful shift happened when I started seeing how these mathematical ideas move into domains that affect real lives.

In social systems, they can support:

- forecasting,
- decision support,
- behavioural pattern analysis,
- risk-aware modelling.

In medical and biomedical settings, they can support:

- image interpretation,
- signal analysis,
- disease modelling,
- biomarker discovery,
- uncertainty-aware decision systems.

That final step matters.

A formula becomes much more meaningful once it participates in a chain that runs from theory to an interpretable real-world outcome. In biomedical research especially, the path often looks something like this:

1. start from assumptions,
2. define a mathematical model,
3. derive or justify its structure,
4. simulate or estimate behaviour,
5. test it on data,
6. interpret it cautiously,
7. decide whether it is trustworthy enough to matter.

This is where mathematics stops being an isolated subject and becomes part of scientific responsibility.

## What I Understand Differently Now

When I was younger, I thought mathematics and physics were mostly about solving problems correctly.

Now I see them more as a layered framework for thought:

- notation,
- assumption,
- abstraction,
- reduction,
- theorem,
- proof,
- simulation,
- implementation,
- application.

That sequence is not always linear, but it is one of the clearest ways I now understand how theory becomes practice.

The older formulas did not lose their relevance. I simply reached the stage where I could finally see what they were supporting.

## Final Reflection

I do not think every student must immediately love mathematics or physics. Confusion and boredom are real experiences. I had them too.

But I now think many of those early formulas deserve more respect than they often receive, because they are not merely decorative pieces of a syllabus. They are part of a long intellectual infrastructure that supports scientific explanation, computational reasoning, and practical systems.

Some of that infrastructure begins with a triangle.  
Some of it begins with a circle.  
Some of it appears in a gradient, a divergence, a curl, or a Laplacian.  
Some of it appears in probability and inference.  
Some of it appears in machine learning, deep learning, and language models.  
And some of it returns, eventually, to human questions in medicine and society.

That is why I no longer see those old school formulas as time wasted.

I see them as the early pieces of a much larger map.
