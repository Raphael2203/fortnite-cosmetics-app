FROM python:3.13-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD sh -c "alembic upgrade head && python -m app.services.sync_service && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    