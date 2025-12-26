import { useState } from "react";
import { extractOCR, evaluateAnswer } from "../services/api";
import ResultCard from "./ResultCard";

export default function EvaluationForm() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ocrError, setOcrError] = useState("");

  const handleOCR = async () => {
    if (!file) return;
    setOcrError("");
    try {
      const res = await extractOCR(file);
      setAnswer(res.data.text);
    } catch {
      setOcrError("OCR failed to extract text");
    }
  };

  const handleEvaluate = async () => {
    setLoading(true);
    try {
      const res = await evaluateAnswer({
        question,
        answer,
      });
      setResult(res.data);
    } catch {
      alert("Evaluation failed");
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Evaluate Answer</h2>

      <input
        type="text"
        placeholder="Enter question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleOCR}>Extract (OCR)</button>
      {ocrError && <p className="error">{ocrError}</p>}

      <textarea
        placeholder="Student answer (OCR text will appear here)"
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />

      <button onClick={handleEvaluate} disabled={loading}>
        {loading ? "Evaluating..." : "Evaluate"}
      </button>

      {result && <ResultCard result={result} />}
    </div>
  );
}
