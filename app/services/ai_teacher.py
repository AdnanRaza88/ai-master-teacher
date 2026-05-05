import re
import logging
from typing import Dict, List
from app.models.schemas import TeachingResponse
from app.services.llm_client import LLMClient

logger = logging.getLogger(__name__)

class TeachingEngine:
    SYSTEM_PROMPT = (
        "You are an expert, patient, and strict AI teacher. "
        "Your goal is to make the student truly understand any topic from absolute basics.\n"
        "Rules:\n"
        "1. Mix simple Urdu and English.\n"
        "2. Explain step-by-step.\n"
        "3. Give real-life examples.\n"
        "4. If user is wrong, correct them clearly. NEVER agree.\n"
        "5. Engage with a thoughtful Quick Question.\n"
        "6. Format:\n"
        "   Explanation: ...\n"
        "   Example: ...\n"
        "   Diagram: <ASCII art>\n"
        "   Quick Question: ...\n"
        "No other text outside these sections."
    )

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def get_teaching_response(self, user_message: str, history: List[Dict] = None) -> TeachingResponse:
        raw_output = self.llm.generate(
            system_prompt=self.SYSTEM_PROMPT,
            user_message=user_message,
            history=history,
        )
        parsed = self._parse_structured_output(raw_output)
        return TeachingResponse(**parsed)

    @staticmethod
    def _parse_structured_output(text: str) -> Dict[str, str]:
        sections = {"explanation": "", "example": "", "diagram": "", "question": ""}
        key_map = {
            "Explanation": "explanation",
            "Example": "example",
            "Diagram": "diagram",
            "Quick Question": "question",
        }
        parts = re.split(r"(Explanation|Example|Diagram|Quick Question)\s*:\s*", text)
        i = 1
        while i < len(parts):
            marker = parts[i].strip()
            content = parts[i+1].strip() if i+1 < len(parts) else ""
            content = re.sub(r"\n\s*(Explanation|Example|Diagram|Quick Question)\s*:.*", "", content, flags=re.DOTALL)
            if marker in key_map:
                sections[key_map[marker]] = content.strip()
            i += 2
        if not any(sections.values()):
            sections["explanation"] = text.strip()
            sections["example"] = "Example not found."
            sections["diagram"] = "No diagram."
            sections["question"] = "What did you think?"
        return sections
