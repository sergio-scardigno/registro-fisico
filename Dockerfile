FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

WORKDIR /app

RUN apt-get update && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear usuario y directorio instance con permisos correctos
RUN adduser --disabled-password --gecos '' appuser \
    && mkdir -p /app/instance \
    && chown -R appuser:appuser /app/instance

USER appuser

EXPOSE 5000

CMD ["python", "init_db.py"]
