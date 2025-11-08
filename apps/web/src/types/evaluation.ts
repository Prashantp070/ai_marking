export type Evaluation = {
  submissionId: number;
  finalScore: number;
  confidence: number;
  feedback?: string | null;
  scoreBreakdown: Record<string, unknown>;
};



