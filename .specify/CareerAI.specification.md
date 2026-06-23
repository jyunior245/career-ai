# CareerAI - Analisador Inteligente de Currículos

## Sumário Executivo
Aplicação web que analisa currículos em PDF contra vagas de emprego, utilizando IA (Groq API) para fornecer feedback personalizado sobre compatibilidade, pontos fortes, pontos fracos e recomendações de melhoria.

---

## Problema Resolvido
Candidatos enfrentam dificuldades em validar se seus currículos estão adequados para uma vaga específica, sem entender quais competências faltam, quais experiências são relevantes ou como melhorar suas chances de contratação. O CareerAI fornece avaliação automatizada e instantânea.

---

## Histórias de Usuário

### US01 - Upload de Currículo
**Como** candidato
**Quero** enviar meu currículo em PDF
**Para que** ele seja analisado automaticamente

**Critérios de Aceitação:**
- ✅ Sistema aceita arquivos PDF
- ✅ Validação de tipo de arquivo
- ✅ Rejeição de formatos inválidos
- ✅ Mensagens de erro claras no upload

---

### US02 - Informar Vaga
**Como** candidato
**Quero** informar a descrição da vaga desejada
**Para que** a análise seja contextualizada

**Critérios de Aceitação:**
- ✅ Sistema aceita descrições textuais
- ✅ Vaga enviada juntamente com currículo

---

### US03 - Visualizar Texto Extraído
**Como** candidato
**Quero** visualizar o texto extraído do currículo
**Para** confirmar que o PDF foi processado corretamente

**Critérios de Aceitação:**
- ✅ Prévia do conteúdo extraído
- ✅ Texto legível e bem formatado

---

### US04 - Receber Análise
**Como** candidato
**Quero** receber uma avaliação automática
**Para** identificar melhorias no currículo

**Critérios de Aceitação:**
- ✅ Apresentação de pontos fortes
- ✅ Apresentação de pontos fracos
- ✅ Recomendações de melhoria

---

### US05 - Receber Pontuação
**Como** candidato
**Quero** visualizar uma pontuação de aderência
**Para** entender meu alinhamento com a vaga

**Critérios de Aceitação:**
- ✅ Nota entre 0 e 100
- ✅ Justificativa da pontuação

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF01 | Upload de currículo PDF | Alta |
| RF02 | Extração automática de texto do PDF | Alta |
| RF03 | Inserção da descrição da vaga | Alta |
| RF04 | Integração com Groq API | Alta |
| RF05 | Geração de análise automática (pontos fortes/fracos) | Alta |
| RF06 | Geração de pontuação (0-100) | Alta |
| RF07 | Exibição dos resultados | Alta |
| RF08 | Persistência das análises | Média |

---

## Requisitos Não Funcionais

### Desempenho (RNF01)
- Tempo de resposta < 5 segundos para currículos comuns
- Processamento assíncrono para arquivos grandes

### Segurança (RNF02)
- Validação de uploads (tipo, tamanho, conteúdo)
- Sanitização de entradas
- Proteção contra uploads maliciosos
- Isolamento de processamento de PDFs

### Compatibilidade (RNF03)
- Desktop (Chrome, Firefox, Safari, Edge)
- Tablets (iOS, Android)
- Smartphones (iOS, Android)
- Responsividade 100%

### Qualidade (RNF04)
- Código tipado (Python type hints)
- Arquitetura em camadas (apresentação, serviço, dados)
- Cobertura de testes unitários ≥ 80%
- Documentação de API

### Escalabilidade (RNF05)
- Compatível com Docker
- Pronto para deploy em cloud
- Stateless para múltiplas instâncias

---

## Casos de Borda

| Caso | Tratamento |
|------|-----------|
| PDF vazio | Mensagem: "PDF sem conteúdo detectado" |
| PDF corrompido | Mensagem: "PDF inválido ou corrompido" |
| PDF protegido por senha | Mensagem: "PDF protegido, tente novamente" |
| Vaga não informada | Usar análise genérica de competências |
| Arquivo > 10MB | Rejeitar com mensagem de tamanho |
| Falha da API Groq | Fallback ou mensagem de indisponibilidade |
| Sem JavaScript habilitado | Fornecer fallback (opcional) |

---

## Arquitetura

### Stack Tecnológico
- **Backend:** Python 3.10+ (Flask)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **PDF Processing:** PyPDF2 ou pdfplumber
- **IA:** Groq API (LLM)
- **Database:** SQLite (opcional, para persistência)
- **Containerização:** Docker
- **Deploy:** Cloud-ready

### Camadas
1. **Presentation Layer:** Flask routes, HTML/CSS/JS
2. **Service Layer:** PDF extraction, validation, Groq integration
3. **Data Layer:** Database models, persistence

---

## Fora do Escopo

❌ Cadastro de usuários
❌ Login/Autenticação
❌ Histórico por usuário
❌ Integração LinkedIn
❌ OCR (reconhecimento de imagem)
❌ Banco de dados vetorial
❌ Chat em tempo real
❌ Análise de múltiplos currículos simultâneos

---

## Critérios de Aceitação Técnicos

- [ ] PDF upload com validação
- [ ] Extração de texto funcional
- [ ] Integração com Groq API documentada
- [ ] Análise estruturada (JSON)
- [ ] Pontuação entre 0-100
- [ ] Interface responsiva
- [ ] Testes unitários com cobertura ≥ 80%
- [ ] Documentação completa
- [ ] Docker pronto
- [ ] Sem erros em console (frontend e backend)

---

## Glossário

- **Currículo:** Documento PDF contendo histórico profissional
- **Vaga:** Descrição textual dos requisitos da posição
- **Análise:** Avaliação de compatibilidade entre CV e vaga
- **Pontuação:** Nota numérica (0-100) de aderência
- **Feedback:** Pontos fortes, fracos e recomendações

---

## Próximos Passos

1. ✅ Especificação aprovada
2. ⏳ Implementação de features
3. ⏳ Testes e validação
4. ⏳ Deploy e documentação
