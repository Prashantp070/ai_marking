type QuestionRow = {
  id: number;
  number: string;
  text: string;
  marks: number;
};

type Props = {
  rows: QuestionRow[];
};

export default function AdminTable({ rows }: Props) {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-800">
      <table className="min-w-full divide-y divide-slate-800">
        <thead className="bg-slate-900/80">
          <tr className="text-left text-xs uppercase tracking-wider text-slate-400">
            <th className="px-4 py-3">ID</th>
            <th className="px-4 py-3">Question</th>
            <th className="px-4 py-3">Marks</th>
            <th className="px-4 py-3">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800 bg-slate-900/40 text-sm text-slate-200">
          {rows.map((row) => (
            <tr key={row.id}>
              <td className="px-4 py-3 text-slate-400">{row.number}</td>
              <td className="px-4 py-3">{row.text}</td>
              <td className="px-4 py-3">{row.marks}</td>
              <td className="px-4 py-3 text-right">
                <button className="text-sm text-primary hover:underline">Edit</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

