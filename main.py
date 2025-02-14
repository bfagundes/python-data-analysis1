import pandas as pd
#import matplotlib.pyplot as plt

# Set up header with two lines, 0 = column title, 1 = flag (ignore, open_question, fixed_question)
df = pd.read_csv('Cuestionario_UTPJ.csv', sep=";", header=[0,1])
print(f"The file has {df.shape} rows x columns")

total_columns = len(df.columns)
total_rows = len(df.index)

for column in range (total_columns):
    # if header 2nd line is ignore or open_question SKIP
    if df.columns[column][1] in ("ignore"):
        continue

    else:
        count = df.iloc[:, column].value_counts(normalize=True, dropna=False)
        print(f"{count}\n")
