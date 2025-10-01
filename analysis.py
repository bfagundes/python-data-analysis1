import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# =============== Settings ===============
INPUT_XLSX  = "./files/2025-09-30-uece.xlsx"   # <- change to your file
OUTPUT_XLSX         = "./charts/analysis.xlsx"
CHARTS_DIR          = "charts"
CONTROL_SHEET_NAME  = "respostas_validas"  # row 1 controls; row 2 headers
MULTIPLE_SEPARATOR  = ";"
TOP_N               = 10

os.makedirs(CHARTS_DIR, exist_ok=True)

# Colors
PIE_COLORS = ["#1E325A", "#710101", "#051C48", "#141E34"]
BAR_COLOR  = "#1E325A"

# =============== Helpers ===============
def sanitize_sheet_name(name, existing):
    """Valid, unique Excel sheet name (<=31 chars, no []:*?/\\)."""
    clean = re.sub(r'[\[\]\:\*\?\/\\]', "_", str(name))[:31] or "Sheet"
    base = clean
    i = 1
    while clean in existing:
        tail = f"_{i}"
        clean = (base[:(31 - len(tail))] + tail) if len(base) + len(tail) > 31 else base + tail
        i += 1
    return clean

def sanitize_filename(s, max_len=140):
    """Safe filename for saving charts."""
    s = str(s)
    s = re.sub(r'[^\w\-\.\(\) ]+', '_', s)   # keep letters/digits/._-()
    s = re.sub(r'\s+', '_', s).strip('_')
    return s[:max_len] if len(s) > max_len else s

def colnum_to_excel(n: int) -> str:
    """Convert 0-based column index to Excel letters (A, B, ..., AA...)."""
    string = ""
    n += 1
    while n > 0:
        n, r = divmod(n - 1, 26)
        string = chr(65 + r) + string
    return string

def clean_single(series: pd.Series) -> pd.Series:
    """Single-choice: strip, drop NaN/empty/whitespace-only."""
    s = series.apply(
        lambda x: None
        if (pd.isna(x) or (isinstance(x, str) and x.strip() == ""))
        else (x.strip() if isinstance(x, str) else x)
    )
    return s.dropna()

def expand_multiple(series: pd.Series, sep=MULTIPLE_SEPARATOR) -> pd.Series:
    """Multi-choice: split by sep, strip, drop empties, flatten selections."""
    def split_cell(x):
        if pd.isna(x):
            return []
        if isinstance(x, str):
            parts = [p.strip() for p in x.split(sep)]
            return [p for p in parts if p != ""]
        return [x]
    exploded = series.apply(split_cell).explode()
    exploded = exploded[exploded.notna()]
    return exploded

def cap_top_n_with_outros(counts: pd.Series, n: int = TOP_N, outros_label: str = "Outros") -> pd.Series:
    """Keep top n; sum the rest into 'Outros'."""
    counts = counts.sort_values(ascending=False)
    if len(counts) <= n:
        return counts
    top = counts.iloc[:n]
    outros_sum = counts.iloc[n:].sum()
    if outros_sum > 0:
        top.loc[outros_label] = top.get(outros_label, 0) + outros_sum
    return top

def to_percentages(counts: pd.Series) -> pd.Series:
    """Counts -> % (0–100, rounded 2), sorted desc."""
    total = counts.sum()
    if total == 0:
        return pd.Series(dtype=float)
    return (counts / total * 100).round(2).sort_values(ascending=False)

def save_pie_jpg(values_pct: pd.Series, outfile: str):
    """Pie with fixed colors (up to 4 categories), no title."""
    if len(values_pct) == 0:
        return
    
    fracs = (values_pct / 100.0).values
    labels = [f"{idx} ({val:.1f}%)" for idx, val in values_pct.items()]
    colors = PIE_COLORS[:len(values_pct)]

    # Fixed figure size for consistent width and height
    fig, ax = plt.subplots(figsize=(9,9))

    # Draw pie chart with label formatting
    wedges, texts = ax.pie(
        fracs,
        labels=labels,
        startangle=90,
        colors=colors,
        textprops={'fontsize': 10},
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
    )

    # Ensure pie is centered
    ax.axis('equal')
    plt.subplots_adjust(left=0.20, right=0.80, top=0.80, bottom=0.20)
    plt.savefig(outfile, format="jpg", dpi=200)
    plt.close()

