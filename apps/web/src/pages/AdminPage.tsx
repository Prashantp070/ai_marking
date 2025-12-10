import { useState } from "react";

import AdminTable from "../components/AdminTable";

const seedQuestions = [
  { id: 1, number: "Q1", text: "Explain photosynthesis", marks: 5 },
  { id: 2, number: "Q2", text: "Describe Newton's laws", marks: 10 }
];

export default function AdminPage() {
  const [questions, setQuestions] = useState(seedQuestions);

  const handleAdd = () => {
    setQuestions((prev) => [...prev, { id: prev.length + 1, number: `Q${prev.length + 1}`, text: "New question", marks: 5 }]);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-semibold">Admin Management</h1>
        <button onClick={handleAdd} className="rounded bg-primary px-4 py-2 text-sm font-semibold">
          Add Question
        </button>
      </div>
      <AdminTable rows={questions} />
    </div>
  );
}





