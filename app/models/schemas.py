from pydantic import BaseModel, Field

class TeachingResponse(BaseModel):
    explanation: str = Field(..., description="Step-by-step explanation in Urdu+English mix")
    example: str = Field(..., description="Real-life example")
    diagram: str = Field(..., description="Text-based diagram (ASCII art)")
    question: str = Field(..., description="Engaging follow-up question")
