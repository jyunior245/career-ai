import re
from typing import Tuple


class InputValidator:
    """Service layer for input validation and sanitization."""
    
    MIN_JOB_DESCRIPTION_LENGTH: int = 50
    MAX_JOB_DESCRIPTION_LENGTH: int = 10000
    
    @staticmethod
    def validate_job_description(job_description: str) -> Tuple[bool, str]:
        """
        Validate job description text.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not job_description or not job_description.strip():
            return False, "Job description cannot be empty"
        
        job_description = job_description.strip()
        
        if len(job_description) < InputValidator.MIN_JOB_DESCRIPTION_LENGTH:
            return False, f"Job description must be at least {InputValidator.MIN_JOB_DESCRIPTION_LENGTH} characters"
        
        if len(job_description) > InputValidator.MAX_JOB_DESCRIPTION_LENGTH:
            return False, f"Job description cannot exceed {InputValidator.MAX_JOB_DESCRIPTION_LENGTH} characters"
        
        return True, ""
    
    @staticmethod
    def validate_pdf_filename(filename: str) -> Tuple[bool, str]:
        """
        Validate PDF filename.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not filename:
            return False, "No file selected"
        
        # Check extension (case-insensitive, supports special chars in name)
        filename_lower = filename.lower()
        if not filename_lower.endswith('.pdf'):
            return False, f"File must be a PDF. Received: {filename}"
        
        return True, ""
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Sanitize input text to remove dangerous characters.
        
        Returns:
            str: Sanitized text
        """
        # Remove null characters
        text = text.replace("\x00", "")
        
        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
