"""
M1/M2 — EDA plotting helpers (Notebook 01).

Saves PNGs to figures/eda/ and displays inline when show=True (Jupyter).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

PALETTE = ["#1a6b5a", "#c47a1e", "#b84038", "#1e3a6e", "#6b3fa0"]

RESULT_COLORS = {
    "Pass": PALETTE[0],
    "Distinction": PALETTE[1],
    "Fail": PALETTE[2],
    "Withdrawn": PALETTE[3],
}

RESULT_ORDER = ["Distinction", "Pass", "Fail", "Withdrawn"]

WEEK_COLS = [f"week_{w}_clicks" for w in range(34)]

CORR_COLS = [
    "total_clicks",
    "active_days",
    "clicks_per_day",
    "active_day_rate",
    "first_access_day",
    "last_access_day",
    "avg_score",
    "score_std",
    "avg_submission_delay",
    "total_missing",
    "num_of_prev_attempts",
    "studied_credits",
]

DEMO_COLS = ["age_band", "highest_education", "gender", "num_of_prev_attempts"]

# Bump when adding plots — notebook setup checks this string
EDA_PLOTS_VERSION = "2.1"

__all__ = [
    "PALETTE",
    "RESULT_COLORS",
    "RESULT_ORDER",
    "WEEK_COLS",
    "CORR_COLS",
    "DEMO_COLS",
    "EDA_PLOTS_VERSION",
    "add_missing_rate",
    "plot_result_distribution",
    "plot_cohort_registrations",
    "plot_click_distribution",
    "plot_clicks_by_outcome",
    "plot_active_days_distribution",
    "plot_engagement_scatter",
    "plot_disengagement_by_outcome",
    "plot_activity_type_by_outcome",
    "plot_missing_rate_by_outcome",
    "plot_submission_delay_by_outcome",
    "plot_temporal_heatmap",
    "plot_score_distribution_by_outcome",
    "plot_demographics_by_outcome",
    "plot_correlation_matrix",
    "plot_module_comparison",
]


def _style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _result_colors_for(columns: pd.Index) -> list[str]:
    return [RESULT_COLORS.get(c, PALETTE[4]) for c in columns]


def _finalize(fig: plt.Figure, save_path: Path | None, show: bool = True) -> Path:
    """Save figure, optionally display inline, return path to PNG."""
    if save_path is None:
        plt.close(fig)
        raise ValueError("save_path is required for notebook EDA plots")
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    else:
        plt.close(fig)
    return save_path


def add_missing_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Compute missing_rate; safe when total_assessments_due is 0."""
    out = df.copy()
    due = out["total_assessments_due"].replace(0, np.nan)
    out["missing_rate"] = (out["total_missing"] / due).fillna(0)
    return out