def wrap_labels(labels, wrap_width=50, max_chars=150):
    wrapped = []
    for label in labels:
        label = str(label)  # ensure string
        
        # Truncate if label exceeds max_chars
        if len(label) > max_chars:
            label = label[:max_chars].rstrip() + "..."
        
        # Wrap the label text
        wrapped.append('\n'.join(textwrap.wrap(label, wrap_width)))
    return wrapped

def save_bar_jpg(values_pct: pd.Series, outfile: str):
    """Horizontal bar chart, no title; 'Outros' rendered at the bottom; minimal frame."""
    if len(values_pct) == 0:
        return

    # Move 'Outros' to end, then reverse so it renders bottom in barh
    if "Outros" in values_pct.index:
        outros_val = values_pct["Outros"]
        values_pct = pd.concat([values_pct.drop("Outros"), pd.Series({"Outros": outros_val})])
    values_pct = values_pct[::-1]  # first rendered at top -> reverse so 'Outros' ends bottom

    labels = list(values_pct.index)
    vals   = list(values_pct.values)

    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    bars = ax.barh(range(len(vals)), vals, color=BAR_COLOR)

    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(wrap_labels(labels), fontsize=10)
    ax.set_xlabel("Porcentagem (%)")

    # Remove top/right/left borders
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    # Add % labels at end of bars
    for rect, v in zip(bars, vals):
        ax.text(rect.get_width() + 0.5,
                rect.get_y() + rect.get_height()/2,
                f"{v:.1f}%", va="center", fontsize=9)

    #plt.tight_layout()
    # left=0.3: Sets the left margin to 50% of the figure width. This gives more space for long y-axis labels.
    # right=0.95: Sets the right margin to 95% of the figure width, leaving a small space on the right.
    # top=0.95: Sets the top margin to 95% of the figure height.
    # bottom=0.05: Sets the bottom margin to 10% of the figure height.
    plt.subplots_adjust(left=0.35, right=0.95, top=0.95, bottom=0.1)
    plt.savefig(outfile, format="jpg", dpi=200)
    plt.close()

def summarize_df_to_excel_and_charts(df: pd.DataFrame, writer, workbook, sheet_label: str,
                                     control_map: dict):
    """
    Write one summary sheet for the provided df (overall or per group),
    save charts to disk using <sheet_label>_column<Letter>.jpg.
    """
    title_fmt   = workbook.add_format({"bold": True})
    percent_fmt = workbook.add_format({"num_format": "0.00%"})
    header_fmt  = workbook.add_format({"bold": True})
    note_fmt    = workbook.add_format({"italic": True, "font_color": "#666666"})

    # Sheet name is just the group label (e.g., 'geral', 'UERN', ...)
    ws_name = sanitize_sheet_name(sheet_label, set(writer.sheets.keys()))
    ws = workbook.add_worksheet(ws_name)
    writer.sheets[ws_name] = ws

    row = 0
    ws.write(row, 0, "Question / Answer", header_fmt)
    ws.write(row, 1, "Percentage", header_fmt)
    row += 1

    for col in df.columns:
        ctrl_kw = control_map.get(col, "FECHADA")
        if ctrl_kw in ("IGNORAR", "ABERTA"):
            continue

        ws.write(row, 0, f"Question: {col}", title_fmt)
        row += 1

        if ctrl_kw == "FECHADA":
            s = clean_single(df[col])
            if len(s) == 0:
                ws.write(row, 0, "(no valid responses — all blank/NA)", note_fmt)
                row += 2
                continue
            counts = s.value_counts()

        elif ctrl_kw == "MÚLTIPLA":
            expanded = expand_multiple(df[col], sep=MULTIPLE_SEPARATOR)
            if len(expanded) == 0:
                ws.write(row, 0, "(no valid selections — all blank/NA)", note_fmt)
                row += 2
                continue
            counts = expanded.value_counts()

        else:
            s = clean_single(df[col])
            if len(s) == 0:
                ws.write(row, 0, "(no valid responses — all blank/NA)", note_fmt)
                row += 2
                continue
            counts = s.value_counts()

        # Top N + Outros, then to percentages
        counts_capped = cap_top_n_with_outros(counts, n=TOP_N, outros_label="Outros")
        pct = to_percentages(counts_capped)

        # In Excel, keep descending order but place 'Outros' last if present
        if "Outros" in pct.index:
            outros_val = pct["Outros"]
            pct_excel = pct.drop("Outros")
            pct_excel = pd.concat([pct_excel, pd.Series({"Outros": outros_val})])
        else:
            pct_excel = pct

        # Write to Excel (as real % values)
        for answer, p in pct_excel.items():
            ws.write(row, 0, str(answer))
            ws.write_number(row, 1, float(p) / 100.0, percent_fmt)
            row += 1

        # Save chart (pie if ≤4, else horizontal bar) with file name <sheet>_column<Letter>.jpg
        col_letter = colnum_to_excel(df.columns.get_loc(col))
        base_name  = sanitize_filename(sheet_label, max_len=50)
        chart_path = os.path.join(CHARTS_DIR, f"{base_name}_column{col_letter}.jpg")

        if len(pct) <= 4:
            save_pie_jpg(pct, chart_path)
        else:
            save_bar_jpg(pct, chart_path)

        row += 1

    ws.set_column(0, 0, 50)
    ws.set_column(1, 1, 12)

