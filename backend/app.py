from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import tempfile

# ---------- INTERNAL IMPORTS ----------
from loader.dataset_loader import get_all_questions
from evaluators.question_matcher import match_question
from evaluators.final_evaluator import evaluate_answer
from ocr.ocr_engine import extract_text

app = Flask(__name__)
CORS(app)

# ---------- LOAD DATA ONCE ----------
with open("data/answers.json", encoding="utf-8") as f:
    RAW_ANSWERS = json.load(f)


# ---------- SAFE FLATTEN ----------
def flatten_answers(data):
    flat = []
    if isinstance(data, dict) and "answers" in data:
        data = data["answers"]

    for item in data:
        if isinstance(item, list):
            flat.extend(flatten_answers(item))
        elif isinstance(item, dict):
            flat.append(item)
    return flat


ANSWERS = flatten_answers(RAW_ANSWERS)


# --------------------------------------------------
# HOME
# --------------------------------------------------
@app.route("/")
def home():
    return "Subjective Answer Evaluation Backend Running"


# --------------------------------------------------
# OCR ENDPOINT
# --------------------------------------------------
@app.route("/ocr", methods=["POST"])
def ocr_api():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"}), 400

    file = request.files["file"]
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        text = extract_text(tmp.name)

    return jsonify({
        "success": True,
        "text": text.strip()
    })


# --------------------------------------------------
# EVALUATION ENDPOINT (MAIN)
# --------------------------------------------------
@app.route("/evaluate", methods=["POST"])
def evaluate_api():
    data = request.get_json()

    question_text = data.get("question", "").strip()
    student_answer = data.get("answer", "").strip()

    if not question_text or not student_answer:
        return jsonify({
            "success": False,
            "message": "Question and answer are required"
        }), 400

    # ---------- LOAD QUESTIONS ----------
    QUESTIONS = get_all_questions()

    # ---------- QUESTION MATCHING ----------
    matched_q, q_score = match_question(question_text, QUESTIONS)

    if not matched_q or q_score < 0.55:
        return jsonify({
            "success": True,
            "grade": "Manual Review Recommended",
            "score": 0,
            "feedback": "Question not found in dataset"
        })

    # ---------- FIND ANSWER KEY ----------
    key = next(
        (
            a for a in ANSWERS
            if isinstance(a, dict)
            and a.get("question_id") == matched_q["id"]
        ),
        None
    )

    if not key:
        return jsonify({
            "success": True,
            "grade": "Manual Review Recommended",
            "score": 0,
            "feedback": "Answer key not found"
        })

    model_answer = key.get("correct_answer") or key.get("student_answer", "")

    # ---------- EVALUATION (SBERT + TFIDF + KG) ----------
    result = evaluate_answer(
        student_answer=student_answer,
        model_answer=model_answer,
        max_marks=matched_q["max-marks"]
    )

    return jsonify({
        "success": True,
        "question": matched_q["question"],
        "score": result["score"],
        "grade": result["grade"],
        "feedback": result["feedback"]
    })


# --------------------------------------------------
# RUN
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
