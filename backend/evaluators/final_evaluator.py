from evaluators.tfidf_evaluator import tfidf_score
from evaluators.sbert_evaluator import sbert_score
from evaluators.kg_evaluator import kg_scores, extract_concepts_from_text


# -----------------------------
# Combined similarity
# -----------------------------
def combined_score(student_answer, model_answer):
    tfidf = tfidf_score(student_answer, model_answer)
    sbert = sbert_score(student_answer, model_answer)

    # build "KG" as concept set from model answer
    model_concepts = extract_concepts_from_text(model_answer)
    kg = kg_scores(student_answer, model_concepts)

    # weighted combination
    final = (0.3 * tfidf) + (0.5 * sbert) + (0.2 * kg)
    return final


# -----------------------------
# Final evaluator
# -----------------------------
def evaluate_answer(student_answer, model_answer, max_marks):
    """
    Returns ALWAYS:
    {
        score: int,
        grade: str,
        feedback: str
    }
    """

    similarity = combined_score(student_answer, model_answer)

    # ---- GRADING LOGIC ----
    if similarity >= 0.75:
        grade = "Correct"
        score = max_marks
        feedback = "Answer correctly covers the required concepts."

    elif similarity >= 0.45:
        grade = "Partially Correct"
        score = max(1, max_marks // 2)
        feedback = "Answer is partially correct but missing some concepts."

    else:
        grade = "Incorrect"
        score = 0
        feedback = "Answer does not cover the required concepts."

    return {
        "score": int(score),
        "grade": grade,
        "feedback": feedback
    }
