export type AnalyticsOverview = {
  average_score: number;
  confidence_distribution: Record<string, number>;
  missed_keywords: Record<string, number>;
  status_breakdown: Record<string, number>;
  updated_at: string;
};

