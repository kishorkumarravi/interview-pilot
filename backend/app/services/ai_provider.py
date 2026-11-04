from abc import ABC, abstractmethod
import anthropic
from app.core.config import get_settings

settings = get_settings()


class AIProvider(ABC):
    @abstractmethod
    def chat(self, system_prompt: str, messages: list[dict], max_tokens: int = 4096) -> str:
        ...


class AnthropicProvider(AIProvider):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def chat(self, system_prompt: str, messages: list[dict], max_tokens: int = 4096) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text


class DemoProvider(AIProvider):
    RESPONSES = {
        "interview_start": (
            "Welcome! I'm your AI interviewer. Let's begin.\n\n"
            "Tell me about a complex distributed system you've designed or worked on. "
            "What were the key technical challenges, and how did you address them?"
        ),
        "interview_followup": (
            "That's interesting. Let me dig deeper:\n\n"
            "1. How did you handle data consistency across services?\n"
            "2. What was your approach to failure recovery?\n"
            "3. How did you monitor and observe the system in production?\n\n"
            "Please walk me through your thought process on any of these."
        ),
        "interview_end": (
            "## Interview Assessment\n\n"
            "**Overall Score: 7.5/10**\n\n"
            "### Strengths\n"
            "- Strong understanding of distributed systems concepts\n"
            "- Good articulation of trade-offs\n"
            "- Practical experience evident\n\n"
            "### Areas for Improvement\n"
            "- Could provide more specific metrics and numbers\n"
            "- Consider discussing failure scenarios more proactively\n"
            "- Explore alternative approaches before settling on a solution\n\n"
            "### Recommendations\n"
            "- Practice explaining capacity estimation with concrete numbers\n"
            "- Prepare examples of production incidents and how you resolved them\n"
            "- Study CAP theorem trade-offs for different database choices"
        ),
        "star_feedback": (
            "## STAR Response Feedback\n\n"
            "**Score: 7/10**\n\n"
            "**Situation:** Clear context provided. Consider adding more about the business impact.\n\n"
            "**Task:** Well-defined responsibility. Good ownership language.\n\n"
            "**Action:** Strong technical detail. Include more about collaboration and leadership.\n\n"
            "**Result:** Good outcome. Quantify impact with metrics where possible.\n\n"
            "**Tips:** Lead with the most impressive metric. Practice the 2-minute version."
        ),
        "resume_analysis": (
            "## Resume Analysis\n\n"
            "**Match Score: 72%**\n\n"
            "### Strengths\n"
            "- Strong backend engineering experience\n"
            "- Relevant distributed systems work\n\n"
            "### Gaps to Address\n"
            "- Add more quantified achievements\n"
            "- Highlight Canadian work authorization\n"
            "- Include system design leadership examples\n\n"
            "### Suggested Improvements\n"
            "- Lead each bullet with an action verb and a metric\n"
            "- Tailor technology keywords to the job description\n"
            "- Add a summary section targeting Staff/Principal level"
        ),
        "system_design_feedback": (
            "## System Design Review\n\n"
            "**Score: 7/10**\n\n"
            "### What Went Well\n"
            "- Good high-level architecture\n"
            "- Reasonable API design\n\n"
            "### Missing Elements\n"
            "- Capacity estimation needs more detail\n"
            "- Consider adding caching layer\n"
            "- Discuss database sharding strategy\n\n"
            "### Suggestions\n"
            "- Start with requirements clarification\n"
            "- Use back-of-envelope math for every component\n"
            "- Discuss monitoring and alerting"
        ),
    }

    def __init__(self):
        self._call_count = 0

    def chat(self, system_prompt: str, messages: list[dict], max_tokens: int = 4096) -> str:
        self._call_count += 1
        last_msg = messages[-1]["content"].lower() if messages else ""

        if "end" in last_msg or "done" in last_msg or "finish" in last_msg:
            return self.RESPONSES["interview_end"]
        if "resume" in system_prompt.lower():
            return self.RESPONSES["resume_analysis"]
        if "star" in system_prompt.lower():
            return self.RESPONSES["star_feedback"]
        if "system design" in system_prompt.lower() and "review" in system_prompt.lower():
            return self.RESPONSES["system_design_feedback"]

        if self._call_count <= 1 or len(messages) <= 1:
            return self.RESPONSES["interview_start"]
        return self.RESPONSES["interview_followup"]


def get_ai_provider() -> AIProvider:
    if settings.ai_provider == "anthropic" and settings.anthropic_api_key:
        return AnthropicProvider()
    return DemoProvider()
