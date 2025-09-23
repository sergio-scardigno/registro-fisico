# Usar Python 3.11 slim como base
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear usuario no-root para seguridad
RUN adduser --disabled-password --gecos '' appuser

# Crear directorio para la base de datos como root
RUN mkdir -p instance

# Cambiar propietario de todo el directorio /app al usuario appuser
RUN chown -R appuser:appuser /app

# Cambiar a usuario appuser
USER appuser

# Crear directorio instance como appuser
RUN mkdir -p /app/instance

# Dar permisos correctos al directorio instance
RUN chmod 755 /app/instance

# Exponer puerto 5000
EXPOSE 5000

# Comando de inicio
CMD ["sh", "-c", "python init_db.py && python app.py"]
