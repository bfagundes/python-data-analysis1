# This is the main file that runs everything. It reads a spreadsheet, looks at answers,
# makes pretty charts, and saves everything in a new Excel file.

import os  
import shutil
import pandas as pd
from config import INPUT_XLSX, OUTPUT_XLSX, CONTROL_SHEET_NAME, GROUP_BY_COL_INDEX, QTYPE_CLOSED, GENERAL_LABEL, LLM_FEATURES_ON, OUTPUT_DIR
from summarizer import summarize_df_to_excel_and_charts

# Make a folder called "charts" to save our pictures (if it doesn't exist yet)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Clean up any old charts before saving new ones
for filename in os.listdir(OUTPUT_DIR):
    file_path = os.path.join(OUTPUT_DIR, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path) #Remove file or symlink
    except Exception as e:
        print(f"Failed to delete {file_path}. Reason: {e}")

# Open the Excel file that has all the answers
xls = pd.ExcelFile(INPUT_XLSX)

# If the sheet with answers isn't there, stop and shout!
if CONTROL_SHEET_NAME not in xls.sheet_names:
    raise ValueError(f"Sheet '{CONTROL_SHEET_NAME}' not found in workbook.")

# Read the first row (row 1) to see what kind of question each column is
ctrl_row = pd.read_excel(INPUT_XLSX, sheet_name=CONTROL_SHEET_NAME, header=None, nrows=1)

# Read the second row (row 2) to get the column names
headers_df = pd.read_excel(INPUT_XLSX, sheet_name=CONTROL_SHEET_NAME, header=1, nrows=0)
control_headers = list(headers_df.columns)

# Make a map that says: "This column is this kind of question"
control_map = {}
for i, col_name in enumerate(control_headers):
    
    # Get the keyword from the control row (like FECHADA or MULTIPLA)
    kw = ctrl_row.iloc[0, i] if i < ctrl_row.shape[1] else None
    
    # If it's empty, we say it's a closed question (FECHADA)
    if pd.isna(kw):
        kw = QTYPE_CLOSED
    
    # Save the keyword in our map
    control_map[col_name] = str(kw).strip().upper()

# Now read all the real answers from the sheet (starting from row 2)
df_full = pd.read_excel(INPUT_XLSX, sheet_name=CONTROL_SHEET_NAME, header=1)

# We open a new Excel file to write our results
with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
    workbook = writer.book

    # First, we make a summary for everyone together (called "geral")
    summarize_df_to_excel_and_charts(
        df=df_full,
        writer=writer,
        workbook=workbook,
        sheet_label=GENERAL_LABEL,
        control_map=control_map
    )

    # If we want to split by groups (like schools or cities), we do that here
    if GROUP_BY_COL_INDEX is not None:
        
        # Make sure the group column index is not too big
        if GROUP_BY_COL_INDEX >= len(df_full.columns):
            raise IndexError(f"GROUP_BY_COL_INDEX {GROUP_BY_COL_INDEX} out of range for sheet '{CONTROL_SHEET_NAME}'")

        # Get the name of the column we want to group by
        group_col_name = df_full.columns[GROUP_BY_COL_INDEX]

        # Clean up the group names (remove spaces and empty ones)
        groups_df = df_full.copy()
        if groups_df[group_col_name].dtype == object:
            groups_df[group_col_name] = groups_df[group_col_name].astype(str).str.strip()
        groups_df = groups_df[groups_df[group_col_name].notna()]
        groups_df = groups_df[groups_df[group_col_name] != ""]

        # Get a list of all the different groups
        unique_groups = groups_df[group_col_name].unique().tolist()

        # For each group, make a separate summary and chart
        for g in unique_groups:
            df_g = groups_df[groups_df[group_col_name] == g]
            group_label = str(g).strip() or "Unknown"
            summarize_df_to_excel_and_charts(
                df=df_g,
                writer=writer,
                workbook=workbook,
                sheet_label=group_label,
                control_map=control_map
            )

# Use LLM to generate a report based on the questions
if LLM_FEATURES_ON:
    try:
        from generate_report import generate_diagnosis_report
        generate_diagnosis_report()
    
    except Exception as e:
        print(f"Failed to generate report: {e}")

else:
    print("Skipping LLM report generation (RUN_REPORT_GENERATION=False).")

# Formatting the filename for the ZIP file
print("Packaging charts and reports into ZIP...")
base_name = os.path.splitext(os.path.basename(INPUT_XLSX))[0]
zip_path = os.path.join(OUTPUT_DIR, f"{base_name}.zip")

# Remove any existing zip file
if os.path.exists(zip_path):
    os.remove(zip_path)

# Create a ZIP file with all charts
shutil.make_archive(zip_path.replace(".zip", ""), 'zip', OUTPUT_DIR)

# Tell the user where we saved the zip file
print(f"Done! Saved Excel to {OUTPUT_XLSX}, charts to '{OUTPUT_DIR}/', and zip to {zip_path}")