"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Loading from "@/components/ui/Loading";
import { fetchProgress } from "@/lib/api";
import type { Progress } from "@/types";
import {
  BookOpen,
  Code,
  Mic,
  Clock,
  ArrowRight,
  TrendingUp,
  CheckSquare,
} from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const [progress, setProgress] = useState<Progress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchProgress()
      .then(setProgress)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const quickActions = [
    { label: "Start Learning", href: "/learning", icon: BookOpen, color: "bg-blue-600" },
    { label: "Practice Coding", href: "/coding", icon: Code, color: "bg-green-600" },
    { label: "Mock Interview", href: "/interview", icon: Mic, color: "bg-purple-600" },
  ];

  return (
    <AuthLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-slate-400 mt-1">Track your interview preparation progress</p>
        </div>

        {loading ? (
          <Loading message="Loading your progress..." />
        ) : error ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        ) : progress ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
              <Card>
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-blue-600/20 rounded-xl">
                    <BookOpen className="w-6 h-6 text-blue-400" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-white">
                      {progress.lessons_completed}
                      <span className="text-sm text-slate-500 font-normal">
                        /{progress.total_lessons}
                      </span>
                    </p>
                    <p className="text-sm text-slate-400">Lessons</p>
                  </div>
                </div>
              </Card>

              <Card>
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-cyan-600/20 rounded-xl">
                    <CheckSquare className="w-6 h-6 text-cyan-400" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-white">
                      {progress.quizzes_passed}
                      <span className="text-sm text-slate-500 font-normal">
                        /{progress.total_quizzes}
                      </span>
                    </p>
                    <p className="text-sm text-slate-400">Quizzes Passed</p>
                  </div>
                </div>
              </Card>

              <Card>
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-green-600/20 rounded-xl">
                    <Code className="w-6 h-6 text-green-400" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-white">
                      {progress.coding_solved}
                      <span className="text-sm text-slate-500 font-normal">
                        /{progress.total_coding}
                      </span>
                    </p>
                    <p className="text-sm text-slate-400">Coding Solved</p>
                  </div>
                </div>
              </Card>

              <Card>
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-purple-600/20 rounded-xl">
                    <Mic className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-white">
                      {progress.interviews_done}
                    </p>
                    <p className="text-sm text-slate-400">Interviews Done</p>
                  </div>
                </div>
              </Card>

              <Card>
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-amber-600/20 rounded-xl">
                    <Clock className="w-6 h-6 text-amber-400" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-white">
                      {progress.total_hours.toFixed(1)}
                    </p>
                    <p className="text-sm text-slate-400">Study Hours</p>
                  </div>
                </div>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card title="Skill Scores">
                <div className="space-y-3">
                  {Object.entries(progress.skill_scores).map(([skill, score]) => (
                    <div key={skill}>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-slate-300 capitalize">
                          {skill.replace(/_/g, " ")}
                        </span>
                        <span className="text-slate-400">{score}%</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${Math.min(score, 100)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                  {Object.keys(progress.skill_scores).length === 0 && (
                    <p className="text-slate-500 text-sm">
                      No skill data yet. Start practicing to see your scores.
                    </p>
                  )}
                </div>
              </Card>

              <Card title="Recommendations">
                <div className="space-y-3">
                  {progress.recommendations.map((rec, i) => (
                    <div
                      key={i}
                      className="flex items-start gap-3 p-3 bg-slate-900/50 rounded-lg"
                    >
                      <TrendingUp className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-slate-300">{rec}</p>
                    </div>
                  ))}
                  {progress.recommendations.length === 0 && (
                    <p className="text-slate-500 text-sm">
                      Complete some activities to get personalized recommendations.
                    </p>
                  )}
                </div>
              </Card>
            </div>

            <Card title="Quick Actions">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {quickActions.map((action) => {
                  const Icon = action.icon;
                  return (
                    <button
                      key={action.href}
                      onClick={() => router.push(action.href)}
                      className="flex items-center gap-3 p-4 bg-slate-900/50 hover:bg-slate-700/50 rounded-xl transition-colors group"
                    >
                      <div className={`p-2 ${action.color} rounded-lg`}>
                        <Icon className="w-5 h-5 text-white" />
                      </div>
                      <span className="text-sm font-medium text-slate-300 group-hover:text-white">
                        {action.label}
                      </span>
                      <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-slate-400 ml-auto" />
                    </button>
                  );
                })}
              </div>
            </Card>
          </>
        ) : null}
      </div>
    </AuthLayout>
  );
}