def plot_result_distribution(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    counts = df["final_result"].value_counts()
    order = [x for x in RESULT_ORDER if x in counts.index]
    order += [x for x in counts.index if x not in order]
    counts = counts.reindex(order)
    pcts = counts / counts.sum() * 100

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(
        counts.index, counts.values,
        color=[RESULT_COLORS.get(x, PALETTE[4]) for x in counts.index],
    )
    ax.set_xlabel("Number of students")
    ax.set_title(f"Distribution of Final Results — {len(df):,} Registrations")
    _style_axes(ax)
    for bar, n, pct in zip(bars, counts.values, pcts):
        ax.text(
            bar.get_width() + counts.max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{n:,} ({pct:.1f}%)",
            va="center",
            fontsize=9,
        )
    return _finalize(fig, save_path, show)


def plot_cohort_registrations(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    """Students per module–presentation (standard OULAD overview)."""
    cohort = (
        df.groupby(["code_module", "code_presentation"], observed=True)
        .size()
        .reset_index(name="n_students")
    )
    cohort["label"] = cohort["code_module"] + "-" + cohort["code_presentation"]
    cohort = cohort.sort_values("n_students", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(cohort["label"], cohort["n_students"], color=PALETTE[3])
    ax.set_xlabel("Number of registrations")
    ax.set_title("Cohort Size by Module and Presentation")
    _style_axes(ax)
    return _finalize(fig, save_path, show)


def plot_click_distribution(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    zero = (df["total_clicks"] == 0).sum()
    log_clicks = np.log1p(df["total_clicks"])

    axes[0].hist(df["total_clicks"], bins=50, color=PALETTE[0], edgecolor="white")
    axes[0].axvline(df["total_clicks"].median(), color=PALETTE[2], linestyle="--",
                    label=f"Median = {df['total_clicks'].median():.0f}")
    axes[0].set_title(f"Total Clicks (Raw) — {zero:,} at zero")
    axes[0].set_xlabel("Total clicks")
    axes[0].legend()

    axes[1].hist(log_clicks, bins=50, color=PALETTE[3], edgecolor="white")
    axes[1].axvline(log_clicks.median(), color=PALETTE[2], linestyle="--",
                    label=f"Median = {log_clicks.median():.2f}")
    axes[1].set_title("Total Clicks (log1p)")
    axes[1].set_xlabel("log1p(total_clicks)")
    axes[1].legend()

    for ax in axes:
        _style_axes(ax)
    fig.suptitle("VLE Click Volume Distribution", y=1.02)
    return _finalize(fig, save_path, show)


def plot_clicks_by_outcome(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    """Boxplot of total_clicks by outcome (log y) — common in OULAD papers."""
    order = [x for x in RESULT_ORDER if x in df["final_result"].unique()]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=df, x="final_result", y="total_clicks", order=order,
        hue="final_result", palette=[RESULT_COLORS[o] for o in order],
        dodge=False, legend=False, ax=ax,
    )
    ax.set_yscale("symlog", linthresh=1)
    ax.set_xlabel("Final result")
    ax.set_ylabel("Total clicks (symlog scale)")
    ax.set_title("VLE Engagement Volume by Final Result")
    _style_axes(ax)
    return _finalize(fig, save_path, show)


def plot_active_days_distribution(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df["active_days"], bins=40, kde=True, color=PALETTE[0], ax=ax)
    p25 = df["active_days"].quantile(0.25)
    ax.axvline(p25, color=PALETTE[2], linestyle="--", linewidth=2,
               label=f"25th percentile = {p25:.0f} days")
    ax.set_xlabel("Active days")
    ax.set_title("Distribution of Active Days on the VLE")
    ax.legend()
    _style_axes(ax)
    return _finalize(fig, save_path, show)


def plot_engagement_scatter(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    plot_df = df.dropna(subset=["avg_score", "clicks_per_day"])
    plot_df = plot_df[plot_df["clicks_per_day"] > 0]

    fig, ax = plt.subplots(figsize=(10, 6))
    for outcome in RESULT_ORDER:
        sub = plot_df[plot_df["final_result"] == outcome]
        if sub.empty:
            continue
        ax.scatter(
            sub["clicks_per_day"], sub["avg_score"],
            c=RESULT_COLORS.get(outcome, PALETTE[4]),
            label=outcome, alpha=0.35, s=14,
        )
    ax.set_xscale("log")
    ax.axhline(40, color="gray", linestyle=":", linewidth=1)
    ax.set_xlabel("Clicks per day (log scale)")
    ax.set_ylabel("Average assessment score")
    ax.set_title("Engagement Rate vs Average Score")
    ax.legend(markerscale=2, frameon=False)
    _style_axes(ax)
    return _finalize(fig, save_path, show)


def plot_disengagement_by_outcome(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    """Share of students with zero VLE clicks, by outcome."""
    order = [x for x in RESULT_ORDER if x in df["final_result"].unique()]
    rates = (
        df.assign(zero_clicks=df["total_clicks"] == 0)
        .groupby("final_result", observed=True)["zero_clicks"]
        .mean()
        .reindex(order)
        * 100
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(
        rates.index, rates.values,
        color=[RESULT_COLORS.get(x, PALETTE[4]) for x in rates.index],
    )
    ax.set_ylabel("% with zero total clicks")
    ax.set_xlabel("Final result")
    ax.set_title("Platform Disengagement (No VLE Activity) by Outcome")
    _style_axes(ax)
    for i, v in enumerate(rates.values):
        ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9)
    return _finalize(fig, save_path, show)


def plot_activity_type_by_outcome(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    """Mean quiz / forum / resource clicks by outcome."""
    order = [x for x in RESULT_ORDER if x in df["final_result"].unique()]
    means = (
        df.groupby("final_result", observed=True)[["quiz_clicks", "forum_clicks", "resource_clicks"]]
        .mean()
        .reindex(order)
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(order))
    w = 0.25
    ax.bar(x - w, means["quiz_clicks"], width=w, label="Quiz", color=PALETTE[0])
    ax.bar(x, means["forum_clicks"], width=w, label="Forum", color=PALETTE[1])
    ax.bar(x + w, means["resource_clicks"], width=w, label="Resource", color=PALETTE[3])
    ax.set_xticks(x)
    ax.set_xticklabels(order)
    ax.set_ylabel("Mean clicks")
    ax.set_title("Mean Clicks by Activity Type and Outcome")
    ax.legend()
    _style_axes(ax)
    return _finalize(fig, save_path, show)


def plot_missing_rate_by_outcome(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    data = add_missing_rate(df)
    order = [x for x in RESULT_ORDER if x in data["final_result"].unique()]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=data, x="final_result", y="missing_rate", order=order,
        hue="final_result", palette=[RESULT_COLORS[o] for o in order],
        dodge=False, legend=False, ax=ax, width=0.5,
    )
    sample = data.sample(min(2000, len(data)), random_state=42)
    sns.stripplot(
        data=sample, x="final_result", y="missing_rate", order=order,
        color="0.35", alpha=0.15, size=2, ax=ax,
    )
    ax.set_xlabel("Final result")
    ax.set_ylabel("Missing submission rate")
    ax.set_title("Share of Assessments Not Submitted, by Outcome")
    _style_axes(ax)
    return _finalize(fig, save_path, show)


def plot_submission_delay_by_outcome(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    data = df.dropna(subset=["avg_submission_delay"])
    order = [x for x in RESULT_ORDER if x in data["final_result"].unique()]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(
        data=data, x="final_result", y="avg_submission_delay", order=order,
        hue="final_result", palette=[RESULT_COLORS[o] for o in order],
        dodge=False, legend=False, ax=ax, inner="quartile",
    )
    ax.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Final result")
    ax.set_ylabel("Average submission delay (days)")
    ax.set_title("Submission Timing vs Deadline, by Outcome")
    ax.legend(["Deadline (0)"], frameon=False)
    _style_axes(ax)
    return _finalize(fig, save_path, show)


def plot_temporal_heatmap(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    week_cols = [c for c in WEEK_COLS if c in df.columns]
    heat = (
        df.groupby("final_result", observed=True)[week_cols]
        .mean()
        .reindex([x for x in RESULT_ORDER if x in df["final_result"].unique()])
    )
    heat.columns = [int(c.split("_")[1]) for c in heat.columns]
    fig, ax = plt.subplots(figsize=(14, 4))
    sns.heatmap(heat, cmap="YlOrRd", ax=ax)
    ax.set_xlabel("Week of module")
    ax.set_ylabel("Final result")
    ax.set_title("Mean Weekly Clicks by Outcome")
    return _finalize(fig, save_path, show)


def plot_score_distribution_by_outcome(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    data = df.dropna(subset=["avg_score"])
    fig, ax = plt.subplots(figsize=(10, 6))
    for outcome in RESULT_ORDER:
        sub = data.loc[data["final_result"] == outcome, "avg_score"]
        if len(sub) < 2:
            continue
        sns.kdeplot(sub, label=outcome, color=RESULT_COLORS.get(outcome, PALETTE[4]), ax=ax)
    ax.axvline(40, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Average assessment score")
    ax.set_title("Score Distributions by Final Result")
    ax.legend(frameon=False)
    _style_axes(ax)
    return _finalize(fig, save_path, show)


def plot_demographics_by_outcome(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    """Stacked bars: demographics × final_result (OULAD descriptive standard)."""
    cols = [c for c in DEMO_COLS if c in df.columns][:4]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
    axes = axes.flatten()

    for ax, col in zip(axes, cols):
        ct = pd.crosstab(df[col], df["final_result"])
        cols_ord = [c for c in RESULT_ORDER if c in ct.columns]
        ct = ct[cols_ord]
        ct.plot(
            kind="bar", stacked=True, ax=ax,
            color=_result_colors_for(ct.columns),
            width=0.85,
        )
        ax.set_title(f"Outcome by {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=25)
        _style_axes(ax)
        ax.legend(title="final_result", fontsize=8, loc="upper right")

    fig.suptitle("Demographics and Prior Attempts vs Final Result", y=1.01)
    return _finalize(fig, save_path, show)


def plot_correlation_matrix(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    cols = [c for c in CORR_COLS if c in df.columns]
    corr = df[cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
        center=0, square=True, linewidths=0.5, ax=ax, vmin=-1, vmax=1,
    )
    ax.set_title("Correlation Matrix — Behavioral and Academic Variables")
    return _finalize(fig, save_path, show)


def plot_module_comparison(
    df: pd.DataFrame, save_path: Path | None = None, show: bool = True
) -> plt.Figure:
    mod = (
        df.groupby("code_module", observed=True)
        .agg(
            withdrawal_rate=("is_withdrawn", "mean"),
            mean_clicks_per_day=("clicks_per_day", "mean"),
        )
        .reset_index()
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    w = mod.sort_values("withdrawal_rate", ascending=False)
    axes[0].bar(w["code_module"], w["withdrawal_rate"] * 100, color=PALETTE[2])
    axes[0].set_ylabel("Withdrawal rate (%)")
    axes[0].set_title("Withdrawal Rate by Module")
    c = mod.sort_values("mean_clicks_per_day", ascending=False)
    axes[1].bar(c["code_module"], c["mean_clicks_per_day"], color=PALETTE[0])
    axes[1].set_ylabel("Mean clicks per day")
    axes[1].set_title("Mean Engagement by Module")
    for ax in axes:
        _style_axes(ax)
    fig.suptitle("Module-Level Differences", y=1.02)
    return _finalize(fig, save_path, show)
