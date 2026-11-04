from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import InterviewSession, InterviewMessage
from app.services.ai_provider import get_ai_provider

SYSTEM_PROMPTS = {
    "coding": (
        "You are a senior technical interviewer at a top tech company conducting a coding interview. "
        "Ask one coding problem at a time. Wait for the candidate's answer. "
        "Challenge their approach, ask about time/space complexity, suggest edge cases, "
        "and ask follow-up questions about optimization. Be thorough but encouraging. "
        "When the candidate says 'done' or 'end interview', provide a detailed scored report."
    ),
    "system_design": (
        "You are a Staff Engineer conducting a system design interview for a Senior/Staff position. "
        "Present one system design problem. Guide the candidate through: requirements gathering, "
        "capacity estimation, API design, data model, high-level architecture, deep dives on components, "
        "scaling, and failure handling. Ask probing follow-up questions. Challenge assumptions. "
        "When done, provide a scored assessment across: requirements, estimation, API design, "
        "data model, scalability, reliability, and trade-off analysis."
    ),
    "backend": (
        "You are interviewing a candidate for a Senior/Staff Backend Engineer position. "
        "Ask questions about backend concepts: API design, database design, caching strategies, "
        "message queues, microservices patterns, performance optimization, security, "
        "and production operations. One question at a time. Challenge answers with follow-ups. "
        "Assess depth of practical experience. Provide a scored report when done."
    ),
    "distributed": (
        "You are interviewing for a Distributed Systems role. Cover topics like: "
        "CAP theorem, consensus algorithms, distributed transactions, event sourcing, "
        "CQRS, service mesh, observability, chaos engineering, and data replication. "
        "Ask one question at a time, probe for depth, challenge assumptions. "
        "Assess both theoretical knowledge and practical experience."
    ),
    "staff": (
        "You are conducting a Staff/Principal Engineer interview. Focus on: "
        "technical leadership, architecture decisions, cross-team influence, "
        "mentoring, technical strategy, dealing with ambiguity, driving alignment, "
        "and building engineering culture. Ask behavioural and scenario-based questions. "
        "One question at a time. Probe for specific examples with measurable impact."
    ),
    "behavioural": (
        "You are conducting a behavioural interview for a senior engineering leadership role. "
        "Ask about: conflict resolution, handling failure, driving change, "
        "stakeholder management, team building, and decision-making under uncertainty. "
        "Use the STAR framework to evaluate responses. One question at a time. "
        "Ask follow-ups to probe depth and authenticity."
    ),
}


def start_interview(db: Session, user_id: int, interview_type: str, topic: str) -> InterviewSession:
    session = InterviewSession(
        user_id=user_id,
        interview_type=interview_type,
        topic=topic,
        status="active",
    )
    db.add(session)
    db.flush()

    system_prompt = SYSTEM_PROMPTS.get(interview_type, SYSTEM_PROMPTS["backend"])
    if topic:
        system_prompt += f"\n\nFocus area: {topic}"

    provider = get_ai_provider()
    opening = provider.chat(system_prompt, [{"role": "user", "content": "Begin the interview."}])

    ai_msg = InterviewMessage(session_id=session.id, role="assistant", content=opening)
    db.add(ai_msg)
    db.commit()
    db.refresh(session)
    return session


def send_message(db: Session, session_id: int, user_id: int, content: str) -> InterviewMessage:
    session = db.query(InterviewSession).filter_by(id=session_id, user_id=user_id).first()
    if not session or session.status != "active":
        raise ValueError("Interview session not found or already ended")

    user_msg = InterviewMessage(session_id=session_id, role="user", content=content)
    db.add(user_msg)
    db.flush()

    messages_db = db.query(InterviewMessage).filter_by(session_id=session_id).order_by(InterviewMessage.id).all()
    chat_messages = [{"role": m.role, "content": m.content} for m in messages_db]

    system_prompt = SYSTEM_PROMPTS.get(session.interview_type, SYSTEM_PROMPTS["backend"])
    if session.topic:
        system_prompt += f"\n\nFocus area: {session.topic}"

    provider = get_ai_provider()
    reply = provider.chat(system_prompt, chat_messages)

    ai_msg = InterviewMessage(session_id=session_id, role="assistant", content=reply)
    db.add(ai_msg)

    end_keywords = {"end interview", "done", "finish interview", "stop interview"}
    if any(kw in content.lower() for kw in end_keywords):
        session.status = "completed"
        session.ended_at = datetime.now(timezone.utc)
        session.feedback_summary = reply
        session.overall_score = _extract_score(reply)

    db.commit()
    db.refresh(ai_msg)
    return ai_msg


def end_interview(db: Session, session_id: int, user_id: int) -> InterviewSession:
    session = db.query(InterviewSession).filter_by(id=session_id, user_id=user_id).first()
    if not session:
        raise ValueError("Session not found")

    if session.status == "active":
        messages_db = db.query(InterviewMessage).filter_by(session_id=session_id).order_by(InterviewMessage.id).all()
        chat_messages = [{"role": m.role, "content": m.content} for m in messages_db]
        chat_messages.append({"role": "user", "content": "End the interview and provide a detailed scored assessment."})

        system_prompt = SYSTEM_PROMPTS.get(session.interview_type, SYSTEM_PROMPTS["backend"])
        provider = get_ai_provider()
        feedback = provider.chat(system_prompt, chat_messages)

        ai_msg = InterviewMessage(session_id=session_id, role="assistant", content=feedback)
        db.add(ai_msg)

        session.status = "completed"
        session.ended_at = datetime.now(timezone.utc)
        session.feedback_summary = feedback
        session.overall_score = _extract_score(feedback)
        db.commit()

    db.refresh(session)
    return session


def _extract_score(text: str) -> float | None:
    import re
    match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", text)
    if match:
        return float(match.group(1))
    return None
