@echo off
REM CareerAI Setup Script for Windows

echo 🚀 CareerAI Setup
echo =================

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing backend dependencies...
pip install -r backend\requirements.txt

echo 📥 Installing frontend dependencies...
pip install -r requirements-frontend.txt

REM Create .env file
echo ⚙️  Setting up environment variables...
if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo ⚠️  Please edit backend\.env with your OpenAI API key
)

REM Initialize database
echo 🗄️  Initializing database...
python -c "from app.data.database import db; db.init_db()"

echo.
echo ✨ Setup complete!
echo.
echo To start the application:
echo 1. Run backend: cd backend ^&^& python main.py
echo 2. Run frontend: python app.py (in another terminal)
echo.
