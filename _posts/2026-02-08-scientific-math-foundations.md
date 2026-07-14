---
title: "Scientific and Mathematical Foundations: Formulas I Once Memorised, Then Finally Understood"
layout: post
categories: [foundations, mathematics, scientific-computing]
tags: [trigonometry, linear-algebra, machine-learning, optimization]
excerpt: "A practical reflection on why trigonometry, linear algebra, and optimization are not isolated school topics, but part of the working language of modern computation."
---

## A School-Time Memory

When I was at school, I often looked at pages full of formulas and thought:

> Why am I memorising this? What is it actually for?

At the time, the symbols felt detached from reality. They looked like exercises for passing exams, not tools for understanding anything meaningful.

That changed later.

As I moved into scientific computing, machine learning, image analysis, and data-driven research, I began to see that many of those same formulas were not academic ornaments at all. They were compact descriptions of how computation, geometry, signals, and learning behave.

Three themes became especially clear:

- **Trigonometry** explains rotation, periodicity, oscillation, and geometry.
- **Linear algebra** explains vectors, similarity, transformations, and data representation.
- **Calculus and optimization** explain training, learning dynamics, and parameter updates.

These are not just school topics. They are part of the working language of modern science and computing.

## Part A: Trigonometry as a Computational Tool

### 1. The basic ratios are scale-stable

For a right triangle with angle $\theta$,

$$
\sin \theta = \frac{\text{opposite}}{\text{hypotenuse}}, \qquad
\cos \theta = \frac{\text{adjacent}}{\text{hypotenuse}}, \qquad
\tan \theta = \frac{\text{opposite}}{\text{adjacent}}.
$$

The important idea is not memorisation for its own sake. These are **ratios**, so they remain unchanged when the triangle is scaled up or down. That is why they are useful: they describe shape and orientation, not absolute size.

### 2. The unit circle is the central picture

The most useful geometric interpretation is the unit circle.

At angle $\theta$, the corresponding point on the unit circle is

$$
(\cos \theta, \sin \theta).
$$

This immediately tells us:

- $\cos \theta$ is the horizontal coordinate,
- $\sin \theta$ is the vertical coordinate.

It also explains the identity

$$
\sin^2 \theta + \cos^2 \theta = 1,
$$

because the unit circle itself satisfies $x^2 + y^2 = 1$.

This is one reason the unit-circle viewpoint is better than treating trigonometry as a list of disconnected formulas.

### 3. Why trigonometry appears in computing

#### Rotation and coordinate changes

In two dimensions, a rotation by angle $\theta$ is represented by

$$
R(\theta) =
\begin{bmatrix}
\cos \theta & -\sin \theta \\
\sin \theta & \cos \theta
\end{bmatrix}.
$$

This structure appears in:

- image alignment,
- robotics and pose estimation,
- coordinate transforms,
- geometric processing pipelines.

#### Periodic structure and signals

Sine and cosine are also the natural language of oscillatory behaviour. Waves, vibration, periodic sampling, and Fourier analysis all depend on trigonometric structure.

That is why trigonometry becomes practical in tasks such as:

- signal filtering,
- denoising,
- frequency-domain analysis,
- image reconstruction and compression.

### 4. A few identities are genuinely useful

The identities worth keeping close are not a huge list. A small number already takes you far:

$$
\tan \theta = \frac{\sin \theta}{\cos \theta},
$$

$$
\sec \theta = \frac{1}{\cos \theta}, \qquad
\csc \theta = \frac{1}{\sin \theta}, \qquad
\cot \theta = \frac{1}{\tan \theta},
$$

and

$$
\sin^2 \theta + \cos^2 \theta = 1, \qquad
1 + \tan^2 \theta = \sec^2 \theta.
$$

The real value of these identities is not symbolic manipulation alone. They let us move between equivalent views of the same structure.

## Part B: Linear Algebra as the Language of Data

If trigonometry explains geometry, linear algebra explains how data is represented and transformed.

### 1. Vectors are structured data points

A data point with $d$ features can be written as

$$
x = (x_1, x_2, \dots, x_d)^\top.
$$

Each coordinate carries meaning: intensity, measurement, score, frequency, biomarker, embedding component, or something else depending on the application.

