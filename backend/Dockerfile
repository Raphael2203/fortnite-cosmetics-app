FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# corrigido: apontar para app.api.main (arquivo real que expõe 'app')
CMD ["bash", "-c", "alembic upgrade head && uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload"]