# =============== Load workbook & control map from respostas_validas ===============
xls = pd.ExcelFile(INPUT_XLSX)
if CONTROL_SHEET_NAME not in xls.sheet_names:
    raise ValueError(f"Sheet '{CONTROL_SHEET_NAME}' not found in workbook.")

# Control row (row 1) + headers (row 2)
ctrl_row = pd.read_excel(INPUT_XLSX, sheet_name=CONTROL_SHEET_NAME, header=None, nrows=1)
headers_df = pd.read_excel(INPUT_XLSX, sheet_name=CONTROL_SHEET_NAME, header=1, nrows=0)
control_headers = list(headers_df.columns)

# Column -> keyword map (default FECHADA)
control_map = {}
for i, col_name in enumerate(control_headers):
    kw = ctrl_row.iloc[0, i] if i < ctrl_row.shape[1] else None
    if pd.isna(kw):
        kw = "FECHADA"
    control_map[col_name] = str(kw).strip().upper()

# Full data with real headers (row 2)
df_full = pd.read_excel(INPUT_XLSX, sheet_name=CONTROL_SHEET_NAME, header=1)

# =============== Configurable output mode ===============
# Default: only geral (overall). 
# If you set GROUP_BY_COL_INDEX = 3 (or any valid index), it will also create per-group outputs.
GROUP_BY_COL_INDEX = None   # <- set to None for geral only; or integer for per-group

# =============== Build output (Overall 'geral' + optional Per-Group) ===============
with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
    workbook = writer.book

    # Always produce geral
    summarize_df_to_excel_and_charts(
        df=df_full,
        writer=writer,
        workbook=workbook,
        sheet_label="geral",
        control_map=control_map
    )

    # Only produce per-group if GROUP_BY_COL_INDEX is set
    if GROUP_BY_COL_INDEX is not None:
        if GROUP_BY_COL_INDEX >= len(df_full.columns):
            raise IndexError(
                f"GROUP_BY_COL_INDEX {GROUP_BY_COL_INDEX} out of range for sheet '{CONTROL_SHEET_NAME}'"
            )

        group_col_name = df_full.columns[GROUP_BY_COL_INDEX]

        # Drop NA/blank groups
        groups_df = df_full.copy()
        if groups_df[group_col_name].dtype == object:
            groups_df[group_col_name] = groups_df[group_col_name].astype(str).str.strip()
        groups_df = groups_df[groups_df[group_col_name].notna()]
        groups_df = groups_df[groups_df[group_col_name] != ""]

        unique_groups = groups_df[group_col_name].unique().tolist()

        for g in unique_groups:
            df_g = groups_df[groups_df[group_col_name] == g]
            group_label = str(g).strip() or "Unknown"  # sheet + filename base
            summarize_df_to_excel_and_charts(
                df=df_g,
                writer=writer,
                workbook=workbook,
                sheet_label=group_label,
                control_map=control_map
            )

print(f"Done! Saved Excel to {OUTPUT_XLSX} and charts to '{CHARTS_DIR}/'.")
