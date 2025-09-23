# 🚀 Guía de Despliegue en Servidor

## 📋 Pasos para Despliegue en SupaBase/Servidores Cloud

### 1. Conectar al Servidor
```bash
ssh usuario@tu-servidor.com
```

### 2. Instalar Docker (si no está instalado)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Clonar el Repositorio
```bash
git clone https://github.com/sergio-scardigno/registro-fisico.git
cd registro-fisico
```

### 4. Configurar Directorios y Permisos (IMPORTANTE)
```bash
# Crear directorio de datos
mkdir -p ./data

# Configurar permisos (Linux/Ubuntu)
sudo chown -R $USER:$USER ./data
chmod -R 775 ./data

# Crear directorio instance en el contenedor
mkdir -p /app/instance
```

### 5. Ejecutar la Aplicación
```bash
# Con Docker Compose (recomendado)
docker-compose -f docker-compose.prod.yml up -d

# O con Docker directamente
docker run -d -p 5000:5000 -v $(pwd)/data:/app/instance --name registro-fisico sergioscardigno82/registro-fisico:latest
```

### 6. Verificar Funcionamiento
```bash
# Ver estado de contenedores
docker ps | grep registro-fisico

# Ver logs
docker logs registro-fisico-app

# Verificar salud
curl http://localhost:5000
```

## 🔧 Comandos de Mantenimiento

### Ver Estado
```bash
docker ps | grep registro-fisico
docker-compose -f docker-compose.prod.yml ps
```

### Ver Logs
```bash
# Logs en tiempo real
docker-compose -f docker-compose.prod.yml logs -f

# Logs específicos
docker logs registro-fisico-app
```

### Reiniciar
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Actualizar
```bash
# Descargar última versión
docker-compose -f docker-compose.prod.yml pull

# Reiniciar con nueva versión
docker-compose -f docker-compose.prod.yml up -d
```

### Detener
```bash
docker-compose -f docker-compose.prod.yml down
```

### Respaldar Datos
```bash
# Crear respaldo
tar -czf backup-$(date +%Y%m%d).tar.gz ./data/

# Restaurar respaldo
tar -xzf backup-YYYYMMDD.tar.gz
```

## 🌐 Configuración de Dominio (Opcional)

### Con Nginx
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Con Apache
```apache
<VirtualHost *:80>
    ServerName tu-dominio.com
    ProxyPreserveHost On
    ProxyPass / http://localhost:5000/
    ProxyPassReverse / http://localhost:5000/
</VirtualHost>
```

## 🔒 Configuración de Firewall

```bash
# Abrir puerto 5000
sudo ufw allow 5000
sudo ufw enable

# O abrir puerto 80/443 si usas proxy
sudo ufw allow 80
sudo ufw allow 443
```

## 📊 Monitoreo

### Verificar Salud
```bash
# Health check
curl -f http://localhost:5000

# Ver uso de recursos
docker stats registro-fisico-app
```

### Logs de Sistema
```bash
# Ver logs del sistema
sudo journalctl -u docker

# Ver logs de la aplicación
docker logs registro-fisico-app --tail 100
```

## 🚨 Solución de Problemas

### Error de Permisos
```bash
# Si hay problemas de permisos
sudo chown -R $USER:$USER ./data
chmod -R 775 ./data
```

### Error de Puerto en Uso
```bash
# Ver qué está usando el puerto 5000
sudo netstat -tulpn | grep :5000

# Cambiar puerto en docker-compose.prod.yml
ports:
  - "8080:5000"  # Cambiar 5000 por 8080
```

### Error de Memoria
```bash
# Ver uso de memoria
docker stats

# Limpiar contenedores no utilizados
docker system prune -f
```

### Error de Base de Datos
```bash
# Ver logs de la base de datos
docker logs registro-fisico-app | grep -i error

# Reiniciar solo la base de datos
docker-compose -f docker-compose.prod.yml restart
```

## 📝 Notas Importantes

1. **Permisos**: Es crucial configurar correctamente los permisos del directorio `./data`
2. **Puerto**: La aplicación corre en el puerto 5000 por defecto
3. **Datos**: Los datos se almacenan en `./data/` y se montan en `/app/instance`
4. **Logs**: Siempre revisa los logs si hay problemas
5. **Respaldos**: Haz respaldos regulares de la carpeta `./data/`

## 🔄 Actualización Automática

Para configurar actualizaciones automáticas, puedes usar un cron job:

```bash
# Editar crontab
crontab -e

# Agregar línea para actualizar cada día a las 2 AM
0 2 * * * cd /ruta/a/registro-fisico && docker-compose -f docker-compose.prod.yml pull && docker-compose -f docker-compose.prod.yml up -d
```
