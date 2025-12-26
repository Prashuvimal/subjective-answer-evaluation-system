export default function ResultCard({ result }) {
  return (
    <div className="result">
      <h3>Evaluation Result</h3>
      <p><b>Question:</b> {result.question}</p>
      <p><b>Score:</b> {result.score}</p>
      <p><b>Grade:</b> {result.grade}</p>
      <p><b>Feedback:</b> {result.feedback}</p>
    </div>
  );
}
