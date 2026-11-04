"use client";

import React, { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import Loading from "@/components/ui/Loading";
import Tabs from "@/components/ui/Tabs";
import { fetchSystemDesignProblem, submitSystemDesignAttempt } from "@/lib/api";
import type { SystemDesignProblem } from "@/types";
import { ArrowLeft, Clock, Send, Play, Square } from "lucide-react";
import Link from "next/link";

const DESIGN_TABS = [
  "Requirements",
  "Estimation",
  "API Design",
  "Schema",
  "Architecture",
  "Scaling",
  "Failures",
  "Trade-offs",
];

export default function SystemDesignDetailPage() {
  const params = useParams();
  const slug = params.slug as string;

  const [problem, setProblem] = useState<SystemDesignProblem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("Requirements");
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [timerRunning, setTimerRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    fetchSystemDesignProblem(slug)
      .then(setProblem)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [slug]);

  useEffect(() => {
    if (timerRunning) {
      timerRef.current = setInterval(() => setElapsed((e) => e + 1), 1000);
    } else if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [timerRunning]);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  const handleSubmit = async () => {
    if (!problem || !notes.trim()) return;
    setSubmitting(true);
    setTimerRunning(false);
    try {
      const result = await submitSystemDesignAttempt(
        problem.id,
        notes,
        Math.ceil(elapsed / 60)
      );
      setFeedback(result.feedback || result.analysis || JSON.stringify(result));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Submission failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthLayout>
      <div className="max-w-5xl mx-auto">
        <Link
          href="/system-design"
          className="inline-flex items-center gap-2 text-slate-400 hover:text-slate-200 mb-6 text-sm"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to System Design Lab
        </Link>

        {loading ? (
          <Loading message="Loading problem..." />
        ) : error && !problem ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        ) : problem ? (
          <>
            <div className="flex items-start justify-between mb-6">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <Badge
                    variant={
                      problem.difficulty === "medium"
                        ? "medium"
                        : problem.difficulty === "hard"
                        ? "hard"
                        : "easy"
                    }
                  >
                    {problem.difficulty}
                  </Badge>
                  <Badge variant="default">{problem.category}</Badge>
                </div>
                <h1 className="text-3xl font-bold text-white">{problem.title}</h1>
                <p className="text-slate-400 mt-2">{problem.description}</p>
              </div>
            </div>

            <div className="flex items-center gap-4 mb-6">
              <div className="flex items-center gap-2 bg-slate-800 px-4 py-2 rounded-lg border border-slate-700">
                <Clock className="w-4 h-4 text-slate-400" />
                <span className="text-lg font-mono text-white">{formatTime(elapsed)}</span>
              </div>
              <Button
                variant={timerRunning ? "danger" : "primary"}
                size="sm"
                onClick={() => setTimerRunning(!timerRunning)}
              >
                {timerRunning ? (
                  <>
                    <Square className="w-4 h-4 mr-1" /> Stop
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 mr-1" /> Start Timer
                  </>
                )}
              </Button>
            </div>

            {problem.requirements && (
              <Card title="Requirements" className="mb-6">
                {problem.requirements.functional && problem.requirements.functional.length > 0 && (
                  <div className="mb-4">
                    <h3 className="text-sm font-semibold text-slate-400 mb-2">Functional</h3>
                    <ul className="space-y-2">
                      {problem.requirements.functional.map((req: string, i: number) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                          <span className="text-blue-400 mt-1">-</span>
                          {req}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {problem.requirements.non_functional && problem.requirements.non_functional.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-slate-400 mb-2">Non-Functional</h3>
                    <ul className="space-y-2">
                      {problem.requirements.non_functional.map((req: string, i: number) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                          <span className="text-purple-400 mt-1">-</span>
                          {req}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </Card>
            )}

            {problem.estimation_hints && Object.keys(problem.estimation_hints).length > 0 && (
              <Card title="Estimation Hints" className="mb-6">
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                  {Object.entries(problem.estimation_hints).map(([key, value]) => (
                    <div key={key} className="p-3 bg-slate-900/50 rounded-lg">
                      <p className="text-xs text-slate-500 capitalize">{key.replace(/_/g, " ")}</p>
                      <p className="text-sm font-medium text-white mt-1">{value}</p>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            <Tabs tabs={DESIGN_TABS} activeTab={activeTab} onTabChange={setActiveTab} className="mb-4" />

            <Card className="mb-6">
              {activeTab === "Requirements" && problem.requirements && (
                <div className="space-y-4">
                  {problem.requirements.functional?.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-slate-400 mb-2">Functional Requirements</h3>
                      <ul className="space-y-1">
                        {problem.requirements.functional.map((r: string, i: number) => (
                          <li key={i} className="text-sm text-slate-300">- {r}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {problem.requirements.non_functional?.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-slate-400 mb-2">Non-Functional Requirements</h3>
                      <ul className="space-y-1">
                        {problem.requirements.non_functional.map((r: string, i: number) => (
                          <li key={i} className="text-sm text-slate-300">- {r}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {activeTab === "Estimation" && problem.estimation_hints && Object.keys(problem.estimation_hints).length > 0 && (
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                  {Object.entries(problem.estimation_hints).map(([key, value]) => (
                    <div key={key} className="p-3 bg-slate-900/50 rounded-lg">
                      <p className="text-xs text-slate-500 capitalize">{key.replace(/_/g, " ")}</p>
                      <p className="text-sm font-medium text-white mt-1">{value}</p>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === "API Design" && problem.api_design && Object.keys(problem.api_design).length > 0 && (
                <div className="space-y-3">
                  {Object.entries(problem.api_design).map(([key, value]) => (
                    <div key={key} className="p-3 bg-slate-900/50 rounded-lg">
                      <p className="text-xs text-slate-500 capitalize font-semibold">{key.replace(/_/g, " ")}</p>
                      <p className="text-sm text-slate-300 mt-1 whitespace-pre-wrap">{value}</p>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === "Schema" && problem.schema_design && Object.keys(problem.schema_design).length > 0 && (
                <div className="space-y-3">
                  {Object.entries(problem.schema_design).map(([key, value]) => (
                    <div key={key} className="p-3 bg-slate-900/50 rounded-lg">
                      <p className="text-xs text-slate-500 capitalize font-semibold">{key.replace(/_/g, " ")}</p>
                      <p className="text-sm text-slate-300 mt-1 whitespace-pre-wrap">{value}</p>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === "Architecture" && problem.diagram_description && (
                <div className="prose prose-invert max-w-none text-sm text-slate-300">
                  <ReactMarkdown>{problem.diagram_description}</ReactMarkdown>
                </div>
              )}

              {activeTab === "Scaling" && problem.scaling_notes && (
                <div className="prose prose-invert max-w-none text-sm text-slate-300">
                  <ReactMarkdown>{problem.scaling_notes}</ReactMarkdown>
                </div>
              )}

              {activeTab === "Failures" && problem.failure_modes && problem.failure_modes.length > 0 && (
                <ul className="space-y-2">
                  {problem.failure_modes.map((mode: string, i: number) => (
                    <li key={i} className="text-sm text-slate-300">- {mode}</li>
                  ))}
                </ul>
              )}

              {activeTab === "Trade-offs" && problem.trade_offs && problem.trade_offs.length > 0 && (
                <ul className="space-y-2">
                  {problem.trade_offs.map((t: string, i: number) => (
                    <li key={i} className="text-sm text-slate-300">- {t}</li>
                  ))}
                </ul>
              )}
            </Card>

            <Card title="Your Notes" className="mb-6">
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Write your design notes here..."
                className="w-full h-64 bg-slate-900 border border-slate-600 rounded-lg p-4 text-slate-200 placeholder-slate-500 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              />
              <div className="flex justify-end mt-4">
                <Button
                  onClick={handleSubmit}
                  loading={submitting}
                  disabled={!notes.trim()}
                >
                  <Send className="w-4 h-4 mr-2" />
                  Submit for AI Review
                </Button>
              </div>
            </Card>

            {feedback && (
              <Card title="AI Feedback" className="mb-6">
                <div className="prose prose-invert max-w-none text-slate-300">
                  <ReactMarkdown>{feedback}</ReactMarkdown>
                </div>
              </Card>
            )}

            {error && problem && (
              <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400 mb-6">
                {error}
              </div>
            )}
          </>
        ) : null}
      </div>
    </AuthLayout>
  );
}
