# BSI Operational Manual - Fase 7

Este documento descreve como operar o sistema BTC Signal Intelligence (BSI) em ambiente local.

## 1. Configuração de Ambiente
Escolha um template de configuração em `bsi-backend` e salve como `.env`:
- `.env.demo.example`: Para auditoria e demonstração com dados semente.
- `.env.minimal.example`: Para desenvolvimento rápido.
- `.env.real.example`: Template para conexão com Postgres e OpenAI real.

## 2. População de Dados (Seeds)
O script `seed_db.py` permite popular o banco local:
```bash
# Para massa completa de auditoria (Padrão)
python seed_db.py --mode demo --clean

# Para massa mínima de teste
python seed_db.py --mode minimal --clean
```

## 3. Execução Local
### Backend
```bash
cd bsi-backend
python -m uvicorn main:app --reload
```
Acesse: http://localhost:8000/docs (Swagger) ou http://localhost:8000/health (Status).

### Frontend
```bash
cd bsi-frontend
npm run dev
```
Acesse: http://localhost:5173

## 4. Observabilidade e Saúde
O sistema expõe um endpoint de governança:
`GET /api/v1/system/status`

Retorna:
- Status do banco de dados.
- Contagem de sinais, interpretações e desfechos.
- Indicador de presença de dados semente vs. reais.

## 5. Auditoria de Pacotes
Sempre execute a limpeza de arquivos temporários antes de gerar um pacote:
- Remova `__pycache__`
- Remova `.env` real
- Remova arquivos `.db` locais
