import { useEffect, useState } from "react";
import { useApi } from "../api/useApi";
import { Link } from "react-router-dom";
import { DocumentArrowUpIcon, CheckCircleIcon, ClockIcon, ExclamationCircleIcon, ArrowPathIcon } from "@heroicons/react/24/outline";

type Submission = {
  id: string | number;
  filename?: string;
  status?: string;
  score?: number | null;
  confidence?: number | null;
  created_at?: string;
  exam_id?: number;
  has_evaluation?: boolean;
};

export default function DashboardPage() {
  const api = useApi();
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const userEmail = localStorage.getItem("user_email") || "User";

  const loadSubmissions = async () => {
    try {
      const res = await api.get("/submissions");
      console.log("Submissions response:", res.data);
      const submissionsData = res.data?.submissions || res.data || [];
      setSubmissions(Array.isArray(submissionsData) ? submissionsData : []);
      setError(null);
    } catch (err: any) {
      console.error("Error loading submissions:", err);
      console.error("Error details:", err.response?.data);
      setSubmissions([]);
      setError(null);
    }
  };

  useEffect(() => {
    async function load() {
      setLoading(true);
      await loadSubmissions();
      setLoading(false);
    }

    load();
  }, [api]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadSubmissions();
    setRefreshing(false);
  };

  const getStatusIcon = (status?: string) => {
    switch (status) {
      case "completed":
      case "evaluated":
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case "processing":
      case "pending":
        return <ClockIcon className="w-5 h-5 text-blue-500 animate-spin" />;
      case "error":
      case "failed":
        return <ExclamationCircleIcon className="w-5 h-5 text-red-500" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status?: string) => {
    switch (status) {
      case "completed":
      case "evaluated":
        return "bg-green-50 border-green-200";
      case "processing":
      case "pending":
        return "bg-blue-50 border-blue-200";
      case "error":
      case "failed":
        return "bg-red-50 border-red-200";
      default:
        return "bg-gray-50 border-gray-200";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-white rounded-full shadow-lg mb-4">
              <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
            </div>
            <p className="text-gray-600 font-medium">Loading submissions...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6 sm:p-8">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600 mt-2">Welcome, {userEmail}</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="flex items-center gap-2 px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-lg transition-all disabled:opacity-50"
            >
              <ArrowPathIcon className={`w-5 h-5 ${refreshing ? "animate-spin" : ""}`} />
              {refreshing ? "Refreshing..." : "Refresh"}
            </button>
            <Link
              to="/upload"
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg hover:shadow-lg transform hover:-translate-y-0.5 transition-all"
            >
              <DocumentArrowUpIcon className="w-5 h-5" />
              Upload Answer Sheet
            </Link>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm">Total Submissions</p>
            <p className="text-3xl font-bold text-gray-900 mt-2">{submissions.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm">Evaluated</p>
            <p className="text-3xl font-bold text-green-600 mt-2">
              {submissions.filter((s) => s.status === "completed" || s.has_evaluation).length}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm">Pending</p>
            <p className="text-3xl font-bold text-blue-600 mt-2">
              {submissions.filter((s) => s.status === "pending" || s.status === "processing").length}
            </p>
          </div>
        </div>
      </div>

      {/* Submissions List */}
      <div className="max-w-7xl mx-auto">
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="px-6 sm:px-8 py-6 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900">Recent Submissions</h2>
          </div>

          {error && (
            <div className="m-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {submissions.length === 0 ? (
            <div className="p-8 sm:p-12 text-center">
              <DocumentArrowUpIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-600 mb-2">No Submissions Yet</h3>
              <p className="text-gray-500 mb-6">Upload your first answer sheet to get started</p>
              <Link
                to="/upload"
                className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
              >
                <DocumentArrowUpIcon className="w-5 h-5" />
                Upload Now
              </Link>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {submissions.map((submission) => (
                <div
                  key={submission.id}
                  className={`p-6 sm:p-8 border-l-4 ${getStatusColor(submission.status)}`}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        {getStatusIcon(submission.status)}
                        <h3 className="text-lg font-semibold text-gray-900">
                          Submission #{submission.id}
                        </h3>
                      </div>
                      <p className="text-gray-600 text-sm">
                        {submission.created_at
                          ? new Date(submission.created_at).toLocaleDateString("en-US", {
                              year: "numeric",
                              month: "long",
                              day: "numeric",
                              hour: "2-digit",
                              minute: "2-digit",
                            })
                          : "N/A"}
                      </p>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-4 sm:items-center">
                      <div className="text-right">
                        <p className="text-gray-600 text-xs uppercase tracking-wide mb-1">Status</p>
                        <p className="text-gray-900 font-semibold capitalize">
                          {submission.status || "Pending"}
                        </p>
                      </div>

                      {submission.score !== null && submission.score !== undefined && (
                        <div className="text-right">
                          <p className="text-gray-600 text-xs uppercase tracking-wide mb-1">Score</p>
                          <p className="text-2xl font-bold text-green-600">{submission.score.toFixed(2)}%</p>
                        </div>
                      )}

                      <Link
                        to={`/upload?id=${submission.id}`}
                        className="px-4 py-2 bg-blue-100 text-blue-700 font-medium rounded-lg hover:bg-blue-200 transition-colors text-center"
                      >
                        View Details
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
