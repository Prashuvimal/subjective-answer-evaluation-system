import json

DATA_QUESTIONS = "data/questions.json"
DATA_ANSWERS = "data/answers.json"
DATA_CONTEXTS = "data/contexts.json"


# ------------------------------
# LOAD ALL QUESTIONS (FLAT LIST)
# ------------------------------
def get_all_questions():
    with open(DATA_QUESTIONS, encoding="utf-8") as f:
        data = json.load(f)

    questions = []
    for ctx in data.get("contexts", []):
        for level in ctx:
            if level.endswith("_Level"):
                questions.extend(ctx[level].get("Questions", []))
    return questions


# ------------------------------
# LOAD ALL ANSWERS
# ------------------------------
def get_all_answers():
    with open(DATA_ANSWERS, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "answers" in data:
        return data["answers"]

    return data


# ------------------------------
# LOAD ALL CONTEXTS
# ------------------------------
def get_all_contexts():
    with open(DATA_CONTEXTS, encoding="utf-8") as f:
        return json.load(f)
