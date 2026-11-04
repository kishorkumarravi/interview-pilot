import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import engine, Base
from app.seed.seed_data import seed_all

Base.metadata.create_all(bind=engine)
seed_all()

client = TestClient(app)


_registered = False

def _login() -> str:
    global _registered
    if not _registered:
        resp = client.post("/api/auth/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
        })
        assert resp.status_code in (200, 409)
        _registered = True
    resp = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123",
    })
    assert resp.status_code == 200
    return resp.json()["access_token"]


def _headers():
    return {"Authorization": f"Bearer {_login()}"}


class TestHealth:
    def test_health(self):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


class TestAuth:
    def test_login_success(self):
        token = _login()
        assert token

    def test_login_wrong_password(self):
        resp = client.post("/api/auth/login", json={"email": "test@example.com", "password": "wrong"})
        assert resp.status_code == 401

    def test_register_duplicate(self):
        resp = client.post("/api/auth/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
        })
        assert resp.status_code == 409


class TestLessons:
    def test_list_lessons(self):
        resp = client.get("/api/lessons", headers=_headers())
        assert resp.status_code == 200
        lessons = resp.json()
        assert len(lessons) > 0

    def test_list_categories(self):
        resp = client.get("/api/lessons/categories", headers=_headers())
        assert resp.status_code == 200
        cats = resp.json()
        assert "java" in cats

    def test_get_lesson_by_slug(self):
        resp = client.get("/api/lessons", headers=_headers())
        slug = resp.json()[0]["slug"]
        resp2 = client.get(f"/api/lessons/{slug}", headers=_headers())
        assert resp2.status_code == 200
        assert resp2.json()["content"]

    def test_get_quizzes(self):
        resp = client.get("/api/lessons", headers=_headers())
        slug = resp.json()[0]["slug"]
        resp2 = client.get(f"/api/lessons/{slug}/quizzes", headers=_headers())
        assert resp2.status_code == 200


class TestSystemDesign:
    def test_list_problems(self):
        resp = client.get("/api/system-design", headers=_headers())
        assert resp.status_code == 200
        assert len(resp.json()) >= 25

    def test_get_problem(self):
        resp = client.get("/api/system-design", headers=_headers())
        slug = resp.json()[0]["slug"]
        resp2 = client.get(f"/api/system-design/{slug}", headers=_headers())
        assert resp2.status_code == 200
        data = resp2.json()
        assert data["requirements"]
        assert data["estimation_hints"]


class TestCoding:
    def test_list_problems(self):
        resp = client.get("/api/coding", headers=_headers())
        assert resp.status_code == 200
        assert len(resp.json()) >= 70

    def test_filter_by_difficulty(self):
        resp = client.get("/api/coding?difficulty=easy", headers=_headers())
        assert resp.status_code == 200
        for p in resp.json():
            assert p["difficulty"] == "easy"

    def test_get_problem(self):
        resp = client.get("/api/coding", headers=_headers())
        slug = resp.json()[0]["slug"]
        resp2 = client.get(f"/api/coding/{slug}", headers=_headers())
        assert resp2.status_code == 200
        data = resp2.json()
        assert data["solution_java"]
        assert data["solution_python"]


class TestInterviews:
    def test_start_and_message(self):
        headers = _headers()
        resp = client.post(
            "/api/interviews/start",
            json={"interview_type": "backend", "topic": "microservices"},
            headers=headers,
        )
        assert resp.status_code == 200
        session = resp.json()
        assert session["status"] == "active"
        assert len(session["messages"]) > 0

        resp2 = client.post(
            f"/api/interviews/{session['id']}/message",
            json={"content": "I would use event-driven architecture with Kafka."},
            headers=headers,
        )
        assert resp2.status_code == 200
        assert resp2.json()["role"] == "assistant"

    def test_end_interview(self):
        headers = _headers()
        resp = client.post(
            "/api/interviews/start",
            json={"interview_type": "system_design"},
            headers=headers,
        )
        session_id = resp.json()["id"]
        resp2 = client.post(f"/api/interviews/{session_id}/end", headers=headers)
        assert resp2.status_code == 200
        assert resp2.json()["status"] == "completed"

    def test_list_history(self):
        headers = _headers()
        resp = client.get("/api/interviews", headers=headers)
        assert resp.status_code == 200


class TestSTAR:
    def test_list_questions(self):
        resp = client.get("/api/star", headers=_headers())
        assert resp.status_code == 200
        assert len(resp.json()) >= 50


class TestResume:
    def test_analyse(self):
        resp = client.post(
            "/api/resume/analyse",
            json={
                "resume_text": "Senior Backend Engineer with 11 years experience in Java, Spring Boot, microservices.",
                "job_description": "Staff Engineer needed for distributed systems team.",
            },
            headers=_headers(),
        )
        assert resp.status_code == 200
        assert resp.json()["analysis"]


class TestProgress:
    def test_get_progress(self):
        resp = client.get("/api/progress", headers=_headers())
        assert resp.status_code == 200
        data = resp.json()
        assert "lessons_completed" in data
        assert "recommendations" in data
        assert "skill_scores" in data
