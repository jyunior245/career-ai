#!/usr/bin/env python3
"""
CareerAI CLI - Command line interface for project management

Usage:
    python cli.py init        - Initialize the project
    python cli.py test        - Run tests
    python cli.py serve       - Start development servers
    python cli.py build       - Build Docker image
    python cli.py deploy      - Deploy to production
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd: list, description: str) -> int:
    """Run a shell command."""
    print(f"\n📦 {description}...")
    result = subprocess.run(cmd, cwd="backend" if cmd[0] == "pytest" else ".")
    return result.returncode


def init_project() -> None:
    """Initialize the project."""
    print("🚀 Initializing CareerAI project...")
    
    # Check Python version
    if sys.version_info < (3, 12):
        print("❌ Python 3.12+ required")
        sys.exit(1)
    
    # Create venv
    run_command([sys.executable, "-m", "venv", "venv"], "Creating virtual environment")
    
    # Install dependencies
    run_command([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], 
                "Installing backend dependencies")
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements-frontend.txt"],
                "Installing frontend dependencies")
    
    # Copy .env
    if not Path("backend/.env").exists():
        run_command(["cp", "backend/.env.example", "backend/.env"],
                    "Creating .env file")
    
    print("\n✨ Project initialized!")
    print("⚠️  Edit backend/.env with your OpenAI API key")


def test_project() -> None:
    """Run tests."""
    print("🧪 Running tests...")
    run_command(["pytest", "-v"], "Running pytest")


def serve_project() -> None:
    """Start development servers."""
    print("🚀 Starting development servers...")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:5000")
    
    print("\nStart two terminals:")
    print("1. Terminal 1: cd backend && python main.py")
    print("2. Terminal 2: python app.py")


def build_docker() -> None:
    """Build Docker image."""
    print("🐳 Building Docker image...")
    run_command(["docker-compose", "build"], "Building Docker image")


def deploy_project() -> None:
    """Deploy to production."""
    print("🚀 Deploying to production...")
    print("See DEPLOYMENT.md for detailed instructions")


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "init":
        init_project()
    elif command == "test":
        test_project()
    elif command == "serve":
        serve_project()
    elif command == "build":
        build_docker()
    elif command == "deploy":
        deploy_project()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
