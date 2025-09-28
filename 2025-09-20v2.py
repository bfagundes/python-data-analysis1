import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# --- Settings ---
INPUT_XLSX  = "./files/2025-09-20 v3.xlsx"   # <- change to your file
OUTPUT_XLSX  = "survey_analysis_multi.xlsx"
CHARTS_DIR   = "charts"  # where JPGs will be saved
os.makedirs(CHARTS_DIR, exist_ok=True)

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

def clean_series(series):
    """
    Strip strings; convert NaN/empty/whitespace-only to NaN (to be dropped).
    Result: only real answers remain.
    """
    return series.apply(
        lambda x: pd.NA
        if (pd.isna(x) or (isinstance(x, str) and x.strip() == ""))
        else (x.strip() if isinstance(x, str) else x)
    )

def save_pie_jpg(values_pct, outfile):
    """
    values_pct: Series with percentages (0–100) indexed by answer string.
    outfile: path to save .jpg (no title).
    """
    fracs = (values_pct / 100.0).values
    labels = [f"{idx} ({val:.1f}%)" for idx, val in values_pct.items()]

    plt.figure(figsize=(7, 7))
    plt.pie(fracs, labels=labels, startangle=90)
    plt.axis('equal')  # keep circular
    plt.savefig(outfile, format="jpg", dpi=200, bbox_inches="tight")
    plt.close()

# Discover sheet names
xls = pd.ExcelFile(INPUT_XLSX)
sheet_names = xls.sheet_names

with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
    workbook = writer.book
    title_fmt   = workbook.add_format({"bold": True})
    percent_fmt = workbook.add_format({"num_format": "0.00%"})
    header_fmt  = workbook.add_format({"bold": True})
    note_fmt    = workbook.add_format({"italic": True, "font_color": "#666666"})

    used_sheetnames = set()

    for raw_name in sheet_names:
        df = pd.read_excel(INPUT_XLSX, sheet_name=raw_name)

        # Worksheet per input sheet
        ws_name = sanitize_sheet_name(f"Summary_{raw_name}", used_sheetnames)
        used_sheetnames.add(ws_name)
        ws = workbook.add_worksheet(ws_name)
        writer.sheets[ws_name] = ws

        # Header
        row = 0
        ws.write(row, 0, "Question / Answer", header_fmt)
        ws.write(row, 1, "Percentage", header_fmt)
        row += 1

        # For each column (question)
        for col in df.columns:
            ws.write(row, 0, f"Question: {col}", title_fmt)
            row += 1

            # Clean data and drop empties entirely
            s = clean_series(df[col]).dropna()

            if len(s) == 0:
                # No valid answers — note it in Excel; skip chart
                ws.write(row, 0, "(no valid responses — all blank/NA)", note_fmt)
                row += 2
                continue

            # Percentages (0–100) excluding empties
            percentages = (s.value_counts(normalize=True) * 100).round(2).sort_values(ascending=False)

            # Write answers + percentages (as real % values)
            for answer, pct in percentages.items():
                ws.write(row, 0, str(answer))
                ws.write_number(row, 1, float(pct) / 100.0, percent_fmt)
                row += 1

            # Save pie chart without title, excluding empties
            safe_sheet = sanitize_filename(raw_name, max_len=50)
            safe_col   = sanitize_filename(col, max_len=70)
            chart_path = os.path.join(CHARTS_DIR, f"{safe_sheet}_{safe_col}.jpg")
            save_pie_jpg(percentages, chart_path)

            # Spacer line
            row += 1

        # Column widths
        ws.set_column(0, 0, 50)
        ws.set_column(1, 1, 12)

print(f"Done! Saved Excel to {OUTPUT_XLSX} and charts to '{CHARTS_DIR}/'.")
