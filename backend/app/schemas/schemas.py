from pydantic import BaseModel, Field
from datetime import datetime


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=4, max_length=128)


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    name: str
    token_type: str = "bearer"


class LessonOut(BaseModel):
    id: int
    category: str
    title: str
    slug: str
    difficulty: str
    order_index: int
    content: str
    examples: list
    exercises: list
    tags: list

    model_config = {"from_attributes": True}


class LessonSummary(BaseModel):
    id: int
    category: str
    title: str
    slug: str
    difficulty: str
    order_index: int
    tags: list

    model_config = {"from_attributes": True}


class LessonProgressIn(BaseModel):
    lesson_id: int
    completed: bool = True
    score: float = 100.0
    time_spent_minutes: int = 0


class QuizOut(BaseModel):
    id: int
    lesson_id: int
    question: str
    options: list
    correct_index: int
    explanation: str

    model_config = {"from_attributes": True}


class QuizAnswerIn(BaseModel):
    quiz_id: int
    selected_index: int


class QuizAnswerOut(BaseModel):
    is_correct: bool
    correct_index: int
    explanation: str


class SystemDesignProblemOut(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: str
    category: str
    description: str
    requirements: dict
    estimation_hints: dict
    api_design: dict
    schema_design: dict
    scaling_notes: str
    failure_modes: list
    trade_offs: list
    diagram_description: str

    model_config = {"from_attributes": True}


class SystemDesignProblemSummary(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: str
    category: str

    model_config = {"from_attributes": True}


class SystemDesignAttemptIn(BaseModel):
    problem_id: int
    notes: str = ""
    time_spent_minutes: int = 0


class CodingProblemOut(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: str
    category: str
    description: str
    examples: list
    constraints: list
    hints: list
    solution_java: str
    solution_python: str
    test_cases: list
    time_complexity: str
    space_complexity: str

    model_config = {"from_attributes": True}


class CodingProblemSummary(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: str
    category: str

    model_config = {"from_attributes": True}


class CodingAttemptIn(BaseModel):
    problem_id: int
    language: str
    code: str


class InterviewStartIn(BaseModel):
    interview_type: str = Field(description="coding|system_design|backend|distributed|staff|behavioural")
    topic: str = ""


class InterviewMessageIn(BaseModel):
    content: str


class InterviewMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class InterviewSessionOut(BaseModel):
    id: int
    interview_type: str
    topic: str
    status: str
    overall_score: float | None
    feedback_summary: str
    scores: dict
    started_at: datetime
    ended_at: datetime | None
    messages: list[InterviewMessageOut] = []

    model_config = {"from_attributes": True}


class InterviewSessionSummary(BaseModel):
    id: int
    interview_type: str
    topic: str
    status: str
    overall_score: float | None
    started_at: datetime
    ended_at: datetime | None

    model_config = {"from_attributes": True}


class StarQuestionOut(BaseModel):
    id: int
    category: str
    question: str
    tips: list

    model_config = {"from_attributes": True}


class StarAttemptIn(BaseModel):
    question_id: int
    situation: str
    task: str
    action: str
    result: str


class StarAttemptOut(BaseModel):
    id: int
    question_id: int
    situation: str
    task: str
    action: str
    result: str
    ai_feedback: str
    score: float | None
    attempted_at: datetime

    model_config = {"from_attributes": True}


class ResumeAnalyseIn(BaseModel):
    resume_text: str
    job_description: str = ""


class ProgressOut(BaseModel):
    lessons_completed: int
    total_lessons: int
    quizzes_passed: int
    total_quizzes: int
    coding_solved: int
    total_coding: int
    interviews_done: int
    total_hours: float
    skill_scores: dict
    recommendations: list[str]
