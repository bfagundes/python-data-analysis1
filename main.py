import pandas as pd
import csv, string
from question import Question
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

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

def vectorize_text(texts):
    """
    Applies TF-IDF to a list of documents (strings).
    Returns the fitted vectorizer and the TF-IDF matrix.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

def extract_keywords_from_centroid(
    cluster_center, feature_names, top_n=3
):
    """
    Given the cluster center (array of TF-IDF feature weights),
    return the top_n feature names (keywords).
    """
    # Get the indexes of the largest weights
    top_indices = cluster_center.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices]

def cluster_responses(question, n_clusters=5, top_n=3):
    """
    Clusters the open-ended text responses stored in `question`.
    Assumes `question.tfidf_matrix` is a valid TF-IDF matrix
    and `question.feature_names` holds the corresponding feature names.
    
    Args:
        question (Question): A question object with at least these attributes:
            - question.tfidf_matrix (scipy sparse matrix or np array)
            - question.feature_names (list of strings)
            - question.cleaned_responses (list of original or cleaned text)
        n_clusters (int): How many clusters (K in K-Means)
        top_n (int): How many representative keywords to extract per cluster
        
    Returns:
        labels (array): Cluster label for each document/response
        cluster_names (list of list of str): Representative keywords for each cluster
    """

    # If no TF-IDF matrix present, we can’t cluster
    if not hasattr(question, "tfidf_matrix"):
        print(f"No tfidf data found for question: {question.question}")
        return None, None
    
    X = question.tfidf_matrix  # The TF-IDF feature matrix
    feature_names = question.feature_names  # The vocabulary list
    
    # Example clustering with K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    
    # Identify top terms for each cluster using the cluster centroids
    cluster_centers = kmeans.cluster_centers_
    cluster_names = []
    
    for c_index in range(n_clusters):
        keywords = extract_keywords_from_centroid(
            cluster_centers[c_index], feature_names, top_n
        )
        cluster_names.append(keywords)
    
    # Store or print the clusters + keywords
    print(f"\n--- Clustering results for question: '{question.question}' ---")
    for cluster_id in range(n_clusters):
        print(f"\nCluster {cluster_id} (keywords = {', '.join(cluster_names[cluster_id])}):")
        
        # Gather the responses that belong to this cluster
        doc_indices = np.where(labels == cluster_id)[0]
        for doc_idx in doc_indices:
            # Assuming we stored the original or cleaned responses in question.cleaned_responses
            resp_text = question.cleaned_responses[doc_idx]
            print(f"   - {resp_text}")
    
    return labels, cluster_names

def handle_open_question(column_index):
    """
    Handles open-ended text questions. For each row:
      - Cleans the response (remove punctuation, lowercase, strip whitespace).
      - Flags invalid/gibberish if it fails the `is_gibberish()` check.
      - Collects the cleaned responses.
      - Vectorizes them (TF-IDF).
      - Clusters them and assigns cluster names based on top keywords.
    """
    q = Question()
    q.question = df.columns[column_index][0]
    print("---------- ---------- ---------- ---------- ----------")
    print(f"Processing open question: {q.question}")

    # List to hold the cleaned versions of each response
    cleaned_responses = []

    # Iterate over the entire column, dropping NaN
    for original_answer in df.iloc[:, column_index].dropna():
        cleaned = clean_response(original_answer)
        if is_gibberish(cleaned):
            cleaned = "Invalid/Gibberish/NA"
        cleaned_responses.append(cleaned)
    
    # Store the cleaned responses in the Question object
    q.cleaned_responses = cleaned_responses

    # Vectorize with TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cleaned_responses)
    q.tfidf_matrix = tfidf_matrix
    q.feature_names = vectorizer.get_feature_names_out()

    # Now cluster the responses
    labels, cluster_keywords = cluster_responses(q, n_clusters=5, top_n=3)

    # Optionally, store these cluster labels or keywords on the question object
    q.cluster_labels = labels
    q.cluster_names = cluster_keywords

    question_list.append(q)

def handle_open_question(column_index):
    """
    Handles open-ended text questions. For each row:
      - Cleans the response (remove punctuation, lowercase, strip whitespace).
      - Flags invalid/gibberish if it fails the `is_gibberish()` check.
      - Collects responses for TF-IDF vectorization.
    """
    q = Question()
    q.question = df.columns[column_index][0]  # Store the question text
    print("---------- ---------- ---------- ---------- ----------")
    print(q.question)

    # Collect cleaned (or gibberish-labeled) responses here
    cleaned_responses = []

    # We iterate over the entire column (dropping NaN)
    for original_answer in df.iloc[:, column_index].dropna():
        cleaned = clean_response(original_answer)
        print(cleaned)
        
        if is_gibberish(cleaned):
            cleaned = "Invalid/Gibberish/NA"
            print(cleaned)
            print()

        cleaned_responses.append(cleaned)

    # Now that all responses have been collected and cleaned, vectorize them.
    # This turns the list of strings into a TF-IDF matrix.
    if cleaned_responses:
        vectorizer, tfidf_matrix = vectorize_text(cleaned_responses)

        # You can store the vectorizer and matrix in the Question object,
        # or handle them however you like.
        q.vectorizer = vectorizer
        q.tfidf_matrix = tfidf_matrix
        # Example: you might store the feature names as well
        q.feature_names = vectorizer.get_feature_names_out()

    # Finally, add the processed question to your question list
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