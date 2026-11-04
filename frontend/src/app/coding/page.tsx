"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Loading from "@/components/ui/Loading";
import Tabs from "@/components/ui/Tabs";
import { fetchCodingProblems } from "@/lib/api";
import type { CodingProblem } from "@/types";
import { Code } from "lucide-react";

export default function CodingPage() {
  const router = useRouter();
  const [problems, setProblems] = useState<CodingProblem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [category, setCategory] = useState("All");
  const [difficulty, setDifficulty] = useState("All");
  const [categories, setCategories] = useState<string[]>(["All"]);

  useEffect(() => {
    fetchCodingProblems()
      .then((data: CodingProblem[]) => {
        setProblems(data);
        const cats = Array.from(new Set(data.map((p: CodingProblem) => p.category)));
        setCategories(["All", ...cats]);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = problems.filter((p) => {
    if (category !== "All" && p.category !== category) return false;
    if (difficulty !== "All" && p.difficulty !== difficulty.toLowerCase()) return false;
    return true;
  });

  const difficultyVariant = (d: string) => {
    switch (d) {
      case "easy":
        return "easy" as const;
      case "medium":
        return "medium" as const;
      case "hard":
        return "hard" as const;
      default:
        return "default" as const;
    }
  };

  return (
    <AuthLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Coding Practice</h1>
          <p className="text-slate-400 mt-1">
            Sharpen your problem-solving skills
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <Tabs
            tabs={categories}
            activeTab={category}
            onTabChange={setCategory}
            className="flex-1"
          />
          <Tabs
            tabs={["All", "Easy", "Medium", "Hard"]}
            activeTab={difficulty}
            onTabChange={setDifficulty}
          />
        </div>

        {loading ? (
          <Loading message="Loading problems..." />
        ) : error ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-12 text-slate-500">No problems found.</div>
        ) : (
          <div className="space-y-3">
            {filtered.map((problem) => (
              <div
                key={problem.id}
                onClick={() => router.push(`/coding/${problem.slug}`)}
                className="flex items-center justify-between p-4 bg-slate-800 border border-slate-700 rounded-xl hover:border-blue-500/50 cursor-pointer transition-all"
              >
                <div className="flex items-center gap-4">
                  <div className="p-2 bg-slate-700 rounded-lg">
                    <Code className="w-5 h-5 text-green-400" />
                  </div>
                  <div>
                    <h3 className="font-medium text-white">{problem.title}</h3>
                    <p className="text-sm text-slate-500">{problem.category}</p>
                  </div>
                </div>
                <Badge variant={difficultyVariant(problem.difficulty)}>
                  {problem.difficulty}
                </Badge>
              </div>
            ))}
          </div>
        )}
      </div>
    </AuthLayout>
  );
}
