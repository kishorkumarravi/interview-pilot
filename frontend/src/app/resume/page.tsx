"use client";

import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Loading from "@/components/ui/Loading";
import { analyseResume } from "@/lib/api";
import { FileText, Send } from "lucide-react";

export default function ResumePage() {
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [analysis, setAnalysis] = useState<string | null>(null);

  const handleAnalyse = async () => {
    if (!resumeText.trim()) return;
    setLoading(true);
    setError("");
    try {
      const result = await analyseResume(resumeText, jobDescription || undefined);
      setAnalysis(result.analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Resume Analyser</h1>
          <p className="text-slate-400 mt-1">
            Get AI-powered feedback on your resume
          </p>
        </div>

        <Card title="Your Resume" className="mb-6">
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste your resume text here..."
            className="w-full h-64 bg-slate-900 border border-slate-600 rounded-lg p-4 text-slate-200 placeholder-slate-500 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
        </Card>

        <Card title="Job Description (Optional)" className="mb-6">
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description for targeted analysis..."
            className="w-full h-40 bg-slate-900 border border-slate-600 rounded-lg p-4 text-slate-200 placeholder-slate-500 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
        </Card>

        {error && (
          <div className="mb-6 p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        )}

        <div className="flex justify-end mb-8">
          <Button onClick={handleAnalyse} loading={loading} disabled={!resumeText.trim()} size="lg">
            <FileText className="w-4 h-4 mr-2" />
            Analyse Resume
          </Button>
        </div>

        {loading && <Loading message="Analysing your resume..." />}

        {analysis && (
          <Card title="Analysis" className="mt-6">
            <div className="prose prose-invert max-w-none text-sm text-slate-300">
              <ReactMarkdown>{analysis}</ReactMarkdown>
            </div>
          </Card>
        )}
      </div>
    </AuthLayout>
  );
}
