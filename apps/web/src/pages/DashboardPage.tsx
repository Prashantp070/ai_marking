import { useEffect, useState } from "react";

import ResultCard from "../components/ResultCard";
import { useApi } from "../api/useApi";
import { Evaluation } from "../types/evaluation";

export default function DashboardPage() {
  const api = useApi();
  const [results, setResults] = useState<Evaluation[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const response = await api.get("/results/1");
        setResults([
          {
            submissionId: 1,
            finalScore: response.data.final_score,
            confidence: response.data.confidence,
            feedback: response.data.feedback,
            scoreBreakdown: response.data.score_breakdown
          }
        ]);
      } catch (error) {
        console.error("Failed to load results", error);
      }
    };
    load();
  }, [api]);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Evaluation Dashboard</h1>
      <div className="grid gap-4 lg:grid-cols-2">
        {results.map((result) => (
          <ResultCard key={result.submissionId} result={result} />
        ))}
      </div>
    </div>
  );
}

