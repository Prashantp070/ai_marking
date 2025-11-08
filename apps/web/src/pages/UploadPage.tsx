import { useState } from "react";

import { useApi } from "../api/useApi";

interface EvaluationResult {
  status: string;
  score: number;
  confidence: number;
  student_answer?: string;
  reference_answer?: string;
  similarity?: number;
  feedback?: string;
}

export default function UploadPage() {
  const api = useApi();
  const [examId, setExamId] = useState("1");
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [submissionId, setSubmissionId] = useState<number | null>(null);
  const [evaluationResult, setEvaluationResult] = useState<EvaluationResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setMessage("Please select a file to upload");
      return;
    }

    // Check authentication
    const token = localStorage.getItem("access_token");
    if (!token) {
      setMessage("Authentication required. Please log in first.");
      console.error("No access token found in localStorage");
      return;
    }

    console.log("Starting upload...", { examId, fileName: file.name, fileSize: file.size });
    
    const formData = new FormData();
    formData.append("exam_id", examId);
    formData.append("file", file);

    try {
      console.log("Sending request to /api/v1/uploads...");
      // Don't set Content-Type manually - axios will set it automatically with boundary
      const uploadResponse = await api.post("/uploads", formData);
      console.log("Upload successful:", uploadResponse.data);
      const newSubmissionId = uploadResponse.data.submission_id;
      setSubmissionId(newSubmissionId);
      setMessage(`Upload successful! Starting ML evaluation for submission #${newSubmissionId}...`);
      
      // Start processing/evaluation
      setIsProcessing(true);
      try {
        const processResponse = await api.post(`/process/start/${newSubmissionId}`);
        console.log("Processing started:", processResponse.data);
        
        // Poll for results (simple polling, in production use WebSockets or better polling)
        const pollResults = async () => {
          for (let i = 0; i < 30; i++) {
            await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds
            
            try {
              const resultsResponse = await api.get(`/results/${newSubmissionId}`);
              if (resultsResponse.data.status === "success") {
                setEvaluationResult(resultsResponse.data);
                setIsProcessing(false);
                setMessage("Evaluation complete!");
                return;
              }
            } catch (err: any) {
              if (err?.response?.status !== 404) {
                console.error("Error polling results:", err);
              }
            }
          }
          setIsProcessing(false);
          setMessage("Evaluation is taking longer than expected. Please check results later.");
        };
        
        pollResults();
      } catch (processError: any) {
        setIsProcessing(false);
        console.error("Processing error:", processError);
        setMessage("Upload successful, but evaluation failed. Please try processing manually.");
      }
    } catch (error: any) {
      console.error("Upload error details:", {
        message: error?.message,
        code: error?.code,
        status: error?.response?.status,
        data: error?.response?.data,
        fullError: error
      });
      
      const errorMessage = error?.response?.data?.detail || error?.message || "Upload failed. Please try again.";
      if (error?.response?.status === 401) {
        setMessage("Authentication required. Please log in first.");
      } else if (error?.response?.status === 400) {
        setMessage(`Upload failed: ${errorMessage}`);
      } else if (error?.code === "ERR_NETWORK" || error?.message?.includes("Network")) {
        setMessage("Network Error: Backend not reachable. Please check if backend is running on http://localhost:8000");
      } else {
        setMessage(`Upload failed: ${errorMessage}`);
      }
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Upload Answer Sheets</h1>
      <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border border-slate-800 bg-slate-900/60 p-6">
        <div>
          <label className="block text-sm text-slate-300">Exam ID</label>
          <input
            value={examId}
            onChange={(event) => setExamId(event.target.value)}
            className="mt-1 w-full rounded border border-slate-700 bg-slate-800 px-3 py-2 text-slate-100"
          />
        </div>
        <div>
          <label className="block text-sm text-slate-300">Answer Sheet PDF/Image</label>
          <input
            type="file"
            accept=".pdf,image/*"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
            className="mt-1 w-full text-slate-100"
          />
        </div>
        <button type="submit" className="rounded bg-primary px-4 py-2 font-semibold text-white hover:bg-primary/80">
          Upload &amp; Process
        </button>
        {message && (
          <p className={`text-sm ${message.includes("successful") || message.includes("complete") ? "text-green-400" : "text-slate-300"}`}>
            {message}
          </p>
        )}
        {isProcessing && (
          <div className="mt-4 rounded bg-slate-800/50 p-4">
            <p className="text-sm text-slate-300">⏳ ML evaluation in progress...</p>
            <p className="text-xs text-slate-400 mt-1">This may take 10-30 seconds</p>
          </div>
        )}
      </form>

      {/* ML Evaluation Results */}
      {evaluationResult && (
        <div className="mt-6 rounded-lg border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="text-xl font-semibold mb-4">🤖 ML Evaluation Results</h2>
          
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="rounded bg-slate-800/50 p-4">
              <p className="text-sm text-slate-400">Score (0-10)</p>
              <p className="text-2xl font-bold text-primary">{evaluationResult.score?.toFixed(2) || "N/A"}</p>
            </div>
            <div className="rounded bg-slate-800/50 p-4">
              <p className="text-sm text-slate-400">Confidence</p>
              <p className="text-2xl font-bold text-blue-400">
                {(evaluationResult.confidence * 100)?.toFixed(1) || "N/A"}%
              </p>
            </div>
          </div>

          {evaluationResult.confidence !== undefined && evaluationResult.confidence < 0.5 && (
            <div className="mb-4 rounded bg-yellow-900/30 border border-yellow-700 p-3">
              <p className="text-sm text-yellow-300">
                ⚠️ <strong>Low AI confidence</strong> – Teacher review needed
              </p>
            </div>
          )}

          {evaluationResult.similarity !== undefined && (
            <div className="mb-4 rounded bg-slate-800/50 p-4">
              <p className="text-sm text-slate-400">Semantic Similarity</p>
              <p className="text-lg font-semibold text-slate-200">
                {(evaluationResult.similarity * 100).toFixed(1)}%
              </p>
            </div>
          )}

          {evaluationResult.feedback && (
            <div className="mb-4 rounded bg-slate-800/50 p-3">
              <p className="text-sm text-slate-300">{evaluationResult.feedback}</p>
            </div>
          )}

          {evaluationResult.student_answer && (
            <div className="mb-4 rounded bg-slate-800/50 p-4">
              <p className="text-sm font-semibold text-slate-300 mb-2">Student Answer (OCR):</p>
              <p className="text-sm text-slate-400 whitespace-pre-wrap">{evaluationResult.student_answer}</p>
            </div>
          )}

          {evaluationResult.reference_answer && (
            <div className="rounded bg-slate-800/50 p-4">
              <p className="text-sm font-semibold text-slate-300 mb-2">Reference Answer:</p>
              <p className="text-sm text-slate-400 whitespace-pre-wrap">{evaluationResult.reference_answer}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}



