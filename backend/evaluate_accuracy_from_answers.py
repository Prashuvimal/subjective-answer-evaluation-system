import json
import requests
import os
import re

API_URL = "http://127.0.0.1:5000/evaluate"   # ✅ correct endpoint
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- TEXT PREPROCESSOR ----------------
def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ---------------- LABEL MAP ----------------
LABEL_MAP = {
    "Incorrect": 0,
    "Partially Correct": 1,
    "Correct": 2
}

# ---------------- LOAD & FLATTEN ANSWERS ----------------
with open("data/answers.json", encoding="utf-8") as f:
    raw_answers = json.load(f)

def flatten_answers(data):
    flat = []
    if isinstance(data, dict) and "answers" in data:
        data = data["answers"]

    for item in data:
        if isinstance(item, list):
            flat.extend(item)
        elif isinstance(item, dict):
            flat.append(item)
    return flat

answers = flatten_answers(raw_answers)
print(f"✔ Flattened answers count: {len(answers)}")

# ---------------- LOAD QUESTIONS ----------------
with open("data/questions.json", encoding="utf-8") as f:
    questions_raw = json.load(f)

def build_question_map(data):
    qmap = {}
    for ctx in data["contexts"]:
        for level in ctx:
            if level == "Context_id":
                continue
            for q in ctx[level]["Questions"]:
                qmap[q["id"]] = q["question"]
    return qmap

QUESTION_MAP = build_question_map(questions_raw)
print(f"✔ Loaded questions: {len(QUESTION_MAP)}")

# ---------------- STORAGE ----------------
evaluation_results = []
total = 0
relaxed_correct = 0
strict_correct = 0

# ---------------- MAIN LOOP ----------------
for item in answers:
    if not isinstance(item, dict):
        continue

    qid = item.get("question_id")
    if not qid or qid not in QUESTION_MAP:
        continue

    question = clean_text(QUESTION_MAP[qid])

    test_cases = [
        (item.get("student_answer"), "Correct"),
        (item.get("partially_correct_answer"), "Partially Correct"),
        (item.get("weak_answer"), "Incorrect")
    ]

    for student_text, expected_label in test_cases:
        if not student_text:
            continue

        payload = {
            "question": question,
            "answer": clean_text(student_text)
        }

        response = requests.post(API_URL, json=payload)
        if response.status_code != 200:
            continue

        result = response.json()
        system_label = result.get("grade")

        if system_label not in LABEL_MAP:
            continue

        gt = LABEL_MAP[expected_label]
        pred = LABEL_MAP[system_label]

        strict_match = gt == pred
        relaxed_match = abs(gt - pred) <= 1   # ✅ key fix

        total += 1
        if strict_match:
            strict_correct += 1
        if relaxed_match:
            relaxed_correct += 1

        evaluation_results.append({
            "question_id": qid,
            "expected": expected_label,
            "predicted": system_label,
            "strict_match": strict_match,
            "relaxed_match": relaxed_match
        })

# ---------------- SAVE RESULTS ----------------
with open(f"{OUTPUT_DIR}/evaluation_results.json", "w", encoding="utf-8") as f:
    json.dump(evaluation_results, f, indent=2)

strict_accuracy = (strict_correct / total) * 100 if total else 0
relaxed_accuracy = (relaxed_correct / total) * 100 if total else 0

with open(f"{OUTPUT_DIR}/accuracy_report.json", "w", encoding="utf-8") as f:
    json.dump({
        "total_samples": total,
        "strict_accuracy_percent": round(strict_accuracy, 2),
        "relaxed_accuracy_percent": round(relaxed_accuracy, 2)
    }, f, indent=2)

print("\n==============================")
print("✔ Evaluation completed")
print(f"✔ Strict Accuracy:  {strict_accuracy:.2f}%")
print(f"✔ Relaxed Accuracy: {relaxed_accuracy:.2f}%")
print("==============================\n")
