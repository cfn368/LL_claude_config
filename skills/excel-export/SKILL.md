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
  the numbers. Lead with an overview sheet — see "Multi-sheet outputs".

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

## Multi-sheet outputs: lead with an overview sheet

For a Long result set (several blocks, one sheet each), make sheet 1 a one-screen overview
so the colleague sees the story before the tables:

- A short **plain-language block**: one line on what was analysed, then the 4–6 headline
  findings in prose — the "so what", in the reader's language, not a restatement of column
  headers.
- A **nøgletal table** — the handful of numbers that carry the finding — laid out
  `Basis | Scenarie | Δ`. Pull the base/scenarie cells from the detail sheets by
  **cross-sheet reference** (green text, per "Colour system"); write Δ as a formula on top
  of those refs. Editing a detail cell then flows through to the overview automatically.
- If part of the analysis is unfinished, say so here (a "mangler endnu" line), so a
  **partial** result isn't read as a complete one. A welfare account missing ΔCS, or a
  run missing a year, should announce that on the front page, not bury it.

**Cross-sheet reference gotcha:** a sheet name containing a space, period, or `&` **must be
quoted** in the reference — `='2. Priser'!C9`, not `=2. Priser!C9` (the latter parses to
`#NAME?`). Numbered tab names (`"2. Priser"`, `"3. Handel"`) therefore *always* need the
quotes. Build the detail sheets first, note the exact cells the totals land in, then wire
the overview to them — and verify those links after recalc (see "Recalculate before shipping").

## Colour system

| Role | Hex | Constant |
|---|---|---|
| Primary text, header fill, primary series | `#1F2A44` | `NAVY` |
| Sub-header fill (paired-group columns) | `#41546E` | `SUBHEADER` |
| Deltas, subtitles, secondary series | `#E04131` | `ACCENT` |
| Cross-sheet link (provenance) | `#008000` | `LINK_GREEN` |
| Aggregate/total row background | `#EEF1F5` | `ZEBRA` |
| Small section dividers | `#7A8699` | `LABEL_GRAY` |
| Chart gridlines | `#878787` | `GRID_GRAY` |

Two colours carry all *emphasis*: navy for "what is," red for "what changed." Don't add a
third accent colour — if a sheet needs to distinguish more than two series, use navy/red
plus greyscale tints, not a rainbow.

Green is the one sanctioned exception, and it is **not** a third emphasis colour — it's a
*provenance* marker. A cell whose value is pulled from another sheet (a nøgletal on the
overview sheet linking to its detail sheet) gets green text so the reader knows it's a
link, not a re-typed number; emphasis still runs on navy/red only. This resolves the
earlier navy-vs-green ambiguity in favour of green-for-links, and matches
`PROJECT_CONTEXT §9` and the base `xlsx` convention. (Levels that are typed in, not linked,
stay navy — green is reserved for genuine cross-sheet references.)

## Deltas are live formulas, never hardcoded

If the paste already contains a computed comparison column (delta, growth rate, ratio,
whatever), don't just copy the number in — write the formula, e.g. `=F6-E6`, so the sheet
stays self-checking if a colleague edits an input cell. Delta cells: bold, red
(`ACCENT`), signed number format so + and − are visible without conditional formatting.

The same goes for a total or a derived quantity the paste happens to print: prefer
`=C12-E12` (netto = eksport − import) or `=SUM(...)` over the printed value, so the sheet
recomputes itself. A live formula off rounded inputs can land a hundredth away from a
paste's higher-precision figure — that's the self-check working, not a bug; note the
convention (e.g. "netto = eksport − import") in the subtitle rather than hardcoding to match.

## Recalculate before shipping (mandatory when the file has formulas)

openpyxl writes formulas as strings with **no cached value** — until the file is
recalculated, every formula cell reads back as `None` to pandas / `data_only=True` / most
previewers, and a broken reference ships silently. Before sending:

- **Recalculate.** In a sandbox, run the `xlsx` skill's `scripts/recalc.py output.xlsx`
  (LibreOffice; rewrites in place; reports `total_errors` and names the offending cells).
  On a machine with Excel, simply opening the file recalculates it — but still verify.
  Never ship while a `#REF!` / `#NAME?` / `#VALUE!` remains.
