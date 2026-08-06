"""
excel-export skill helpers — domain-agnostic openpyxl building blocks for the
house style (navy/red, gridlines off, live delta formulas, charts sized to
the content). Applies to any analysis, not just the energy example the style
was reverse-engineered from (transmission_shock_results.xlsx).
"""
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.utils import get_column_letter

# ---- palette --------------------------------------------------------------
NAVY = "1F2A44"        # primary text, header fill, primary series
SUBHEADER = "41546E"   # lighter navy, sub-header fill (paired-group columns)
ACCENT = "E04131"      # subtitles, delta values, secondary series
LINK_GREEN = "008000"  # cross-sheet link (provenance marker, not an emphasis colour)
ZEBRA = "EEF1F5"       # aggregate / total row background
LABEL_GRAY = "7A8699"  # small section dividers ("Aggregater", "I alt")
GRID_GRAY = "878787"   # chart gridlines
WHITE = "FFFFFF"

# ---- number formats ---------------------------------------------------
# Pick by magnitude/nature of the value, not by habit — see SKILL.md "Number formats".
FMT_3DP = "0.000"                          # precise small-magnitude levels
FMT_DELTA_3DP = r"\+0.000;\-0.000;0"       # deltas on that same scale
FMT_INT = "#,##0"                          # large levels / counts
FMT_DELTA_INT = r"\+#,##0;\-#,##0;0"       # signed integer deltas
FMT_PCT1 = "0.0%"                          # shares / rates
FMT_DELTA_PCT1 = r"\+0.0%;\-0.0%;0.0%"     # signed percentage-point deltas
FMT_2DP_PAREN = r"0.00;\(0.00\)"           # 2dp, negative = reduction, shown in parens
FMT_DELTA_2DP = r"\+0.00;\-0.00;0.00"      # signed 2dp delta (e.g. TWh)
FMT_1DP = "0.0"                            # small level, one decimal (e.g. hours)
FMT_DELTA_1DP = r"\+0.0;\-0.0;0.0"         # signed one-decimal delta
FMT_INT_PAREN = r"#,##0;\(#,##0\)"         # large value, negative = reduction, in parens
FMT_MDKK_1DP = r"#,##0.0;\(#,##0.0\)"      # large value, 1dp, negative = reduction (e.g. mDKK)
FMT_DELTA_MDKK_1DP = r"\+#,##0.0;\-#,##0.0;0.0"  # signed 1dp large-value delta (e.g. Δ mDKK)


def setup_sheet(ws, zoom=130, margin_width=3.0):
    """Gridlines off, house zoom level, narrow column A as left margin."""
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = zoom
    ws.column_dimensions["A"].width = margin_width


def write_title(ws, title, subtitle="", row=2):
    """B{row}: bold 14pt navy headline. B{row+1}: 10pt red subtitle (units/scope)."""
    c = ws.cell(row=row, column=2, value=title)
    c.font = Font(bold=True, size=14, color=NAVY)
    ws.row_dimensions[row].height = 17.55
    if subtitle:
        ws.cell(row=row + 1, column=2, value=subtitle).font = Font(size=10, color=ACCENT)


def header_row(ws, row, headers, start_col=2):
    """Bold white text on navy fill, centered — top-level column headers."""
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col + i, value=h)
        c.font = Font(bold=True, size=10, color=WHITE)
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(horizontal="center")


def subheader_row(ws, row, labels, start_col=3):
    """Bold white on lighter navy — second header row for base/shock/Δ/Δ% groups."""
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=start_col + i, value=lab)
        c.font = Font(bold=True, size=9, color=WHITE)
        c.fill = PatternFill("solid", fgColor=SUBHEADER)
        c.alignment = Alignment(horizontal="center")


def data_row(ws, row, label, values, start_col=3, numfmt=FMT_INT, bold_label=True, zebra=False):
    """One data row: bold navy label in column B, centered values from start_col."""
    lc = ws.cell(row=row, column=2, value=label)
    lc.font = Font(bold=bold_label, size=10, color=ACCENT if zebra else NAVY)
    if zebra:
        lc.fill = PatternFill("solid", fgColor=ZEBRA)
    for i, v in enumerate(values):
        c = ws.cell(row=row, column=start_col + i, value=v)
        c.font = Font(bold=bold_label, size=10, color=NAVY)
        c.number_format = numfmt
        c.alignment = Alignment(horizontal="center")
        if zebra:
            c.fill = PatternFill("solid", fgColor=ZEBRA)


def delta_formula(ws, row, col, minuend_col, subtrahend_col, numfmt=FMT_DELTA_INT):
    """Write a live =B-A formula (never a hardcoded number) styled as a delta: bold, red."""
    col_l = get_column_letter(col)
    m_l = get_column_letter(minuend_col)
    s_l = get_column_letter(subtrahend_col)
    c = ws.cell(row=row, column=col, value=f"={m_l}{row}-{s_l}{row}")
    c.font = Font(bold=True, size=10, color=ACCENT)
    c.number_format = numfmt
    c.alignment = Alignment(horizontal="center")
    return c


def section_label(ws, row, text, col=2):
    """Small gray divider above a sub-block, e.g. 'Aggregater (vægtet)'."""
    ws.cell(row=row, column=col, value=text).font = Font(bold=True, size=9, color=LABEL_GRAY)


def _finish_chart(ws, chart, anchor, title, cats_ref, data_ref, colors,
                   legend, numfmt, width, height):
    """Shared house styling: gray horizontal gridlines, navy/red series, sized legend."""
    chart.title = title
    chart.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill=GRID_GRAY))
    chart.y_axis.numFmt = numfmt
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    for s, color in zip(chart.series, colors):
        s.graphicalProperties.solidFill = color
        if isinstance(chart, LineChart):
            s.graphicalProperties.line.solidFill = color
            s.graphicalProperties.line.width = 20000  # EMU, ~1.6pt
    if legend:
        chart.legend.position = legend
    else:
        chart.legend = None
    chart.width = width
    chart.height = height
    ws.add_chart(chart, anchor)
    return chart


def add_bar_chart(ws, anchor, title, cats_ref, data_ref, colors=(NAVY, ACCENT),
                   legend="r", numfmt=FMT_INT, width=15, height=7.5, gap_width=60):
    """Clustered column chart — the default for cross-sectional comparisons
    across categories (regions, sectors, groups, base-vs-shock per item, ...).

    title: plain string (openpyxl wraps it). cats_ref / data_ref: openpyxl Reference objects.
    legend: "r" for 2+ series, None for a single-series chart.
    """
    chart = BarChart()
    chart.type = "col"
    chart.grouping = "clustered"
    chart.gapWidth = gap_width
    return _finish_chart(ws, chart, anchor, title, cats_ref, data_ref, colors,
                          legend, numfmt, width, height)


def add_line_chart(ws, anchor, title, cats_ref, data_ref, colors=(NAVY, ACCENT),
                    legend="r", numfmt=FMT_INT, width=15, height=7.5):
    """Line chart — for a time series (year-by-year, period-by-period).

    Same signature and house styling as add_bar_chart; use this instead when the
    x-axis categories are a time index rather than discrete groups.
    """
    chart = LineChart()
    return _finish_chart(ws, chart, anchor, title, cats_ref, data_ref, colors,
                          legend, numfmt, width, height)