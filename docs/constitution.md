# Constituição Técnica — CareerAI

> **Gerado por:** `speckit.constitution` — GitHub Copilot SpecKit  
> **Data:** 2026-06-22  
> **Versão:** 1.0

---

## 1. Propósito

Este documento estabelece as regras imutáveis de tecnologia, arquitetura e qualidade que todo código deste repositório deve obedecer. Nenhuma decisão de implementação pode contradizer as diretrizes aqui definidas sem uma revisão e aprovação explícita.

---

## 2. Stack Tecnológico

### 2.1 Backend
| Componente | Tecnologia | Versão Mínima | Justificativa |
|---|---|---|---|
| Linguagem | Python | 3.10+ | Tipagem estática, async nativo, ecossistema maduro |
| Framework API | FastAPI | 0.100+ | OpenAPI automático, validação via Pydantic, async |
| Servidor ASGI | Uvicorn | 0.24+ | Alta performance para I/O assíncrono |
| Validação | Pydantic v2 | 2.9+ | Type-safe, geração automática de schema |
| PDF Extraction | pdfplumber | 0.10+ | Melhor extração de layout complexo |
| LLM Provider | Groq API SDK | latest | Inferência ultrarrápida com modelos Llama 3 gratuitos |
| Banco de Dados | SQLite | — | Sem dependência externa, adequado ao escopo MVP |
| Variáveis de Ambiente | python-dotenv | 1.0+ | Separação de config do código |

### 2.2 Frontend
| Componente | Tecnologia | Versão | Justificativa |
|---|---|---|---|
| Servidor Web | Flask | 3.0+ | Leve, adequado para camada de apresentação |
| Templates | Jinja2 | — | Integrado ao Flask, seguro contra XSS |
| Estilos | Bootstrap 5 | CDN | Responsividade sem overhead de build |
| HTTP Client | httpx | 0.27+ | Async-ready, substitui requests |

### 2.3 Infraestrutura
| Componente | Tecnologia | Justificativa |
|---|---|---|
| Containerização | Docker + Compose | Portabilidade de ambiente |
| CI/CD | GitHub Actions | Integrado ao repositório |
| Deploy Gratuito | Render.com | Free tier com suporte a Python |

---

## 3. Regras de Arquitetura

### 3.1 Separação em Camadas (obrigatório)
O backend **deve** seguir a arquitetura em três camadas:

```
backend/app/
├── presentation/   ← Rotas FastAPI, schemas de request/response
├── service/        ← Regras de negócio, integração com IA e PDF
└── data/           ← Modelos de banco de dados, operações CRUD
```

- A camada `presentation` **não pode** acessar a camada `data` diretamente.
- A camada `data` **não pode** conter lógica de negócio.
- Toda comunicação entre camadas deve ser por interfaces bem definidas.

### 3.2 Configuração Centralizada
- Toda variável de ambiente deve ser lida **exclusivamente** em `backend/app/config.py`.
- Nenhum arquivo fora de `config.py` pode chamar `os.getenv()` diretamente.
- O objeto `settings = Settings()` deve ser importado pelos serviços.

### 3.3 Stateless por Design
- Nenhum estado de sessão deve ser armazenado em memória entre requisições.
- Arquivos de upload devem ser deletados após o processamento.
- O sistema deve funcionar com múltiplas instâncias em paralelo.

---

## 4. Regras de Qualidade de Código

### 4.1 Tipagem Estática (obrigatório)
- **Todo** código Python deve ter type hints completos (parâmetros e retorno).
- Proibido o uso de `Any` sem justificativa explícita em comentário.

```python
# ✅ Correto
def analyze_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:

# ❌ Proibido
def analyze_resume(self, resume_text, job_description):
```

### 4.2 Tratamento de Erros
- Toda integração externa (Groq API, leitura de PDF) deve estar envolta em `try/except`.
- Exceções devem ser capturadas, logadas e relançadas com contexto.
- O cliente **nunca** deve receber stacktrace ou detalhes internos de erro.

### 4.3 Logging
- Usar `logging` padrão do Python (proibido `print()` em produção).
- Nível mínimo de log: `INFO` para operações normais, `ERROR` para falhas.

### 4.4 Testes
- Cobertura de testes unitários mínima: **80%** das linhas do diretório `service/`.
- Testes devem usar `pytest` e `unittest.mock` para isolar dependências externas.
- Proibido fazer chamadas reais à Groq API nos testes.

---

## 5. Regras de Segurança

### 5.1 Uploads
- Somente arquivos `.pdf` são aceitos (validação de extensão e content-type).
- Tamanho máximo de upload: **10 MB**.
- Nome do arquivo salvo deve ser gerado com `uuid4()` (nunca usar o nome original).
- Arquivo deve ser **deletado** do disco imediatamente após processamento.

### 5.2 Segredos
- `GROQ_API_KEY` e qualquer credencial **nunca** devem ser commitados no repositório.
- O arquivo `.env` deve estar no `.gitignore`.
- O repositório deve conter apenas o `.env.example` com valores fictícios.

### 5.3 Validação de Entrada
- `job_description`: mínimo 50, máximo 10.000 caracteres.
- Texto de currículo extraído: mínimo 100, máximo 50.000 caracteres.
- Toda entrada do usuário deve ser sanitizada antes de ser enviada à IA.

---

## 6. Convenções de Nomeação

| Contexto | Convenção | Exemplo |
|---|---|---|
| Classes Python | PascalCase | `GroqService`, `PDFService` |
| Funções/Variáveis | snake_case | `analyze_resume`, `resume_text` |
| Constantes | UPPER_SNAKE_CASE | `MAX_PDF_SIZE_MB` |
| Arquivos Python | snake_case | `groq_service.py` |
| Rotas de API | kebab-case | `/api/v1/analyze` |
| Variáveis de Ambiente | UPPER_SNAKE_CASE | `GROQ_API_KEY` |

---

## 7. Proibições Explícitas

❌ Usar `requests` (usar `httpx`)  
❌ Usar `print()` em código de produção (usar `logging`)  
❌ Commitar arquivos `.env` com credenciais reais  
❌ Acessar camada `data` diretamente da camada `presentation`  
❌ Chamar `os.getenv()` fora de `config.py`  
❌ Commitar a pasta `venv/` no repositório  
❌ Fazer chamadas reais à API Groq dentro dos testes automatizados  
