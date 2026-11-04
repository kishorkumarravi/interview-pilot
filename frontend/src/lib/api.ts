const TOKEN_KEY = "interview_pilot_token";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem("interview_pilot_name");
}

async function apiFetch(path: string, options: RequestInit = {}): Promise<Response> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> || {}),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(`/api${path}`, { ...options, headers });
  if (res.status === 401) {
    clearToken();
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new Error("Unauthorized");
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || body.message || `Request failed: ${res.status}`);
  }
  return res;
}

// Auth
export async function login(email: string, password: string): Promise<{ access_token: string; name: string }> {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Login failed");
  }
  return res.json();
}

export async function register(name: string, email: string, password: string): Promise<{ access_token: string; name: string }> {
  const res = await fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Registration failed");
  }
  return res.json();
}

export function getUserName(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("interview_pilot_name");
}

export function setUserName(name: string): void {
  localStorage.setItem("interview_pilot_name", name);
}

// Lessons
export async function fetchLessons(category?: string) {
  const params = category ? `?category=${encodeURIComponent(category)}` : "";
  const res = await apiFetch(`/lessons${params}`);
  return res.json();
}

export async function fetchLesson(slug: string) {
  const res = await apiFetch(`/lessons/${slug}`);
  return res.json();
}

export async function fetchQuizzes(slug: string) {
  const res = await apiFetch(`/lessons/${slug}/quizzes`);
  return res.json();
}

export async function submitQuiz(quizId: number, selectedIndex: number) {
  const res = await apiFetch("/lessons/quizzes/answer", {
    method: "POST",
    body: JSON.stringify({ quiz_id: quizId, selected_index: selectedIndex }),
  });
  return res.json();
}

export async function markLessonProgress(
  lessonId: number,
  completed: boolean,
  score: number,
  timeSpent: number
) {
  const res = await apiFetch("/lessons/progress", {
    method: "POST",
    body: JSON.stringify({
      lesson_id: lessonId,
      completed,
      score,
      time_spent_minutes: timeSpent,
    }),
  });
  return res.json();
}

// System Design
export async function fetchSystemDesignProblems(category?: string) {
  const params = category ? `?category=${encodeURIComponent(category)}` : "";
  const res = await apiFetch(`/system-design${params}`);
  return res.json();
}

export async function fetchSystemDesignProblem(slug: string) {
  const res = await apiFetch(`/system-design/${slug}`);
  return res.json();
}

export async function submitSystemDesignAttempt(
  problemId: number,
  notes: string,
  timeSpent: number
) {
  const res = await apiFetch("/system-design/attempt", {
    method: "POST",
    body: JSON.stringify({
      problem_id: problemId,
      notes,
      time_spent_minutes: timeSpent,
    }),
  });
  return res.json();
}

// Coding
export async function fetchCodingProblems(category?: string, difficulty?: string) {
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  if (difficulty) params.set("difficulty", difficulty);
  const query = params.toString() ? `?${params.toString()}` : "";
  const res = await apiFetch(`/coding${query}`);
  return res.json();
}

export async function fetchCodingProblem(slug: string) {
  const res = await apiFetch(`/coding/${slug}`);
  return res.json();
}

export async function submitCodingAttempt(
  problemId: number,
  language: string,
  code: string
) {
  const res = await apiFetch("/coding/attempt", {
    method: "POST",
    body: JSON.stringify({ problem_id: problemId, language, code }),
  });
  return res.json();
}

// Interview
export async function startInterview(type: string, topic?: string) {
  const res = await apiFetch("/interviews/start", {
    method: "POST",
    body: JSON.stringify({ interview_type: type, topic: topic || "" }),
  });
  return res.json();
}

export async function sendInterviewMessage(sessionId: string, content: string) {
  const res = await apiFetch(`/interviews/${sessionId}/message`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
  return res.json();
}

export async function endInterview(sessionId: string) {
  const res = await apiFetch(`/interviews/${sessionId}/end`, {
    method: "POST",
  });
  return res.json();
}

export async function fetchInterviewHistory() {
  const res = await apiFetch("/interviews");
  return res.json();
}

export async function fetchInterviewSession(sessionId: string) {
  const res = await apiFetch(`/interviews/${sessionId}`);
  return res.json();
}

// STAR
export async function fetchStarQuestions(category?: string) {
  const params = category ? `?category=${encodeURIComponent(category)}` : "";
  const res = await apiFetch(`/star${params}`);
  return res.json();
}

export async function submitStarAttempt(
  questionId: number,
  situation: string,
  task: string,
  action: string,
  result: string
) {
  const res = await apiFetch("/star/attempt", {
    method: "POST",
    body: JSON.stringify({
      question_id: questionId,
      situation,
      task,
      action,
      result,
    }),
  });
  return res.json();
}

// Resume
export async function analyseResume(resumeText: string, jobDescription?: string) {
  const res = await apiFetch("/resume/analyse", {
    method: "POST",
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription || "",
    }),
  });
  return res.json();
}

// Progress
export async function fetchProgress() {
  const res = await apiFetch("/progress");
  return res.json();
}
