---
title: "Scientific & Mathematical Foundations: The “Magic” Formulas I Once Ignored"
layout: post
categories: [foundations, mathematics, scientific-computing]
tags: [trigonometry, linear-algebra, machine-learning, optimization]
---

## A school-time memory (and what changed later)

When I was at school, I used to see these formula sheets and honestly think:

> “Why am I memorising this? It feels like a total waste of time.”

At that time, I couldn’t connect the symbols to anything real.

But with the passage of time—moving into **scientific computing, AI, imaging, and machine learning**—I began to see the “magic” behind those formulas:

- **Trigonometry** explains rotations, signals, waves, periodic patterns, projections, and geometry.  
- **Linear algebra** explains data as vectors, transformations, embeddings, PCA, and model layers.  
- **Calculus + optimization** explains learning: how parameters move to reduce error.

So today I see it differently:

These are not school-only topics.  
They are the **core language** of computation.

---

<p align="center">
  <img src="/assets/img/fundamental-trigonometry-formula-sheet.png" width="700" />
</p>

---

# Part A — Trigonometry (but explained like a computation tool)

## A1) The meaning of sin, cos, tan (Right triangle view)

For a right triangle with angle \(\theta\):

\[
\sin\theta = \frac{\text{Opposite}}{\text{Hypotenuse}},\quad
\cos\theta = \frac{\text{Adjacent}}{\text{Hypotenuse}},\quad
\tan\theta = \frac{\text{Opposite}}{\text{Adjacent}}
\]

**Computational meaning:**  
These are ratios—**normalised measurements**—so they stay stable even if the triangle is scaled up/down.

---

## A2) The unit circle trick (the “no memorisation” method)

If you remember only one idea, remember this:

> On the unit circle, the point at angle \(\theta\) is  
> \[
(\cos\theta, \sin\theta)
\]

So:
- \(\cos\theta\) = x-coordinate  
- \(\sin\theta\) = y-coordinate

This makes the identity obvious:

\[
\sin^2\theta + \cos^2\theta = 1
\]

Because it’s literally the circle equation \(x^2 + y^2 = 1\).

---

## A3) Why trig keeps appearing in AI, vision, and signals

### (i) Rotations (vision, robotics, geometry)
A 2D rotation matrix:

\[
R(\theta)=
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
\]

This is the basis of:
- camera alignment,
- image registration,
- coordinate transforms,
- geometry in ML pipelines.

### (ii) Waves and frequency (signal processing)
Many real-world signals can be represented using sine/cosine components (Fourier idea). That’s why trig is foundational for:
- image filtering,
- denoising,
- compression,
- spectral analysis.

(If you work with medical images, this becomes extremely practical.)

---

## A4) Short list of trig identities you actually use

### Reciprocal identities
\[
\sec\theta = \frac{1}{\cos\theta},\quad
\csc\theta = \frac{1}{\sin\theta},\quad
\cot\theta = \frac{1}{\tan\theta}
\]

### Quotient identity
\[
\tan\theta = \frac{\sin\theta}{\cos\theta}
\]

### Pythagorean identities
\[
\sin^2\theta + \cos^2\theta = 1,\quad
1 + \tan^2\theta = \sec^2\theta
\]

---

# Part B — Linear algebra (the backbone of machine learning)

If trigonometry explains geometry, **linear algebra explains data**.

## B1) Vectors = features (a row of numbers with meaning)
A data point in ML is often a vector:

\[
x = (x_1, x_2, \dots, x_d)
\]

Each coordinate is a feature.  
So “learning” often means learning relationships between vectors.

---

## B2) Dot product = similarity (why cosine similarity works)

The dot product:

\[
a \cdot b = \sum_i a_i b_i
\]

Geometric identity:

\[
a \cdot b = \|a\|\|b\|\cos(\theta)
\]

So:
- same direction ⇒ \(\cos(\theta)\approx 1\) ⇒ high similarity  
- perpendicular ⇒ \(\cos(\theta)=0\) ⇒ no alignment  
- opposite ⇒ \(\cos(\theta)\approx -1\)

This is exactly why:
- cosine similarity works for embeddings,
- attention uses dot products,
- nearest-neighbour geometry matters.

---

## B3) Matrices = transformations (the simplest powerful idea)

A matrix is a function that transforms a vector:

\[
y = Ax
\]

In ML:
- a linear layer is a matrix multiplication
- stacking layers = composing transformations

In statistics:
- covariance is a matrix
- regression can be written in matrix form

---

## B4) Eigenvalues + PCA intuition (why “principal directions” matter)

Eigen relation:

\[
Av = \lambda v
\]

Interpretation:
- \(v\) is a direction that stays “in the same line” after transformation
- \(\lambda\) is how much stretching happens

PCA uses this idea to find directions of maximum variance (data structure), which is why eigen concepts keep appearing in scientific ML.

---

# Part C — Machine learning essentials (math that explains training)

## C1) Training is optimization (not magic)

We choose parameters \(\theta\) to minimise a loss \(L(\theta)\):

\[
\theta \leftarrow \theta - \alpha \nabla_\theta L(\theta)
\]

- \(\alpha\) is the learning rate
- \(\nabla\) is the gradient (direction of steepest increase)
- we move *against* it to reduce loss

This is the simplest mathematical explanation of learning.

---

## C2) Two core losses that appear everywhere

### Regression (MSE)
\[
\text{MSE}=\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2
\]

### Classification (cross-entropy)
For true label distribution \(y\) and predicted probabilities \(\hat{p}\):

\[
L = -\sum_k y_k \log(\hat{p}_k)
\]

These are not just formulas—they define what the model learns to prioritise.

---

## C3) Regularization (how models avoid overfitting)

L2 (ridge-style) regularization:
\[
L_{\text{total}} = L + \lambda \|\theta\|_2^2
\]

L1 (lasso-style) regularization:
\[
L_{\text{total}} = L + \lambda \|\theta\|_1
\]

Very simple story:
- L2 shrinks weights smoothly
- L1 encourages sparsity (feature selection behaviour)

---

# A compact “mental map” of everything above

**Trigonometry**
→ rotations, unit circle, periodicity, geometry  
**Linear algebra**
→ vectors, dot products, transformations, eigen structure  
**Machine learning**
→ loss functions, gradients, optimization, generalization

Once I started seeing this as one connected chain, the “memorisation pain” disappeared.

---

# References (reliable, widely used)

- Strang, G. *Introduction to Linear Algebra*. Wellesley-Cambridge Press.  
- Goodfellow, I., Bengio, Y., & Courville, A. *Deep Learning*. MIT Press.  
- Bishop, C. M. *Pattern Recognition and Machine Learning*. Springer.  
- Murphy, K. P. *Machine Learning: A Probabilistic Perspective*. MIT Press.  
- Boyd, S., & Vandenberghe, L. *Convex Optimization*. Cambridge University Press.

---

## Final note to my future self

If I ever catch myself thinking “why do I need this?”, I’ll remember:

These formulas are not decoration.  
They are the **tools that explain how computation behaves**.
