# This file is the brain that takes answers from a spreadsheet,
# counts them, makes charts, and writes everything into a new Excel file.

import os
import pandas as pd
from config import CHARTS_DIR, TOP_N, MULTIPLE_SEPARATOR
from config import QTYPE_CLOSED, QTYPE_MULTIPLE, QTYPE_OPEN, QTYPE_IGNORE, OTHERS_LABEL
from helpers import sanitize_sheet_name, sanitize_filename, colnum_to_excel
from data_cleaning import clean_single, expand_multiple, cap_top_n_with_outros, to_percentages
from chart_utils import save_pie_jpg, save_bar_jpg

# This function makes one summary sheet and saves charts for each question
def summarize_df_to_excel_and_charts(df: pd.DataFrame, writer, workbook, sheet_label: str, control_map: dict):
    
    # Set up styles for Excel cells
    title_fmt   = workbook.add_format({"bold": True})  # Bold for question titles
    percent_fmt = workbook.add_format({"num_format": "0.00%"})  # Format for percentages
    header_fmt  = workbook.add_format({"bold": True})  # Bold for headers
    note_fmt    = workbook.add_format({"italic": True, "font_color": "#666666"})  # Gray italic for notes

    # Make a clean sheet name that doesn’t break Excel rules
    ws_name = sanitize_sheet_name(sheet_label, set(writer.sheets.keys()))

    # Create a new sheet in the Excel file
    ws = workbook.add_worksheet(ws_name)
    writer.sheets[ws_name] = ws

    # Write the header row
    row = 0
    ws.write(row, 0, "Question / Answer", header_fmt)
    ws.write(row, 1, "Percentage", header_fmt)
    row += 1

    # Go through each column (question) in the data
    for col in df.columns:
        ctrl_kw = control_map.get(col, QTYPE_CLOSED)

        # Skip if the question is open or marked to ignore
        if ctrl_kw in (QTYPE_IGNORE, QTYPE_OPEN):
            continue

        # Write the question title
        ws.write(row, 0, f"Question: {col}", title_fmt)
        row += 1

        # Clean and count answers based on question type
        if ctrl_kw == QTYPE_CLOSED:
            s = clean_single(df[col])
            if len(s) == 0:
                ws.write(row, 0, "(no valid responses — all blank/NA)", note_fmt)
                row += 2
                continue
            counts = s.value_counts()

        elif ctrl_kw == QTYPE_MULTIPLE:
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

        # Keep only the top answers and group the rest as "Outros"
        counts_capped = cap_top_n_with_outros(counts, n=TOP_N, outros_label=OTHERS_LABEL)

        # Turn counts into percentages
        pct = to_percentages(counts_capped)

        # Move "Outros" to the bottom of the list
        if OTHERS_LABEL in pct.index:
            outros_val = pct[OTHERS_LABEL]
            pct_excel = pct.drop(OTHERS_LABEL)
            pct_excel = pd.concat([pct_excel, pd.Series({OTHERS_LABEL: outros_val})])
        else:
            pct_excel = pct

        # Write each answer and its percentage to the Excel sheet
        for answer, p in pct_excel.items():
            ws.write(row, 0, str(answer))
            ws.write_number(row, 1, float(p) / 100.0, percent_fmt)
            row += 1

        # Save a chart for this question
        col_letter = colnum_to_excel(df.columns.get_loc(col))  # Get column letter like A, B, C...
        base_name  = sanitize_filename(sheet_label, max_len=50)  # Clean up the sheet name for the file
        chart_path = os.path.join(CHARTS_DIR, f"{base_name}_column{col_letter}.jpg")

        # If there are 4 or fewer answers, make a pie chart
        if len(pct) <= 4:
            save_pie_jpg(pct, chart_path)
        else:
            save_bar_jpg(pct, chart_path)

        row += 1  # Leave a space before the next question

    # Make columns wide enough to read nicely
    ws.set_column(0, 0, 50)
    ws.set_column(1, 1, 12)