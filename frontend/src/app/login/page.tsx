"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { login, register, setToken, setUserName, getToken } from "@/lib/api";
import Button from "@/components/ui/Button";
import {
  ArrowRight,
  Brain,
  Code2,
  MessageSquare,
  BarChart3,
  BookOpen,
  Boxes,
} from "lucide-react";

const FEATURES = [
  { icon: BookOpen, label: "22 Lessons", desc: "Core backend concepts" },
  { icon: Boxes, label: "25 System Design", desc: "Real-world problems" },
  { icon: Code2, label: "70 Coding Problems", desc: "Java & Python" },
  { icon: MessageSquare, label: "AI Mock Interviews", desc: "6 interview types" },
  { icon: Brain, label: "STAR Coach", desc: "Behavioural prep" },
  { icon: BarChart3, label: "Progress Tracking", desc: "Skill analytics" },
];

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (getToken()) {
      router.replace("/dashboard");
    }
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data =
        mode === "register"
          ? await register(name, email, password)
          : await login(email, password);
      setToken(data.access_token);
      setUserName(data.name);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left panel - branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-950 via-slate-900 to-indigo-950 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500 rounded-full blur-3xl" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-indigo-500 rounded-full blur-3xl" />
          <div className="absolute top-1/2 left-1/3 w-64 h-64 bg-cyan-500 rounded-full blur-3xl" />
        </div>

        <div className="relative z-10 flex flex-col justify-center px-16 w-full">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-blue-500/20 border border-blue-500/30 rounded-xl flex items-center justify-center">
              <Brain className="w-7 h-7 text-blue-400" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white tracking-tight">InterviewPilot</h1>
              <p className="text-blue-300/80 text-sm font-medium">AI Career Coach</p>
            </div>
          </div>

          <p className="text-slate-300 text-lg mt-6 mb-10 max-w-md leading-relaxed">
            Your personal AI-powered platform for mastering backend engineering interviews.
            Staff, Principal, Lead - level up your career.
          </p>

          <div className="grid grid-cols-2 gap-4">
            {FEATURES.map(({ icon: Icon, label, desc }) => (
              <div
                key={label}
                className="flex items-start gap-3 p-3 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm"
              >
                <div className="mt-0.5 p-1.5 rounded-lg bg-blue-500/15">
                  <Icon className="w-4 h-4 text-blue-400" />
                </div>
                <div>
                  <p className="text-white text-sm font-semibold">{label}</p>
                  <p className="text-slate-400 text-xs">{desc}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-12 flex items-center gap-4 text-sm text-slate-500">
            <span>Next.js</span>
            <span className="w-1 h-1 rounded-full bg-slate-600" />
            <span>FastAPI</span>
            <span className="w-1 h-1 rounded-full bg-slate-600" />
            <span>Claude AI</span>
            <span className="w-1 h-1 rounded-full bg-slate-600" />
            <span>PostgreSQL</span>
          </div>
        </div>
      </div>

      {/* Right panel - auth form */}
      <div className="flex-1 flex items-center justify-center px-6 bg-slate-950">
        <div className="w-full max-w-sm">
          {/* Mobile-only branding */}
          <div className="lg:hidden text-center mb-10">
            <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-500/20 border border-blue-500/30 rounded-xl mb-4">
              <Brain className="w-8 h-8 text-blue-400" />
            </div>
            <h1 className="text-2xl font-bold text-white">InterviewPilot</h1>
            <p className="text-slate-400 text-sm mt-1">AI Career Coach</p>
          </div>

          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white">
              {mode === "login" ? "Welcome back" : "Create your account"}
            </h2>
            <p className="text-slate-400 mt-1">
              {mode === "login"
                ? "Sign in to continue your preparation"
                : "Start your interview preparation journey"}
            </p>
          </div>

          {/* Login / Register toggle */}
          <div className="flex bg-slate-900 rounded-xl p-1 mb-6">
            <button
              type="button"
              onClick={() => { setMode("login"); setError(""); }}
              className={`flex-1 py-2 text-sm font-medium rounded-lg transition-all ${
                mode === "login"
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Sign In
            </button>
            <button
              type="button"
              onClick={() => { setMode("register"); setError(""); }}
              className={`flex-1 py-2 text-sm font-medium rounded-lg transition-all ${
                mode === "register"
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Sign Up
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {mode === "register" && (
              <div className="mb-4">
                <label htmlFor="name" className="block text-sm font-medium text-slate-300 mb-2">
                  Name
                </label>
                <input
                  id="name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your name"
                  className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  required
                />
              </div>
            )}

            <div className="mb-4">
              <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                autoFocus
                required
              />
            </div>

            <div className="mb-6">
              <label htmlFor="password" className="block text-sm font-medium text-slate-300 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={mode === "register" ? "Choose a password (4+ chars)" : "Enter your password"}
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                required
              />
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-900/20 border border-red-800/50 rounded-xl text-red-400 text-sm">
                {error}
              </div>
            )}

            <Button type="submit" loading={loading} className="w-full" size="lg">
              {mode === "login" ? "Sign In" : "Create Account"}
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </form>

          <p className="text-center text-xs text-slate-600 mt-8">
            Designed for Senior Backend Engineers targeting Staff+ roles
          </p>
        </div>
      </div>
    </div>
  );
}
