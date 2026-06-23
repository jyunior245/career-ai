# CareerAI Constitution

## Core Principles

### I. Layered Architecture (NON-NEGOTIABLE)
Every feature must fit into exactly one of the three defined layers:
- **Presentation** (`backend/app/presentation/`): FastAPI routes and Pydantic schemas only. No business logic.
- **Service** (`backend/app/service/`): All business logic, AI integration, and file processing. No direct DB access from routes.
- **Data** (`backend/app/data/`): Database operations only. No business logic.

Violations require explicit justification in the PR description with reference to this constitution.

### II. Type Safety (NON-NEGOTIABLE)
All Python functions must have complete type hints on parameters and return values. `Any` may only be used in Dict return types for AI responses and must be commented.

```python
# ✅ Valid
def analyze_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:

# ❌ Invalid - no type hints
def analyze_resume(self, resume_text, job_description):
```

### III. External Integration Isolation
All calls to external services (Groq API, PDF processing) must live in dedicated service classes:
- `GroqService` → only class allowed to call Groq API
- `PDFService` → only class allowed to call pdfplumber
- Configuration loaded exclusively from `config.py` via the `settings` singleton

Direct instantiation of `Groq()` or `pdfplumber.open()` outside these classes is forbidden.

### IV. Security-First Uploads
Every file upload must pass through this exact sequence before any processing:
1. Extension validation (`.pdf` only)
2. Size validation (≤ 10 MB)
3. Rename via `uuid4()` — original filename never used for I/O
4. Delete in `finally` block — even on exceptions

Skipping any step is a constitution violation.

### V. Test Coverage Gate
The `backend/app/service/` directory must maintain ≥ 80% line coverage as measured by `pytest --cov`. No merge to `main` branch may reduce coverage below this threshold. External API calls (Groq) must always be mocked in tests.

### VI. Logging Over Printing
`print()` is forbidden in all application code. Use the standard `logging` module at appropriate levels:
- `INFO`: Normal operations (requests received, analysis complete)
- `WARNING`: Recoverable issues (validation failures)
- `ERROR`: Failures requiring attention (API errors, parsing failures)

### VII. Stateless Design
No user session state may be stored in memory between requests. The application must scale horizontally without coordination between instances. Uploaded files must be deleted after each request.

## Security Requirements

- `GROQ_API_KEY` and all secrets loaded exclusively via environment variables
- `.env` file must be in `.gitignore` — only `.env.example` with placeholder values is committed
- All user text inputs sanitized by `InputValidator` before being sent to the LLM
- LLM responses parsed via `json.loads()` — `eval()` is permanently forbidden
- Job description: 50–10,000 characters enforced at both frontend (JS) and backend (InputValidator)
- Resume text: 100–50,000 characters enforced at backend

## Technology Stack

| Layer | Technology | Version |
|---|---|---|
| Backend API | FastAPI | ≥ 0.100 |
| Backend Server | Uvicorn | ≥ 0.24 |
| Validation | Pydantic v2 | ≥ 2.9 |
| PDF Extraction | pdfplumber | ≥ 0.10 |
| AI Provider | Groq SDK | latest |
| Database | SQLite (via stdlib) | — |
| Frontend | Flask + Jinja2 | ≥ 3.0 |
| HTTP Client | httpx | ≥ 0.27 |
| Container | Docker + Compose | — |
| Cloud Deploy | Render.com | — |

Substituting any item in this table requires a constitution amendment.

## Governance

This constitution supersedes all other development practices in this repository. Any amendment requires:
1. A PR modifying this file with a clear justification
2. Update to `**Last Amended**` date below
3. A corresponding update to any affected `plan.md` or `spec.md`

All PRs must include a "Constitution Check" section verifying compliance with Principles I–VII.

**Version**: 1.0.0 | **Ratified**: 2026-06-01 | **Last Amended**: 2026-06-22
