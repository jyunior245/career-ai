# Plano de Implementação — CareerAI

> **Gerado por:** `speckit.plan` — GitHub Copilot SpecKit  
> **Leu:** `.specify/CareerAI.specification.md` (RNF01–RNF05) + `docs/schema.md`  
> **Data:** 2026-06-22  
> **Versão:** 1.0

---

## 1. Visão Geral

Este plano descreve como cada Requisito Não Funcional (RNF) foi traduzido em decisões de arquitetura e estrutura de código, com base no schema de dados e na constituição técnica do projeto.

---

## 2. Decisões Arquiteturais por RNF

### RNF01 — Desempenho (< 5s de resposta)

**Decisões:**
- Groq API escolhida como provedor de LLM por oferecer latência < 1s (inferência em hardware especializado).
- Upload e processamento de PDF tratados de forma **síncrona** por serem operações rápidas (pdfplumber em < 500ms para PDFs < 10MB).
- Timeout de 60s configurado no cliente HTTP do frontend para cobrir eventuais picos.
- Arquivos de upload deletados imediatamente pós-processamento para liberar disco.

**Métricas esperadas:**
| Etapa | Tempo Estimado |
|---|---|
| Upload → Backend | < 200ms |
| Extração de texto PDF | < 500ms |
| Chamada à Groq API | < 2s |
| Render da página de resultado | < 300ms |
| **Total** | **< 3s** |

---

### RNF02 — Segurança

**Decisões:**
- **Validação em duas camadas:** frontend (JS) e backend (InputValidator).
- Nome do arquivo gerado via `uuid4()` — jamais usar o nome original do usuário.
- Arquivo deletado no bloco `finally` da rota, mesmo em caso de exceção.
- `GROQ_API_KEY` carregada exclusivamente via variável de ambiente (`config.py`).
- Arquivo `.env` adicionado ao `.gitignore`.
- Saída do LLM parseada via `json.loads()` — nunca executada (`eval()` proibido).

**Módulos responsáveis:**
```
backend/app/service/input_validator.py  ← Sanitização e validação de texto
backend/app/config.py                   ← Carregamento seguro de credenciais
backend/app/presentation/routes.py      ← Validação de upload e limpeza de arquivo
```

---

### RNF03 — Compatibilidade (Desktop, Tablet, Mobile)

**Decisões:**
- Bootstrap 5 via CDN utilizado como base de grid e componentes responsivos.
- Templates Jinja2 com `viewport` meta tag configurado.
- Nenhum layout com `position: fixed` que possa quebrar em mobile.
- Testado visualmente em 320px (mobile mínimo) e 1440px (desktop).

---

### RNF04 — Qualidade de Código

**Decisões:**
- Type hints em **todas** as funções Python (validado pelo linter).
- Arquitetura em camadas conforme a `constitution.md`:
  - `presentation/` → FastAPI routes + Pydantic schemas
  - `service/` → Lógica de negócio isolada e testável
  - `data/` → Acesso ao SQLite desacoplado dos serviços

**Estrutura de testes:**
```
backend/tests/
├── test_input_validator.py    ← Testa sanitização e validação
├── test_pdf_service.py        ← Testa extração de texto
├── test_analysis_service.py   ← Testa parsing de resposta do LLM
└── conftest.py                ← Fixtures compartilhadas
```

**Cobertura alvo:** ≥ 80% no diretório `service/`.

---

### RNF05 — Escalabilidade (Docker + Cloud)

**Decisões:**
- `Dockerfile` único com instalação das dependências de backend e frontend.
- `docker-compose.yml` orquestra os dois serviços (`backend :8000`, `frontend :5000`).
- `render.yaml` com Blueprint para deploy automático no Render.com (free tier).
- Aplicação **stateless**: sem sessões em memória, sem arquivos persistidos entre requests.

---

## 3. Estrutura de Arquivos (Resultado da Implementação)

```
my-project/
│
├── docs/                         ← Documentação orientada a requisitos (SpecKit)
│   ├── constitution.md           ← Regras de tecnologia e arquitetura
│   ├── schema.md                 ← Modelo de dados derivado dos RFs
│   └── plan.md                   ← Este arquivo — plano derivado dos RNFs
│
├── backend/
│   ├── app/
│   │   ├── presentation/
│   │   │   ├── routes.py         ← RF01, RF02, RF03, RF07 — endpoint /analyze
│   │   │   └── schemas.py        ← RF06, RF07 — AnalysisResponse Pydantic
│   │   ├── service/
│   │   │   ├── groq_service.py   ← RF04, RF05 — integração com Groq API
│   │   │   ├── pdf_service.py    ← RF02 — extração de texto do PDF
│   │   │   ├── input_validator.py← RNF02 — validação e sanitização
│   │   │   └── analysis_service.py← RF05 — parsing de resposta JSON
│   │   ├── data/
│   │   │   └── database.py       ← RF08 — persistência SQLite
│   │   ├── config.py             ← RNF02 — carregamento de env vars
│   │   └── main.py               ← Entry point FastAPI
│   ├── tests/                    ← RNF04 — testes unitários
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── templates/
│   │   ├── index.html            ← RF01, RF03 — formulário de upload
│   │   └── results.html          ← RF07 — exibição dos resultados
│   └── static/
│       ├── css/style.css
│       └── js/main.js
│
├── app.py                        ← Entry point Flask frontend
├── Dockerfile                    ← RNF05 — containerização
├── docker-compose.yml            ← RNF05 — orquestração local
├── render.yaml                   ← RNF05 — deploy no Render.com
├── .gitignore
└── README.md
```

---

## 4. Roadmap de Implementação

> Detalhamento executado pelo `speckit.tasks` — ver histórico de commits.

| Fase | Entregável | RF/RNF |
|---|---|---|
| 1 | Estrutura do projeto + config + constitution | RNF04 |
| 2 | Endpoint `/analyze` + schemas Pydantic | RF01, RF03, RF07 |
| 3 | PDFService — extração de texto | RF02 |
| 4 | GroqService — integração com LLM | RF04, RF05, RF06 |
| 5 | InputValidator — validação e sanitização | RNF02 |
| 6 | Database — persistência SQLite | RF08 |
| 7 | Flask Frontend + templates HTML | RF01, RF03, RF07, RNF03 |
| 8 | Testes unitários | RNF04 |
| 9 | Docker + Render.yaml | RNF05 |
| 10 | Migração Ollama → Groq API | RF04 — melhoria de deploy |

---

## 5. Riscos e Mitigações

| Risco | Probabilidade | Mitigação |
|---|---|---|
| Groq depreciar modelo `llama-3.1-8b-instant` | Média | Modelo configurável via `GROQ_MODEL` env var |
| PDF com texto em imagem (não extraível) | Alta | Mensagem clara ao usuário; OCR fora do escopo |
| Limite de rate da Groq API (free tier) | Baixa | Tratamento de erro com mensagem amigável |
| Render pausar serviço (cold start) | Alta | Esperado no free tier; aceito para MVP |
| Perda de dados SQLite no redeploy | Média | Aceito para MVP; banco é histórico auxiliar |
