---
name: econ-plotting
description: Matplotlib-only plotting standards for economics figures — AEJ rcParams, SEC_PALETTE, figure sizing, legend placement rules. Apply whenever writing or reviewing any plot.
---

## Hard rules

- **matplotlib only.** No seaborn, plotly, or altair.
- **Width always 12.** Height is case-dependent (4 for single-panel line; 6–9 for multi-panel).
- **300 DPI** for all saves. `savefig.dpi` is set globally via `set_aej()`; pass `dpi=300` explicitly too.
- `plt.tight_layout()` before every save.

## Colour palette

```python
SEC_PALETTE = [
    "#E04131", "#DE7626", "#18DBB1", "#6A7015", "#5E3F27",
    "#63110A", "#090BDF", "#34BA5B", "#7B81E0", "#275C51",
    "#F5C518", "#C084FC", "#FB7185", "#38BDF8", "#EBD87C",
    "#4ADE80", "#FB923C", "#818CF8", "#A3E635", "#34D399",
]
```

Index into `SEC_PALETTE` in order. Two-series default: `SEC_PALETTE[0]` (red) solid, `SEC_PALETTE[1]` (orange) dashed — or use `#1F2A44` (dark navy) as a neutral second series.

## Legend placement

- **Default:** `loc='lower left'` inside the axes.
- **Grid with an unused subplot:** turn the empty axes off and place the legend there:
  ```python
  ax_legend.axis('off')
  ax_legend.legend(handles=handles, labels=labels, loc='center', frameon=True)
  ```
  Never waste the empty cell on whitespace.

## Grid and reference lines

```python
ax.grid(linewidth=0.6, alpha=0.35)
ax.axhline(0, color='0.2', lw=1, ls='--')   # reference line convention
```

## Time-series x-axis

```python
ax.set_xlim(df.index.min(), df.index.max())
ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=12))
```

## Save pattern

```python
plt.tight_layout()
if save_path:
    plt.savefig(save_path, dpi=300)
plt.show()
return fig, ax
```

See `assets/template.py` for full copy-paste templates and `assets/matplotlibrc` for the rcParams file.