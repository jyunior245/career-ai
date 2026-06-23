#!/bin/bash

# CareerAI Setup Script

echo "🚀 CareerAI Setup"
echo "================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "📥 Installing frontend dependencies..."
pip install -r requirements-frontend.txt

# Create .env file
echo "⚙️  Setting up environment variables..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your OpenAI API key"
fi

# Initialize database
echo "🗄️  Initializing database..."
python -c "from app.data.database import db; db.init_db()"

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the application:"
echo "1. Run backend: cd backend && python main.py"
echo "2. Run frontend: python app.py (in another terminal)"
echo ""
