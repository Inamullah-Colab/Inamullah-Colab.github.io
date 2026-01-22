import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib.pyplot as plt

FOLDER = Path(r"C:\Users\i1n23\OneDrive - University of Southampton\Documents\codex_folder\Check for the normality")
PLOTS = FOLDER / "plots"
PLOTS.mkdir(parents=True, exist_ok=True)

ALPHA = 0.05
NORMALITY_SAMPLE = 5000
RNG = np.random.default_rng(7)


def sample_series(x, n=5000, seed=7):
    if len(x) <= n:
        return x
    return x.sample(n=n, random_state=seed)


def normality_metrics(x):
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

    shapiro_p = np.nan
    if n_s <= 5000:
        shapiro_p = stats.shapiro(x_s).pvalue

    k2_p = np.nan
    if n_s >= 20:
        k2_p = stats.normaltest(x_s).pvalue

    jb_p = stats.jarque_bera(x_s).pvalue
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
    x = x.dropna()
    if len(x) < 2:
        return {"variance": np.nan, "std": np.nan, "skew": np.nan, "kurtosis": np.nan}
    return {
        "variance": float(x.var(ddof=1)),
        "std": float(x.std(ddof=1)),
        "skew": float(stats.skew(x)),
        "kurtosis": float(stats.kurtosis(x, fisher=True)),
    }


def main():
    files = sorted(FOLDER.glob("*.csv"))
    if not files:
        raise SystemExit("No CSV files found in: " + str(FOLDER))

    all_rows = []
    summary_rows = []

    for f in files:
        df = pd.read_csv(f).select_dtypes(include="number")
        rows = []
        for col in df.columns:
            nm = normality_metrics(df[col])
            vm = variance_metrics(df[col])
            row = {"dataset": f.stem, "column": col}
            row.update(vm)
            row.update(nm)
            rows.append(row)

        out_df = pd.DataFrame(rows)
        out_df.to_csv(FOLDER / f"{f.stem}_univariate_summary.csv", index=False)
        all_rows.extend(rows)

        def pass_rate(series):
            return float((series >= ALPHA).mean())

        summary_rows.append({
            "dataset": f.stem,
            "n_cols": df.shape[1],
            "shapiro_pass_rate": pass_rate(out_df["shapiro_p"].dropna()),
            "k2_pass_rate": pass_rate(out_df["k2_p"].dropna()),
            "jb_pass_rate": pass_rate(out_df["jb_p"].dropna()),
            "ad_pass_rate": float((~out_df["ad_reject_5pct"]).mean()),
            "mean_abs_skew": float(out_df["skew"].abs().mean()),
            "mean_abs_kurtosis": float(out_df["kurtosis"].abs().mean()),
        })

    combined = pd.DataFrame(all_rows)
    combined.to_csv(FOLDER / "ALL_univariate_summary.csv", index=False)

    summary = pd.DataFrame(summary_rows).sort_values("dataset")
    summary.to_csv(FOLDER / "ALL_dataset_summary.csv", index=False)

    # Pass-rate plot
    plot_df = summary.melt(
        id_vars=["dataset"],
        value_vars=["shapiro_pass_rate", "k2_pass_rate", "jb_pass_rate", "ad_pass_rate"],
        var_name="test",
        value_name="pass_rate",
    )
    plt.figure(figsize=(10, 5))
    for test in plot_df["test"].unique():
        sub = plot_df[plot_df["test"] == test]
        plt.plot(sub["dataset"], sub["pass_rate"], marker="o", label=test)
    plt.axhline(0.8, color="gray", linestyle="--", linewidth=1)
    plt.title("Normality Pass Rates by Dataset")
    plt.ylabel("Pass rate (p >= 0.05)")
    plt.xticks(rotation=35, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS / "pass_rate_by_dataset.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    main()
