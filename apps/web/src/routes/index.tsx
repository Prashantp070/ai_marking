import { useRoutes } from "react-router-dom";

import AdminPage from "../pages/AdminPage";
import AnalyticsPage from "../pages/AnalyticsPage";
import AuthGuard from "../components/AuthGuard";
import DashboardPage from "../pages/DashboardPage";
import LoginPage from "../pages/LoginPage";
import UploadPage from "../pages/UploadPage";

export default function AppRoutes() {
  const element = useRoutes([
    { path: "/login", element: <LoginPage /> },
    { 
      path: "/", 
      element: (
        <AuthGuard>
          <UploadPage />
        </AuthGuard>
      )
    },
    { 
      path: "/dashboard", 
      element: (
        <AuthGuard>
          <DashboardPage />
        </AuthGuard>
      )
    },
    { 
      path: "/analytics", 
      element: (
        <AuthGuard>
          <AnalyticsPage />
        </AuthGuard>
      )
    },
    { 
      path: "/admin", 
      element: (
        <AuthGuard>
          <AdminPage />
        </AuthGuard>
      )
    }
  ]);

  return element;
}



