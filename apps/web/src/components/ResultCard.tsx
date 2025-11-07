import { Evaluation } from "../types/evaluation";

type Props = {
  result: Evaluation;
};

export default function ResultCard({ result }: Props) {
  return (
    <article className="rounded-lg border border-slate-800 bg-slate-900/60 p-5 shadow-lg">
      <header className="mb-3 flex items-center justify-between">
        <span className="text-sm uppercase tracking-wide text-slate-400">Submission #{result.submissionId}</span>
        <span className="rounded bg-slate-800 px-2 py-1 text-xs text-slate-300">Confidence {Math.round(result.confidence * 100)}%</span>
      </header>
      <div className="space-y-2">
        <p className="text-lg font-semibold text-white">Score: {result.finalScore}</p>
        {result.feedback && <p className="text-sm text-slate-300">Feedback: {result.feedback}</p>}
      </div>
      <footer className="mt-4 text-xs text-slate-400">
        <pre className="whitespace-pre-wrap break-words rounded bg-slate-950/40 p-3">{JSON.stringify(result.scoreBreakdown, null, 2)}</pre>
      </footer>
    </article>
  );
}

