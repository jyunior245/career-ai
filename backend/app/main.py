from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.data.database import db
from app.presentation.routes import router
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    logger.info("Creating FastAPI application")
    app = FastAPI(title="CareerAI", version="1.0.0")
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize database
    logger.info("Initializing database")
    db.init_db()
    
    # Include routes
    logger.info("Including routes")
    app.include_router(router)
    
    logger.info("FastAPI application created successfully")
    return app


app = create_app()
