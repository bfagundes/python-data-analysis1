import string, spacy
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the Spanish language model at module level
nlp = spacy.load("es_core_news_sm")

def clean_response(text: str) -> str:
    """
    Perform baseline text cleaning:
      - Convert to lowercase.
      - Remove all punctuation.
      - Strip leading/trailing whitespace.

    Args:
        text (str): The raw input string to be cleaned.

    Returns:
        str: The cleaned text.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    return text

def is_gibberish(text: str) -> bool:
    """
    Heuristically determines if the given text is "gibberish" or invalid.

    Checks:
      1. Length <= 2 characters.
      2. Contains at least one vowel.
      3. Not purely numeric.

    Args:
        text (str): The text to analyze.

    Returns:
        bool: True if text is likely gibberish or invalid, False otherwise.
    """
    # Check if too short
    if len(text) <= 2:
        return True
    
    # Check if it has at least one vowel
    vowels = set("aeiou")
    if not any(ch in vowels for ch in text):
        return True
    
    # Check if it is purely numeric
    if text.isdigit():
        return True

    return False

def remove_stopwords_and_lemmatize_spanish(text: str) -> str:
    """
    Tokenize the input text with spaCy (Spanish), remove stopwords and punctuation tokens, and lemmatize the remaining tokens.

    Args:
        text (str): The text to be processed.

    Returns:
        str: A single string of space-separated lemmas after stopword and punctuation removal.
    """
    doc = nlp(text)
    lemmas = []
    for token in doc:
        if not token.is_stop and not token.is_punct and token.lemma_.strip():
            lemmas.append(token.lemma_)
    return " ".join(lemmas)

def vectorize_text(texts):
    """
    Applies TF-IDF vectorization to a list of text documents.

    Args:
        texts (list of str): The collection of documents (strings) to vectorize.

    Returns:
        (TfidfVectorizer, sparse matrix):
            - The fitted TfidfVectorizer instance.
            - The resulting TF-IDF matrix (sparse) where each row corresponds to a document and each column corresponds to a term.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

def extract_keywords_from_centroid(cluster_center, feature_names, top_n=3):
    """
    Given a cluster center (array of TF-IDF feature weights), identify the top_n most
    influential features (keywords).

    Args:
        cluster_center (np.array): 1-D array of TF-IDF weights for a cluster centroid.
        feature_names (array-like): List of feature (term) names corresponding to indices.
        top_n (int, optional): Number of top keywords to extract. Defaults to 3.

    Returns:
        list of str: The top_n keywords (feature names) in descending order of weight.
    """
    top_indices = cluster_center.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices]

def cluster_responses(question, n_clusters=5, top_n=3):
    """
    Clusters open-ended responses in a `Question` object using K-Means, then
    derives representative keywords for each cluster centroid.

    Args:
        question (Question): The Question object containing:
            - tfidf_matrix: The TF-IDF representation of its cleaned responses.
            - feature_names: The corresponding feature (term) names.
            - question: The question text (used for logging).
            - cleaned_responses: The list of processed text responses.
        n_clusters (int, optional): Number of clusters to form with K-Means. Defaults to 5.
        top_n (int, optional): Number of top keywords to extract per cluster. Defaults to 3.

    Returns:
        (labels, cluster_keywords):
            - labels (np.array): An array of cluster assignments for each response.
            - cluster_keywords (list of list of str): A list where each element is a list of top_n keywords for a cluster.
    """
    # If there's no TF-IDF data, clustering cannot proceed
    if question.tfidf_matrix is None:
        print(f"No TF-IDF data found for question: {question.question}. Skipping clustering.")
        return None, None

    X = question.tfidf_matrix
    feature_names = question.feature_names

    # Initialize and fit the K-Means model
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    # Extract cluster centers and compute top keywords
    cluster_centers = kmeans.cluster_centers_
    cluster_keywords = []

    for c_index in range(n_clusters):
        top_keywords = extract_keywords_from_centroid(
            cluster_centers[c_index], feature_names, top_n
        )
        cluster_keywords.append(top_keywords)

    # Print the results
    print(f"\n--- Clustering results for question: '{question.question}' ---")
    for cluster_id in range(n_clusters):
        print(f"Cluster {cluster_id} (keywords = {', '.join(cluster_keywords[cluster_id])}):")
        doc_indices = np.where(labels == cluster_id)[0]
        for idx in doc_indices:
            print(f"  - {question.cleaned_responses[idx]}")

    return labels, cluster_keywords