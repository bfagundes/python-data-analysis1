import re
import pandas as pd

# --- Settings ---
INPUT_XLSX  = "./files/2025-09-20.xlsx"   # <- change to your file
OUTPUT_XLSX = "survey_analysis_multi.xlsx"

def sanitize_sheet_name(name, existing):
    """Make a valid, unique Excel sheet name (<=31 chars, no []:*?/\\)."""
    clean = re.sub(r'[\[\]\:\*\?\/\\]', "_", str(name))[:31] or "Sheet"
    base = clean
    i = 1
    while clean in existing:
        tail = f"_{i}"
        clean = (base[:(31 - len(tail))] + tail) if len(base) + len(tail) > 31 else base + tail
        i += 1
    return clean

# Discover sheet names
xls = pd.ExcelFile(INPUT_XLSX)
sheet_names = xls.sheet_names

with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
    workbook = writer.book
    # Common formats
    title_fmt   = workbook.add_format({"bold": True})
    percent_fmt = workbook.add_format({"num_format": "0.00%"})
    header_fmt  = workbook.add_format({"bold": True})

    used_sheetnames = set()

    for raw_name in sheet_names:
        # Read this sheet
        df = pd.read_excel(INPUT_XLSX, sheet_name=raw_name)

        # Prepare a worksheet for this sheet's summary
        ws_name = sanitize_sheet_name(f"Summary_{raw_name}", used_sheetnames)
        used_sheetnames.add(ws_name)
        worksheet = workbook.add_worksheet(ws_name)
        writer.sheets[ws_name] = worksheet

        # Header
        row = 0
        worksheet.write(row, 0, "Question / Answer", header_fmt)
        worksheet.write(row, 1, "Percentage", header_fmt)
        row += 1

        # For each column (question)
        for col in df.columns:
            # Question title
            worksheet.write(row, 0, f"Question: {col}", title_fmt)
            row += 1

            # Treat NaN/whitespace as "Empty"
            s = df[col].apply(
                lambda x: "Empty"
                if (pd.isna(x) or (isinstance(x, str) and x.strip() == ""))
                else (x.strip() if isinstance(x, str) else x)
            )

            # Percentages (as real % values)
            percentages = (s.value_counts(dropna=False, normalize=True)).sort_values(ascending=False)

            # Write answers + percentages
            for answer, pct in percentages.items():
                worksheet.write(row, 0, str(answer))
                worksheet.write_number(row, 1, float(pct), percent_fmt)
                row += 1

            # Spacer line
            row += 1

        # Column widths
        worksheet.set_column(0, 0, 50)
        worksheet.set_column(1, 1, 12)

print(f"Done! Saved to {OUTPUT_XLSX}")
