---
title: "Normality and Variance Diagnostics for Causal Discovery"
date: 2026-01-22 20:51:00 +0000
last_modified_at: 2026-01-22 20:51:00 +0000
published: true
permalink: /posts/2026/01/normality-variance-diagnostics/
tags:
  - causal discovery
  - normality
  - statistics
  - LiNGAM
  - NOTEARS
  - PC
  - GraNDAG
---

Below is a ready-to-publish write-up that explains why these checks matter, how the tests behave, and what our synthetic results suggest for method choice.

## Code (how to reproduce the diagnostics)

The script used to compute the test summaries and plots is included here (path in the site repo):

`assets/normality-report/normality_tests.py`

To run it locally:

```bash
python assets/normality-report/normality_tests.py
```

## 1) Why check normality and variance before causal discovery?

Causal discovery is not one algorithm, it is a family of methods with different assumptions. In practice, performance and identifiability depend on these assumptions (Spirtes et al., 2000) [1]:

- Linearity vs. nonlinearity
- Gaussian vs. non-Gaussian noise
- Tail heaviness and outliers
- Scale and variance stability across variables

That is why I run a lightweight diagnostic suite before modeling. It keeps the comparison fair and helps avoid the common trap where one method "wins" just because the data matches its assumptions.

## 2) Synthetic datasets at a glance

The benchmark uses synthetic datasets with different dimensionalities. The number of variables per dataset is:

| Dataset         | Variables |
|----------------|-----------|
| LowDim-D_data  | 20        |
| LowDim-L_data  | 20        |
| LowDim-N_data  | 20        |
| LowDim-P_data  | 20        |
| MidDim-C_data  | 50        |
| MidDim-D_data  | 100       |
| MidDim-P_data  | 100       |
| MidDim-S_data  | 100       |
| HighDim-D_data | 200       |
| HighDim-S_data | 200       |

## 3) What normality tests actually test

A normality test checks whether a variable looks like it came from a Gaussian distribution. Each test emphasizes different departures:

- Shapiro-Wilk: strong for small samples and common in practice [2].
- D'Agostino K2: combines skewness and kurtosis, good for moderate/large n [3].
- Jarque-Bera: another skew/kurtosis omnibus test [4].
- Anderson-Darling: more sensitive in the tails [5].

Important: with many variables, some tests will fail even if the data is mostly normal. That is why I read p-values together with skew/kurtosis and the plots.

## 4) Overview plots (quick reading guide)

- Pass-rate plot: higher means more Gaussian-like across columns.
- Skew vs kurtosis: points near (0, 0) are closer to normality.
- P-value histograms: a pile-up near 0 suggests non-Gaussianity.
- QQ plots: straight line means Gaussian; curvature means skew or heavy tails.

![Pass rates by dataset](/assets/normality-report/pass_rate_by_dataset.png)
![Skew vs kurtosis scatter](/assets/normality-report/skew_kurtosis_scatter.png)

## 5) Dataset summary table (from the diagnostics)

| Dataset         | n_cols | Shapiro pass | K2 pass | JB pass | AD pass | mean |skew| | mean |kurt| |
|----------------|--------|--------------|---------|---------|---------|-----------|-----------|
| HighDim-D_data | 200    | 0.415        | 0.415   | 0.415   | 0.460   | 20.345    | 1520.341  |
| HighDim-S_data | 200    | 0.945        | 0.950   | 0.940   | 0.955   | 0.026     | 0.047     |
| LowDim-D_data  | 20     | 0.900        | 0.900   | 0.900   | 0.950   | 0.053     | 0.535     |
| LowDim-L_data  | 20     | 1.000        | 0.900   | 0.950   | 1.000   | 0.018     | 0.063     |
| LowDim-N_data  | 20     | 0.900        | 0.950   | 0.950   | 0.950   | 0.024     | 0.105     |
| LowDim-P_data  | 20     | 0.900        | 0.900   | 0.900   | 0.950   | 0.024     | 0.047     |
| MidDim-C_data  | 50     | 0.920        | 0.920   | 0.920   | 0.960   | 0.029     | 0.050     |
| MidDim-D_data  | 100    | 0.780        | 0.780   | 0.780   | 0.820   | 1.099     | 70.508    |
| MidDim-P_data  | 100    | 0.970        | 0.970   | 0.970   | 0.980   | 0.024     | 0.048     |
| MidDim-S_data  | 100    | 0.920        | 0.940   | 0.940   | 0.920   | 0.582     | 27.523    |

## 6) What the results suggest (dataset by dataset)

### HighDim-S_data (200 vars): clean Gaussian-like
Pass rates are near 0.95 across tests and skew/kurtosis are close to zero. This is the linear-Gaussian comfort zone.
Suggested methods: PC or NOTEARS, which are typically strong in linear-Gaussian regimes [1,6].

