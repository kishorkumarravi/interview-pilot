"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import AuthLayout from "@/components/layout/AuthLayout";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import Loading from "@/components/ui/Loading";
import { fetchLesson, fetchQuizzes, submitQuiz, markLessonProgress } from "@/lib/api";
import type { Lesson, Quiz, QuizResult } from "@/types";
import { ArrowLeft, CheckCircle, XCircle, ChevronDown, ChevronUp } from "lucide-react";
import Link from "next/link";

export default function LessonDetailPage() {
  const params = useParams();
  const slug = params.slug as string;

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [quizAnswers, setQuizAnswers] = useState<Record<number, number>>({});
  const [quizResults, setQuizResults] = useState<Record<number, QuizResult>>({});
  const [submittingQuiz, setSubmittingQuiz] = useState<number | null>(null);
  const [marking, setMarking] = useState(false);
  const [marked, setMarked] = useState(false);
  const [exerciseOpen, setExerciseOpen] = useState<Record<number, boolean>>({});

  useEffect(() => {
    Promise.all([fetchLesson(slug), fetchQuizzes(slug)])
      .then(([lessonData, quizData]) => {
        setLesson(lessonData);
        setQuizzes(quizData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [slug]);

  const handleQuizSubmit = async (quizId: number) => {
    const selectedIndex = quizAnswers[quizId];
    if (selectedIndex === undefined) return;
    setSubmittingQuiz(quizId);
    try {
      const result = await submitQuiz(quizId, selectedIndex);
      setQuizResults((prev) => ({ ...prev, [quizId]: result }));
    } catch (err) {
      // ignore
    } finally {
      setSubmittingQuiz(null);
    }
  };

  const handleMarkComplete = async () => {
    if (!lesson) return;
    setMarking(true);
    try {
      const correctCount = Object.values(quizResults).filter((r) => r.is_correct).length;
      const score = quizzes.length > 0 ? Math.round((correctCount / quizzes.length) * 100) : 100;
      await markLessonProgress(lesson.id, true, score, 0);
      setMarked(true);
    } catch {
      // ignore
    } finally {
      setMarking(false);
    }
  };

  return (
    <AuthLayout>
      <div className="max-w-4xl mx-auto">
        <Link
          href="/learning"
          className="inline-flex items-center gap-2 text-slate-400 hover:text-slate-200 mb-6 text-sm"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Learning Academy
        </Link>

        {loading ? (
          <Loading message="Loading lesson..." />
        ) : error ? (
          <div className="p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-400">
            {error}
          </div>
        ) : lesson ? (
          <>
            <div className="mb-8">
              <div className="flex items-center gap-3 mb-2">
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
              <h1 className="text-3xl font-bold text-white">{lesson.title}</h1>
            </div>

            {lesson.tags && lesson.tags.length > 0 && (
              <Card className="mb-6">
                <h2 className="text-lg font-semibold text-white mb-3">Topics</h2>
                <div className="flex flex-wrap gap-2">
                  {lesson.tags.map((tag, i) => (
                    <Badge key={i} variant="info">{tag}</Badge>
                  ))}
                </div>
              </Card>
            )}

            <Card className="mb-6">
              <div className="prose prose-invert max-w-none text-slate-300 leading-relaxed">
                <ReactMarkdown>{lesson.content}</ReactMarkdown>
              </div>
            </Card>

            {lesson.examples && lesson.examples.length > 0 && (
              <Card title="Examples" className="mb-6">
                {lesson.examples.map((example, i) => (
                  <div key={i} className="mb-6 last:mb-0">
                    <h3 className="text-sm font-semibold text-slate-200 mb-2">
                      {example.title}
                    </h3>
                    {example.code && (
                      <pre className="mb-2">
                        <code>{example.code}</code>
                      </pre>
                    )}
                    {example.description && (
                      <p className="text-sm text-slate-400">{example.description}</p>
                    )}
                  </div>
                ))}
              </Card>
            )}

            {lesson.exercises && lesson.exercises.length > 0 && (
              <Card title="Exercises" className="mb-6">
                {lesson.exercises.map((exercise, i) => (
                  <div key={i} className="mb-4 last:mb-0 p-4 bg-slate-900/50 rounded-lg">
                    <p className="text-slate-200 mb-2">{exercise.question}</p>
                    <button
                      onClick={() =>
                        setExerciseOpen((prev) => ({ ...prev, [i]: !prev[i] }))
                      }
                      className="flex items-center gap-1 text-sm text-blue-400 hover:text-blue-300"
                    >
                      {exerciseOpen[i] ? (
                        <ChevronUp className="w-4 h-4" />
                      ) : (
                        <ChevronDown className="w-4 h-4" />
                      )}
                      {exerciseOpen[i] ? "Hide" : "Show"} hint
                    </button>
                    {exerciseOpen[i] && (
                      <div className="mt-3 space-y-2">
                        <p className="text-sm text-amber-400">
                          Hint: {exercise.hint}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </Card>
            )}

            {quizzes.length > 0 && (
              <Card title="Quiz" className="mb-6">
                {quizzes.map((quiz) => (
                  <div key={quiz.id} className="mb-6 last:mb-0 p-4 bg-slate-900/50 rounded-lg">
                    <p className="text-slate-200 font-medium mb-3">{quiz.question}</p>
                    <div className="space-y-2 mb-3">
                      {quiz.options.map((option, oi) => {
                        const result = quizResults[quiz.id];
                        const selected = quizAnswers[quiz.id] === oi;
                        let optClass = "border-slate-600 hover:border-slate-500";
                        if (result) {
                          if (oi === result.correct_index) {
                            optClass = "border-green-500 bg-green-900/20";
                          } else if (selected && !result.is_correct) {
                            optClass = "border-red-500 bg-red-900/20";
                          }
                        } else if (selected) {
                          optClass = "border-blue-500 bg-blue-900/20";
                        }
                        return (
                          <button
                            key={oi}
                            onClick={() => {
                              if (!result) {
                                setQuizAnswers((prev) => ({ ...prev, [quiz.id]: oi }));
                              }
                            }}
                            disabled={!!result}
                            className={`w-full text-left px-4 py-3 border rounded-lg text-sm text-slate-300 transition-colors ${optClass}`}
                          >
                            {option}
                          </button>
                        );
                      })}
                    </div>
                    {quizResults[quiz.id] ? (
                      <div className="flex items-start gap-2">
                        {quizResults[quiz.id].is_correct ? (
                          <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                        ) : (
                          <XCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                        )}
                        <p className="text-sm text-slate-400">
                          {quizResults[quiz.id].explanation}
                        </p>
                      </div>
                    ) : (
                      <Button
                        size="sm"
                        onClick={() => handleQuizSubmit(quiz.id)}
                        loading={submittingQuiz === quiz.id}
                        disabled={quizAnswers[quiz.id] === undefined}
                      >
                        Submit Answer
                      </Button>
                    )}
                  </div>
                ))}
              </Card>
            )}

            <div className="flex justify-end">
              <Button
                onClick={handleMarkComplete}
                loading={marking}
                disabled={marked}
                size="lg"
              >
                {marked ? "Completed" : "Mark as Complete"}
                {marked && <CheckCircle className="w-4 h-4 ml-2" />}
              </Button>
            </div>
          </>
        ) : null}
      </div>
    </AuthLayout>
  );
}
