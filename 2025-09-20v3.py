import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# =============== Settings ===============
INPUT_XLSX  = "./files/2025-09-20 v3.xlsx"   # <- change to your file
OUTPUT_XLSX         = "survey_analysis_multi.xlsx"
CHARTS_DIR          = "charts"   # folder to save JPGs
CONTROL_SHEET_NAME  = "respostas_validas"  # sheet with control keywords in row 1
MULTIPLE_SEPARATOR  = ";"        # for MÚLTIPLA columns
os.makedirs(CHARTS_DIR, exist_ok=True)

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
    """Convert 0-based column index to Excel-style letters (A, B, ..., AA, AB, ...)."""
    string = ""
    n += 1  # 1-based
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
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
    """
    Multiple-choice: split by sep, strip parts, drop empties, flatten to a 1D Series of selections.
    """
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

def to_percentages(counts: pd.Series) -> pd.Series:
    """Convert counts to percentages (0–100, rounded 2), sorted desc."""
    total = counts.sum()
    if total == 0:
        return pd.Series(dtype=float)
    return (counts / total * 100).round(2).sort_values(ascending=False)

def save_pie_jpg(values_pct: pd.Series, outfile: str):
    """Save a pie chart without a title. values_pct are percentages (0–100) by answer."""
    if len(values_pct) == 0:
        return
    fracs = (values_pct / 100.0).values
    labels = [f"{idx} ({val:.1f}%)" for idx, val in values_pct.items()]

    plt.figure(figsize=(7, 7))
    plt.pie(fracs, labels=labels, startangle=90)
    plt.axis('equal')  # keep circular
    plt.savefig(outfile, format="jpg", dpi=200, bbox_inches="tight")
    plt.close()

# =============== Load workbook & control map ===============
xls = pd.ExcelFile(INPUT_XLSX)
sheet_names = xls.sheet_names

# Pick control sheet (prefer explicit name, fallback to first sheet)
control_sheet = CONTROL_SHEET_NAME if CONTROL_SHEET_NAME in sheet_names else sheet_names[0]

# Read control row (row 1) and headers (row 2) from control sheet
ctrl_row = pd.read_excel(INPUT_XLSX, sheet_name=control_sheet, header=None, nrows=1)
headers_df = pd.read_excel(INPUT_XLSX, sheet_name=control_sheet, header=1, nrows=0)
control_headers = list(headers_df.columns)

# Build column -> keyword map; default to FECHADA when missing/NaN
control_map = {}
for i, col_name in enumerate(control_headers):
    kw = ctrl_row.iloc[0, i] if i < ctrl_row.shape[1] else None
    if pd.isna(kw):
        kw = "FECHADA"
    control_map[col_name] = str(kw).strip().upper()

# =============== Build output workbook & charts ===============
with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
    workbook = writer.book
    title_fmt   = workbook.add_format({"bold": True})
    percent_fmt = workbook.add_format({"num_format": "0.00%"})
    header_fmt  = workbook.add_format({"bold": True})
    note_fmt    = workbook.add_format({"italic": True, "font_color": "#666666"})

    used_sheetnames = set()

    for raw_name in sheet_names:
        # Read each sheet:
        # - control sheet: data headers start on row 2 (header=1), row 1 holds control keywords
        # - other sheets: standard headers (header=0)
        if raw_name == control_sheet:
            df = pd.read_excel(INPUT_XLSX, sheet_name=raw_name, header=1)
        else:
            df = pd.read_excel(INPUT_XLSX, sheet_name=raw_name, header=0)

        # Prepare summary worksheet for this sheet
        ws_name = sanitize_sheet_name(f"Summary_{raw_name}", used_sheetnames)
        used_sheetnames.add(ws_name)
        ws = workbook.add_worksheet(ws_name)
        writer.sheets[ws_name] = ws

        # Header
        row = 0
        ws.write(row, 0, "Question / Answer", header_fmt)
        ws.write(row, 1, "Percentage", header_fmt)
        row += 1

        # Loop columns/questions
        for col in df.columns:
            ctrl_kw = control_map.get(col, "FECHADA")

            if ctrl_kw in ("IGNORAR", "ABERTA"):
                # Skip entirely
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
                # Unknown keyword => treat as FECHADA
                s = clean_single(df[col])
                if len(s) == 0:
                    ws.write(row, 0, "(no valid responses — all blank/NA)", note_fmt)
                    row += 2
                    continue
                counts = s.value_counts()

            pct = to_percentages(counts)

            # Write answers + percentages (as real % values)
            for answer, p in pct.items():
                ws.write(row, 0, str(answer))
                ws.write_number(row, 1, float(p) / 100.0, percent_fmt)
                row += 1

            # Save pie (no title) with column letter in filename
            safe_sheet = sanitize_filename(raw_name, max_len=50)
            col_letter = colnum_to_excel(df.columns.get_loc(col))  # e.g., A, B, C...
            chart_path = os.path.join(CHARTS_DIR, f"{safe_sheet}_column{col_letter}.jpg")
            save_pie_jpg(pct, chart_path)

            # Spacer
            row += 1

        # Column widths
        ws.set_column(0, 0, 50)
        ws.set_column(1, 1, 12)

print(f"Done! Saved Excel to {OUTPUT_XLSX} and charts to '{CHARTS_DIR}/'.")
