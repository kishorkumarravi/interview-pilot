"use client";

import React, { useEffect, useState } from "react";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import Loading from "@/components/ui/Loading";
import Tabs from "@/components/ui/Tabs";
import { fetchStarQuestions, submitStarAttempt } from "@/lib/api";
import type { StarQuestion, StarAttempt } from "@/types";
import { Star, Send, ChevronDown, ChevronUp } from "lucide-react";
import ReactMarkdown from "react-markdown";

export default function StarCoachPage() {
  const [questions, setQuestions] = useState<StarQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [category, setCategory] = useState("All");
  const [categories, setCategories] = useState<string[]>(["All"]);
  const [selected, setSelected] = useState<StarQuestion | null>(null);
  const [form, setForm] = useState({ situation: "", task: "", action: "", result: "" });
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<StarAttempt | null>(null);
  const [tipsOpen, setTipsOpen] = useState(false);

  useEffect(() => {
    fetchStarQuestions()
      .then((data: StarQuestion[]) => {
        setQuestions(data);
        const cats = Array.from(new Set(data.map((q: StarQuestion) => q.category)));
        setCategories(["All", ...cats]);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = category === "All" ? questions : questions.filter((q) => q.category === category);

  const handleSubmit = async () => {
    if (!selected) return;
    setSubmitting(true);
    try {
      const result = await submitStarAttempt(
        selected.id,
        form.situation,
        form.task,
        form.action,
        form.result
      );
      setFeedback(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Submission failed");
    } finally {
      setSubmitting(false);
    }
  };

  const resetForm = () => {
    setForm({ situation: "", task: "", action: "", result: "" });
    setFeedback(null);
    setTipsOpen(false);
  };

  return (
    <AuthLayout>
      <div className="max-w-5xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">STAR Behavioural Coach</h1>
          <p className="text-slate-400 mt-1">
            Practice structured behavioural responses with AI feedback
          </p>
        </div>

        {loading ? (
          <Loading message="Loading questions..." />
        ) : error ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400 mb-6">
            {error}
          </div>
        ) : !selected ? (
          <>
            <Tabs
              tabs={categories}
              activeTab={category}
              onTabChange={setCategory}
              className="mb-6"
            />

            {filtered.length === 0 ? (
              <div className="text-center py-12 text-slate-500">No questions found.</div>
            ) : (
              <div className="space-y-3">
                {filtered.map((q) => (
                  <div
                    key={q.id}
                    onClick={() => { setSelected(q); resetForm(); }}
                    className="flex items-start gap-4 p-4 bg-slate-800 border border-slate-700 rounded-xl hover:border-blue-500/50 cursor-pointer transition-all"
                  >
                    <div className="p-2 bg-amber-600/20 rounded-lg flex-shrink-0">
                      <Star className="w-5 h-5 text-amber-400" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-white text-sm">{q.question}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge variant="default">{q.category}</Badge>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        ) : (
          <>
            <button
              onClick={() => { setSelected(null); resetForm(); }}
              className="text-slate-400 hover:text-slate-200 text-sm mb-6 inline-flex items-center gap-2"
            >
              <ChevronUp className="w-4 h-4 rotate-[-90deg]" />
              Back to questions
            </button>

            <Card className="mb-6">
              <h2 className="text-lg font-semibold text-white mb-2">{selected.question}</h2>
              <div className="flex items-center gap-2 mb-4">
                <Badge variant="default">{selected.category}</Badge>
              </div>

              {selected.tips && selected.tips.length > 0 && (
                <div className="mb-4">
                  <button
                    onClick={() => setTipsOpen(!tipsOpen)}
                    className="flex items-center gap-1 text-sm text-amber-400 hover:text-amber-300"
                  >
                    {tipsOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    {tipsOpen ? "Hide" : "Show"} Tips
                  </button>
                  {tipsOpen && (
                    <ul className="mt-2 space-y-1">
                      {selected.tips.map((tip, i) => (
                        <li key={i} className="text-sm text-slate-400">- {tip}</li>
                      ))}
                    </ul>
                  )}
                </div>
              )}

            </Card>

            <div className="space-y-4 mb-6">
              {(["situation", "task", "action", "result"] as const).map((field) => (
                <Card key={field}>
                  <h3 className="text-sm font-semibold text-slate-300 mb-2 capitalize">
                    {field}
                  </h3>
                  <textarea
                    value={form[field]}
                    onChange={(e) => setForm((f) => ({ ...f, [field]: e.target.value }))}
                    placeholder={`Describe the ${field}...`}
                    className="w-full h-24 bg-slate-900 border border-slate-600 rounded-lg p-3 text-slate-200 placeholder-slate-500 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  />
                </Card>
              ))}
            </div>

            <div className="flex justify-end mb-6">
              <Button
                onClick={handleSubmit}
                loading={submitting}
                disabled={!form.situation || !form.task || !form.action || !form.result}
              >
                <Send className="w-4 h-4 mr-2" />
                Submit for AI Feedback
              </Button>
            </div>

            {feedback && (
              <Card title="AI Feedback" className="mb-6">
                <div className="space-y-4">
                  {feedback.score !== null && (
                    <div className="flex items-center gap-4">
                      <div className="text-4xl font-bold text-blue-400">
                        {feedback.score}/10
                      </div>
                    </div>
                  )}
                  {feedback.ai_feedback && (
                    <div className="prose prose-invert max-w-none text-sm text-slate-300">
                      <ReactMarkdown>{feedback.ai_feedback}</ReactMarkdown>
                    </div>
                  )}
                </div>
              </Card>
            )}
          </>
        )}
      </div>
    </AuthLayout>
  );
}
