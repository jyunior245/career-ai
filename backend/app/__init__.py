"""
CareerAI - Resume Analysis Platform

This module initializes the main FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.data.database import db
from app.presentation.routes import router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="CareerAI",
        description="AI-powered resume analysis platform",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize database
    db.init_db()
    
    # Include routers
    app.include_router(router)
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return JSONResponse({"message": "CareerAI API", "version": "1.0.0"})
    
    return app


# Create app instance
app = create_app()
