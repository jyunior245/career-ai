<!-- SPECKIT START -->

## CareerAI — Coding Agent Context

This project was developed using the **GitHub Copilot SpecKit** specification-driven workflow (`/speckit`). Read the documents below before generating any code or making architectural decisions.

### Active Plan
`.specify/templates/plan-template.md`

### Key Context

**Project**: CareerAI — AI-powered resume analysis platform  
**Stack**: Python 3.10+, FastAPI (backend :8000), Flask (frontend :5000), Groq API (Llama 3), pdfplumber, SQLite  
**Feature Branch**: `001-career-ai-core` — **Status: Implemented ✅**

### Architecture Rules (from Constitution)
- **Three-layer architecture is NON-NEGOTIABLE**: `presentation/` → `service/` → `data/`. No layer may skip another.
- All Python functions MUST have complete type hints. No `print()` — use `logging`.
- `GroqService` is the ONLY class allowed to call the Groq API.
- `PDFService` is the ONLY class allowed to use pdfplumber.
- All env vars loaded exclusively from `backend/app/config.py` via `settings` singleton.
- Uploaded files MUST be renamed with `uuid4()` and deleted in a `finally` block.

### Project Structure
```
backend/app/presentation/   ← FastAPI routes + Pydantic schemas
backend/app/service/        ← Business logic (GroqService, PDFService, InputValidator)
backend/app/data/           ← SQLite CRUD
backend/app/config.py       ← Env var loading (GROQ_API_KEY, GROQ_MODEL)
frontend/templates/         ← Jinja2 HTML templates
app.py                      ← Flask frontend entry point
```

### Specification Documents
- Constitution: `.specify/memory/constitution.md`
- Feature Spec: `.specify/templates/spec-template.md`
- Implementation Plan: `.specify/templates/plan-template.md`
- Task Roadmap: `.specify/templates/tasks-template.md`
- Quality Checklist: `.specify/templates/checklist-template.md`

<!-- SPECKIT END -->
