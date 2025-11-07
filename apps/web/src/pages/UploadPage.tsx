import { useState } from "react";

import { useApi } from "../api/useApi";

export default function UploadPage() {
  const api = useApi();
  const [examId, setExamId] = useState("1");
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setMessage("Please select a file to upload");
      return;
    }
    const formData = new FormData();
    formData.append("exam_id", examId);
    formData.append("file", file);

    try {
      const response = await api.post("/uploads", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setMessage(`Upload successful: submission #${response.data.submission_id}`);
    } catch (error) {
      setMessage("Upload failed. Please try again.");
      console.error(error);
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
        {message && <p className="text-sm text-slate-300">{message}</p>}
      </form>
    </div>
  );
}

