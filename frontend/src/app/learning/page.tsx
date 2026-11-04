"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Loading from "@/components/ui/Loading";
import Tabs from "@/components/ui/Tabs";
import { fetchLessons } from "@/lib/api";
import type { LessonSummary } from "@/types";
import { BookOpen, Tag } from "lucide-react";

export default function LearningPage() {
  const router = useRouter();
  const [lessons, setLessons] = useState<LessonSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [category, setCategory] = useState("All");
  const [categories, setCategories] = useState<string[]>(["All"]);

  useEffect(() => {
    fetchLessons()
      .then((data: LessonSummary[]) => {
        setLessons(data);
        const cats = Array.from(new Set(data.map((l: LessonSummary) => l.category)));
        setCategories(["All", ...cats]);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = category === "All" ? lessons : lessons.filter((l) => l.category === category);

  const grouped = filtered.reduce<Record<string, LessonSummary[]>>((acc, lesson) => {
    const cat = lesson.category;
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(lesson);
    return acc;
  }, {});

  return (
    <AuthLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Learning Academy</h1>
          <p className="text-slate-400 mt-1">
            Master core concepts for your interviews
          </p>
        </div>

        <Tabs
          tabs={categories}
          activeTab={category}
          onTabChange={setCategory}
          className="mb-6"
        />

        {loading ? (
          <Loading message="Loading lessons..." />
        ) : error ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        ) : Object.keys(grouped).length === 0 ? (
          <div className="text-center py-12 text-slate-500">No lessons found.</div>
        ) : (
          Object.entries(grouped).map(([cat, catLessons]) => (
            <div key={cat} className="mb-8">
              <h2 className="text-lg font-semibold text-slate-200 mb-4 capitalize">
                {cat.replace(/_/g, " ")}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {catLessons.map((lesson) => (
                  <Card
                    key={lesson.id}
                    hover
                    onClick={() => router.push(`/learning/${lesson.slug}`)}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="p-2 bg-blue-600/20 rounded-lg">
                        <BookOpen className="w-5 h-5 text-blue-400" />
                      </div>
                      <Badge
                        variant={
                          lesson.difficulty === "beginner"
                            ? "easy"
                            : lesson.difficulty === "intermediate"
                            ? "medium"
                            : "hard"
                        }
                      >
                        {lesson.difficulty}
                      </Badge>
                    </div>
                    <h3 className="font-semibold text-white mb-2">{lesson.title}</h3>
                    {lesson.tags && lesson.tags.length > 0 && (
                      <div className="flex items-center gap-1 flex-wrap text-sm text-slate-500">
                        <Tag className="w-3.5 h-3.5" />
                        {lesson.tags.join(", ")}
                      </div>
                    )}
                  </Card>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </AuthLayout>
  );
}
