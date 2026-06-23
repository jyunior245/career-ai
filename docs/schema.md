# Schema de Dados — CareerAI

> **Gerado por:** `speckit.specify` — GitHub Copilot SpecKit  
> **Leu:** `.specify/CareerAI.specification.md` (Requisitos Funcionais RF01–RF08)  
> **Data:** 2026-06-22  
> **Versão:** 1.0

---

## 1. Origem dos Requisitos

Este schema foi derivado diretamente dos seguintes Requisitos Funcionais:

| RF | Requisito | Entidade Gerada |
|---|---|---|
| RF01 | Upload de currículo PDF | — (arquivo temporário, sem persistência) |
| RF02 | Extração automática de texto do PDF | Campo `resume_text` em `analyses` |
| RF03 | Inserção da descrição da vaga | Campo `job_description` em `analyses` |
| RF04 | Integração com Groq API | — (serviço externo, sem entidade) |
| RF05 | Geração de análise (pontos fortes/fracos) | Campos `strengths`, `weaknesses`, `suggestions` |
| RF06 | Geração de pontuação (0-100) | Campo `compatibility_score` em `analyses` |
| RF07 | Exibição dos resultados | Schema de response (Pydantic) |
| RF08 | Persistência das análises | Tabela `analyses` no SQLite |

---

## 2. Modelo de Dados (SQLite)

### 2.1 Tabela `analyses`

Armazena cada análise realizada pelo sistema.

```sql
CREATE TABLE IF NOT EXISTS analyses (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_text         TEXT    NOT NULL,           -- Texto extraído do PDF
    job_description     TEXT    NOT NULL,           -- Descrição da vaga informada pelo usuário
    compatibility_score INTEGER NOT NULL            -- Pontuação de compatibilidade (0–100)
                        CHECK (compatibility_score >= 0 AND compatibility_score <= 100),
    strengths           TEXT    NOT NULL,           -- Lista serializada de pontos fortes
    weaknesses          TEXT    NOT NULL,           -- Lista serializada de pontos fracos
    suggestions         TEXT    NOT NULL,           -- Lista serializada de recomendações
    created_at          TEXT    NOT NULL            -- Timestamp ISO 8601 da análise
                        DEFAULT (datetime('now'))
);
```

**Índice:** `created_at DESC` para consultas ordenadas por data.

---

## 3. Schemas de API (Pydantic)

### 3.1 Request — `POST /api/v1/analyze`

O request é do tipo `multipart/form-data`, pois inclui arquivo e campo de texto:

| Campo | Tipo | Obrigatório | Regras |
|---|---|---|---|
| `resume_file` | `UploadFile` (PDF) | ✅ | Tipo `.pdf`, máx 10 MB |
| `job_description` | `str` | ✅ | 50–10.000 caracteres |

```python
# Capturado via FastAPI Form/File params (não é um schema Pydantic de body)
resume_file: UploadFile = File(...)
job_description: str = Form(...)
```

### 3.2 Response — `AnalysisResponse`

```python
class AnalysisResponse(BaseModel):
    compatibility_score: int       # 0 a 100
    strengths: List[str]           # 3 a 5 pontos fortes
    weaknesses: List[str]          # 3 a 5 pontos fracos
    suggestions: List[str]         # 3 a 5 recomendações
```

**Exemplo de resposta:**
```json
{
    "compatibility_score": 72,
    "strengths": [
        "Experiência sólida com Python e FastAPI",
        "Familiaridade com deploy em cloud",
        "Boas práticas de tipagem e testes"
    ],
    "weaknesses": [
        "Sem experiência declarada com Kubernetes",
        "Portfolio com projetos pouco detalhados"
    ],
    "suggestions": [
        "Adicionar projeto com orquestração de containers",
        "Incluir métricas de impacto nos projetos anteriores",
        "Certificar conhecimento em cloud (AWS/GCP)"
    ]
}
```

### 3.3 Response — `GET /api/v1/health`

```python
class HealthResponse(BaseModel):
    status: str   # "ok"
```

---

## 4. Contrato com a Groq API

### 4.1 Request enviado ao LLM

```python
client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are an expert HR assistant..."},
        {"role": "user",   "content": "<prompt com currículo e vaga>"}
    ],
    response_format={"type": "json_object"}
)
```

### 4.2 Estrutura esperada na resposta do LLM

```json
{
    "compatibility_score": 72,
    "strengths":   ["...", "...", "..."],
    "weaknesses":  ["...", "...", "..."],
    "suggestions": ["...", "...", "..."]
}
```

> **Regra:** a resposta deve ser parseada via `json.loads()`. Se o JSON for inválido, a exceção deve ser capturada e relançada com mensagem descritiva.

---

## 5. Fluxo de Dados

```
Usuário
  │
  │  multipart/form-data (resume_file + job_description)
  ▼
Flask Frontend (app.py :5000)
  │
  │  POST /api/v1/analyze  (httpx)
  ▼
FastAPI Backend (:8000)
  │
  ├─► InputValidator.validate_job_description()
  ├─► InputValidator.validate_pdf_filename()
  ├─► PDFService.extract_text_from_pdf()     ── pdfplumber
  ├─► InputValidator.sanitize_text()
  ├─► GroqService.analyze_resume()           ── Groq API (HTTPS)
  │       └─► GroqService._parse_response()
  ├─► Database.save_analysis()               ── SQLite
  │
  │  AnalysisResponse (JSON)
  ▼
Flask Frontend
  │
  │  render_template("results.html", ...)
  ▼
Usuário (página de resultados)
```

---

## 6. Restrições de Dados

| Campo | Tipo Python | Constraint | Motivo |
|---|---|---|---|
| `resume_text` | `str` | 100–50.000 chars | RNF02 — segurança e custo de token |
| `job_description` | `str` | 50–10.000 chars | RF03 — validação mínima de conteúdo |
| `compatibility_score` | `int` | `0 ≤ x ≤ 100` | RF06 — escala definida na spec |
| PDF | `UploadFile` | `.pdf`, ≤ 10 MB | RF01 — segurança e performance |
| `strengths/weaknesses/suggestions` | `List[str]` | 1–10 itens | RF05 — qualidade da análise |
