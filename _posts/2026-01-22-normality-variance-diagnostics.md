---
title: "Normality and Variance Diagnostics for Causal Discovery"
date: 2026-01-22
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

This post explains why we check normality and variance before running causal discovery, shows the plots, and gives dataset-level guidance based on the results.

## Why we do this

Many causal discovery methods assume something about the data distribution:

- PC and NOTEARS (linear-Gaussian) usually work best when variables are close to Gaussian.
- LiNGAM depends on non-Gaussian noise to recover causal directions.
- GraNDAG is more flexible for nonlinear patterns but heavier to train.

So before modeling, we first check how Gaussian each dataset looks. This helps select the most suitable algorithm.

## Overview plots

### Pass-rate overview

This shows the fraction of columns that pass each normality test (p >= 0.05).

![Pass rates by dataset](/assets/normality-report/pass_rate_by_dataset.png)

### Skew vs kurtosis

Points near (0, 0) are close to Gaussian. Large deviations indicate skew or heavy tails.

![Skew vs kurtosis scatter](/assets/normality-report/skew_kurtosis_scatter.png)

## Dataset summary table

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

How to read this table:
- Pass rate near 1.0 means many columns look Gaussian.
- Large mean absolute skew or kurtosis means stronger non-Gaussian behavior.

## Dataset notes and recommended algorithms

### HighDim-D_data
- Very low pass rates and extreme skew/kurtosis.
- Suggestion: LiNGAM or GraNDAG if you expect nonlinear relationships.

![HighDim-D p-values](/assets/normality-report/pvalues_HighDim-D_data.png)
![HighDim-D QQ + hist](/assets/normality-report/qq_hist_HighDim-D_data.png)

### HighDim-S_data
- Very Gaussian-like.
- Suggestion: PC or NOTEARS.

![HighDim-S p-values](/assets/normality-report/pvalues_HighDim-S_data.png)
![HighDim-S QQ + hist](/assets/normality-report/qq_hist_HighDim-S_data.png)

### LowDim-D_data
- Mostly Gaussian with mild tails.
- Suggestion: PC or NOTEARS.

![LowDim-D p-values](/assets/normality-report/pvalues_LowDim-D_data.png)
![LowDim-D QQ + hist](/assets/normality-report/qq_hist_LowDim-D_data.png)

### LowDim-L_data
- Very Gaussian-like.
- Suggestion: PC or NOTEARS.

![LowDim-L p-values](/assets/normality-report/pvalues_LowDim-L_data.png)
![LowDim-L QQ + hist](/assets/normality-report/qq_hist_LowDim-L_data.png)

### LowDim-N_data
- Gaussian-like.
- Suggestion: PC or NOTEARS.

![LowDim-N p-values](/assets/normality-report/pvalues_LowDim-N_data.png)
![LowDim-N QQ + hist](/assets/normality-report/qq_hist_LowDim-N_data.png)

### LowDim-P_data
- Gaussian-like.
- Suggestion: PC or NOTEARS.

![LowDim-P p-values](/assets/normality-report/pvalues_LowDim-P_data.png)
![LowDim-P QQ + hist](/assets/normality-report/qq_hist_LowDim-P_data.png)

### MidDim-C_data
- Gaussian-like.
- Suggestion: PC or NOTEARS.

![MidDim-C p-values](/assets/normality-report/pvalues_MidDim-C_data.png)
![MidDim-C QQ + hist](/assets/normality-report/qq_hist_MidDim-C_data.png)

### MidDim-D_data
- Non-Gaussian with heavy tails.
- Suggestion: LiNGAM; GraNDAG if nonlinear.

![MidDim-D p-values](/assets/normality-report/pvalues_MidDim-D_data.png)
![MidDim-D QQ + hist](/assets/normality-report/qq_hist_MidDim-D_data.png)

### MidDim-P_data
- Very Gaussian-like.
- Suggestion: PC or NOTEARS.

![MidDim-P p-values](/assets/normality-report/pvalues_MidDim-P_data.png)
![MidDim-P QQ + hist](/assets/normality-report/qq_hist_MidDim-P_data.png)

### MidDim-S_data
- Mixed behavior: good pass rates but elevated skew/kurtosis.
- Suggestion: PC/NOTEARS may work, but LiNGAM can help if non-Gaussian noise is present.

![MidDim-S p-values](/assets/normality-report/pvalues_MidDim-S_data.png)
![MidDim-S QQ + hist](/assets/normality-report/qq_hist_MidDim-S_data.png)

## Limitations

- These are univariate tests; multivariate normality can still fail.
- With many columns, some false positives are expected.
- Use these checks alongside domain knowledge and downstream validation.
