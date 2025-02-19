import csv
import pandas as pd
import config

from question_handlers import (
    handle_question_multi_choice,
    handle_question_default,
    handle_open_question
)

# ---- Constants / Config ----
INPUT_FILE = 'files/input.csv'
OUTPUT_FILE = 'files/output.csv'
MAX_ANSWERS_PER_QUESTION = 10
MAX_ANSWERS_SPILL_LABEL = "Otros"

def write_csv(question_list):
    """
    Writes the processed data into a CSV file.

    Args:
        question_list (list): A list of Question objects that hold the processed data.
    """
    with open(OUTPUT_FILE, mode='w', encoding='ansi', errors='ignore', newline='') as output_csv_file:
        output_writer = csv.writer(output_csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Iterate over each processed question object
        for question in question_list:
            # Write the question text
            output_writer.writerow([question.question])

            # Get a dictionary with the answers to write
            answer_dict = question.get_answers(MAX_ANSWERS_PER_QUESTION, MAX_ANSWERS_SPILL_LABEL)
            
            # Write each answer, normalized freq, and absolute count
            for answer, answers_normalized in answer_dict.items():
                answers_count = int(answers_normalized * question.num_answers)
                output_writer.writerow([answer, answers_normalized, answers_count])

def main():
    # Load CSV with a multi-line header (first line = column title, second line = flag)
    survey_data = pd.read_csv(INPUT_FILE, sep=";", header=[0, 1])

    # Retriving the total columns and rows
    total_columns = len(survey_data.columns)
    total_rows = len(survey_data.index)

    # A list to store processed Question objects
    question_list = []  

    print(f"The file has {total_rows} rows and {total_columns} columns.")
    print("Processing ...")

    # Loop through each column
    for column_index in range(total_columns):
        
        # Check the second header row (the "flag")
        flag = survey_data.columns[column_index][1]

        
        if flag == "ignore":
            continue
        elif flag == "multi_choice":
            handle_question_multi_choice(survey_data, column_index, question_list)
        elif flag == "open":
            handle_open_question(survey_data, column_index, question_list)
        else:
            handle_question_default(survey_data, column_index, question_list)

    # Once all columns are processed, write to CSV
    write_csv(question_list)
    print("Process completed successfully.")

if __name__ == "__main__":
    main()