![HighDim-S p-values](/assets/normality-report/pvalues_HighDim-S_data.png)
![HighDim-S QQ + hist](/assets/normality-report/qq_hist_HighDim-S_data.png)

### HighDim-D_data (200 vars): extreme tails
Pass rates are low (about 0.41 to 0.46) and skew/kurtosis are extremely large. This is strongly non-Gaussian.
Suggested methods: LiNGAM; GraNDAG if you expect nonlinear mechanisms [7,8].

![HighDim-D p-values](/assets/normality-report/pvalues_HighDim-D_data.png)
![HighDim-D QQ + hist](/assets/normality-report/qq_hist_HighDim-D_data.png)

### LowDim datasets (20 vars): mostly Gaussian
All LowDim variants have high pass rates and low skew/kurtosis. Minor tails show up in LowDim-D, but nothing severe.
Suggested methods: PC or NOTEARS. LiNGAM is not required here [1,6].

![LowDim-D p-values](/assets/normality-report/pvalues_LowDim-D_data.png)
![LowDim-D QQ + hist](/assets/normality-report/qq_hist_LowDim-D_data.png)

### MidDim-D_data (100 vars): heavy tails
Pass rates drop to around 0.78 to 0.82 and skew/kurtosis are elevated. This is non-Gaussian.
Suggested methods: LiNGAM; GraNDAG if you suspect nonlinear structure [7,8].

![MidDim-D p-values](/assets/normality-report/pvalues_MidDim-D_data.png)
![MidDim-D QQ + hist](/assets/normality-report/qq_hist_MidDim-D_data.png)

### MidDim-S_data (100 vars): mixed behavior
Pass rates are reasonably high, but kurtosis is elevated. This suggests some heavy-tailed variables even when many pass normality.
Suggested methods: PC/NOTEARS can work, but LiNGAM may gain from the non-Gaussian subset [1,6,7].

![MidDim-S p-values](/assets/normality-report/pvalues_MidDim-S_data.png)
![MidDim-S QQ + hist](/assets/normality-report/qq_hist_MidDim-S_data.png)

## 7) Practical guidance for method choice

Regime A: near Gaussian (high pass-rate, low skew/kurt) [1,6]
- Recommended: PC, NOTEARS
- Optional: GraNDAG if you expect nonlinear relations

Regime B: clearly non-Gaussian (tails or skew) [7]
- Recommended: LiNGAM
- Also viable: PC/NOTEARS with robust preprocessing

Regime C: mixed or nonlinear [8]
- Recommended: GraNDAG
- Compare against: PC/NOTEARS as baselines

## 8) Why I do not over-trust p-values

In high dimensions we run one test per variable. Some rejections are expected by chance. Also, with large n, tests become very sensitive and can reject for tiny deviations. That is why the plots and skew/kurtosis matter as much as the p-values.

If this were a formal hypothesis testing exercise, I would treat it as a multiple testing problem. Here, the goal is to characterize the data regime, not to "prove" normality (Benjamini and Hochberg, 1995) [9].

## 9) Limitations and next steps

- These are univariate tests; multivariate normality can still fail.
- Heteroscedasticity, nonlinearity, and hidden confounding still matter even if marginals look normal.
- Next step: add a multivariate normality check and a lightweight nonlinear dependence screen.

## References

- [1] Spirtes, P., Glymour, C., & Scheines, R. (2000). Causation, Prediction, and Search (2nd ed.). MIT Press.
- [2] Shapiro, S. S., & Wilk, M. B. (1965). An analysis of variance test for normality (complete samples). Biometrika.
- [3] D'Agostino, R. (1973). Tests for departure from normality: empirical results for the distributions of b2 and sqrt(b1). Biometrika.
- [4] Jarque, C. M., & Bera, A. K. (1980). Efficient tests for normality, homoscedasticity and serial independence of regression residuals. Economics Letters.
- [5] Anderson, T. W., & Darling, D. A. (1954). A test of goodness of fit. Journal of the American Statistical Association.
- [6] Zheng, X., Aragam, B., Ravikumar, P., & Xing, E. (2018). DAGs with NO TEARS: Continuous Optimization for Structure Learning. NeurIPS.
- [7] Shimizu, S., Hoyer, P. O., Hyvarinen, A., & Kerminen, A. (2006). A Linear Non-Gaussian Acyclic Model for Causal Discovery. JMLR.
- [8] Lachapelle, S., Brouillard, P., Deleu, T., & Lacoste-Julien, S. (2019). Gradient-Based Neural DAG Learning. ICLR.
- [9] Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: a practical and powerful approach to multiple testing. JRSS-B.
