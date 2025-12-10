import { useState } from "react";
import { useApi } from "../api/useApi";
import { Link, useNavigate } from "react-router-dom";
import { DocumentArrowUpIcon, CheckCircleIcon, ExclamationCircleIcon, ArrowLeftIcon } from "@heroicons/react/24/outline";

export default function UploadPage() {
  const api = useApi();
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState<"success" | "error" | null>(null);
  const [examId, setExamId] = useState("1");
  const [dragActive, setDragActive] = useState(false);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file first.");
      setMessageType("error");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("exam_id", examId);

      const res = await api.post("/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMessage(
        `Upload successful! Submission ID: ${res.data?.submission_id || "Unknown"}`
      );
      setMessageType("success");
      setFile(null);

      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        navigate("/dashboard");
      }, 2000);
    } catch (err: any) {
      setMessage(err.response?.data?.detail || "Upload failed. Please try again.");
      setMessageType("error");
    } finally {
      setLoading(false);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-100 p-6 sm:p-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold mb-6"
          >
            <ArrowLeftIcon className="w-5 h-5" />
            Back to Dashboard
          </Link>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Upload Answer Sheet</h1>
          <p className="text-gray-600">Submit your answer sheets for evaluation</p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="px-6 sm:px-8 py-8 sm:py-10">
            {/* Alert Messages */}
            {message && (
              <div
                className={`mb-6 p-4 rounded-lg border flex items-start gap-3 ${
                  messageType === "success"
                    ? "bg-green-50 border-green-200"
                    : "bg-red-50 border-red-200"
                }`}
              >
                {messageType === "success" ? (
                  <CheckCircleIcon className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                ) : (
                  <ExclamationCircleIcon className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                )}
                <p
                  className={`text-sm font-medium ${
                    messageType === "success" ? "text-green-700" : "text-red-700"
                  }`}
                >
                  {message}
                </p>
              </div>
            )}

            <form onSubmit={handleUpload} className="space-y-6">
              {/* Exam ID Selection */}
              <div>
                <label htmlFor="exam" className="block text-sm font-semibold text-gray-700 mb-3">
                  Select Exam
                </label>
                <select
                  id="exam"
                  value={examId}
                  onChange={(e) => setExamId(e.target.value)}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all"
                >
                  <option value="1">Exam 1 - Mathematics</option>
                  <option value="2">Exam 2 - Science</option>
                  <option value="3">Exam 3 - English</option>
                  <option value="4">Exam 4 - History</option>
                  <option value="5">Custom Exam</option>
                </select>
              </div>

              {/* File Upload Area */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  Upload File
                </label>
                <div
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                  className={`relative border-2 border-dashed rounded-xl p-8 sm:p-12 transition-all ${
                    dragActive
                      ? "border-purple-500 bg-purple-50"
                      : "border-gray-300 bg-gray-50 hover:border-purple-400"
                  }`}
                >
                  <input
                    type="file"
                    id="file-input"
                    accept="image/*,application/pdf,.doc,.docx"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="hidden"
                  />

                  <label htmlFor="file-input" className="cursor-pointer block">
                    <div className="text-center">
                      <DocumentArrowUpIcon className="w-12 h-12 text-purple-500 mx-auto mb-4" />
                      <p className="text-lg font-semibold text-gray-900 mb-2">
                        {file ? file.name : "Drag & drop your file here"}
                      </p>
                      <p className="text-gray-600 text-sm mb-4">
                        or click to browse from your computer
                      </p>
                      <p className="text-xs text-gray-500">
                        Supported formats: PDF, Images (JPG, PNG), DOC, DOCX
                      </p>
                    </div>
                  </label>

                  {file && (
                    <div className="mt-6 pt-6 border-t border-gray-200">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-gray-900">{file.name}</p>
                          <p className="text-xs text-gray-600 mt-1">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                        <button
                          type="button"
                          onClick={() => setFile(null)}
                          className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded transition-colors"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Upload Button */}
              <button
                type="submit"
                disabled={loading || !file}
                className="w-full mt-8 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-lg hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Uploading...
                  </>
                ) : (
                  <>
                    <DocumentArrowUpIcon className="w-5 h-5" />
                    Upload Answer Sheet
                  </>
                )}
              </button>
            </form>

            {/* Info Box */}
            <div className="mt-8 pt-8 border-t border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-4">📋 Instructions:</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">1.</span>
                  <span>Select the exam you're submitting answers for</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">2.</span>
                  <span>Upload a clear image or document of your answer sheet</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">3.</span>
                  <span>Our AI system will automatically evaluate your answers</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">4.</span>
                  <span>Check your dashboard for results within minutes</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
