import { Suspense } from "react";

import MainLayout from "./layouts/MainLayout";
import AppRoutes from "./routes";

function App() {
  return (
    <MainLayout>
      <Suspense fallback={<div className="p-10 text-white">Loading...</div>}>
        <AppRoutes />
      </Suspense>
    </MainLayout>
  );
}

export default App;

