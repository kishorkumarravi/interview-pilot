"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import Loading from "@/components/ui/Loading";
import Tabs from "@/components/ui/Tabs";
import { fetchCodingProblem, submitCodingAttempt } from "@/lib/api";
import type { CodingProblem } from "@/types";
import { ArrowLeft, Send, Eye, EyeOff, ChevronDown, ChevronUp } from "lucide-react";
import Link from "next/link";

export default function CodingDetailPage() {
  const params = useParams();
  const slug = params.slug as string;

  const [problem, setProblem] = useState<CodingProblem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [language, setLanguage] = useState("java");
  const [code, setCode] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<{ status: string; passed: boolean } | null>(null);
  const [showSolution, setShowSolution] = useState(false);
  const [showHints, setShowHints] = useState(false);

  useEffect(() => {
    fetchCodingProblem(slug)
      .then((data: CodingProblem) => {
        setProblem(data);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [slug]);

  const handleSubmit = async () => {
    if (!problem || !code.trim()) return;
    setSubmitting(true);
    try {
      const res = await submitCodingAttempt(problem.id, language, code);
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Submission failed");
    } finally {
      setSubmitting(false);
    }
  };

  const solution = language === "java" ? problem?.solution_java : problem?.solution_python;

  return (
    <AuthLayout>
      <div className="max-w-6xl mx-auto">
        <Link
          href="/coding"
          className="inline-flex items-center gap-2 text-slate-400 hover:text-slate-200 mb-6 text-sm"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Coding Practice
        </Link>

        {loading ? (
          <Loading message="Loading problem..." />
        ) : error && !problem ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        ) : problem ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="space-y-6">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <Badge
                    variant={
                      problem.difficulty === "easy"
                        ? "easy"
                        : problem.difficulty === "medium"
                        ? "medium"
                        : "hard"
                    }
                  >
                    {problem.difficulty}
                  </Badge>
                  <Badge variant="default">{problem.category}</Badge>
                </div>
                <h1 className="text-2xl font-bold text-white">{problem.title}</h1>
              </div>

              <Card>
                <div className="prose prose-invert max-w-none text-slate-300 text-sm">
                  <ReactMarkdown>{problem.description}</ReactMarkdown>
                </div>
              </Card>

              {problem.examples && problem.examples.length > 0 && (
                <Card title="Examples">
                  {problem.examples.map((ex, i) => (
                    <div key={i} className="mb-4 last:mb-0 p-3 bg-slate-900/50 rounded-lg">
                      <div className="text-sm">
                        <p className="text-slate-400">
                          <span className="text-slate-500">Input: </span>
                          <code className="text-blue-300">{ex.input}</code>
                        </p>
                        <p className="text-slate-400 mt-1">
                          <span className="text-slate-500">Output: </span>
                          <code className="text-green-300">{ex.output}</code>
                        </p>
                        {ex.explanation && (
                          <p className="text-slate-500 mt-1 text-xs">{ex.explanation}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </Card>
              )}

              {problem.constraints && problem.constraints.length > 0 && (
                <Card title="Constraints">
                  <ul className="space-y-1">
                    {problem.constraints.map((c, i) => (
                      <li key={i} className="text-sm text-slate-400">- {c}</li>
                    ))}
                  </ul>
                </Card>
              )}

              {problem.hints && problem.hints.length > 0 && (
                <Card>
                  <button
                    onClick={() => setShowHints(!showHints)}
                    className="flex items-center gap-2 text-sm text-amber-400 hover:text-amber-300"
                  >
                    {showHints ? (
                      <ChevronUp className="w-4 h-4" />
                    ) : (
                      <ChevronDown className="w-4 h-4" />
                    )}
                    {showHints ? "Hide" : "Show"} Hints ({problem.hints.length})
                  </button>
                  {showHints && (
                    <ul className="mt-3 space-y-2">
                      {problem.hints.map((hint, i) => (
                        <li key={i} className="text-sm text-slate-400">
                          {i + 1}. {hint}
                        </li>
                      ))}
                    </ul>
                  )}
                </Card>
              )}

              <Card>
                <div className="flex items-center gap-2 text-sm text-slate-400">
                  <span>Time: {problem.time_complexity}</span>
                  <span className="text-slate-600">|</span>
                  <span>Space: {problem.space_complexity}</span>
                </div>
              </Card>
            </div>

            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <Tabs
                  tabs={["java", "python"]}
                  activeTab={language}
                  onTabChange={setLanguage}
                />
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowSolution(!showSolution)}
                >
                  {showSolution ? (
                    <EyeOff className="w-4 h-4 mr-1" />
                  ) : (
                    <Eye className="w-4 h-4 mr-1" />
                  )}
                  {showSolution ? "Hide" : "Show"} Solution
                </Button>
              </div>

              {showSolution && solution && (
                <Card>
                  <h3 className="text-sm font-semibold text-slate-300 mb-2">
                    Reference Solution ({language})
                  </h3>
                  <pre className="text-sm">
                    <code>{solution}</code>
                  </pre>
                </Card>
              )}

              <div>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder={`Write your ${language} solution here...`}
                  className="w-full h-96 bg-slate-900 border border-slate-600 rounded-lg p-4 text-slate-200 placeholder-slate-500 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                  spellCheck={false}
                />
                <div className="flex justify-end mt-4">
                  <Button
                    onClick={handleSubmit}
                    loading={submitting}
                    disabled={!code.trim()}
                  >
                    <Send className="w-4 h-4 mr-2" />
                    Submit Code
                  </Button>
                </div>
              </div>

              {result && (
                <Card title="Result">
                  <div className="flex items-center gap-3">
                    <Badge variant={result.passed ? "success" : "warning"}>
                      {result.passed ? "Submitted" : "Failed"}
                    </Badge>
                    <span className="text-sm text-slate-400">{result.status}</span>
                  </div>
                </Card>
              )}

              {error && problem && (
                <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
                  {error}
                </div>
              )}
            </div>
          </div>
        ) : null}
      </div>
    </AuthLayout>
  );
}
