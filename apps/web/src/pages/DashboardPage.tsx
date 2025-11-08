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
        // Get all submissions
        const submissionsResponse = await api.get("/submissions");
        const submissions = submissionsResponse.data.submissions || [];
        
        // Get results for each submission that has evaluation
        const resultsList: Evaluation[] = [];
        for (const submission of submissions) {
          if (submission.has_evaluation) {
            try {
              const resultResponse = await api.get(`/results/${submission.id}`);
              resultsList.push({
                submissionId: submission.id,
                finalScore: resultResponse.data.score || resultResponse.data.final_score || 0,
                confidence: resultResponse.data.confidence || 0,
                feedback: resultResponse.data.feedback || "",
                scoreBreakdown: resultResponse.data.score_breakdown || {}
              });
            } catch (err) {
              console.error(`Failed to load result for submission ${submission.id}`, err);
            }
          }
        }
        
        setResults(resultsList);
      } catch (error) {
        console.error("Failed to load submissions", error);
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



