# BSI — Behavioral Signal Intelligence

Sistema de análise de sinais com interpretação via LLM, geração de outcomes, gestão de portfólio e histórico de decisões.

## Principais Módulos

- Signal ingestion
- LLM interpretation
- Outcome tracking
- Portfolio allocation
- Decision tracking

## Stack

- Backend: FastAPI + SQLAlchemy
- Frontend: React + TypeScript
- DB: SQLite (demo) / PostgreSQL (produção)
- LLM: OpenAI

## Como Rodar o Backend

```bash
cd bsi-backend
pip install -r requirements.txt
cp ../.env.example .env
python seed_db.py
uvicorn main:app --reload
```

## Como Rodar o Frontend

```bash
cd frontend
npm install
npm run dev
```

## URLs

- API: http://localhost:8000
- Frontend: http://localhost:5173

## Histórico do projeto

Os documentos históricos de fases, auditorias e changelogs detalhados estão organizados em:

- docs/history/changelogs/
- docs/history/readmes/

## Segurança

Nunca suba `.env` com credenciais reais. Use `.env.example` como template e mantenha credenciais apenas no ambiente local ou no gerenciador de segredos do deploy.
