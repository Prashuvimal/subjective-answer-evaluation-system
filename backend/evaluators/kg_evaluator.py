import re

# -----------------------------
# Extract concepts from TEXT
# -----------------------------
def extract_concepts_from_text(text):
    if not isinstance(text, str):
        return set()

    text = text.lower()
    words = re.findall(r"[a-zA-Z]+", text)

    # simple concept filter
    return set(words)


# -----------------------------
# KG concept overlap score
# -----------------------------
def kg_scores(student_text, model_concepts):
    """
    student_text : string
    model_concepts : set of concepts
    """

    student_concepts = extract_concepts_from_text(student_text)

    if not student_concepts or not model_concepts:
        return 0.0

    overlap = student_concepts.intersection(model_concepts)
    return len(overlap) / len(model_concepts)