- **Then spot-check 2–3 cells.** A clean recalc proves formulas *evaluate*, not that
  they're *right* — an off-by-one reference recalculates cleanly to the wrong number.
  Reload with `data_only=True` and confirm the totals and every cross-sheet link pull the
  values you expect from the paste. This is the step that catches a mis-wired overview.
- **Stay in the LibreOffice-safe function set:** `SUM`, `SUMIFS`, `INDEX`/`MATCH`,
  `IFERROR`, `SUMPRODUCT` need no prefix. Avoid `XLOOKUP`/`FILTER`/`UNIQUE`/`SORT` and
  other spilling array functions — an openpyxl-written file has no spill metadata, so they
  silently truncate or become `#NAME?`.

## Number formats

Pick by the magnitude and nature of the value, not by habit:

| Value type | Format | Constant |
|---|---|---|
| Precise small-magnitude levels (e.g. GW, ratios) | `0.000` | `FMT_3DP` |
| Deltas on that same 3-decimal scale | `+0.000;-0.000;0` | `FMT_DELTA_3DP` |
| Two-decimal levels, negative = a reduction (e.g. TWh, index pts) | `0.00;(0.00)` | `FMT_2DP_PAREN` |
| Deltas on a 2-decimal scale (e.g. TWh) | `+0.00;-0.00;0.00` | `FMT_DELTA_2DP` |
| Small level, one decimal (e.g. hours, rates) | `0.0` | `FMT_1DP` |
| Signed one-decimal delta | `+0.0;-0.0;0.0` | `FMT_DELTA_1DP` |
| Large levels / counts (e.g. DKK/MWh, headcounts) | `#,##0` | `FMT_INT` |
| Signed integer deltas | `+#,##0;-#,##0;0` | `FMT_DELTA_INT` |
| Large value, negative = a reduction (e.g. mDKK, budget lines) | `#,##0;(#,##0)` | `FMT_INT_PAREN` |
| Large value, one decimal, negative = a reduction (e.g. mDKK) | `#,##0.0;(#,##0.0)` | `FMT_MDKK_1DP` |
| Signed one-decimal large-value delta (e.g. Δ mDKK) | `+#,##0.0;-#,##0.0;0.0` | `FMT_DELTA_MDKK_1DP` |
| Shares / rates (e.g. unemployment rate, hours share) | `0.0%` | `FMT_PCT1` |
| Signed percentage-point deltas | `+0.0%;-0.0%;0.0%` | `FMT_DELTA_PCT1` |

Sign conventions live in the format string, not conditional formatting — simpler to
reason about and survives copy-paste into another workbook. If a constant isn't yet in
`excel_style.py`, add it **there** rather than inlining the raw format string at call
sites — one definition, reused, is the whole point of the table.

## Charts

Not mandatory — see "Scale to the input." When one earns its place, match chart type to
data shape:
- **Clustered column** — cross-sectional comparison across categories (regions, sectors,
  base-vs-shock per line item). The default case.
- **Line** — a time series (a year-by-year or period-by-period series).
- **Single-series column** — one derived quantity across categories (e.g. Δ profit per
  technology). Pass `colors=(NAVY,)` and `legend=None`; the title carries the meaning.
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
- Size ≈15×7.5cm, anchored a couple of rows below the table. A 7.5cm chart spans ~14 rows —
  leave that gap before the next table so they don't collide.

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
part of the house style. When a table keys on model codes the reader won't know (plant
types, area codes), add a Danish gloss column beside the code and a glossary sheet — the
codes stay, the reader still follows.

## Helper module

`assets/excel_style.py` has the constants above plus `setup_sheet`, `write_title`,
`header_row`, `subheader_row`, `data_row`, `delta_formula`, `section_label`,
`add_bar_chart`, and `add_line_chart` — openpyxl wrappers, not a new abstraction to learn.
Import or copy from there; don't reimplement the styling by hand each time.

`data_row` is for **uniform** tables: one number format, plain values, a label in column
B. The moment a row needs a second text column (a Danish description beside a code),
per-cell formats, or a live formula, don't fight `data_row` — write those cells directly
(navy, centered, the right `numfmt`) and use `delta_formula` for the Δ. Most base/shock/Δ
tables fall in this second category, so expect to hand-write their rows; `data_row` earns
its keep on the simple ones.

If the reference example workbook (`transmission_shock_results.xlsx`) is to hand, keep it
beside the skill in `assets/` — one look at the target output calibrates spacing, column
widths, and chart size faster than any amount of prose here.