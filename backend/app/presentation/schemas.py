from pydantic import BaseModel
from typing import List


class AnalysisRequest(BaseModel):
    """Request model for resume analysis (for API)."""
    resume_text: str  # Extracted resume text
    job_description: str


class AnalysisResponse(BaseModel):
    """Response model for resume analysis."""
    compatibility_score: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
