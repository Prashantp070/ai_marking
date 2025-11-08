import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    setMessage(null);

    try {
      console.log("Attempting login...", { email });
      const response = await axios.post("/api/v1/auth/login", {
        email,
        password,
      });

      console.log("Login response:", response.data);
      if (response.data.access_token) {
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("refresh_token", response.data.refresh_token || "");
        setMessage("Login successful! Redirecting...");
        setTimeout(() => {
          navigate("/");
        }, 1000);
      }
    } catch (error: any) {
      console.error("Login error details:", {
        message: error?.message,
        code: error?.code,
        status: error?.response?.status,
        data: error?.response?.data,
        fullError: error
      });
      
      const errorMessage = error?.response?.data?.detail || error?.message || "Login failed. Please try again.";
      
      if (error?.code === "ERR_NETWORK" || error?.message?.includes("Network")) {
        setMessage("Network Error: Backend not reachable. Please check if backend is running on http://localhost:8000");
      } else if (error?.response?.status === 401) {
        setMessage("Invalid email or password. Please try again.");
      } else {
        setMessage(`Login failed: ${errorMessage}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    setMessage(null);

    try {
      console.log("Attempting registration...", { email });
      const response = await axios.post("/api/v1/auth/register", {
        email,
        password,
        full_name: email.split("@")[0], // Use email prefix as name
      });

      console.log("Registration response:", response.data);
      if (response.data.access_token) {
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("refresh_token", response.data.refresh_token || "");
        setMessage("Registration successful! Redirecting...");
        setTimeout(() => {
          navigate("/");
        }, 1000);
      }
    } catch (error: any) {
      console.error("Registration error details:", {
        message: error?.message,
        code: error?.code,
        status: error?.response?.status,
        data: error?.response?.data,
        fullError: error
      });
      
      const errorMessage = error?.response?.data?.detail || error?.message || "Registration failed. Please try again.";
      
      if (error?.code === "ERR_NETWORK" || error?.message?.includes("Network")) {
        setMessage("Network Error: Backend not reachable. Please check if backend is running on http://localhost:8000");
      } else {
        setMessage(`Registration failed: ${errorMessage}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900 px-4">
      <div className="w-full max-w-md space-y-8 rounded-lg border border-slate-800 bg-slate-900/60 p-8">
        <div>
          <h1 className="text-center text-3xl font-semibold text-white">AI Evaluator</h1>
          <p className="mt-2 text-center text-sm text-slate-400">Login or Register to continue</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300">Email</label>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              className="mt-1 w-full rounded border border-slate-700 bg-slate-800 px-3 py-2 text-slate-100 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="your@email.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300">Password</label>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              className="mt-1 w-full rounded border border-slate-700 bg-slate-800 px-3 py-2 text-slate-100 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="Enter your password"
            />
          </div>
          {message && (
            <p className={`text-sm ${message.includes("successful") ? "text-green-400" : "text-red-400"}`}>
              {message}
            </p>
          )}
          <div className="flex gap-4">
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 rounded bg-primary px-4 py-2 font-semibold text-white hover:bg-primary/80 disabled:opacity-50"
            >
              {isLoading ? "Loading..." : "Login"}
            </button>
            <button
              type="button"
              onClick={handleRegister}
              disabled={isLoading}
              className="flex-1 rounded border border-slate-700 bg-slate-800 px-4 py-2 font-semibold text-slate-300 hover:bg-slate-700 disabled:opacity-50"
            >
              {isLoading ? "Loading..." : "Register"}
            </button>
          </div>
        </form>

        <div className="mt-4 rounded bg-slate-800/50 p-4 text-xs text-slate-400">
          <p className="font-semibold text-slate-300">Demo Credentials:</p>
          <p>Email: teacher@example.com</p>
          <p>Password: Password123!</p>
        </div>
      </div>
    </div>
  );
}

