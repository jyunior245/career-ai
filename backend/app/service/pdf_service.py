import pdfplumber
from pathlib import Path
from typing import Tuple
import logging


logger = logging.getLogger(__name__)


class PDFService:
    """Service layer for PDF extraction and processing."""
    
    MAX_PDF_SIZE_MB: int = 10
    ALLOWED_MIME_TYPES: list = ["application/pdf"]
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Tuple[bool, str]:
        """
        Extract text from PDF file.
        
        Args:
            file_path: Path to PDF file
        
        Returns:
            Tuple[bool, str]: (success, text or error_message)
        """
        try:
            # Check file exists
            if not Path(file_path).exists():
                logger.error(f"PDF file not found: {file_path}")
                return False, "File not found"
            
            # Check file size
            file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
            if file_size_mb > PDFService.MAX_PDF_SIZE_MB:
                logger.error(f"PDF file too large: {file_size_mb}MB")
                return False, f"File exceeds {PDFService.MAX_PDF_SIZE_MB}MB limit"
            
            # Extract text from PDF
            text = ""
            try:
                with pdfplumber.open(file_path) as pdf:
                    if len(pdf.pages) == 0:
                        logger.error("PDF has no pages")
                        return False, "PDF has no pages"
                    
                    logger.info(f"Extracting text from {len(pdf.pages)} pages")
                    
                    # Extract text from all pages
                    for page in pdf.pages:
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        except Exception as e:
                            logger.warning(f"Failed to extract text from page: {e}")
                            continue
            
            except Exception as e:
                logger.error(f"Failed to read PDF: {str(e)}")
                return False, f"Failed to read PDF: {str(e)}"
            
            if not text or not text.strip():
                logger.error("PDF contains no extractable text")
                return False, "PDF contains no extractable text"
            
            return True, text.strip()
        
        except Exception as e:
            return False, f"PDF extraction error: {str(e)}"
    
    @staticmethod
    def validate_pdf_file(filename: str) -> Tuple[bool, str]:
        """
        Validate PDF filename and format.
        
        Args:
            filename: Name of file
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        # Check extension
        if not filename.lower().endswith('.pdf'):
            return False, "File must be a PDF"
        
        return True, ""
