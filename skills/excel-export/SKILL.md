---
name: excel-export
description: Turn pasted Python/terminal output (printed DataFrames, dicts, arrays) into a Danish-language Excel workbook for non-technical colleagues — house palette, live delta formulas, charts sized to the content. Domain-agnostic — applies to any analysis (energy, macro, labour, whatever), from a single small table to a multi-sheet result set. Apply whenever the deliverable is an .xlsx for colleagues, not a notebook figure or a raw CSV dump.
---

## When this applies

The input is Python output pasted into chat — usually a printed `DataFrame` (often with
a `MultiIndex`), sometimes a dict or array — and the output is an `.xlsx` file meant for
a colleague who doesn't read Python. This is not for data destined for further analysis
(use Parquet/CSV per the project's storage convention) and not for a plot going in a
notebook or paper (use `econ-plotting`). It's the "send this to a colleague who opens
Excel" path — as relevant to a two-line labour-market table as to a ten-sheet CGE run.

The style below was reverse-engineered from one energy-modelling example workbook, but
nothing in it is energy-specific: the palette, formulas, and layout rules are the point,
not the units. Every energy term below (GW, DKK/MWh) is an *illustration* of a rule, not
the rule itself — swap in whatever unit the actual data is in.

## Reading the pasted output

Terminal-pasted `DataFrame` prints are small enough to read by eye — don't try to regex
or auto-parse a MultiIndex dump. Read the column structure, row index levels, and values
directly, then write them into the sheet with the helpers below. Ask the user only if a
column's unit or meaning is genuinely ambiguous — usually it isn't, infer it from the
variable names in the paste (e.g. `GW_base`/`GW_shock`/`delta` is baseline vs. shock).

## Scale to the input

A two-column, five-row result and a ten-block model run need different amounts of
scaffolding. Don't apply every element below to everything:

- **Short** (one small table, one finding): a single sheet — title, subtitle, table. Skip
  the chart if the table alone already makes the point (e.g. 3 numbers); skip the
  sub-header row and aggregate block if there's nothing to aggregate.
- **Medium** (one table needing a comparison visual, or 2–3 related tables): one sheet
  per table, chart where it earns its place.
- **Long** (many result blocks / a full model run): one sheet per logical block, numbered
  sheet names for navigation, chart on the sheets where a visual comparison beats reading
  the numbers.

The judgment call is "does a chart or a second header row help this specific colleague
read this specific result" — not "did the last workbook have one."

## Sheet structure

One sheet per logical block of results, not one giant sheet, once there's more than one
block. Name sheets `"N. Kort dansk titel"` (numbered, e.g. `"1. Kapacitetsstød"`) —
Excel's 31-character tab limit means the title must be short; put the full description in
the in-sheet subtitle instead. For a single-sheet deliverable the number prefix is
unnecessary.

Each sheet, as applicable (see "Scale to the input"):
1. **Title** (B2): bold, 14pt, navy — the finding or scope, not "Table 1".
2. **Subtitle** (B3): 10pt, red — units, scope, and what Δ means. State explicitly that Δ
   columns are live formulas if any are present.
3. Blank row, then the **header row** (bold white on navy fill, centered). Add a second,
   smaller sub-header row (white on lighter navy) only when columns come in paired groups
   (base/shock/Δ, before/after, actual/target — whatever the comparison is).
4. Data rows, then optionally an **aggregate/total block** below a blank row, marked with
   a small gray section label (e.g. "Aggregater", "I alt") and a light zebra fill on the
   total row(s).
5. Optionally, a **chart** below the table (leave one blank row of gap) — see "Charts".

Sheet-level setup: gridlines off, freeze panes just below the header row, zoom 115–145%,
column A narrow (width ≈3) as a left margin so the title/table doesn't hug the tab edge.

## Colour system

| Role | Hex | Constant |
|---|---|---|
| Primary text, header fill, primary series | `#1F2A44` | `NAVY` |
| Sub-header fill (paired-group columns) | `#41546E` | `SUBHEADER` |
| Deltas, subtitles, secondary series | `#E04131` | `ACCENT` |
| Aggregate/total row background | `#EEF1F5` | `ZEBRA` |
| Small section dividers | `#7A8699` | `LABEL_GRAY` |
| Chart gridlines | `#878787` | `GRID_GRAY` |

Two colours carry all emphasis: navy for "what is," red for "what changed." Don't add a
third accent colour — if a sheet needs to distinguish more than two series, use navy/red
plus greyscale tints, not a rainbow. This is a general-purpose two-colour system, not tied
to any one domain's palette.

## Deltas are live formulas, never hardcoded

If the paste already contains a computed comparison column (delta, growth rate, ratio,
whatever), don't just copy the number in — write the formula, e.g. `=F6-E6`, so the sheet
stays self-checking if a colleague edits an input cell. Delta cells: bold, red
(`ACCENT`), signed number format so + and − are visible without conditional formatting.

## Number formats

Pick by the magnitude and nature of the value, not by habit:

| Value type | Format | Constant |
|---|---|---|
| Precise small-magnitude levels (e.g. GW, ratios) | `0.000` | `FMT_3DP` |
| Deltas on the same scale | `+0.000;-0.000;0` | `FMT_DELTA_3DP` |
| Large levels / counts (e.g. DKK/MWh, headcounts) | `#,##0` | `FMT_INT` |
| Signed integer deltas | `+#,##0;-#,##0;0` | `FMT_DELTA_INT` |
| Shares / rates (e.g. unemployment rate, hours share) | `0.0%` | `FMT_PCT1` |
| Signed percentage-point deltas | `+0.0%;-0.0%;0.0%` | `FMT_DELTA_PCT1` |
| Two-decimal values where negative = a reduction (e.g. TWh, index points) | `0.00;(0.00)` | `FMT_2DP_PAREN` |
| Large values where negative = a reduction (e.g. mDKK, budget lines) | `#,##0;(#,##0)` | `FMT_INT_PAREN` |

Sign conventions live in the format string, not conditional formatting — simpler to
reason about and survives copy-paste into another workbook.

## Charts

Not mandatory — see "Scale to the input." When one earns its place, match chart type to
data shape:
- **Clustered column** — cross-sectional comparison across categories (regions, sectors,
  base-vs-shock per line item). The default case.
- **Line** — a time series (a year-by-year or period-by-period series).
- Skip charting a single number, a short list with no natural x-axis, or anything the
  table already communicates in one glance.

House style regardless of type:
- Navy first series, red second series (`colors=(NAVY, ACCENT)`).
- Horizontal gridlines only, thin, `#878787`. No chart-area border or fill.
- Legend on the right (`legend="r"`) when the chart has 2+ series; no legend for a
  single-series chart — the title already says what it is.
- Chart title states the finding, in Danish, with units — e.g. "Ændring i
  gennemsnitspris efter zone (DKK/MWh)" or "Ledighed 2015–2025 (pct.)", not "Chart 1" or
  a restatement of the table's column headers.
- Size ≈15×7.5cm, anchored a couple of rows below the table.

## Danish language

Everything the colleague reads — sheet names, titles, subtitles, column headers, chart
titles/axes — is in Danish. Code, variable names, and this skill's helper module stay
English per the project's language convention. Core EN→DA terms that recur across
domains:

| EN | DA |
|---|---|
| baseline | basis |
| scenario / shock | scenarie / stød |
| delta / change | Δ / ændring |
| mean / average | middelværdi / gennemsnit |
| min / max | min / maks |
| std dev | spredning |
| share / rate | andel / rate |
| total | i alt |
| growth | vækst |

Domain-specific vocabulary (energy: zone, eksport/import, timer; macro: ledighed, BNP,
sektor; whatever the project is) isn't listed here — translate it in context, it isn't
part of the house style.

## Helper module

`assets/excel_style.py` has the constants above plus `setup_sheet`, `write_title`,
`header_row`, `subheader_row`, `data_row`, `delta_formula`, `section_label`,
`add_bar_chart`, and `add_line_chart` — openpyxl wrappers, not a new abstraction to learn.
Import or copy from there; don't reimplement the styling by hand each time.
