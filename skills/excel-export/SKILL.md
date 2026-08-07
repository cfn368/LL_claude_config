---
name: excel-export
description: Turn pasted Python/terminal output (printed DataFrames, dicts, arrays) into a Danish-language Excel workbook for non-technical colleagues — house palette, live delta formulas, charts sized to the content. Domain-agnostic — applies to any analysis (energy, macro, labour, whatever), from a single small table to a multi-sheet result set. Apply whenever the deliverable is an .xlsx for colleagues, not a notebook figure or a raw CSV dump.
---

## When this applies

Input is Python output pasted into chat (a printed `DataFrame`, dict, or array);
output is an `.xlsx` for a colleague who doesn't read Python. Not for data going to
further analysis (use CSV/Parquet) or a plot for a notebook/paper (use `econ-plotting`).
Nothing here is energy-specific — the palette, formulas, and layout are the point; any
`GW`/`DKK` below is just an illustration of a rule.

## Default workflow — build, then verify NUMERICALLY

1. **Read the paste by eye.** Terminal prints are small; read the column structure,
   index levels, and values directly — don't regex a MultiIndex dump. Infer units from
   the variable names; ask only if genuinely ambiguous.
2. **Build with the helpers.** `bs_table` writes a whole basis/scenarie/Δ table (header,
   rows, live Δ formulas, optional SUM total) from a column spec — reach for hand-written
   cells only for the odd table it can't express (see "Helper module").
3. **End the build script with `finalize(path, checks=…)`.** It recalculates the file and
   reads your check cells back **in one process** — no separate recalc/verify shell steps.
4. **Verify by the printed numbers**, not by eye: confirm each `finalize` check matches the
   paste (small rounding gaps from live formulas on rounded inputs are the self-check
   working, not a bug). **Do NOT render the workbook to an image for QA.** Render one page
   only if `finalize` reports `total_errors > 0`, or the user explicitly asks to see it.
   Image inspection is the single most expensive step in this flow and adds nothing once
   the numbers check out.

## Scale to the input

- **Short** (one small table): a single sheet — title, subtitle, table. Skip the chart if
  the table already makes the point; skip the total block if there's nothing to aggregate.
- **Medium** (2–3 related tables): one sheet per table, chart only where it earns its place.
- **Long** (many result blocks): one sheet per logical block, numbered sheet names, and an
  **overview sheet first** (see below). Chart the 1–2 headline comparisons, not every sheet.

## Sheet structure

Name sheets `"N. Kort dansk titel"` (Excel's 31-char tab limit; full description goes in the
in-sheet subtitle). Single-sheet deliverables drop the number prefix. Each sheet:
1. **Title** (B2, `write_title`): bold 14pt navy — the finding, not "Table 1".
2. **Subtitle** (B3): 10pt red — units, scope, what Δ means; say Δ columns are live formulas.
3. Blank row, then **header** (`header_row` / `bs_table`); add a `subheader_row` only for
   paired column groups.
4. Data rows, then an optional **zebra total row** (`bs_table(total=…)` does this).
5. Optional **chart** a blank row below the table.

Sheet setup: `setup_sheet(ws)` (gridlines off, zoom, narrow col A). Freeze under the header
via `bs_table(freeze=True)` on the sheet's first/only table.

## Multi-sheet: overview sheet first

Sheet 1 is a one-screen overview: a short plain-language block (what was analysed + the 4–6
headline "so what" findings in prose), then a **nøgletal table** laid out `Basis | Scenarie | Δ`
whose basis/scenarie cells are **cross-sheet references** (`linkrow`, green) with Δ as a live
formula on top. If part of the analysis is unfinished, say so here (a "mangler endnu" line) so
a partial result isn't read as complete.

**Cross-sheet quoting gotcha (load-bearing):** a sheet name with a space or period **must be
quoted** — `='2. Priser'!C9`, not `=2. Priser!C9` (the latter → `#NAME?`). Numbered tabs
always need the quotes. Build detail sheets first, note the cells totals land in, then wire the
overview to them and confirm via `finalize` checks.

## Colour system

| Role | Hex | Constant |
|---|---|---|
| Primary text, header fill, primary series | `#1F2A44` | `NAVY` |
| Sub-header fill (paired-group columns) | `#41546E` | `SUBHEADER` |
| Deltas, subtitles, secondary series | `#E04131` | `ACCENT` |
| Cross-sheet link (provenance only) | `#008000` | `LINK_GREEN` |
| Aggregate/total row background | `#EEF1F5` | `ZEBRA` |
| Section dividers | `#7A8699` | `LABEL_GRAY` |
| Chart gridlines | `#878787` | `GRID_GRAY` |

Navy = "what is", red = "what changed"; those two carry all emphasis (use greyscale tints, not
a third accent, for extra series). Green is **not** a third emphasis colour — it marks a cell
pulled from another sheet so the reader knows it's a link, not a re-typed number.

