import pandas as pd
import csv
from question import Question

# Variables
input_file = 'Cuestionario para Comunidad Alumni UTPL_final.csv'
output_file = 'output.csv'

# Set up header with two lines, 0 = column title, 1 = flag (ignore, open_question, fixed_question)
df = pd.read_csv(input_file, sep=";", header=[0,1])
print(f"The file has {df.shape} (rows x columns)")

total_columns = len(df.columns)
total_rows = len(df.index)
question_list = []

for column in range (total_columns):
    # if header 2nd line is ignore or open_question SKIP
    if df.columns[column][1] in ("ignore"):
        continue

    # Retrieve all unique answers on the column | .dropna() removes the NaN values
    unique_answers = df.iloc[:, column].dropna().unique()
    #print(unique_answers)
    
    # Loop through each unique answer
    q = Question()
    q.question = df.columns[column][0]

    for answer in unique_answers:
        # Update the object data

        answers_normalized = df.iloc[:, column].value_counts(normalize=True, dropna=True)[answer]
        answers_count = df.iloc[:, column].value_counts(normalize=False, dropna=True)[answer]

        q.answers[answer] = answers_normalized
        q.num_answers += answers_count
            
    # Add the Question object to a list
    question_list.append(q)

# Write a CSV file with the questions and answers data
with open(output_file, mode='w', encoding='ansi', errors='ignore', newline='') as output_csv_file:
    output_writer = csv.writer(output_csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Looping through each of the questions
    for question in question_list:
        output_writer.writerow([question.question])

        # Sorting answers
        sorted_answers = dict(sorted(question.answers.items(), key=lambda item: item[1], reverse=True))

        # Looping through each of the answers 
        for answer in sorted_answers:
            output_writer.writerow([answer, question.answers[answer], question.answers[answer] * question.num_answers])

print(f"Process completed successfully.")