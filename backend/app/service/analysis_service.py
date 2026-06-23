import json
from typing import Dict, Any
from openai import OpenAI
from app.config import settings


class AnalysisService:
    """Service layer for resume analysis using OpenAI API."""
    
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def analyze_resume(self, resume: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze resume against job description using OpenAI API.
        
        Args:
            resume: Resume text
            job_description: Job description text
        
        Returns:
            Dict with compatibility_score, strengths, weaknesses, suggestions
        """
        prompt = self._build_prompt(resume, job_description)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert HR recruiter analyzing resumes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse response
            content = response.choices[0].message.content
            analysis = self._parse_response(content)
            
            return analysis
        
        except Exception as e:
            raise Exception(f"AI Analysis failed: {str(e)}")
    
    def _build_prompt(self, resume: str, job_description: str) -> str:
        """Build prompt for OpenAI API."""
        return f"""
Analyze the following resume against the job description.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

Provide your analysis in JSON format with the following structure:
{{
    "compatibility_score": <number between 0 and 100>,
    "strengths": <list of strengths>,
    "weaknesses": <list of weaknesses>,
    "suggestions": <list of suggestions for improvement>
}}

Respond ONLY with valid JSON, no additional text.
"""
    
    def _parse_response(self, content: str) -> Dict[str, Any]:
        """Parse OpenAI response."""
        try:
            data = json.loads(content)
            
            # Validate compatibility_score
            score = int(data.get("compatibility_score", 0))
            score = max(0, min(100, score))
            
            return {
                "compatibility_score": score,
                "strengths": data.get("strengths", []),
                "weaknesses": data.get("weaknesses", []),
                "suggestions": data.get("suggestions", [])
            }
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response from AI")
