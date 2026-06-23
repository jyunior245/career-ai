import json
from typing import Dict, Any
from groq import Groq
from app.config import settings

class GroqService:
    """Service layer for Groq/Llama3 analysis."""
    
    def __init__(self) -> None:
        """Initialize Groq client."""
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is missing")
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model
    
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze resume against job description using Groq API.
        
        Args:
            resume_text: Extracted resume text
            job_description: Job description text
        
        Returns:
            Dict with compatibility_score, strengths, weaknesses, suggestions
        """
        prompt = self._build_prompt(resume_text, job_description)
        
        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert HR assistant. Always output your response in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse response
            content = response.choices[0].message.content
            analysis = self._parse_response(content)
            
            return analysis
        
        except Exception as e:
            raise Exception(f"Groq Analysis failed: {str(e)}")
    
    def _build_prompt(self, resume_text: str, job_description: str) -> str:
        """Build prompt for Groq/Llama3."""
        return f"""Analyze the following resume against the job description and provide your analysis in JSON format.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide your analysis in JSON format with the following structure exactly:
{{
    "compatibility_score": <number between 0 and 100>,
    "strengths": <list of 3-5 strengths as strings>,
    "weaknesses": <list of 3-5 weaknesses as strings>,
    "suggestions": <list of 3-5 suggestions as strings>
}}
"""
    
    def _parse_response(self, content: str) -> Dict[str, Any]:
        """Parse Groq response."""
        try:
            data = json.loads(content)
            
            # Validate and clean data
            score = int(data.get("compatibility_score", 0))
            score = max(0, min(100, score))
            
            # Ensure lists are present
            strengths = data.get("strengths", [])
            if isinstance(strengths, str):
                strengths = [strengths]
            
            weaknesses = data.get("weaknesses", [])
            if isinstance(weaknesses, str):
                weaknesses = [weaknesses]
            
            suggestions = data.get("suggestions", [])
            if isinstance(suggestions, str):
                suggestions = [suggestions]
            
            return {
                "compatibility_score": score,
                "strengths": strengths if strengths else ["No strengths identified"],
                "weaknesses": weaknesses if weaknesses else ["No weaknesses identified"],
                "suggestions": suggestions if suggestions else ["No suggestions available"]
            }
        
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from Groq: {str(e)}\nContent: {content}")
        except Exception as e:
            raise Exception(f"Error parsing Groq response: {str(e)}")
