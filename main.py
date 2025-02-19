import pandas as pd
import numpy as np
import csv, string, spacy
from question import Question
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# Variables
input_file = 'input.csv'
output_file = 'output.csv'
max_answers_per_question = 10
max_answers_spill_label = "Otros"

# Load the Spanish language model
nlp = spacy.load("es_core_news_sm")

# Load CSV with a multi-line header (first line = column title, second line = flag)
survey_data = pd.read_csv(input_file, sep=";", header=[0,1])

# Get the total number of columns and rows
total_columns = len(survey_data.columns)
total_rows = len(survey_data.index)
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
    all_answers = survey_data.iloc[:, column_index].dropna().unique()

    # Create a new Question object for this column
    q = Question()
    q.question = survey_data.columns[column_index][0] # Store the question text

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

def handle_question_default(column_index):
    """
    Handles all questions that doesn't fall into more specific functions

    Args:
        column_index (int): The column index from the input file
    """
    # Retrieve all unique answers in the column, dropping NaN values
    unique_answers = survey_data.iloc[:, column_index].dropna().unique()
    
    # Create a new Question object for this column
    q = Question()
    q.question = survey_data.columns[column_index][0] # Store the question text

    # Loop through each unique answer in the column
    for answer in unique_answers:

        # Get the proportion (normalized count) of this answer AND the absolute count
        answers_normalized = survey_data.iloc[:, column_index].value_counts(normalize=True, dropna=True)[answer]
        answers_count = survey_data.iloc[:, column_index].value_counts(normalize=False, dropna=True)[answer]

        # Store the info on the object
        q.answers[answer] = float(answers_normalized)
        q.num_answers += int(answers_count)
            
    # Add the processed question object to the list
    question_list.append(q)

def clean_response(text: str) -> str:
    """
    Removes punctuation and extra spaces, returns lowercased text.
    (A simple 'baseline' cleaning before we do deeper Spanish cleaning.)
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
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

def vectorize_text(texts):
    """
    Applies TF-IDF to a list of documents (strings).
    Returns the fitted vectorizer and the TF-IDF matrix.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

def extract_keywords_from_centroid(cluster_center, feature_names, top_n=3):
    """
    Given the cluster center (array of TF-IDF feature weights),
    return the top_n feature names (keywords).
    """
    # Get the indexes of the largest weights
    top_indices = cluster_center.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices]

def cluster_responses(question, n_clusters=5, top_n=3):
    """
    Clusters the open-ended text responses using K-Means.
    Extracts representative keywords from each cluster centroid.
    """
    if question.tfidf_matrix is None:
        print(f"No TF-IDF data found for question: {question.question}. Skipping clustering.")
        return None, None

    X = question.tfidf_matrix
    feature_names = question.feature_names

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    cluster_centers = kmeans.cluster_centers_
    cluster_keywords = []

    for c_index in range(n_clusters):
        top_keywords = extract_keywords_from_centroid(
            cluster_centers[c_index], feature_names, top_n
        )
        cluster_keywords.append(top_keywords)

    # Print or log the results
    print(f"\n--- Clustering results for question: '{question.question}' ---")
    for cluster_id in range(n_clusters):
        print(f"Cluster {cluster_id} (keywords = {', '.join(cluster_keywords[cluster_id])}):")
        doc_indices = np.where(labels == cluster_id)[0]
        for idx in doc_indices:
            print(f"  - {question.cleaned_responses[idx]}")

    return labels, cluster_keywords

def remove_stopwords_and_lemmatize_spanish(text: str) -> str:
    """
    Uses spaCy (Spanish) to tokenize, remove stopwords/punctuation, and lemmatize.
    """
    doc = nlp(text)
    lemmas = []
    for token in doc:
        if not token.is_stop and not token.is_punct and token.lemma_.strip():
            lemmas.append(token.lemma_)
    return " ".join(lemmas)

def handle_open_question(column_index):
    """
    Handles open-ended text questions. For each row:
      - Cleans the response (baseline cleaning).
      - Removes Spanish stopwords & lemmatizes via spaCy.
      - Flags invalid/gibberish if it fails the `is_gibberish()` check.
      - Vectorizes (TF-IDF).
      - Clusters them.
    """
    q = Question()
    q.question = survey_data.columns[column_index][0]
    print("\n---------- Handling open question ----------")
    print(f"Question: {q.question}")

    cleaned_responses = []

    # Iterate over each row's answer, dropping NaN
    for original_answer in survey_data.iloc[:, column_index].dropna():
        # Step 1: Basic cleaning (punctuation, lower, etc.)
        basic_cleaned = clean_response(original_answer)
        # Step 2: Spanish stopword removal + lemmatization
        advanced_cleaned = remove_stopwords_and_lemmatize_spanish(basic_cleaned)

        # If it's gibberish or too short, label as invalid
        if is_gibberish(advanced_cleaned):
            advanced_cleaned = "Invalid/Gibberish/NA"
        
        cleaned_responses.append(advanced_cleaned)

    # Store final cleaned responses
    q.cleaned_responses = cleaned_responses

    # Vectorize with TF-IDF; handle possible empty vocabulary
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(cleaned_responses)
        q.tfidf_matrix = tfidf_matrix
        q.feature_names = vectorizer.get_feature_names_out()

        # Now cluster the responses
        labels, cluster_keywords = cluster_responses(q, n_clusters=5, top_n=3)
        q.cluster_labels = labels
        q.cluster_names = cluster_keywords

    except ValueError as e:
        # Catches "empty vocabulary" errors, etc.
        print(f"Could not vectorize (ValueError): {e}")
        q.tfidf_matrix = None
        q.feature_names = []

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
    if survey_data.columns[column_index][1] in ("ignore"):
        continue

    # Handle multi choice questions
    elif survey_data.columns[column_index][1] in ("multi_choice"):
        handle_question_multi_choice(column_index)

    # Handle open questions
    elif survey_data.columns[column_index][1] in ("open"):
        handle_open_question(column_index)

    # handle all other questions
    else:
        handle_question_default(column_index)

write_csv()
print(f"Process completed successfully.")