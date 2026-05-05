import logging

logger = logging.getLogger(__name__)

class LLMClient:
    """Simulates Gemma 4. Replace with real API later."""
    def __init__(self, model_name: str = "gemma-4"):
        self.model_name = model_name

    def generate(self, system_prompt: str, user_message: str, history=None) -> str:
        return _placeholder_response(user_message)

def _placeholder_response(user_input: str) -> str:
    text = user_input.lower().strip()
    # Strict correction
    if "sun revolves around earth" in text:
        return _build_response(
            explanation="Aap ka statement galt hai. Actually, Earth revolves around the Sun. Yeh heliocentric model hai.",
            example="Maano aap gol chakkar laga rahe ho centre ke ird gird. Centre Sun hai, aap Earth.",
            diagram="       (Sun)\n         /|\\\n        / | \\\n   (Earth)----> orbit",
            question="Agar Sun itna heavy hai, toh Earth usme kyun nahi gir jaati?",
        )
    if "2+2=5" in text.replace(" ", ""):
        return _build_response(
            explanation="Nahi, 2+2=4 hota hai. Basic addition seekho.",
            example="2 apples + 2 apples = 4 apples.",
            diagram="+---+---+\n| 2 | 2 |\n+---+---+\n  \\   /\n   4",
            question="3+3 kitna hota hai?",
        )
    if "photosynthesis" in text:
        return _build_response(
            explanation="Plants sunlight se khana banate hain. CO₂ + H₂O + light → Glucose + O₂",
            example="Dhoop mein rakha podha acha grow karta hai.",
            diagram="       ☀️\n        |\n      [Leaf]\n   CO₂+H₂O → Glucose+O₂",
            question="Agar plant ko pani na mile toh photosynthesis ruk jayega?",
        )
    return _build_response(
        explanation=f"Aap ne '{user_input[:50]}...' ke baare mein poocha. Chaliye zero level se samjhte hain.",
        example="Real-life example sochiye...",
        diagram="+------------------+\n|   Core Concept   |\n+------------------+\n        |\n        v\n  [Application]",
        question="Is topic ka sab se ahem point kya hai?",
    )

def _build_response(explanation, example, diagram, question):
    return f"Explanation:\n{explanation}\n\nExample:\n{example}\n\nDiagram:\n{diagram}\n\nQuick Question:\n{question}"
