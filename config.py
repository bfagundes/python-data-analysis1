# This file is like our instruction sheet.

# This is the path to the Excel file we want to read.
INPUT_XLSX = "./files/[UPF] Questionários para Professores e Pesquisadores(1-254).xlsx"

# This is where we want to save our new Excel file with the results.
OUTPUT_XLSX = "./output/analysis.xlsx"

# This is the folder where we’ll save all the pretty chart pictures.
# We'll also save the reports and other files we generated throughout the execution.
OUTPUT_DIR = "output"

# This is the name of the sheet inside the Excel file that has the answers.
CONTROL_SHEET_NAME = "respostas_validas"

# This is the symbol we use to split multiple answers in one cell.
MULTIPLE_SEPARATOR = ";"

# This is how many top answers we want to show before grouping the rest as "Outros".
TOP_N = 10

# If we want to split results by groups (like schools), we put the column number here.
# If we don’t want to split, we leave it as None.
# e.g Column A = 0, B = 1, etc.
GROUP_BY_COL_INDEX = None

# These are the colors we use for pie charts. In order, descending.
PIE_COLORS = ["#1E325A", "#710101", "#051C48", "#141E34"]

# This is the color we use for bar charts.
BAR_COLOR = "#1E325A"

# Question type keywords used in the control row
QTYPE_CLOSED = "FECHADA"    # Closed question
QTYPE_MULTIPLE = "MÚLTIPLA"  # Multiple choice question
QTYPE_OPEN = "ABERTA"      # Open-ended question
QTYPE_IGNORE = "IGNORAR"    # Ignore this column

# Label used for grouping less frequent answers
OTHERS_LABEL = "Outros"
GENERAL_LABEL = "Geral"

# Flag to activate - or not - the LLM features
LLM_FEATURES_ON = False