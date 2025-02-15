import pandas as pd
import csv
from question import Question

# Variables
input_file = 'input.csv'
output_file = 'output.csv'
max_answers_per_question = 10
max_answers_spill_label = "Otros"

# Load CSV with a multi-line header (first line = column title, second line = flag)
df = pd.read_csv(input_file, sep=";", header=[0,1])
print(f"The file has {df.shape} (rows, columns)")
print(f"Processing ...")

# Get the total number of columns and rows
total_columns = len(df.columns)
total_rows = len(df.index)
question_list = [] # List to store processed questions

def handle_question_multi_choice(column_index):
    """
    Handles multi-choice type questions, separated by ;

    Args:
        column_index (int): The column index from the input file
    """
    pass

def handle_question_default(column_index):
    """
    Handles all questions that doesn't fall into more specific functions

    Args:
        column_index (int): The column index from the input file
    """
    # Retrieve all unique answers in the column, dropping NaN values
    unique_answers = df.iloc[:, column_index].dropna().unique()
    
    # Create a new Question object for this column
    q = Question()
    q.question = df.columns[column_index][0] # Store the question text

    # Loop through each unique answer in the column
    for answer in unique_answers:

        # Get the proportion (normalized count) of this answer AND the absolute count
        answers_normalized = df.iloc[:, column_index].value_counts(normalize=True, dropna=True)[answer]
        answers_count = df.iloc[:, column_index].value_counts(normalize=False, dropna=True)[answer]

        # Store the info on the object
        q.answers[answer] = float(answers_normalized)
        q.num_answers += int(answers_count)
            
    # Add the processed question object to the list
    question_list.append(q)

def write_csv():
    """
    Writes the processed data into a CSV file
    """
    # Write the processed data to a CSV file
    with open(output_file, mode='w', encoding='ansi', errors='ignore', newline='') as output_csv_file:
        output_writer = csv.writer(output_csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Loop through each processed question
        for question in question_list:
            output_writer.writerow([question.question]) # Write the question text

            # Get the sorted & thresholded answers
            for answer, answers_normalized in question.get_answers(max_answers_per_question, max_answers_spill_label).items():
                answers_count = int(answers_normalized * question.num_answers)
                
                # Write the answer, its normalized frequency, and absolute count to CSV
                output_writer.writerow([answer, answers_normalized, answers_count])

# Loop through each CSV column
for column_index in range (total_columns):
    
    # Skip columns marked as "ignore" in the second header row
    if df.columns[column_index][1] in ("ignore"):
        continue

    # Handle multi choice questions
    elif df.columns[column_index][1] in ("multi_choice"):
        handle_question_multi_choice(column_index)

    # handle all other questions
    else:
        handle_question_default(column_index)

write_csv()
print(f"Process completed successfully.")