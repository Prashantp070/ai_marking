import { Link, useLocation, useNavigate } from "react-router-dom";
import { Bars3Icon, XMarkIcon, ArrowRightOnRectangleIcon, SparklesIcon } from "@heroicons/react/24/outline";
import { useState } from "react";

const navItems = [
  { label: "Dashboard", path: "/dashboard", icon: "📊" },
  { label: "Upload", path: "/upload", icon: "📤" },
];

type Props = {
  children: React.ReactNode;
};

export default function MainLayout({ children }: Props) {
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const userEmail = localStorage.getItem("user_email") || "User";

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_email");
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white shadow-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/dashboard" className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <SparklesIcon className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                AI Marking
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-1">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    location.pathname === item.path
                      ? "bg-blue-100 text-blue-700"
                      : "text-gray-700 hover:bg-gray-100"
                  }`}
                >
                  <span className="mr-1">{item.icon}</span>
                  {item.label}
                </Link>
              ))}
            </nav>

            {/* User Section */}
            <div className="hidden md:flex items-center gap-4">
              <div className="text-sm">
                <p className="text-gray-600">Logged in as</p>
                <p className="font-semibold text-gray-900">{userEmail}</p>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 font-semibold rounded-lg hover:bg-red-100 transition-colors"
              >
                <ArrowRightOnRectangleIcon className="w-5 h-5" />
                Logout
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              {mobileMenuOpen ? (
                <XMarkIcon className="w-6 h-6 text-gray-700" />
              ) : (
                <Bars3Icon className="w-6 h-6 text-gray-700" />
              )}
            </button>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <div className="md:hidden mt-4 pt-4 border-t border-gray-200 space-y-2">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`block px-4 py-2 rounded-lg font-medium transition-all ${
                    location.pathname === item.path
                      ? "bg-blue-100 text-blue-700"
                      : "text-gray-700 hover:bg-gray-100"
                  }`}
                >
                  <span className="mr-1">{item.icon}</span>
                  {item.label}
                </Link>
              ))}
              <div className="pt-2 border-t border-gray-200">
                <p className="text-xs text-gray-600 px-4 py-2">Logged in as</p>
                <p className="font-semibold text-gray-900 px-4 py-1">{userEmail}</p>
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="w-full mt-2 flex items-center justify-center gap-2 px-4 py-2 bg-red-50 text-red-600 font-semibold rounded-lg hover:bg-red-100 transition-colors"
                >
                  <ArrowRightOnRectangleIcon className="w-5 h-5" />
                  Logout
                </button>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="min-h-[calc(100vh-80px)]">{children}</main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-sm text-gray-600">
          <p>© 2025 AI Marking System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}





