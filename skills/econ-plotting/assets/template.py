# assets/template.py — econ-plotting copy-paste templates
from __future__ import annotations

import pathlib

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

TEXT_COLOR = "#3F6469"   # same hue as figure/axes facecolor, much lower lightness

SEC_PALETTE = [
    "#E04131", "#DE7626", "#18DBB1", "#6A7015", "#5E3F27",
    "#63110A", "#090BDF", "#34BA5B", "#7B81E0", "#275C51",
    "#F5C518", "#C084FC", "#FB7185", "#38BDF8", "#EBD87C",
    "#4ADE80", "#FB923C", "#818CF8", "#A3E635", "#34D399",
]

MAANED_DK = ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun",
             "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"]
MAANED_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# ── style ────────────────────────────────────────────────────────────────────

def set_aej(**kwargs) -> None:
    mpl.rcParams.update({
        "font.family":          "serif",
        "font.style":           "italic",
        "font.size":            15,
        "figure.dpi":           150,
        "figure.facecolor":     "#EAF1F2",
        "axes.facecolor":       "#EAF1F2",
        "axes.linewidth":       1.0,
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        "axes.spines.left":     False,
        "axes.spines.bottom":   False,
        "text.color":           TEXT_COLOR,
        "axes.labelcolor":      TEXT_COLOR,
        "xtick.color":          TEXT_COLOR,
        "ytick.color":          TEXT_COLOR,
        "lines.linewidth":      1.2,
        "xtick.direction":      "out",
        "ytick.direction":      "out",
        "legend.frameon":       False,
        "legend.fancybox":      False,
        "legend.borderaxespad": 0.4,
        "legend.handlelength":  2.0,
        "legend.handletextpad": 0.6,
        "legend.labelspacing":  0.35,
        "savefig.bbox":         "tight",
        "savefig.dpi":          300,
        **kwargs,
    })


def fig_title(ax, title: str, subtitle: str = "") -> None:
    """Bold declarative headline + italic subtitle above axes, left-aligned."""
    base = mpl.rcParams["font.size"]
    ax.set_title(
        title, loc="left", fontstyle="normal", fontweight="bold",
        fontsize=base + 1, color=TEXT_COLOR,
        pad=base + 16 if subtitle else 10,
    )
    if subtitle:
        ax.annotate(
            subtitle,
            xy=(0, 1), xycoords="axes fraction",
            xytext=(0, 10), textcoords="offset points",
            fontsize=base - 2, fontstyle="italic",
            color=TEXT_COLOR, va="bottom", ha="left",
        )


def ordered_legend(ax, order=None, **kwargs):
    """Legend centered below the axes, in caller-supplied left-to-right order."""
    handles, labels = ax.get_legend_handles_labels()
    lut = dict(zip(labels, handles))
    order = [l for l in (order or labels) if l in lut]
    ax.legend([lut[l] for l in order], order,
               loc="upper center", bbox_to_anchor=(0.5, -0.12),
               ncol=len(order), **kwargs)


def align_zeros(ax1, ax2) -> None:
    """Expand lower limits so zero sits at the same fractional height on both axes."""
    lo1, hi1 = ax1.get_ylim()
    lo2, hi2 = ax2.get_ylim()
    f1 = (0 - lo1) / (hi1 - lo1) if hi1 != lo1 else 0.5
    f2 = (0 - lo2) / (hi2 - lo2) if hi2 != lo2 else 0.5
    f = max(f1, f2)
    if 0 < f < 1:
        ax1.set_ylim(-f * hi1 / (1 - f), hi1)
        ax2.set_ylim(-f * hi2 / (1 - f), hi2)


def month_ticks(idx, danish: bool = True):
    """Midpoint-free month ticks: first position of each month's contiguous block."""
    names = MAANED_DK if danish else MAANED_EN
    ticks, labels = [], []
    for m in range(1, 13):
        pos = np.where(idx.month == m)[0]
        if not len(pos):
            continue
        gaps = np.where(np.diff(pos) > 1)[0]
        if len(gaps):
            pos = pos[:gaps[0] + 1]   # drop year-boundary tail
        ticks.append(pos[0])
        labels.append(names[m - 1])
    return ticks, labels


def save(fig, save_path=None) -> None:
    plt.tight_layout()
    if save_path:
        pathlib.Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)
    plt.show()


# ── single panel ─────────────────────────────────────────────────────────────

def plot_single(df, save_path=None, title="", subtitle=""):
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(df.index, df["series_a"], color=SEC_PALETTE[0], lw=2, ls="-", label="Series A")
    ax.plot(df.index, df["series_b"], color=SEC_PALETTE[1], lw=2, ls="--", label="Series B")

    ax.axhline(0, color="0.2", lw=1, ls="--")
    ax.set_ylabel("Label (unit)")
    ax.grid(lw=0.6, alpha=0.35)
    ax.set_xlim(df.index.min(), df.index.max())
    ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=12))
    ordered_legend(ax)

    if title:
        fig_title(ax, title, subtitle)
    save(fig, save_path)
    return fig, ax


# ── twin y-axes, zero-aligned ───────────────────────────────────────────────

def plot_twin(df, save_path=None, title="", subtitle=""):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    ax1.fill_between(df.index, 0, df["stock"], color=SEC_PALETTE[2], alpha=0.35, linewidth=0, label="Stock")
    ax1.set_ylabel("Stock (unit)")

    ax2.plot(df.index, df["flow"], color=SEC_PALETTE[0], lw=1.5, label="Flow")
    ax2.set_ylabel("Flow (unit)")

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper center",
               bbox_to_anchor=(0.5, -0.12), ncol=len(h1) + len(h2))

    align_zeros(ax1, ax2)
    if title:
        fig_title(ax1, title, subtitle)
    save(fig, save_path)
    return fig, (ax1, ax2)


# ── grid with unused subplot → legend ───────────────────────────────────────
# Example: 3×3 grid, 8 series. The 9th cell holds the legend.

def plot_grid_with_legend(panels: dict, ncols: int = 3, save_path=None):
    """
    panels: {label: pd.Series}  — up to ncols*nrows - 1 entries
    """
    n = len(panels)
    nrows = -(-n // ncols)  # ceiling division
    total = nrows * ncols

    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 4 * nrows))
    axs = axes.flatten()

    handles = []
    for i, (label, series) in enumerate(panels.items()):
        ax = axs[i]
        h, = ax.plot(series.index, series.values, color=SEC_PALETTE[i % len(SEC_PALETTE)], lw=2)
        handles.append(h)
        ax.set_title(label)
        ax.grid(lw=0.6, alpha=0.35)
        ax.set_xlim(series.index.min(), series.index.max())
        ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=8))

    if n < total:
        ax_legend = axs[n]
        ax_legend.axis("off")
        ax_legend.legend(handles=handles, labels=list(panels.keys()), loc="center")
        for ax in axs[n + 1:]:
            ax.axis("off")

    save(fig, save_path)
    return fig, axes
