# Feature Specification: CareerAI — Resume Analysis Platform

**Feature Branch**: `001-career-ai-core`

**Created**: 2026-06-01

**Status**: Implemented ✅

**Input**: User description: "Plataforma web que analisa currículos PDF contra vagas de emprego utilizando IA, fornecendo pontuação de compatibilidade, pontos fortes, pontos fracos e sugestões de melhoria."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upload de Currículo e Receber Análise (Priority: P1)

O candidato acessa a plataforma, faz upload do seu currículo em PDF, informa a descrição da vaga desejada e submete o formulário. O sistema extrai o texto do PDF, envia para a IA e exibe a análise completa na tela de resultados.

**Why this priority**: É o fluxo principal e único do MVP. Sem ele, nenhum outro valor pode ser entregue.

**Independent Test**: Pode ser testado completamente fazendo o upload de um PDF válido com uma descrição de vaga de pelo menos 50 caracteres e verificando que a página de resultados exibe pontuação, pontos fortes, pontos fracos e sugestões.

**Acceptance Scenarios**:

1. **Given** o candidato está na página inicial, **When** ele faz upload de um PDF válido e insere uma descrição de vaga com ≥ 50 caracteres e clica em "Analisar", **Then** o sistema exibe a página de resultados com `compatibility_score` (0–100), lista de `strengths`, `weaknesses` e `suggestions`.
2. **Given** o candidato faz upload de um arquivo que não é PDF, **When** ele submete o formulário, **Then** o sistema exibe mensagem de erro "File must be a PDF" sem processar o arquivo.
3. **Given** o candidato insere uma descrição de vaga com menos de 50 caracteres, **When** ele submete, **Then** o sistema exibe mensagem de erro de validação.

---

### User Story 2 - Rejeição de Uploads Inválidos (Priority: P2)

O sistema deve proteger o backend contra arquivos maliciosos ou não-suportados, exibindo mensagens de erro claras sem travar ou lançar exceções não tratadas.

**Why this priority**: Segurança e robustez são requisitos não funcionais críticos (RNF02). Sem validação, qualquer arquivo pode ser enviado ao servidor.

**Independent Test**: Pode ser testado enviando um arquivo `.exe`, `.txt` ou um PDF vazio e verificando que o sistema retorna mensagem de erro adequada sem erro 500.

**Acceptance Scenarios**:

1. **Given** o candidato envia um arquivo maior que 10 MB, **When** o backend processa o upload, **Then** retorna HTTP 400 com mensagem "File exceeds 10MB limit".
2. **Given** o candidato envia um PDF protegido por senha, **When** o PDFService tenta extrair o texto, **Then** retorna mensagem de erro clara ao usuário sem stacktrace exposto.
3. **Given** o candidato envia um PDF sem conteúdo textual, **When** o texto é extraído, **Then** o sistema retorna erro "Resume text is too short".

---

### User Story 3 - Persistência da Análise (Priority: P3)

Cada análise realizada deve ser salva automaticamente no banco de dados SQLite para eventual consulta futura, sem que o usuário precise fazer nenhuma ação adicional.

**Why this priority**: Requisito funcional RF08 de prioridade média. Não bloqueia o uso da plataforma caso falhe.

**Independent Test**: Pode ser verificado acessando o arquivo `career_ai.db` após uma análise e confirmando que existe um registro na tabela `analyses` com os campos corretos.

**Acceptance Scenarios**:

1. **Given** uma análise foi concluída com sucesso, **When** o sistema salva no banco, **Then** a tabela `analyses` contém um registro com `resume_text`, `job_description`, `compatibility_score`, `strengths`, `weaknesses`, `suggestions` e `created_at`.
2. **Given** o banco de dados está inacessível, **When** o sistema tenta salvar, **Then** a falha de persistência não impede a exibição dos resultados ao usuário.

---

### Edge Cases

- **PDF vazio**: Sistema retorna "Resume text is too short or empty" (mín. 100 chars)
- **PDF corrompido**: pdfplumber lança exceção capturada pelo PDFService → retorna "Failed to extract text from PDF"
- **PDF protegido por senha**: Tratado como PDF sem texto extraível
- **Vaga com texto excessivo**: Limitado a 10.000 caracteres com mensagem clara
- **Falha da Groq API**: Exceção capturada pelo GroqService com mensagem "Groq Analysis failed: ..."
- **Modelo Groq depreciado**: Configurável via `GROQ_MODEL` env var sem alterar código
- **Arquivo > 10 MB**: Rejeitado pelo backend antes da extração de texto

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Sistema MUST aceitar upload de arquivos PDF via formulário `multipart/form-data`
- **FR-002**: Sistema MUST extrair texto do PDF usando `pdfplumber` com suporte a múltiplas páginas
- **FR-003**: Usuário MUST poder informar a descrição da vaga em campo de texto livre (50–10.000 chars)
- **FR-004**: Sistema MUST integrar com a Groq API usando o modelo `llama-3.1-8b-instant` (configurável)
- **FR-005**: Sistema MUST retornar análise estruturada com `strengths`, `weaknesses` e `suggestions` (3–5 itens cada)
- **FR-006**: Sistema MUST retornar `compatibility_score` entre 0 e 100 (inteiro)
- **FR-007**: Sistema MUST exibir os resultados em página dedicada (`results.html`) com formatação clara
- **FR-008**: Sistema MUST persistir cada análise no SQLite com timestamp

### Key Entities

- **Analysis**: Representa uma análise completa. Atributos: `id`, `resume_text`, `job_description`, `compatibility_score`, `strengths`, `weaknesses`, `suggestions`, `created_at`
- **AnalysisResponse**: Schema Pydantic de response da API. Campos: `compatibility_score: int`, `strengths: List[str]`, `weaknesses: List[str]`, `suggestions: List[str]`

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Análise completa entregue em menos de 5 segundos para PDFs de até 10 MB (RNF01)
- **SC-002**: 100% dos uploads inválidos (extensão, tamanho, conteúdo vazio) retornam erro HTTP 400 com mensagem legível
- **SC-003**: Interface responsiva funciona em resoluções de 320px a 1440px sem quebra de layout (RNF03)
- **SC-004**: Cobertura de testes unitários ≥ 80% no diretório `backend/app/service/` (RNF04)
- **SC-005**: Aplicação dockerizada sobe com `docker-compose up` sem configuração adicional além das env vars (RNF05)
- **SC-006**: Zero credenciais commitadas no repositório — verificado por `git log --all` não conter `gsk_`

## Assumptions

- Usuários possuem currículos em formato PDF (OCR fora do escopo — apenas texto nativo)
- A Groq API free tier é suficiente para o volume de uso do MVP
- Não é necessário autenticação de usuários nesta versão
- O banco de dados SQLite é suficiente para o escopo MVP (sem necessidade de PostgreSQL)
- Render.com free tier com cold start de ~50s é aceitável para demonstração/TCC
- Apenas um currículo pode ser analisado por vez (sem processamento em lote)