Once data is represented as vectors, many computational questions become geometric questions.

### 2. Dot products explain alignment and similarity

The dot product of two vectors $a$ and $b$ is

$$
a^\top b = \sum_{i=1}^{d} a_i b_i.
$$

Geometrically,

$$
a^\top b = \|a\| \, \|b\| \cos \theta.
$$

This matters because it tells us how aligned two vectors are:

- if $\theta \approx 0$, the vectors point in similar directions,
- if $\theta = \frac{\pi}{2}$, they are orthogonal,
- if $\theta \approx \pi$, they point in opposite directions.

This is why dot products and cosine similarity appear so often in:

- embeddings,
- retrieval systems,
- nearest-neighbour methods,
- attention mechanisms in deep learning.

### 3. Matrices are transformations

A matrix acts on a vector to produce another vector:

$$
y = Ax.
$$

This is one of the most important ideas in applied mathematics.

In machine learning, a linear layer is a matrix transformation.  
In statistics, covariance is organised as a matrix.  
In dimensionality reduction, matrices encode directions of variance and projection.

Linear algebra is not just about arranging numbers in rows and columns. It is about describing structured transformations.

### 4. Eigenvalues and principal directions

The eigenvalue relation

$$
Av = \lambda v
$$

means that the vector $v$ keeps its direction under the transformation $A$, while its magnitude is scaled by $\lambda$.

This idea is central to principal component analysis (PCA), spectral methods, and many forms of structured data analysis.

It explains why some directions in data are more informative than others.

## Part C: Machine Learning as Applied Optimization

### 1. Training is not magic

Much of learning can be described by one update rule:

$$
\theta \leftarrow \theta - \alpha \nabla_\theta L(\theta),
$$

where:

- $\theta$ denotes the parameters,
- $L(\theta)$ is the loss,
- $\nabla_\theta L(\theta)$ is the gradient,
- $\alpha$ is the learning rate.

The logic is simple: the gradient points in the direction of steepest increase, so we move in the opposite direction to reduce the loss.

This is the clearest mathematical explanation of what model training is doing.

### 2. Two losses appear again and again

For regression, one standard loss is mean squared error:

$$
\mathrm{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2.
$$

For classification, cross-entropy is fundamental:

$$
L = - \sum_{k} y_k \log \hat{p}_k.
$$

These losses are not merely formulas to optimise. They define what the model is being encouraged to care about.

### 3. Regularization controls complexity

Regularization modifies the objective to discourage overly flexible solutions.

L2 regularization:

$$
L_{\mathrm{total}} = L + \lambda \|\theta\|_2^2
$$

L1 regularization:

$$
L_{\mathrm{total}} = L + \lambda \|\theta\|_1
$$

At a high level:

- **L2** shrinks parameters smoothly,
- **L1** promotes sparsity and can behave like feature selection.

This is one of the simplest examples of how mathematical structure shapes model behaviour.

## A Compact Mental Map

The connection can be summarised like this:

- **Trigonometry**: rotation, periodicity, geometry, waves
- **Linear algebra**: vectors, similarity, transformations, structure
- **Optimization**: losses, gradients, updates, generalization

Once these topics are seen as parts of one connected system, they stop feeling like disconnected chapters and start functioning as a coherent toolkit.

## Why This Matters

What changed for me was not that the formulas themselves became more complicated. What changed was the context.

The same mathematical objects that once looked abstract later appeared in:

- image geometry,
- signal processing,
- statistical modelling,
- machine learning,
- scientific inference.

That is the point I wish I had understood earlier: many formulas become meaningful only when you see what they are modelling.

## References

- Strang, G. *Introduction to Linear Algebra*. Wellesley-Cambridge Press.
- Goodfellow, I., Bengio, Y., and Courville, A. *Deep Learning*. MIT Press.
- Bishop, C. M. *Pattern Recognition and Machine Learning*. Springer.
- Murphy, K. P. *Machine Learning: A Probabilistic Perspective*. MIT Press.
- Boyd, S., and Vandenberghe, L. *Convex Optimization*. Cambridge University Press.

## Final Note

If I ever find myself asking, "Why do I need this?", the better question is:

What behaviour is this formula trying to describe?

That is usually where the meaning begins.
