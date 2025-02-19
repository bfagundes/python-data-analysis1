import pandas as pd
import csv, string
from question import Question

# Variables
input_file = 'input.csv'
output_file = 'output.csv'
max_answers_per_question = 10
max_answers_spill_label = "Otros"

# Load CSV with a multi-line header (first line = column title, second line = flag)
df = pd.read_csv(input_file, sep=";", header=[0,1])

# Get the total number of columns and rows
total_columns = len(df.columns)
total_rows = len(df.index)
question_list = [] # List to store processed questions

print(f"The file has {total_rows} rows and {total_columns} columns)")
print(f"Processing ...")

def handle_question_multi_choice(column_index, separator = ";"):
    """
    Handles multi-choice type questions, separated by ;

    Args:
        column_index (int): The column index from the input file
        separator (string, optional): The answer separator. Defaults to ';'
    """
    # Retrieve all unique answers in the column, dropping NaN values
    all_answers = df.iloc[:, column_index].dropna().unique()

    # Create a new Question object for this column
    q = Question()
    q.question = df.columns[column_index][0] # Store the question text

    # Loop through each response in the column
    choice_counts = {}
    for response in all_answers:
        # Split the response into individual items
        choices = response.split(separator)
        for choice in choices:
            choice = choice.strip() # Remove extra spaces
            if choice:
                choice_counts[choice] = choice_counts.get(choice, 0) + 1 # Couting

    # Get total responses for normalization
    total_responses = sum(choice_counts.values())

    # Store the processed data in the Question object
    for choice, count in choice_counts.items():
        q.answers[choice] = count / total_responses # Normalized 
        q.num_answers += count # Absolute

    # Add the processed question object to the list
    question_list.append(q)

def clean_response(text: str) -> str:
    """
    Removes punctuation, lowercases text, and strips extra whitespace.
    """
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Strip whitespace
    text = text.strip()
    return text

def is_gibberish(text: str) -> bool:
    """
    Naive check to identify gibberish or invalid answers.
    """
    # Check if equal to no
    #if text == "no":
        #return False

    # Check if too short (<= 2 chars)
    if len(text) <= 2:
        return True
    
    # Check if it has at least one vowel
    vowels = set("aeiou")
    if not any(ch in vowels for ch in text):
        return True
    
    # Check if it is purely numeric
    if text.isdigit():
        return True

    # Otherwise, consider it valid
    return False

def handle_open_question(column_index):
    """
    Handles open-ended text questions. For each row:
      - Cleans the response (remove punctuation, lowercase, strip whitespace).
      - Flags invalid/gibberish if it fails the `is_gibberish()` check.
      - Aggregates counts of valid vs. invalid responses.
    """
    # Create a new Question object for this column
    q = Question()
    q.question = df.columns[column_index][0]  # Store the question text
    print("---------- ---------- ---------- ---------- ----------")
    print(q.question)

    # We iterate over the entire column (dropping NaN)
    for original_answer in df.iloc[:, column_index].dropna():
        cleaned = clean_response(original_answer)
        print(cleaned)
        
        if is_gibberish(cleaned):
            cleaned = "Invalid/Gibberish/NA"  # or however you want to label it
            print(cleaned)
            print()

    question_list.append(q)

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

    # Handle open questions
    elif df.columns[column_index][1] in ("open"):
        handle_open_question(column_index)

    # handle all other questions
    else:
        handle_question_default(column_index)

write_csv()
print(f"Process completed successfully.")