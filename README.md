# InterviewPilot - AI Career Coach

A full-stack interview preparation platform built for senior backend engineers targeting Staff, Principal, and Lead positions in Canada.

## Features

- **Learning Academy** - Structured lessons on Java, Spring Boot, Python, DSA, System Design, Distributed Systems, AWS, Azure, Kafka, Redis, and leadership
- **System Design Lab** - 25 real system design problems with requirements, estimation, API design, schemas, scaling, and trade-offs
- **Coding Practice** - 70 DSA problems with Java/Python solutions, tests, hints, and complexity analysis
- **AI Mock Interview Engine** - Coding, system design, backend, distributed systems, Staff Engineer, and behavioural interviews with follow-up questions and scored reports
- **Voice Mock Interviews** - Microphone transcription with text fallback (Web Speech API)
- **STAR Behavioural Coach** - 50 questions with AI-powered STAR response feedback
- **Resume Analyser** - Resume and Canadian job description analysis with match scoring
- **Progress Dashboard** - Skill scores, completion tracking, study hours, and recommendations
- **Interview History** - Persistent history with full transcripts and feedback

## Tech Stack

- **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS 4
- **Backend:** Python FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL (production) / SQLite (local dev)
- **AI:** Anthropic Claude API with provider abstraction and demo mode
- **Infrastructure:** Docker, Docker Compose

## Quick Start (Local - SQLite, no Docker)

### Prerequisites
- Python 3.11+
- Node.js 20+

### 1. Clone and configure

```bash
cd interview-pilot
cp .env.example .env
# Edit .env - set AUTH_PASSWORD and optionally ANTHROPIC_API_KEY
```

### 2. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The backend creates tables and seeds all content on first startup.

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Open http://localhost:3000

Log in with the password you set in `.env`.

## Docker Compose (PostgreSQL)

```bash
cp .env.example .env
# Edit .env - set AUTH_PASSWORD, DATABASE_URL is overridden by compose

docker compose up --build
```

Open http://localhost:3000

## Demo Mode

By default `AI_PROVIDER=demo` - all AI features work with pre-written responses. No API key needed.

To use real Claude AI:
```
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

## Running Tests

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

## API Documentation

With the backend running: http://localhost:8000/docs

## Project Structure

```
interview-pilot/
  backend/
    app/
      api/routes/     # REST endpoints
      core/           # Config, database, auth
      models/         # SQLAlchemy models
      schemas/        # Pydantic schemas
      services/       # Business logic, AI provider
      seed/           # Sample content data
    migrations/       # Alembic migrations
    tests/            # pytest test suite
  frontend/
    src/
      app/            # Next.js pages
      components/     # React components
      lib/            # API client, utilities
      types/          # TypeScript interfaces
  docker-compose.yml
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | sqlite:///./interview_pilot.db | Database connection string |
| SECRET_KEY | change-me-to-a-random-string | JWT signing key |
| AUTH_PASSWORD | change-me | Login password |
| AI_PROVIDER | demo | "demo" or "anthropic" |
| ANTHROPIC_API_KEY | (empty) | Claude API key |
| BACKEND_PORT | 8000 | Backend server port |
| FRONTEND_URL | http://localhost:3000 | Frontend URL for CORS |
