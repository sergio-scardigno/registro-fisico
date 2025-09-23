# Usar Python 3.11 slim como base
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorio instance (propiedad root)
RUN mkdir -p /app/instance

# Exponer puerto 5000
EXPOSE 5000

# Comando de inicio: inicializa la DB y luego arranca Flask
CMD ["sh", "-c", "python init_db.py && python app.py"]
