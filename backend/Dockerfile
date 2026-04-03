FROM python:3.13-slim

# Instala dependências de sistema para o psycopg2 se necessário
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Garante que o diretório atual está no PATH do Python
ENV PYTHONPATH=/app

# Comando de inicialização ajustado para produção
CMD alembic upgrade head && uvicorn app.api.main:app --host 0.0.0.0 --port $PORT
    # celery -A app.celery.config:celery_app worker --loglevel=info & \
    # celery -A app.celery.config:celery_app beat --loglevel=info & \
    