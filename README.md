# CareerAI

A web platform for analyzing resumes using AI. Upload your resume as a PDF and get personalized feedback on your compatibility with specific job descriptions using Groq API.

## Features

- 📄 PDF resume upload and text extraction
- 💼 Job description submission
- 🤖 AI-powered analysis using Groq API (fast, free tier available)
- 📊 Compatibility scoring (0-100)
- ✨ Strengths identification
- ⚠️ Weaknesses analysis
- 💡 Improvement suggestions
- 📱 Responsive design with Bootstrap 5
- 🗄️ SQLite database for analysis history

## Tech Stack

**Backend:**
- Python 3.12
- FastAPI
- Groq API (Llama 3 Cloud AI)
- SQLite
- pdfplumber (PDF extraction)

**Frontend:**
- HTML5
- Bootstrap 5
- Jinja2 Templates
- JavaScript

## Project Structure

```
my-project/
├── backend/
│   ├── app/
│   │   ├── presentation/        # API routes and schemas
│   │   ├── service/             # Business logic
│   │   ├── data/                # Database operations
│   │   ├── config.py            # Configuration
│   │   └── main.py              # FastAPI app
│   ├── tests/                   # Unit tests
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── templates/               # HTML templates
│   │   ├── index.html
│   │   └── results.html
│   └── static/                  # CSS and JS
│       ├── css/style.css
│       └── js/main.js
├── app.py                       # Flask frontend
├── requirements-frontend.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Installation

### Prerequisites
- Python 3.12+
- Groq API key

### Local Setup

1. **Clone the repository**
```bash
cd my-project
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install backend dependencies**
```bash
pip install -r backend/requirements.txt
```

4. **Install frontend dependencies**
```bash
pip install -r requirements-frontend.txt
```

5. **Setup environment variables**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your Groq API key
```

6. **Run backend server**
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

7. **Run frontend server** (in another terminal)
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Docker Deployment

### Using Docker Compose

```bash
docker-compose up --build
```

Access the application at `http://localhost:5000`

### Using Railway

1. Push to GitHub
2. Connect repository to Railway
3. Set environment variables:
   - `GROQ_API_KEY`
4. Deploy

### Using Render

1. Connect GitHub repository
2. Create new Web Service
3. Set build command: `pip install -r backend/requirements.txt && pip install -r requirements-frontend.txt`
4. Set start command: `python app.py`
5. Add environment variables

## API Documentation

### POST /api/v1/analyze

Analyze resume against job description.

**Request:**
```json
{
    "resume": "Software Engineer with 5 years experience...",
    "job_description": "Looking for senior engineer with..."
}
```

**Response:**
```json
{
    "compatibility_score": 75,
    "strengths": ["Good experience", "Strong skills"],
    "weaknesses": ["Limited certifications"],
    "suggestions": ["Add more projects", "Highlight achievements"]
}
```

**Status Codes:**
- 200: Successful analysis
- 400: Invalid input
- 500: Server error

### GET /api/v1/health

Health check endpoint.

## Testing

Run unit tests:

```bash
cd backend
pytest
```

Run specific test file:
```bash
pytest tests/test_input_validator.py -v
```

## Input Validation

- **Resume**: 50-10,000 characters
- **Job Description**: 50-5,000 characters
- Null characters and excessive whitespace are sanitized

## Performance

- Target response time: < 5 seconds
- Optimized for desktop and mobile
- Database indexed for fast queries

## Security

- Input validation on all endpoints
- Text sanitization to prevent injection
- Environment variables for sensitive data
- CORS enabled for frontend requests

## Future Enhancements

- PDF resume upload
- User authentication
- Analysis history
- LinkedIn integration
- Resume templates
- Multiple language support
- Batch analysis
- Email notifications

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
