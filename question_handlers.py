import pandas as pd
import numpy as np

from question import Question
from text_processing import (
    clean_response,
    is_gibberish,
    remove_stopwords_and_lemmatize_spanish,
    vectorize_text,
    cluster_responses,
    find_optimal_k_elbow,
    find_optimal_k_silhouette
)

INVALID_ANSWER_LABEL = 'Invalid/Gibberish/NA'

def handle_question_multi_choice(survey_data, column_index, question_list, separator=";"):
    """
    Processes a multi-choice question column in the survey data.

    Args:
        survey_data (DataFrame): The survey data loaded via pandas.
        column_index (int): Index of the column to process.
        question_list (list): A list to accumulate `Question` objects.
        separator (str, optional): The delimiter for multiple choices in a single response. Defaults to `';'`.
    """
    # Gets non-null unique responses
    all_answers = survey_data.iloc[:, column_index].dropna().unique()

    # Initializing a Question object
    q = Question()
    q.question = survey_data.columns[column_index][0]

    # Counting how many times each choice appears
    choice_counts = {}
    for response in all_answers:

        choices = response.split(separator)
        for choice in choices:

            choice = choice.strip() 
            if choice:
                choice_counts[choice] = choice_counts.get(choice, 0) + 1

    # Calculating the total num of responses
    total_responses = sum(choice_counts.values())

    # Populating the Question object with Normalized and Absolute values for each choice
    for choice, count in choice_counts.items():
        q.answers[choice] = count / total_responses
        q.num_answers += count 

    # Adding the object to the shared list
    question_list.append(q)

def handle_question_default(survey_data, column_index, question_list):
    """
    Processes a default (single-choice or unspecified) question column in the survey data.

    Args:
        survey_data (DataFrame): The survey data loaded via pandas.
        column_index (int): Index of the column to process.
        question_list (list): A list to accumulate `Question` objects.
    """
    # Getting the non-null unique answers
    unique_answers = survey_data.iloc[:, column_index].dropna().unique()

    # Initializing a Question object
    q = Question()
    q.question = survey_data.columns[column_index][0]

    # Calculating the frequencies
    for answer in unique_answers:
        answers_normalized = survey_data.iloc[:, column_index].value_counts(normalize=True, dropna=True)[answer]
        answers_count = survey_data.iloc[:, column_index].value_counts(normalize=False, dropna=True)[answer]

        q.answers[answer] = float(answers_normalized)
        q.num_answers += int(answers_count)

    # Adding the object to the shared list   
    question_list.append(q)

def handle_open_question(survey_data, column_index, question_list):
    """
    Processes an open-ended question column in the survey data.
    
    Args:
        survey_data (DataFrame): The survey data loaded via pandas.
        column_index (int): Index of the column to process.
        question_list (list): A list to accumulate `Question` objects.

    Raises:
        ValueError: If the vocabulary is empty (e.g., all responses are gibberish or invalid).
    """
    # Initializing a Question object
    q = Question()
    q.question = survey_data.columns[column_index][0]
    print("\n---------- Handling open question ----------")
    print(f"Question: {q.question}")

    # Initializing a list to receive the cleaned responses
    cleaned_responses = []

    # Clean and pre-process each response
    for original_answer in survey_data.iloc[:, column_index].dropna():
        #print(f"Origina: {original_answer}")
        basic_cleaned = clean_response(original_answer)
        #print(f"Cleaned: {basic_cleaned}")
        advanced_cleaned = remove_stopwords_and_lemmatize_spanish(basic_cleaned)
        #print(f"Lematiz: {advanced_cleaned}")

        # If response is considered gibberish, convert to placeholder text
        if is_gibberish(advanced_cleaned):
            advanced_cleaned = INVALID_ANSWER_LABEL
            #print(f"Invalid: {advanced_cleaned}")

        #print()

        # Adding the cleaned response to the list
        cleaned_responses.append(advanced_cleaned)

    # Storing the cleaned responses in the Question object
    q.cleaned_responses = cleaned_responses

    # Attempting TF-IDF vectorization
    try:
        vectorizer, tfidf_matrix = vectorize_text(cleaned_responses)
        q.tfidf_matrix = tfidf_matrix
        q.feature_names = vectorizer.get_feature_names_out()

        # Choosing the cluster number with Elbow or Silhouette
        # Elbow
        best_k = find_optimal_k_elbow(tfidf_matrix, k_min=2, k_max=10, plot=True)
        # Silhouette
        #best_k = find_optimal_k_silhouette(tfidf_matrix, k_min=2, k_max=10, plot=True)

        unique_rows = np.unique(tfidf_matrix.toarray(), axis=0)
        num_unique = len(unique_rows)
        if best_k > num_unique:
            best_k = num_unique -2

        print(f"Unique: {num_unique} > Chosen k {best_k}")

        # Clustering the responses using K_Means and extracting top keywords
        labels, cluster_keywords = cluster_responses(q, n_clusters=best_k, top_n=3)
        q.cluster_labels = labels
        q.cluster_names = cluster_keywords

    except ValueError as e:
        # Handling cases where no valid vocabulary could be extracted
        print(f"Could not vectorize (ValueError): {e}")
        q.tfidf_matrix = None
        q.feature_names = []

    # Adding the object to the shared list
    question_list.append(q)