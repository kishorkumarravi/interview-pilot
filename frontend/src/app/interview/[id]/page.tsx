"use client";

import React, { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Loading from "@/components/ui/Loading";
import {
  fetchInterviewSession,
  sendInterviewMessage,
  endInterview,
} from "@/lib/api";
import type { InterviewSession, InterviewMessage } from "@/types";
import { Send, Square, Mic, MicOff, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function InterviewSessionPage() {
  const params = useParams();
  const sessionId = params.id as string;

  const [session, setSession] = useState<InterviewSession | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [sending, setSending] = useState(false);
  const [ending, setEnding] = useState(false);
  const [listening, setListening] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    fetchInterviewSession(sessionId)
      .then(setSession)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [sessionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [session?.messages]);

  const handleSend = async () => {
    if (!message.trim() || sending) return;
    const content = message.trim();
    setMessage("");
    setSending(true);
    try {
      const userMsg: InterviewMessage = {
        id: Date.now(),
        role: "user",
        content,
        created_at: new Date().toISOString(),
      };
      setSession((prev) =>
        prev ? { ...prev, messages: [...(prev.messages || []), userMsg] } : prev
      );
      const aiMsg = await sendInterviewMessage(sessionId, content);
      setSession((prev) =>
        prev ? { ...prev, messages: [...(prev.messages || []), aiMsg] } : prev
      );
      const refreshed = await fetchInterviewSession(sessionId);
      setSession(refreshed);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
    } finally {
      setSending(false);
    }
  };

  const handleEnd = async () => {
    setEnding(true);
    try {
      const updated = await endInterview(sessionId);
      setSession(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to end interview");
    } finally {
      setEnding(false);
    }
  };

  const toggleVoice = () => {
    if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
      return;
    }

    if (listening) {
      recognitionRef.current?.stop();
      setListening(false);
      return;
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const w = window as any;
    const SpeechRecognitionCtor = w.SpeechRecognition || w.webkitSpeechRecognition;
    if (!SpeechRecognitionCtor) return;

    const recognition = new SpeechRecognitionCtor();
    recognition.continuous = true;
    recognition.interimResults = true;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onresult = (event: any) => {
      let transcript = "";
      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      setMessage(transcript);
    };

    recognition.onerror = () => {
      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
    recognitionRef.current = recognition;
    setListening(true);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const isEnded = session?.status === "completed" || session?.status === "ended";

  return (
    <AuthLayout>
      <div className="max-w-4xl mx-auto flex flex-col" style={{ height: "calc(100vh - 8rem)" }}>
        <div className="flex items-center justify-between mb-4">
          <Link
            href="/interview"
            className="inline-flex items-center gap-2 text-slate-400 hover:text-slate-200 text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </Link>
          <div className="flex items-center gap-3">
            {session && (
              <span className="text-sm text-slate-500 capitalize">
                {session.interview_type.replace(/_/g, " ")}
                {session.topic ? ` - ${session.topic}` : ""}
              </span>
            )}
            {!isEnded && session && (
              <Button variant="danger" size="sm" onClick={handleEnd} loading={ending}>
                <Square className="w-4 h-4 mr-1" />
                End Interview
              </Button>
            )}
          </div>
        </div>

        {loading ? (
          <Loading message="Loading interview..." />
        ) : error && !session ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        ) : session ? (
          <>
            <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
              {session.messages.map((msg: InterviewMessage, i: number) => (
                <div
                  key={i}
                  className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[80%] p-4 rounded-2xl ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white rounded-br-md"
                        : "bg-slate-800 text-slate-200 border border-slate-700 rounded-bl-md"
                    }`}
                  >
                    <div className="prose prose-invert max-w-none text-sm">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                    <p className="text-xs mt-2 opacity-50">
                      {new Date(msg.created_at).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              {sending && (
                <div className="flex justify-start">
                  <div className="bg-slate-800 border border-slate-700 p-4 rounded-2xl rounded-bl-md">
                    <div className="flex items-center gap-2 text-sm text-slate-400">
                      <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-blue-500"></div>
                      Thinking...
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {isEnded && (session.overall_score !== null || session.feedback_summary) && (
              <Card title="Assessment Report" className="mb-4">
                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    {session.overall_score !== null && (
                      <div className="text-4xl font-bold text-blue-400">
                        {session.overall_score}/10
                      </div>
                    )}
                    {session.feedback_summary && (
                      <div className="prose prose-invert max-w-none text-sm text-slate-300">
                        <ReactMarkdown>{session.feedback_summary}</ReactMarkdown>
                      </div>
                    )}
                  </div>
                  {session.scores && Object.keys(session.scores).length > 0 && (
                    <div>
                      <h4 className="text-sm font-semibold text-slate-400 mb-2">Score Breakdown</h4>
                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                        {Object.entries(session.scores).map(([key, value]) => (
                          <div key={key} className="p-3 bg-slate-900/50 rounded-lg text-center">
                            <p className="text-xs text-slate-500 capitalize">{key.replace(/_/g, " ")}</p>
                            <p className="text-lg font-bold text-white">{value}/10</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Card>
            )}

            {!isEnded && (
              <div className="flex items-end gap-2">
                <button
                  onClick={toggleVoice}
                  className={`p-3 rounded-xl transition-colors ${
                    listening
                      ? "bg-red-600 text-white"
                      : "bg-slate-800 text-slate-400 hover:text-white border border-slate-700"
                  }`}
                  title={listening ? "Stop recording" : "Start voice input"}
                >
                  {listening ? (
                    <MicOff className="w-5 h-5" />
                  ) : (
                    <Mic className="w-5 h-5" />
                  )}
                </button>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type your response..."
                  className="flex-1 px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={2}
                />
                <Button onClick={handleSend} disabled={!message.trim() || sending}>
                  <Send className="w-5 h-5" />
                </Button>
              </div>
            )}
          </>
        ) : null}
      </div>
    </AuthLayout>
  );
}
