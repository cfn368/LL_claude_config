---
name: econ-plotting
description: Matplotlib-only plotting standards for economics figures — set_aej() rcParams, fig_title(), ordered bottom-legend, twin-axis zero-alignment, Danish month ticks. Apply whenever writing or reviewing any plot.
---

## Hard rules

- **matplotlib only.** No seaborn, plotly, or altair.
- **Width always 12.** Height is case-dependent (4–6 single-panel, more for twin-axis/stacked, 4×nrows for grids).
- **300 DPI**, set once via `savefig.dpi` in `set_aej()` — don't pass `dpi=` per call.
- **No manual titles.** Use `fig_title(ax, title, subtitle)`, never `ax.set_title(...)` directly.
- `plt.tight_layout()` before every save.

## Style

`set_aej()` sets a colour-washed, spineless look: light-tint `figure`/`axes.facecolor`, italic serif body text, frameless legends. `TEXT_COLOR` is the same hue as the facecolor at much lower lightness — drives `text.color`, `axes.labelcolor`, tick colors. Swap both together when adapting to a different project identity; don't lighten/darken independently. Call once from `setup_notebook()` (see `notebook-setup` skill), never inline in a plotting function.

## Titles

`fig_title(ax, title, subtitle="")`: bold, left-aligned, non-italic headline (a finding stated plainly — "Vindkraft dækker vinteren", not "Wind production by month"); optional italic subtitle below carrying scope/units/scenario detail.

## Colour

`SEC_PALETTE` (positional, 20 colours) for ad hoc series — index in order. Two-series default: `SEC_PALETTE[0]` red solid, `SEC_PALETTE[1]` orange dashed, or `#1F2A44` navy as a neutral second series.

When a project has a **stable domain vocabulary** recurring across many figures (e.g. grid/battery/wind/solar dispatch categories), define a semantic `dict` keyed by category name instead of indexing `SEC_PALETTE` positionally. Keep that dict in the project's own module, not this skill.

## Legend

Default: centered below the axes via `ordered_legend(ax, order=...)`, not `lower left` inside it. `order` controls left-to-right legend order independent of stacking order.

**Grid with an unused subplot:** turn the empty axes off and place the legend there instead — never waste the cell on whitespace.

## Twin y-axes

Call `align_zeros(ax1, ax2)` after both axes have data plotted, before legend/title, whenever two y-axes share a meaningful zero (stock left, flow right) — otherwise a sign crossing on one axis reads as misleading relative to the other.

## Time-series x-axis

Numeric/date index, evenly spaced ticks: `ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=12))`.

Daily/weekly data labelled by calendar month (Danish default): `month_ticks(idx)` — ticks at the first position of each month's contiguous block, not every date. Pass `danish=False` for English labels.

## Grid and reference lines

```python
ax.grid(linewidth=0.6, alpha=0.35)
ax.axhline(0, color="0.2", lw=1, ls="--")
```

## Save pattern

Use `save(fig, save_path)` — `tight_layout()`, `mkdir(parents=True, exist_ok=True)` on the parent, `savefig`, `show()`.

---

All functions above (`set_aej`, `fig_title`, `ordered_legend`, `align_zeros`, `month_ticks`, `save`) plus full plot templates (single-panel, twin-axis, grid-with-legend) live in `assets/template.py` — import or copy from there, don't reimplement. rcParams equivalent in `assets/matplotlibrc`.
