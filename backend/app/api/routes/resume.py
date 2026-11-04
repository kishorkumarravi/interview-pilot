from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.schemas.schemas import ResumeAnalyseIn
from app.services.ai_provider import get_ai_provider

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/analyse")
def analyse_resume(req: ResumeAnalyseIn, _user: str = Depends(get_current_user)):
    provider = get_ai_provider()
    prompt = (
        "You are a resume and job description analyst specializing in Canadian tech job market. "
        "Analyse the resume against the job description. Provide: match score, strengths, gaps, "
        "keyword suggestions, and specific improvements. Focus on Staff/Principal/Lead engineer roles."
    )
    content = f"Resume:\n{req.resume_text}"
    if req.job_description:
        content += f"\n\nJob Description:\n{req.job_description}"
    analysis = provider.chat(prompt, [{"role": "user", "content": content}])
    return {"analysis": analysis}
