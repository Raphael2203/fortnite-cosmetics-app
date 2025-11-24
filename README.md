# Fortnite Cosmetics App

Aplicação para navegar e gerenciar cosmetics do Fortnite. Backend em FastAPI com SQLAlchemy e MySQL; frontend em Vue.js + Vite; orquestrado com Docker Compose.

## Sumário
- Visão geral
- Principais tecnologias
- Arquitetura
- Variáveis de ambiente
- Como rodar (Docker e local)
- Migrações e seed
- Frontend (desenvolvimento)
- Testes
- Endpoints úteis
- Contribuição e licença
- Troubleshooting

## Visão geral
Este repositório contém uma API REST (FastAPI) que fornece dados sobre cosmetics do Fortnite e um frontend em Vue.js que consome essa API. O objetivo é permitir consulta, filtragem e sincronização de dados de cosmetics.

## Principais tecnologias
- Backend: FastAPI, Python, SQLAlchemy, Alembic (migrações)
- Banco de dados: MySQL
- Frontend: Vue 3, Vite
- Containers / Orquestração: Docker, Docker Compose
- Testes: pytest (backend)
- Documentação da API: OpenAPI (/docs via FastAPI)

## Arquitetura
- backend/ — FastAPI app com rotas, modelos SQLAlchemy e serviços
- frontend/ — Vue 3 app criado com Vite
- docker-compose.yml — serviço para backend, frontend e banco MySQL
- migrations/ — migrações Alembic
- scripts/ — scripts utilitários (seed, sync de cosmetics)

## Variáveis de ambiente
Crie um arquivo `.env` (ou copie `.env.example`) com as variáveis abaixo:

- BACKEND_HOST=0.0.0.0
- BACKEND_PORT=8000
- DATABASE_URL=mysql+pymysql://user:password@db:3306/fortnite_db
- DATABASE_HOST=db
- DATABASE_USER=youruser
- DATABASE_PASSWORD=yourpassword
- DATABASE_NAME=fortnite_db
- SECRET_KEY=uma_chave_secreta_para_tokens
- FRONTEND_API_URL=http://localhost:8000/api

Ajuste conforme o ambiente (local vs Docker).

## Como rodar com Docker (recomendado)
1. Copie o arquivo de exemplo de ambiente:
   - cp .env.example .env
   - Ajuste variáveis se necessário.
2. Build e up:
   - docker-compose up --build
3. Serviços principais:
   - Backend: http://localhost:8000 (OpenAPI: http://localhost:8000/docs)
   - Frontend: http://localhost:4173
4. Parar:
   - docker-compose down

## Rodando localmente (sem Docker)
Pré-requisitos: Python 3.9+, Node.js 16+, MySQL local.

Backend:
1. Criar e ativar virtualenv:
   - python -m venv .venv
   - source .venv/bin/activate (Linux/macOS) ou .venv\Scripts\activate (Windows)
2. Instalar dependências:
   - pip install -r requirements.txt
3. Configurar `.env` com DATABASE_URL apontando para o MySQL local.
4. Executar migrações:
   - alembic upgrade head
5. Opcional: rodar seed para popular dados iniciais:
   - python scripts/seed.py
6. Iniciar backend:
   - uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

Frontend:
1. Entrar na pasta frontend:
   - cd frontend
2. Instalar dependências:
   - npm install
3. Ajustar variável de API (por exemplo VITE_API_URL) no .env.local ou em config.
4. Rodar em dev:
   - npm run dev (Vite normalmente roda em http://localhost:4173)

## Migrações e seed
- Alembic (migrations):
  - Criar migração: alembic revision --autogenerate -m "descrição"
  - Aplicar migrações: alembic upgrade head
- Seed:
  - scripts/seed.py (exemplo) — roda scripts para popular tabelas iniciais. Execute com o ambiente configurado, p.ex. python scripts/seed.py

## Testes
- Backend (pytest):
  - pytest tests/'nome_do_teste.py'

## Endpoints úteis
- OpenAPI: GET /docs
- Healthcheck (exemplo): GET /health
- Cosmetics list: GET /api/cosmetics
- Cosmetic detail: GET /api/cosmetics/{id}
- Sincronizar catálogo (admin/script): POST /api/admin/sync

(Endereços reais podem variar conforme implementação; consulte /docs para detalhes.)

## Deploy
- Em produção, use um servidor ASGI (uvicorn/gunicorn + uvicorn workers) e um proxy (nginx).
- Configure variáveis de ambiente seguras e credenciais do DB.
- Se usar Docker, crie imagens otimizadas (multi-stage) e utilize um banco gerenciado ou cluster de containers.

## Contribuição
1. Fork do repositório
2. Criar branch feature/bugfix
3. Abrir PR com descrição clara
4. Incluir testes para funcionalidades novas
5. Manter commits pequenos e claros

## Licença
Adicionar arquivo LICENSE no repositório. Por padrão, use MIT ou escolha a licença desejada.

## Troubleshooting
- Erro de conexão com MySQL: verifique DATABASE_URL, usuário/senha, e se o container do DB está pronto.
- Migrações: rode alembic upgrade head. Se houver conflitos, revisar modelos e gerar nova migration.
- Frontend não carrega dados: verifique VITE_API_URL / FRONTEND_API_URL e CORS no backend.
- Logs: verifique logs do container via docker-compose logs -f <service>