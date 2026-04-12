# Fortnite Cosmetics App

Aplicação para navegar e gerenciar cosmetics do Fortnite. Backend em FastAPI com SQLAlchemy e PostgreSQL; frontend em Vue.js 3 + TypeScript + Vite; orquestrado com Docker Compose.

## Sumário
- Visão geral
- Principais tecnologias
- Arquitetura
- Variáveis de ambiente
- Como rodar (Docker)
- Como rodar localmente
- Migrações
- Testes
- Endpoints úteis
- Deploy
- Contribuição
- Troubleshooting

## Visão geral
Este repositório contém uma API REST (FastAPI) que fornece dados sobre cosmetics do Fortnite e um frontend em Vue.js com TypeScript que consome essa API. O objetivo é permitir consulta, filtragem e gerenciamento de dados de cosmetics.

## Principais tecnologias
- **Backend**: FastAPI, Python 3.9+, SQLAlchemy, Alembic (migrações)
- **Banco de dados**: PostgreSQL 15
- **Frontend**: Vue 3, TypeScript, Vite
- **Containers**: Docker, Docker Compose
- **Testes**: pytest (backend)
- **Documentação da API**: OpenAPI/Swagger (/docs)

## Arquitetura
- `backend/` — FastAPI app com rotas, modelos SQLAlchemy e serviços
- `frontend/` — Vue 3 + TypeScript app criado com Vite
- `docker-compose.yml` — orquestração de backend, frontend e banco PostgreSQL
- `backend/alembic/` — migrações Alembic para o banco de dados
- `backend/tests/` — testes unitários com pytest

## Variáveis de ambiente

### Backend

Crie um arquivo `.env.local` na pasta `backend/`:

```
# Database (PostgreSQL)
DATABASE_URL=postgresql://postgres:password@db:5432/fortnite_db

# Environment
APP_ENV=development
APP_PORT=8000
```

### Frontend

Crie um arquivo `.env` na pasta `frontend/`:

```
# API Backend
VITE_API_URL=http://localhost:8000
```

Ajuste conforme o ambiente (local vs Docker).

## Como rodar com Docker (recomendado)

1. Configure as variáveis de ambiente:
   - `backend/.env.local` com `DATABASE_URL` e outras configs
   - `frontend/.env` com `VITE_API_URL`

2. Build e inicie os serviços:
   ```bash
   docker-compose up --build
   ```

3. Acesse os serviços:
   - **Backend**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Frontend**: http://localhost:4173

4. Parar os serviços:
   ```bash
   docker-compose down
   ```

## Rodando localmente (sem Docker)

**Pré-requisitos**: Python 3.9+, Node.js 16+, PostgreSQL 15

### Backend

1. Criar e ativar virtualenv:
   ```bash
   python -m venv .venv
   # Linux/macOS
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate
   ```

2. Instalar dependências:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Configurar `.env.local` com `DATABASE_URL` apontando para PostgreSQL local:
   ```
   DATABASE_URL=postgresql://postgres:password@localhost:5432/fortnite_db
   ```

4. Executar migrações:
   ```bash
   cd backend
   alembic upgrade head
   ```

5. (Opcional) Popular dados iniciais:
   ```bash
   python -m backend.scripts.seed
   ```

6. Iniciar backend:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend

1. Instalar dependências:
   ```bash
   cd frontend
   npm install
   ```

2. Configurar `.env` com URL da API:
   ```
   VITE_API_URL=http://localhost:8000
   ```

3. Rodar em desenvolvimento:
   ```bash
   npm run dev
   ```
   O app estará disponível em http://localhost:5173

## Migrações

O projeto usa Alembic para versionamento do banco de dados.

### Criar uma nova migração:
```bash
cd backend
alembic revision --autogenerate -m "descrição da mudança"
```

### Aplicar migrações:
```bash
cd backend
alembic upgrade head
```

### Reverter última migração:
```bash
cd backend
alembic downgrade -1
```

## Testes

### Backend (pytest):
```bash
cd backend
pytest tests/
# Teste específico
pytest tests/test_file.py::test_function
```

## Endpoints úteis

A documentação completa está disponível em `/docs` (Swagger UI) ou `/redoc` (ReDoc).

Alguns endpoints principais:
- `GET /docs` — Documentação interativa da API
- `GET /api/cosmetics` — Listar todos os cosmetics
- `GET /api/cosmetics/{id}` — Detalhes de um cosmetic específico

Consulte a documentação interativa para detalhes completos.

## Deploy

### Produção com Docker

1. Configure as variáveis de ambiente para produção
2. Crie imagens otimizadas com multi-stage builds
3. Use um serviço de container orchestration (Kubernetes, Docker Swarm, etc.)
4. Configure um proxy reverso (nginx) na frente do backend

### Banco de dados

- Use um banco PostgreSQL gerenciado (ex: AWS RDS, Azure Database for PostgreSQL, Supabase)
- Garanta backups automáticos e alta disponibilidade
- Configure credenciais seguras via secrets manager

### Segurança

- Mantenha as variáveis de ambiente seguras
- Use certificados SSL/TLS
- Configure CORS adequadamente
- Implemente rate limiting e autenticação conforme necessário

## Contribuição
1. Fork do repositório
2. Criar branch feature/bugfix
3. Abrir PR com descrição clara
4. Incluir testes para funcionalidades novas
5. Manter commits pequenos e claros

## Troubleshooting

**Erro de conexão com PostgreSQL**
- Verifique o `DATABASE_URL`
- Confirme que PostgreSQL está rodando
- Se usar Docker, aguarde o container db estar saudável (verifique healthcheck)

**Migrações falham**
- Rode `alembic upgrade head` para aplicar todas as migrações
- Se houver conflitos, revise os modelos e gere nova migração

**Frontend não carrega dados**
- Verifique `VITE_API_URL` e confirme que aponta para o backend correto
- Verifique CORS no backend (FastAPI deve estar configurado para permitir requisições do frontend)
- Abra o DevTools do navegador e verifique a aba Network

**Logs de container**
- Ver logs: `docker-compose logs -f backend` ou `docker-compose logs -f frontend`
- Ver tudo: `docker-compose logs -f`
