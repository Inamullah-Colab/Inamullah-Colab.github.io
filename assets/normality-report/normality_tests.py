import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------
# Config
# -----------------------
FOLDER = Path(r"C:\Users\i1n23\OneDrive - University of Southampton\Documents\codex_folder\Check for the normality")
ALPHA = 0.05
NORMALITY_SAMPLE = 5000
PLOT_SAMPLE_COLS = 6  # number of columns per dataset to show QQ+hist
RNG = np.random.default_rng(7)

# -----------------------
# Helpers
# -----------------------
def sample_series(x, n=5000, seed=7):
    # Limit sample size so tests stay fast for very large columns.
    if len(x) <= n:
        return x
    return x.sample(n=n, random_state=seed)


def normality_metrics(x):
    # Run multiple normality tests to avoid relying on one statistic.
    x = x.dropna()
    n = len(x)
    if n < 8:
        return {
            "n": n,
            "shapiro_p": np.nan,
            "k2_p": np.nan,
            "jb_p": np.nan,
            "ad_stat": np.nan,
            "ad_crit_5pct": np.nan,
            "ad_reject_5pct": np.nan,
        }

    x_s = sample_series(x, NORMALITY_SAMPLE)
    n_s = len(x_s)

    # Shapiro is reliable for small samples.
    shapiro_p = np.nan
    if n_s <= 5000:
        shapiro_p = stats.shapiro(x_s).pvalue

    # D'Agostino K2 works well for larger samples.
    k2_p = np.nan
    if n_s >= 20:
        k2_p = stats.normaltest(x_s).pvalue

    jb_p = stats.jarque_bera(x_s).pvalue

    # Anderson-Darling: returns statistic + critical values.
    ad_res = stats.anderson(x_s, dist="norm")
    ad_stat = ad_res.statistic
    ad_crit_5pct = ad_res.critical_values[2]
    ad_reject_5pct = ad_stat > ad_crit_5pct

    return {
        "n": n,
        "shapiro_p": shapiro_p,
        "k2_p": k2_p,
        "jb_p": jb_p,
        "ad_stat": ad_stat,
        "ad_crit_5pct": ad_crit_5pct,
        "ad_reject_5pct": ad_reject_5pct,
    }


def variance_metrics(x):
    # Basic variance diagnostics for each column.
    x = x.dropna()
    if len(x) < 2:
        return {"variance": np.nan, "std": np.nan, "skew": np.nan, "kurtosis": np.nan}
    return {
        "variance": float(x.var(ddof=1)),
        "std": float(x.std(ddof=1)),
        "skew": float(stats.skew(x)),
        "kurtosis": float(stats.kurtosis(x, fisher=True)),
    }


# -----------------------
# Load datasets
# -----------------------
files = sorted(FOLDER.glob("*.csv"))
print("Found files:", [f.name for f in files])

data = {}
for f in files:
    df = pd.read_csv(f)
    df = df.select_dtypes(include="number")  # all numeric in your case
    data[f.stem] = df

print("Shapes:", {k: v.shape for k, v in data.items()})

# -----------------------
# Compute metrics + save CSVs
# -----------------------
all_rows = []
summary_rows = []

for name, df in data.items():
    rows = []
    for col in df.columns:
        nm = normality_metrics(df[col])
        vm = variance_metrics(df[col])
        row = {"dataset": name, "column": col}
        row.update(vm)
        row.update(nm)
        rows.append(row)

    out_df = pd.DataFrame(rows)
    out_path = FOLDER / f"{name}_univariate_summary.csv"
    out_df.to_csv(out_path, index=False)
    all_rows.extend(rows)

    # Pass/fail rates (p >= ALPHA) for normality tests.
    def pass_rate(series):
        return float((series >= ALPHA).mean())

    summary_rows.append({
        "dataset": name,
        "n_cols": df.shape[1],
        "shapiro_pass_rate": pass_rate(out_df["shapiro_p"].dropna()),
        "k2_pass_rate": pass_rate(out_df["k2_p"].dropna()),
        "jb_pass_rate": pass_rate(out_df["jb_p"].dropna()),
        "ad_pass_rate": float((~out_df["ad_reject_5pct"]).mean()),
        "mean_abs_skew": float(out_df["skew"].abs().mean()),
        "mean_abs_kurtosis": float(out_df["kurtosis"].abs().mean()),
    })

combined = pd.DataFrame(all_rows)
combined_path = FOLDER / "ALL_univariate_summary.csv"
combined.to_csv(combined_path, index=False)

summary = pd.DataFrame(summary_rows).sort_values("dataset")
summary_path = FOLDER / "ALL_dataset_summary.csv"
summary.to_csv(summary_path, index=False)

print(f"Saved: {combined_path}")
print(f"Saved: {summary_path}")
summary

# -----------------------
# Visualization 1: Normality pass rates
# -----------------------
plot_df = summary.melt(
    id_vars=["dataset"],
    value_vars=["shapiro_pass_rate", "k2_pass_rate", "jb_pass_rate", "ad_pass_rate"],
    var_name="test",
    value_name="pass_rate"
)

plt.figure(figsize=(10, 5))
sns.barplot(data=plot_df, x="dataset", y="pass_rate", hue="test")
plt.axhline(0.8, color="gray", linestyle="--", linewidth=1)
plt.title("Normality Pass Rates by Dataset")
plt.ylabel("Pass rate (p >= 0.05)")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.show()

# -----------------------
# Visualization 2: P-value histograms
# -----------------------
for name in data.keys():
    df = combined[combined["dataset"] == name]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    for ax, col, title in zip(
        axes,
        ["shapiro_p", "k2_p", "jb_p"],
        ["Shapiro", "D'Agostino K2", "Jarque-Bera"]
    ):
        vals = df[col].dropna()
        ax.hist(vals, bins=20, alpha=0.8)
        ax.axvline(ALPHA, color="red", linestyle="--", linewidth=1)
        ax.set_title(f"{name}: {title}")
        ax.set_xlabel("p-value")
        ax.set_ylabel("count")
    plt.tight_layout()
    plt.show()

# -----------------------
# Visualization 3: Skew vs Kurtosis
# -----------------------
plt.figure(figsize=(6, 5))
sns.scatterplot(
    data=combined,
    x="skew",
    y="kurtosis",
    hue="dataset",
    alpha=0.7
)
plt.axvline(0, color="gray", linewidth=1)
plt.axhline(0, color="gray", linewidth=1)
plt.title("Skew vs Kurtosis (per column)")
plt.tight_layout()
plt.show()

# -----------------------
# Visualization 4: QQ + Histogram for sampled columns
# -----------------------
for name, df in data.items():
    cols = RNG.choice(df.columns, size=min(PLOT_SAMPLE_COLS, df.shape[1]), replace=False)
    for col in cols:
        x = df[col].dropna()
        x_s = sample_series(x, NORMALITY_SAMPLE)

        fig, axes = plt.subplots(1, 2, figsize=(8, 3))
        sns.histplot(x_s, kde=True, ax=axes[0])
        axes[0].set_title(f"{name} - {col} histogram")

        stats.probplot(x_s, dist="norm", plot=axes[1])
        axes[1].set_title(f"{name} - {col} QQ")

        plt.tight_layout()
        plt.show()
