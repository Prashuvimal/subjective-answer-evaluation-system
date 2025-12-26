from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def match_question(input_question, questions):
    if not questions:
        return None, 0.0

    input_emb = model.encode(input_question, convert_to_tensor=True)
    best_q = None
    best_score = 0.0

    for q in questions:
        q_emb = model.encode(q["question"], convert_to_tensor=True)
        score = float(util.cos_sim(input_emb, q_emb))
        if score > best_score:
            best_score = score
            best_q = q

    return best_q, best_score
