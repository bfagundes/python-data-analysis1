import pandas as pd

# --- Settings ---
INPUT_XLSX  = './files/2025-09-20-direcao-previa.xlsx'
OUTPUT_XLSX = "survey_analysis.xlsx"

# Read Excel
df = pd.read_excel(INPUT_XLSX)

# Create writer with xlsxwriter for nice formatting
with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
    # Add a worksheet
    workbook  = writer.book
    worksheet = workbook.add_worksheet("Summary")
    writer.sheets["Summary"] = worksheet

    # Formats
    title_fmt    = workbook.add_format({"bold": True})
    percent_fmt  = workbook.add_format({"num_format": "0.00%"})
    answer_fmt   = workbook.add_format({})
    header_fmt   = workbook.add_format({"bold": True})
    spacer_rows  = 1  # blank rows between questions

    row = 0
    # Optional sheet header
    worksheet.write(row, 0, "Question / Answer", header_fmt)
    worksheet.write(row, 1, "Percentage", header_fmt)
    row += 1

    for col in df.columns:
        # Write the question title
        worksheet.write(row, 0, f"Question: {col}", title_fmt)
        row += 1

        # Clean values: treat NaN or whitespace-only as "Empty"
        s = df[col].apply(
            lambda x: "Empty"
            if (pd.isna(x) or (isinstance(x, str) and x.strip() == ""))
            else (x.strip() if isinstance(x, str) else x)
        )

        # Percentages
        percentages = (s.value_counts(dropna=False, normalize=True) * 100).round(2)

        # (Optional) sort by percentage descending
        percentages = percentages.sort_values(ascending=False)

        # Write each answer + percentage
        for answer, pct in percentages.items():
            worksheet.write(row, 0, str(answer), answer_fmt)
            worksheet.write_number(row, 1, pct / 100.0, percent_fmt)  # write as real %
            row += 1

        # Spacer line
        row += spacer_rows

    # Autofit-ish: set reasonable column widths
    worksheet.set_column(0, 0, 50)  # Question/Answer column
    worksheet.set_column(1, 1, 12)  # Percentage column

print(f"Done! Saved to {OUTPUT_XLSX}")