"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { startInterview } from "@/lib/api";
import { Mic, ArrowRight } from "lucide-react";

const INTERVIEW_TYPES = [
  { value: "coding", label: "Coding Interview", desc: "Data structures, algorithms, and problem solving" },
  { value: "system_design", label: "System Design", desc: "Large-scale distributed system design" },
  { value: "backend", label: "Backend Engineering", desc: "APIs, databases, and server architecture" },
  { value: "distributed", label: "Distributed Systems", desc: "Consensus, replication, and fault tolerance" },
  { value: "staff", label: "Staff+ Engineering", desc: "Technical leadership and architectural decisions" },
  { value: "behavioural", label: "Behavioural", desc: "Leadership, teamwork, and conflict resolution" },
];

export default function InterviewPage() {
  const router = useRouter();
  const [selectedType, setSelectedType] = useState("");
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleStart = async () => {
    if (!selectedType) return;
    setLoading(true);
    setError("");
    try {
      const session = await startInterview(selectedType, topic || undefined);
      router.push(`/interview/${session.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start interview");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div className="max-w-3xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Mock Interview</h1>
          <p className="text-slate-400 mt-1">
            Practice with an AI interviewer in a realistic setting
          </p>
        </div>

        <Card title="Select Interview Type" className="mb-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {INTERVIEW_TYPES.map((type) => (
              <button
                key={type.value}
                onClick={() => setSelectedType(type.value)}
                className={`text-left p-4 rounded-xl border transition-all ${
                  selectedType === type.value
                    ? "border-blue-500 bg-blue-600/10"
                    : "border-slate-700 hover:border-slate-600 bg-slate-900/50"
                }`}
              >
                <p className="font-medium text-white text-sm">{type.label}</p>
                <p className="text-xs text-slate-500 mt-1">{type.desc}</p>
              </button>
            ))}
          </div>
        </Card>

        <Card title="Topic (Optional)" className="mb-6">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., Design a URL shortener, Binary trees, Leadership scenarios"
            className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </Card>

        {error && (
          <div className="mb-6 p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        )}

        <Button
          onClick={handleStart}
          loading={loading}
          disabled={!selectedType}
          size="lg"
          className="w-full"
        >
          <Mic className="w-5 h-5 mr-2" />
          Start Interview
          <ArrowRight className="w-4 h-4 ml-2" />
        </Button>
      </div>
    </AuthLayout>
  );
}
