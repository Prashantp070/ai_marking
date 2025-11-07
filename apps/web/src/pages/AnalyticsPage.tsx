import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { useApi } from "../api/useApi";
import { AnalyticsOverview } from "../types/analytics";

const COLORS = ["#2563eb", "#22c55e", "#f59e0b", "#ef4444"];

export default function AnalyticsPage() {
  const api = useApi();
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const response = await api.get("/analytics/overview");
        setOverview(response.data);
      } catch (error) {
        console.error("Failed to load analytics", error);
      }
    };
    load();
  }, [api]);

  if (!overview) {
    return <div className="text-slate-300">Loading analytics...</div>;
  }

  const confidenceData = Object.entries(overview.confidence_distribution).map(([band, value]) => ({ band, value }));
  const statusData = Object.entries(overview.status_breakdown).map(([status, count]) => ({ status, count }));
  const missedKeywordData = Object.entries(overview.missed_keywords).map(([keyword, count]) => ({ keyword, count }));

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Analytics &amp; Insights</h1>
      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="text-lg font-semibold">Confidence Distribution</h2>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={confidenceData} dataKey="value" nameKey="band" innerRadius={60} outerRadius={90} label>
                {confidenceData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#1e293b" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="text-lg font-semibold">Submission Status Breakdown</h2>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="status" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" allowDecimals={false} />
              <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#1e293b" }} />
              <Bar dataKey="count" fill="#22c55e" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>
      <section className="rounded-lg border border-slate-800 bg-slate-900/60 p-6">
        <h2 className="text-lg font-semibold">Overview</h2>
        <div className="mt-4 grid gap-4 lg:grid-cols-3">
          <div className="rounded border border-slate-800 bg-slate-950/50 p-4">
            <p className="text-sm text-slate-400">Average Score</p>
            <p className="text-2xl font-semibold text-primary">{overview.average_score.toFixed(2)}</p>
          </div>
          <div className="rounded border border-slate-800 bg-slate-950/50 p-4">
            <p className="text-sm text-slate-400">Updated At</p>
            <p className="text-2xl font-semibold">{overview.updated_at}</p>
          </div>
          <div className="rounded border border-slate-800 bg-slate-950/50 p-4">
            <p className="text-sm text-slate-400">Tracked Statuses</p>
            <p className="text-2xl font-semibold">{statusData.length}</p>
          </div>
        </div>
        <div className="mt-6">
          <h3 className="text-lg font-semibold">Most Missed Keywords</h3>
          {missedKeywordData.length === 0 ? (
            <p className="mt-2 text-sm text-slate-400">No missed keywords logged yet.</p>
          ) : (
            <ul className="mt-2 space-y-2 text-sm text-slate-300">
              {missedKeywordData.map((item) => (
                <li key={item.keyword} className="flex items-center justify-between rounded border border-slate-800 bg-slate-950/40 px-3 py-2">
                  <span>{item.keyword}</span>
                  <span className="text-primary">{item.count}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </section>
    </div>
  );
}

