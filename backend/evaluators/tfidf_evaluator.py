from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def tfidf_score(text1, text2):
    """
    Compute TF-IDF cosine similarity between two texts.
    Returns value between 0 and 1.
    """
    if not text1 or not text2:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return float(score)
