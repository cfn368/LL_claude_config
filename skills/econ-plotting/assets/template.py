# assets/template.py — econ-plotting copy-paste templates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

SEC_PALETTE = [
    "#E04131", "#DE7626", "#18DBB1", "#6A7015", "#5E3F27",
    "#63110A", "#090BDF", "#34BA5B", "#7B81E0", "#275C51",
    "#F5C518", "#C084FC", "#FB7185", "#38BDF8", "#EBD87C",
    "#4ADE80", "#FB923C", "#818CF8", "#A3E635", "#34D399",
]


# ── single panel ──────────────────────────────────────────────────────────────

def plot_single(df, save_path=None):
    fig, ax = plt.subplots(figsize=(12, 4))

    l1, = ax.plot(df.index, df["series_a"], color=SEC_PALETTE[0], lw=2, ls="-")
    l2, = ax.plot(df.index, df["series_b"], color=SEC_PALETTE[1], lw=2, ls="--")

    ax.axhline(0, color="0.2", lw=1, ls="--")
    ax.set_ylabel("Label (unit)")
    ax.set_xlabel("Year")
    ax.grid(lw=0.6, alpha=0.35)
    ax.set_xlim(df.index.min(), df.index.max())
    ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=12))
    ax.legend([l1, l2], ["Series A", "Series B"], loc="lower left")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()
    return fig, ax


# ── grid with unused subplot → legend ─────────────────────────────────────────
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

    # unused subplot(s) → first empty cell gets the legend
    if n < total:
        ax_legend = axs[n]
        ax_legend.axis("off")
        ax_legend.legend(
            handles=handles,
            labels=list(panels.keys()),
            loc="center",
            frameon=True,
        )
        for ax in axs[n + 1:]:
            ax.axis("off")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()
    return fig, axes
