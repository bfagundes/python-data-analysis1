import pandas as pd
import csv
from question import Question
#import matplotlib.pyplot as plt

# Set up header with two lines, 0 = column title, 1 = flag (ignore, open_question, fixed_question)
df = pd.read_csv('Cuestionario_UTPJ.csv', sep=";", header=[0,1])
print(f"The file has {df.shape} rows x columns")

total_columns = len(df.columns)
total_rows = len(df.index)
question_list = []

for column in range (total_columns):
    # if header 2nd line is ignore or open_question SKIP
    if df.columns[column][1] in ("ignore"):
        continue

    # Retrieve all unique answers on the column
    unique_answers = df.iloc[:, column].unique()
    
    # Loop through each unique answer
    q = Question()
    for answer in unique_answers:
        # Update the object data
        q.question = df.columns[column][0]
        q.answers[answer] = df.iloc[:, column].value_counts(normalize=False, dropna=False)[answer]
        q.num_answers += df.iloc[:, column].value_counts(normalize=False, dropna=False)[answer]

    # Add the Question object to a list
    question_list.append(q)

    # Print the object - For troubleshooting purposes
    print(q)

    # Write a CSV file with the questions and answers data
    with open('output.csv', mode='w', encoding='utf-8', newline='') as output_csv_file:
        output_writer = csv.writer(output_csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Looping through each of the questions
        for question in question_list:
            output_writer.writerow([question.question])

            # Looping through each of the answers 
            for answer in question.answers:
                output_writer.writerow([answer, question.answers[answer], question.answers[answer]/question.num_answers])
        
        # This doesnt work
        output_writer.writerow("\n")