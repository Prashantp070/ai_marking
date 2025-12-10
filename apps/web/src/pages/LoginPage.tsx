import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { EnvelopeIcon, LockClosedIcon, EyeIcon, EyeSlashIcon } from "@heroicons/react/24/outline";
import { useApi } from "../api/useApi";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const api = useApi();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      if (response.data?.access_token) {
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("user_email", email);
        navigate("/dashboard");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-blue-500 to-indigo-600 flex items-center justify-center px-4 sm:px-6 lg:px-8">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-white rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
      </div>

      <div className="relative w-full max-w-md">
        {/* Card */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 sm:px-8 py-8 sm:py-10">
            <div className="flex items-center justify-center w-12 h-12 bg-white bg-opacity-20 rounded-xl mx-auto mb-4">
              <span className="text-2xl">📝</span>
            </div>
            <h1 className="text-3xl font-bold text-white text-center">AI Marking</h1>
            <p className="text-blue-100 text-center mt-2 text-sm">Intelligent Answer Evaluation System</p>
          </div>

          {/* Form */}
          <div className="px-6 sm:px-8 py-8 sm:py-10">
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700 text-sm font-medium">{error}</p>
              </div>
            )}

            <form onSubmit={handleLogin} className="space-y-5">
              {/* Email Input */}
              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <EnvelopeIcon className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none"
                    required
                  />
                </div>
              </div>

              {/* Password Input */}
              <div>
                <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <LockClosedIcon className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-10 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? (
                      <EyeSlashIcon className="h-5 w-5" />
                    ) : (
                      <EyeIcon className="h-5 w-5" />
                    )}
                  </button>
                </div>
              </div>

              {/* Login Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full mt-8 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-2.5 rounded-lg hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Signing in...
                  </span>
                ) : (
                  "Sign In"
                )}
              </button>
            </form>

            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Don't have an account?</span>
              </div>
            </div>

            {/* Register Link */}
            <Link
              to="/register"
              className="w-full block text-center px-4 py-2.5 border-2 border-gray-200 rounded-lg font-semibold text-gray-700 hover:bg-gray-50 transition-all"
            >
              Create New Account
            </Link>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-blue-100 text-xs mt-6">
          © 2025 AI Marking System. All rights reserved.
        </p>
      </div>
    </div>
  );
}
