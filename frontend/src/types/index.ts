export interface Lesson {
  id: number;
  slug: string;
  title: string;
  category: string;
  difficulty: string;
  order_index: number;
  content: string;
  examples: { title: string; code?: string; description?: string }[];
  exercises: { question: string; hint: string }[];
  tags: string[];
}

export interface LessonSummary {
  id: number;
  slug: string;
  title: string;
  category: string;
  difficulty: string;
  order_index: number;
  tags: string[];
}

export interface Quiz {
  id: number;
  lesson_id: number;
  question: string;
  options: string[];
  correct_index: number;
  explanation: string;
}

export interface QuizResult {
  is_correct: boolean;
  correct_index: number;
  explanation: string;
}

export interface SystemDesignProblem {
  id: number;
  slug: string;
  title: string;
  category: string;
  difficulty: string;
  description: string;
  requirements: { functional: string[]; non_functional: string[] };
  estimation_hints: Record<string, string>;
  api_design: Record<string, string>;
  schema_design: Record<string, string>;
  scaling_notes: string;
  failure_modes: string[];
  trade_offs: string[];
  diagram_description: string;
}

export interface SystemDesignProblemSummary {
  id: number;
  slug: string;
  title: string;
  category: string;
  difficulty: string;
}

export interface CodingProblem {
  id: number;
  slug: string;
  title: string;
  category: string;
  difficulty: string;
  description: string;
  examples: { input: string; output: string; explanation?: string }[];
  constraints: string[];
  hints: string[];
  solution_java: string;
  solution_python: string;
  test_cases: { input: string; expected: string }[];
  time_complexity: string;
  space_complexity: string;
}

export interface CodingProblemSummary {
  id: number;
  slug: string;
  title: string;
  category: string;
  difficulty: string;
}

export interface InterviewSession {
  id: number;
  interview_type: string;
  topic: string;
  status: string;
  overall_score: number | null;
  feedback_summary: string;
  scores: Record<string, number>;
  started_at: string;
  ended_at: string | null;
  messages: InterviewMessage[];
}

export interface InterviewSessionSummary {
  id: number;
  interview_type: string;
  topic: string;
  status: string;
  overall_score: number | null;
  started_at: string;
  ended_at: string | null;
}

export interface InterviewMessage {
  id: number;
  role: string;
  content: string;
  created_at: string;
}

export interface StarQuestion {
  id: number;
  category: string;
  question: string;
  tips: string[];
}

export interface StarAttempt {
  id: number;
  question_id: number;
  situation: string;
  task: string;
  action: string;
  result: string;
  ai_feedback: string;
  score: number | null;
  attempted_at: string;
}

export interface Progress {
  lessons_completed: number;
  total_lessons: number;
  quizzes_passed: number;
  total_quizzes: number;
  coding_solved: number;
  total_coding: number;
  interviews_done: number;
  total_hours: number;
  skill_scores: Record<string, number>;
  recommendations: string[];
}
