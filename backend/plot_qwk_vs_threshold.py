import json
import matplotlib.pyplot as plt
from sklearn.metrics import cohen_kappa_score
from evaluators.final_evaluator import evaluate_answer

# ---------------- LOAD DATA ----------------
with open("data/answers.json", encoding="utf-8") as f:
    raw = json.load(f)

# ---------------- FLATTEN ANSWERS ----------------
def flatten(data):
    out = []
    for x in data:
        if isinstance(x, list):
            out.extend(flatten(x))
        elif isinstance(x, dict):
            out.append(x)
    return out

answers = flatten(raw)

# ---------------- PARAMETERS ----------------
thresholds = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
qwk_scores = []

LABEL_MAP = {
    "Incorrect": 0,
    "Partially Correct": 1,
    "Correct": 2
}

MAX_MARKS = 2  # ordinal scale: 0,1,2

# ---------------- THRESHOLD SWEEP ----------------
for ct in thresholds:
    y_true = []
    y_pred = []

    # keep partial threshold relative
    pt = ct - 0.2

    for item in answers:
        model_answer = item.get("correct_answer")
        if not model_answer:
            continue

        test_cases = [
            (item.get("student_answer"), 2),              # correct
            (item.get("partially_correct_answer"), 1),    # partial
            (item.get("weak_answer"), 0)                  # incorrect
        ]

        for student_answer, true_label in test_cases:
            if not student_answer:
                continue

            # -------- SYSTEM PREDICTION --------
            result = evaluate_answer(
                student_answer=student_answer,
                model_answer=model_answer,
                max_marks=MAX_MARKS,
                correct_threshold=ct,
                partial_threshold=pt
            )

            y_true.append(true_label)
            y_pred.append(LABEL_MAP[result["grade"]])

    # -------- QWK COMPUTATION --------
    if len(y_true) > 0:
        qwk = cohen_kappa_score(y_true, y_pred, weights="quadratic")
    else:
        qwk = 0.0

    qwk_scores.append(qwk)

# ---------------- PLOT ----------------
plt.figure(figsize=(8, 5))
plt.plot(thresholds, qwk_scores, marker="o")
plt.xlabel("Correct Threshold")
plt.ylabel("Quadratic Weighted Kappa (QWK)")
plt.title("QWK vs Threshold (TF-IDF + SBERT + KG)")
plt.grid(True)
plt.show()
