"use client";

import React, { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Loading from "@/components/ui/Loading";
import { fetchInterviewHistory, fetchInterviewSession } from "@/lib/api";
import type { InterviewSessionSummary, InterviewSession } from "@/types";
import { History, ChevronDown, ChevronUp, MessageSquare } from "lucide-react";

export default function HistoryPage() {
  const [history, setHistory] = useState<InterviewSessionSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [expandedSession, setExpandedSession] = useState<InterviewSession | null>(null);
  const [expandLoading, setExpandLoading] = useState(false);

  useEffect(() => {
    fetchInterviewHistory()
      .then(setHistory)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const toggleExpand = async (id: number) => {
    if (expandedId === id) {
      setExpandedId(null);
      setExpandedSession(null);
      return;
    }
    setExpandedId(id);
    setExpandLoading(true);
    try {
      const session = await fetchInterviewSession(String(id));
      setExpandedSession(session);
    } catch {
      // ignore
    } finally {
      setExpandLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Interview History</h1>
          <p className="text-slate-400 mt-1">
            Review your past interview sessions
          </p>
        </div>

        {loading ? (
          <Loading message="Loading history..." />
        ) : error ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        ) : history.length === 0 ? (
          <div className="text-center py-12">
            <History className="w-12 h-12 text-slate-600 mx-auto mb-4" />
            <p className="text-slate-500">No interview history yet.</p>
            <p className="text-slate-600 text-sm mt-1">
              Complete a mock interview to see it here.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {history.map((item) => (
              <div key={item.id}>
                <div
                  onClick={() => toggleExpand(item.id)}
                  className="flex items-center justify-between p-4 bg-slate-800 border border-slate-700 rounded-xl hover:border-slate-600 cursor-pointer transition-all"
                >
                  <div className="flex items-center gap-4">
                    <div className="p-2 bg-purple-600/20 rounded-lg">
                      <MessageSquare className="w-5 h-5 text-purple-400" />
                    </div>
                    <div>
                      <p className="font-medium text-white text-sm capitalize">
                        {item.interview_type.replace(/_/g, " ")}
                        {item.topic ? ` - ${item.topic}` : ""}
                      </p>
                      <p className="text-xs text-slate-500 mt-1">
                        {new Date(item.started_at).toLocaleDateString()} at{" "}
                        {new Date(item.started_at).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {item.overall_score !== undefined && item.overall_score !== null && (
                      <Badge variant="info">{item.overall_score}/10</Badge>
                    )}
                    <Badge
                      variant={item.status === "completed" ? "success" : "warning"}
                    >
                      {item.status}
                    </Badge>
                    {expandedId === item.id ? (
                      <ChevronUp className="w-4 h-4 text-slate-500" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-slate-500" />
                    )}
                  </div>
                </div>

                {expandedId === item.id && (
                  <div className="mt-2 ml-4 border-l-2 border-slate-700 pl-4">
                    {expandLoading ? (
                      <Loading message="Loading transcript..." />
                    ) : expandedSession ? (
                      <div className="space-y-3 py-3">
                        {expandedSession.messages.map((msg, i) => (
                          <div
                            key={i}
                            className={`p-3 rounded-lg text-sm ${
                              msg.role === "user"
                                ? "bg-blue-900/20 border border-blue-800/30 ml-8"
                                : "bg-slate-800/50 border border-slate-700/50 mr-8"
                            }`}
                          >
                            <p className="text-xs text-slate-500 mb-1 font-medium capitalize">
                              {msg.role}
                            </p>
                            <div className="prose prose-invert max-w-none text-sm text-slate-300">
                              <ReactMarkdown>{msg.content}</ReactMarkdown>
                            </div>
                          </div>
                        ))}

                        {(expandedSession.overall_score !== null || expandedSession.feedback_summary) && (
                          <Card title="Assessment" className="mt-4">
                            <div className="space-y-3">
                              <div className="flex items-center gap-3">
                                {expandedSession.overall_score !== null && (
                                  <span className="text-2xl font-bold text-blue-400">
                                    {expandedSession.overall_score}/10
                                  </span>
                                )}
                              </div>
                              {expandedSession.feedback_summary && (
                                <div className="prose prose-invert max-w-none text-sm text-slate-300">
                                  <ReactMarkdown>
                                    {expandedSession.feedback_summary}
                                  </ReactMarkdown>
                                </div>
                              )}
                            </div>
                          </Card>
                        )}
                      </div>
                    ) : null}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </AuthLayout>
  );
}
