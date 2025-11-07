import { useRoutes } from "react-router-dom";

import AdminPage from "../pages/AdminPage";
import AnalyticsPage from "../pages/AnalyticsPage";
import DashboardPage from "../pages/DashboardPage";
import UploadPage from "../pages/UploadPage";

export default function AppRoutes() {
  const element = useRoutes([
    { path: "/", element: <UploadPage /> },
    { path: "/dashboard", element: <DashboardPage /> },
    { path: "/analytics", element: <AnalyticsPage /> },
    { path: "/admin", element: <AdminPage /> }
  ]);

  return element;
}

