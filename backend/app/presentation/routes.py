from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pathlib import Path
import uuid
import logging
from app.presentation.schemas import AnalysisResponse
from app.service.input_validator import InputValidator
from app.service.pdf_service import PDFService
from app.service.groq_service import GroqService
from app.data.database import db
from app.config import settings


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["analysis"])
pdf_service = PDFService()
groq_service = GroqService()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
) -> AnalysisResponse:
    """
    Analyze resume PDF against job description.
    
    Args:
        resume_file: PDF file upload
        job_description: Job description text
    
    Returns:
        AnalysisResponse with analysis results
    """
    logger.info(f"Received analysis request with file: {resume_file.filename}")
    
    # Validate job description
    is_valid, error_msg = InputValidator.validate_job_description(job_description)
    if not is_valid:
        logger.warning(f"Invalid job description: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Validate PDF filename
    is_valid, error_msg = InputValidator.validate_pdf_filename(resume_file.filename)
    if not is_valid:
        logger.warning(f"Invalid PDF filename: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Save uploaded file temporarily
    try:
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename (to avoid encoding issues)
        file_ext = Path(resume_file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = upload_dir / unique_filename
        
        logger.info(f"Saving file to: {file_path}")
        
        # Save file
        contents = await resume_file.read()
        file_size_mb = len(contents) / (1024 * 1024)
        logger.info(f"File size: {file_size_mb}MB")
        
        if file_size_mb > PDFService.MAX_PDF_SIZE_MB:
            logger.error(f"File too large: {file_size_mb}MB")
            raise HTTPException(
                status_code=400, 
                detail=f"File exceeds {PDFService.MAX_PDF_SIZE_MB}MB limit"
            )
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        logger.info("File saved successfully")
        
        # Extract text from PDF
        logger.info("Extracting text from PDF")
        success, result = pdf_service.extract_text_from_pdf(str(file_path))
        
        if not success:
            logger.error(f"PDF extraction failed: {result}")
            raise HTTPException(status_code=400, detail=result)
        
        resume_text = result
        logger.info(f"Extracted {len(resume_text)} characters from PDF")
        
        # Sanitize inputs
        job_description = InputValidator.sanitize_text(job_description)
        
        try:
            # Perform analysis with Groq
            logger.info("Calling Groq API for analysis")
            analysis = groq_service.analyze_resume(resume_text, job_description)
            logger.info(f"Analysis complete: score={analysis['compatibility_score']}")
            
            # Save to database
            db.save_analysis(
                resume=resume_text,
                job_description=job_description,
                compatibility_score=analysis["compatibility_score"],
                strengths=str(analysis["strengths"]),
                weaknesses=str(analysis["weaknesses"]),
                suggestions=str(analysis["suggestions"])
            )
            
            return AnalysisResponse(
                compatibility_score=analysis["compatibility_score"],
                strengths=analysis["strengths"],
                weaknesses=analysis["weaknesses"],
                suggestions=analysis["suggestions"]
            )
        
        finally:
            # Clean up uploaded file
            try:
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"Cleaned up uploaded file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up file: {e}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "ok"}
