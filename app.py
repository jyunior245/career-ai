from flask import Flask, render_template, request, redirect, url_for
import httpx
import asyncio
import logging
import os
from typing import Dict, Any, Tuple
from dotenv import load_dotenv

load_dotenv()


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
API_BASE_URL = os.environ.get("API_BASE_URL")


def call_analysis_api(resume_file, job_description: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Call the backend API for analysis.
    
    Returns:
        Tuple[bool, Dict]: (success, data)
    """
    try:
        logger.info(f"Calling API with job description length: {len(job_description)}")
        
        files = {
            'resume_file': (
                resume_file.filename,
                resume_file,
                'application/pdf'
            )
        }
        data = {'job_description': job_description}
        
        response = httpx.post(
            f"{API_BASE_URL}/analyze",
            files=files,
            data=data,
            timeout=60
        )
        
        logger.info(f"API response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                logger.info("Analysis successful")
                return True, response_data
            except Exception as e:
                logger.error(f"Failed to parse successful response: {str(e)}")
                return False, {"error": "Received invalid format from server. Please try again later."}
        else:
            try:
                error_data = response.json()
                error_msg = error_data.get("detail", f"Analysis failed with status {response.status_code}")
            except Exception:
                # Fallback for non-JSON errors (like 502 Bad Gateway from Render)
                error_msg = f"Server error ({response.status_code}). The backend service might be waking up or temporarily unavailable."
                
            logger.error(f"API error: {error_msg}")
            return False, {"error": error_msg}
    
    except httpx.TimeoutException:
        logger.error("Request timeout")
        return False, {"error": "Request timeout. Please try again."}
    except httpx.ConnectError:
        logger.error("Cannot connect to API")
        return False, {"error": "Cannot connect to API. Please ensure backend is running."}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return False, {"error": str(e)}


@app.route("/")
def index():
    """Home page with analysis form."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Handle analysis request."""
    # Get form data
    if 'resume_file' not in request.files:
        logger.warning("No resume file in request")
        return render_template("index.html", error_message="No resume file provided")
    
    resume_file = request.files['resume_file']
    job_description = request.form.get("job_description", "").strip()
    
    logger.info(f"Received analysis request")
    logger.info(f"  File name: {resume_file.filename}")
    logger.info(f"  File size: {len(resume_file.read())} bytes")
    resume_file.seek(0)  # Reset file pointer after reading
    
    # Validate file
    if resume_file.filename == '':
        logger.warning("No file selected")
        return render_template("index.html", error_message="No file selected")
    
    # Check file extension (case-insensitive)
    filename_lower = resume_file.filename.lower()
    if not filename_lower.endswith('.pdf'):
        logger.warning(f"Invalid file type: {resume_file.filename}")
        return render_template("index.html", error_message=f"File must be a PDF. Received: {resume_file.filename}")
    
    logger.info(f"✓ File validation passed")
    
    # Validate job description
    if not job_description or len(job_description) < 50:
        logger.warning(f"Job description too short: {len(job_description)} chars")
        return render_template("index.html", error_message="Job description must be at least 50 characters")
    
    if len(job_description) > 10000:
        logger.warning(f"Job description too long: {len(job_description)} chars")
        return render_template("index.html", error_message="Job description cannot exceed 10,000 characters")
    
    logger.info(f"✓ Job description validation passed ({len(job_description)} chars)")
    
    # Call API
    logger.info("Calling backend API...")
    success, data = call_analysis_api(resume_file, job_description)
    
    if not success:
        logger.error(f"API call failed: {data.get('error', 'Unknown error')}")
        return render_template("index.html", error_message=data.get("error", "Analysis failed"))
    
    logger.info(f"✓ Analysis successful - Score: {data.get('compatibility_score', 'N/A')}")
    
    # Render results
    return render_template(
        "results.html",
        compatibility_score=data.get("compatibility_score", 0),
        strengths=data.get("strengths", []),
        weaknesses=data.get("weaknesses", []),
        suggestions=data.get("suggestions", [])
    )


@app.route("/health")
def health():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Flask frontend server on port {port}")
    logger.info(f"Using Backend API URL: {API_BASE_URL}")
    app.run(debug=False, host="0.0.0.0", port=port)
