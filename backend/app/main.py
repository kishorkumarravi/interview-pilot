from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import engine, Base
from app.api.routes import auth, lessons, system_design, coding, interviews, star, resume, progress

settings = get_settings()

app = FastAPI(title="InterviewPilot API", version="1.0.0")

origins = [s.strip() for s in settings.frontend_url.split(",") if s.strip()]
if "http://localhost:3000" not in origins:
    origins.append("http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(system_design.router, prefix="/api")
app.include_router(coding.router, prefix="/api")
app.include_router(interviews.router, prefix="/api")
app.include_router(star.router, prefix="/api")
app.include_router(resume.router, prefix="/api")
app.include_router(progress.router, prefix="/api")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    from app.seed.seed_data import seed_all
    seed_all()


@app.get("/api/health")
def health():
    return {"status": "ok", "provider": settings.ai_provider}
