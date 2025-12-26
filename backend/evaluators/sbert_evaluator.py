from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")

def sbert_score(answer, model_answer):
    embeddings = model.encode([model_answer, answer])
    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]
    return float(score)
