import pytest
import json
from unittest.mock import patch, MagicMock
from app.service.analysis_service import AnalysisService


class TestAnalysisService:
    """Unit tests for AnalysisService."""
    
    @pytest.fixture
    def service(self) -> AnalysisService:
        """Create AnalysisService instance for testing."""
        return AnalysisService()
    
    def test_parse_response_valid_json(self, service: AnalysisService) -> None:
        """Test parsing valid JSON response."""
        response = json.dumps({
            "compatibility_score": 75,
            "strengths": ["Good experience", "Strong skills"],
            "weaknesses": ["Limited certifications"],
            "suggestions": ["Add more projects"]
        })
        
        result = service._parse_response(response)
        
        assert result["compatibility_score"] == 75
        assert len(result["strengths"]) == 2
        assert len(result["weaknesses"]) == 1
        assert len(result["suggestions"]) == 1
    
    def test_parse_response_score_out_of_range(self, service: AnalysisService) -> None:
        """Test that compatibility score is clamped between 0 and 100."""
        response = json.dumps({
            "compatibility_score": 150,
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        })
        
        result = service._parse_response(response)
        assert result["compatibility_score"] == 100
        
        response = json.dumps({
            "compatibility_score": -50,
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        })
        
        result = service._parse_response(response)
        assert result["compatibility_score"] == 0
    
    def test_parse_response_invalid_json(self, service: AnalysisService) -> None:
        """Test parsing invalid JSON raises exception."""
        with pytest.raises(Exception, match="Invalid JSON response"):
            service._parse_response("invalid json")
    
    def test_build_prompt_contains_resume(self, service: AnalysisService) -> None:
        """Test that built prompt contains resume."""
        resume = "Software Engineer with 5 years experience"
        job_description = "Looking for senior engineer"
        
        prompt = service._build_prompt(resume, job_description)
        
        assert resume in prompt
        assert job_description in prompt
        assert "JSON" in prompt
