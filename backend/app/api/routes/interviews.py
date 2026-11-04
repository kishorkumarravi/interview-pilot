from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import InterviewSession, InterviewMessage
from app.schemas.schemas import (
    InterviewStartIn, InterviewMessageIn, InterviewMessageOut,
    InterviewSessionOut, InterviewSessionSummary,
)
from app.services.interview_service import start_interview, send_message, end_interview

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("/start", response_model=InterviewSessionOut)
def start(
    req: InterviewStartIn,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    session = start_interview(db, int(user_id), req.interview_type, req.topic)
    messages = db.query(InterviewMessage).filter_by(session_id=session.id).order_by(InterviewMessage.id).all()
    return InterviewSessionOut(
        id=session.id,
        interview_type=session.interview_type,
        topic=session.topic,
        status=session.status,
        overall_score=session.overall_score,
        feedback_summary=session.feedback_summary or "",
        scores=session.scores or {},
        started_at=session.started_at,
        ended_at=session.ended_at,
        messages=[InterviewMessageOut.model_validate(m) for m in messages],
    )


@router.post("/{session_id}/message", response_model=InterviewMessageOut)
def message(
    session_id: int,
    req: InterviewMessageIn,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    try:
        ai_msg = send_message(db, session_id, int(user_id), req.content)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return InterviewMessageOut.model_validate(ai_msg)


@router.post("/{session_id}/end", response_model=InterviewSessionOut)
def end(
    session_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    try:
        session = end_interview(db, session_id, int(user_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    messages = db.query(InterviewMessage).filter_by(session_id=session.id).order_by(InterviewMessage.id).all()
    return InterviewSessionOut(
        id=session.id,
        interview_type=session.interview_type,
        topic=session.topic,
        status=session.status,
        overall_score=session.overall_score,
        feedback_summary=session.feedback_summary or "",
        scores=session.scores or {},
        started_at=session.started_at,
        ended_at=session.ended_at,
        messages=[InterviewMessageOut.model_validate(m) for m in messages],
    )


@router.get("", response_model=list[InterviewSessionSummary])
def list_sessions(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    return (
        db.query(InterviewSession)
        .filter_by(user_id=int(user_id))
        .order_by(InterviewSession.id.desc())
        .limit(50)
        .all()
    )


@router.get("/{session_id}", response_model=InterviewSessionOut)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    session = db.query(InterviewSession).filter_by(id=session_id, user_id=int(user_id)).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = db.query(InterviewMessage).filter_by(session_id=session.id).order_by(InterviewMessage.id).all()
    return InterviewSessionOut(
        id=session.id,
        interview_type=session.interview_type,
        topic=session.topic,
        status=session.status,
        overall_score=session.overall_score,
        feedback_summary=session.feedback_summary or "",
        scores=session.scores or {},
        started_at=session.started_at,
        ended_at=session.ended_at,
        messages=[InterviewMessageOut.model_validate(m) for m in messages],
    )
