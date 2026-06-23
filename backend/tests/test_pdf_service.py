import pytest
from pathlib import Path
import tempfile
from app.service.pdf_service import PDFService


class TestPDFService:
    """Unit tests for PDFService."""
    
    def test_validate_pdf_filename_valid(self) -> None:
        """Test validation of valid PDF filename."""
        is_valid, error_msg = PDFService.validate_pdf_file("resume.pdf")
        assert is_valid
        assert error_msg == ""
    
    def test_validate_pdf_filename_not_pdf(self) -> None:
        """Test validation of non-PDF file."""
        is_valid, error_msg = PDFService.validate_pdf_file("document.txt")
        assert not is_valid
        assert "PDF" in error_msg
    
    def test_validate_pdf_filename_case_insensitive(self) -> None:
        """Test that PDF validation is case-insensitive."""
        is_valid, error_msg = PDFService.validate_pdf_file("resume.PDF")
        assert is_valid
    
    def test_extract_text_file_not_found(self) -> None:
        """Test extraction from non-existent file."""
        success, result = PDFService.extract_text_from_pdf("/nonexistent/path.pdf")
        assert not success
        assert "not found" in result.lower()
    
    def test_extract_text_max_size_exceeded(self) -> None:
        """Test extraction from file exceeding max size."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            # Create a file larger than 10MB
            f.write(b"x" * (11 * 1024 * 1024))
            temp_path = f.name
        
        try:
            success, result = PDFService.extract_text_from_pdf(temp_path)
            assert not success
            assert "exceeds" in result.lower() or "size" in result.lower()
        finally:
            Path(temp_path).unlink()
