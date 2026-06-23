import pytest
from app.service.input_validator import InputValidator


class TestInputValidator:
    """Unit tests for InputValidator service."""
    
    def test_validate_job_description_empty(self) -> None:
        """Test validation of empty job description."""
        is_valid, error_msg = InputValidator.validate_job_description("")
        assert not is_valid
        assert "empty" in error_msg.lower()
    
    def test_validate_job_description_too_short(self) -> None:
        """Test validation of job description that is too short."""
        is_valid, error_msg = InputValidator.validate_job_description("short")
        assert not is_valid
        assert "50 characters" in error_msg
    
    def test_validate_job_description_too_long(self) -> None:
        """Test validation of job description that exceeds max length."""
        long_text = "a" * 10001
        is_valid, error_msg = InputValidator.validate_job_description(long_text)
        assert not is_valid
        assert "10000 characters" in error_msg
    
    def test_validate_job_description_valid(self) -> None:
        """Test validation of valid job description."""
        valid_job = "a" * 100
        is_valid, error_msg = InputValidator.validate_job_description(valid_job)
        assert is_valid
        assert error_msg == ""
    
    def test_validate_pdf_filename_no_file(self) -> None:
        """Test validation of empty filename."""
        is_valid, error_msg = InputValidator.validate_pdf_filename("")
        assert not is_valid
        assert "no file" in error_msg.lower()
    
    def test_validate_pdf_filename_not_pdf(self) -> None:
        """Test validation of non-PDF file."""
        is_valid, error_msg = InputValidator.validate_pdf_filename("document.txt")
        assert not is_valid
        assert "PDF" in error_msg
    
    def test_validate_pdf_filename_valid(self) -> None:
        """Test validation of valid PDF filename."""
        is_valid, error_msg = InputValidator.validate_pdf_filename("resume.pdf")
        assert is_valid
        assert error_msg == ""
    
    def test_sanitize_text_removes_null_characters(self) -> None:
        """Test sanitization removes null characters."""
        text = "Hello\x00World"
        result = InputValidator.sanitize_text(text)
        assert "\x00" not in result
    
    def test_sanitize_text_removes_excessive_whitespace(self) -> None:
        """Test sanitization removes excessive whitespace."""
        text = "Hello    World   Test"
        result = InputValidator.sanitize_text(text)
        assert result == "Hello World Test"
    
    def test_sanitize_text_strips_leading_trailing_whitespace(self) -> None:
        """Test sanitization strips leading/trailing whitespace."""
        text = "   Hello World   "
        result = InputValidator.sanitize_text(text)
        assert result == "Hello World"
