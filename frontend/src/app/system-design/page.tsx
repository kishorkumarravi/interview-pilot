"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Loading from "@/components/ui/Loading";
import Tabs from "@/components/ui/Tabs";
import { fetchSystemDesignProblems } from "@/lib/api";
import type { SystemDesignProblemSummary } from "@/types";
import { Boxes } from "lucide-react";

export default function SystemDesignPage() {
  const router = useRouter();
  const [problems, setProblems] = useState<SystemDesignProblemSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [category, setCategory] = useState("All");
  const [categories, setCategories] = useState<string[]>(["All"]);

  useEffect(() => {
    fetchSystemDesignProblems()
      .then((data: SystemDesignProblemSummary[]) => {
        setProblems(data);
        const cats = Array.from(new Set(data.map((p: SystemDesignProblemSummary) => p.category)));
        setCategories(["All", ...cats]);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered =
    category === "All" ? problems : problems.filter((p) => p.category === category);

  return (
    <AuthLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">System Design Lab</h1>
          <p className="text-slate-400 mt-1">
            Practice designing large-scale distributed systems
          </p>
        </div>

        <Tabs
          tabs={categories}
          activeTab={category}
          onTabChange={setCategory}
          className="mb-6"
        />

        {loading ? (
          <Loading message="Loading problems..." />
        ) : error ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-12 text-slate-500">No problems found.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map((problem) => (
              <Card
                key={problem.id}
                hover
                onClick={() => router.push(`/system-design/${problem.slug}`)}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="p-2 bg-purple-600/20 rounded-lg">
                    <Boxes className="w-5 h-5 text-purple-400" />
                  </div>
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
                </div>
                <h3 className="font-semibold text-white mb-2">{problem.title}</h3>
                <div className="flex items-center gap-3 text-sm text-slate-500 mt-2">
                  <Badge variant="default">{problem.category}</Badge>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </AuthLayout>
  );
}