## Deltas & totals are live formulas, never hardcoded

Even if the paste prints a delta/total, write the formula (`bs_table` does: Δ = `=D6-C6`,
total = `=SUM(...)`), so the sheet stays self-checking. Delta cells: bold red, signed number
format so + / − show without conditional formatting.

## Number formats

| Value type | Format | Constant |
|---|---|---|
| Precise small levels (GW, ratios) | `0.000` | `FMT_3DP` |
| Δ on that scale | `+0.000;-0.000;0` | `FMT_DELTA_3DP` |
| Two-decimal level (TWh) | `0.00` | `FMT_2DP` |
| Δ two-decimal (TWh) | `+0.00;-0.00;0.00` | `FMT_DELTA_2DP` |
| One-decimal level (prices, rates) | `0.0` | `FMT_1DP` |
| Δ one-decimal | `+0.0;-0.0;0.0` | `FMT_DELTA_1DP` |
| Large level / count (DKK/MWh, headcount) | `#,##0` | `FMT_INT` |
| Δ integer | `+#,##0;-#,##0;0` | `FMT_DELTA_INT` |
| Large value, negative = reduction (mDKK) | `#,##0;(#,##0)` | `FMT_INT_PAREN` |
| Large value 1dp, negative in parens (mDKK) | `#,##0.0;(#,##0.0)` | `FMT_MDKK_1DP` |
| Δ large-value 1dp (Δ mDKK) | `+#,##0.0;-#,##0.0;0.0` | `FMT_DELTA_MDKK_1DP` |
| Share / rate | `0.0%` | `FMT_PCT1` |
| Δ percentage-point | `+0.0%;-0.0%;0.0%` | `FMT_DELTA_PCT1` |

Sign conventions live in the format string, not conditional formatting. Missing a constant?
Add it to `excel_style.py`, don't inline the raw string.

## Charts

Not mandatory — chart the 1–2 comparisons a visual beats reading, skip the rest. Match type to
shape: **clustered column** (`add_bar_chart`) for cross-sectional base-vs-shock; **single-series
column** (`colors=(NAVY,), legend=None`) for one derived quantity across categories; **line**
(`add_line_chart`) for a time series. House style is baked into the helpers (gray horizontal
gridlines, navy/red, ~15×7.5cm). Title states the finding in Danish with units. Leave ~14 rows
below a chart before the next table.

## finalize = recalc + verify (mandatory when the file has formulas)

openpyxl writes formulas with no cached value, so an unrecalculated file reads back as `None`
and a broken reference ships silently. `finalize(path, checks={label: "Sheet!Cell"})` recalcs
(LibreOffice) and prints `total_errors` + your check values in one call. Never ship with a
`#REF!`/`#NAME?`/`#VALUE!`. **Stay in the LibreOffice-safe function set** — `SUM`, `SUMIFS`,
`INDEX`/`MATCH`, `IFERROR`, `SUMPRODUCT` are fine; avoid spilling array functions
(`XLOOKUP`/`FILTER`/`UNIQUE`/`SORT`) — no spill metadata, so they truncate or become `#NAME?`.

## Danish language

Everything the colleague reads is Danish (sheet names, titles, subtitles, headers, chart
titles/axes); code and this module stay English. Recurring terms:

| EN | DA | EN | DA |
|---|---|---|---|
| baseline | basis | total | i alt |
| scenario / shock | scenarie / stød | mean | middelværdi / gennemsnit |
| delta / change | Δ / ændring | min / max | min / maks |
| std dev | spredning | share / rate | andel / rate |

Domain vocabulary (zone, eksport, ledighed, BNP…) is translated in context. When a table keys
on model codes the reader won't know, add a Danish gloss column beside the code and a glossary
sheet — the codes stay, the reader still follows.

## Helper module (`assets/excel_style.py`)

Constants above plus: `setup_sheet`, `write_title`, `header_row`, `subheader_row`,
`section_label`; **`bs_table`** (the workhorse — column spec + rows → header, data, live Δ,
optional SUM total; returns row anchors + a `cols` map for wiring charts/refs); `data_row` and
`delta_formula` (low-level, for tables `bs_table` can't express); `link_cell` / `linkrow`
(green cross-sheet refs for the overview); `add_bar_chart` / `add_line_chart`; **`finalize`**
(recalc + read-back). Import from there; don't reimplement styling by hand.

**`bs_table` covers the common label | basis | scenarie | Δ table (with an auto total).** Hand-write
rows only when a table breaks that shape — section-grouped sub-totals, a decomposition where
the "total" column is a sum of two others (`=D+E`, not `=SUM`), or a grand total that sums
country-total rows rather than all data rows. For those, write the cells directly (navy centered,
right `numfmt`) and use `delta_formula` for the Δ.