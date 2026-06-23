from pydantic import BaseModel
from typing import List


class AnalysisRequest(BaseModel):
    """Schema for analysis request."""
    resume: str
    job_description: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "resume": "Software Engineer with 5 years experience...",
                "job_description": "Looking for senior engineer with Python..."
            }
        }


class AnalysisResponse(BaseModel):
    """Schema for analysis response."""
    compatibility_score: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "compatibility_score": 75,
                "strengths": ["Good experience", "Strong technical skills"],
                "weaknesses": ["Limited leadership experience"],
                "suggestions": ["Highlight team leadership", "Add certifications"]
            }
        }
