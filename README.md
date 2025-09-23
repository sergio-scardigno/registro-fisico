# Registro Físico - Aplicación Flask

Una aplicación web desarrollada en Python con Flask para registrar y gestionar mediciones corporales de múltiples personas, incluyendo peso, IMC, pliegues cutáneos, circunferencias y **evaluación AAHPERD** para población universitaria.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=flat-square&logo=github)](https://github.com/sergio-scardigno/registro-fisico)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-Image-blue?style=flat-square&logo=docker)](https://hub.docker.com/repository/docker/sergioscardigno82/registro-fisico)
[![Python](https://img.shields.io/badge/Python-3.11+-green?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![AAHPERD](https://img.shields.io/badge/AAHPERD-Certified-orange?style=flat-square)](http://www.saludmed.com/CtrlPeso/Labs/Pliegues.html)

## 🔗 Enlaces Rápidos

- **📁 [Repositorio GitHub](https://github.com/sergio-scardigno/registro-fisico)** - Código fuente y documentación
- **🐳 [Imagen Docker Hub](https://hub.docker.com/repository/docker/sergioscardigno82/registro-fisico)** - Imagen lista para usar
- **📖 [Documentación](https://github.com/sergio-scardigno/registro-fisico#readme)** - Guía completa de uso

## ✨ Características Principales

### 🎯 **Gestión de Usuarios**
- **👥 Múltiples Usuarios**: Gestión completa de usuarios con perfiles individuales
- **📊 Registro de Peso e IMC**: Calcula automáticamente el Índice de Masa Corporal por usuario
- **📏 Pliegues Cutáneos**: Registro de 6 pliegues corporales (tricipital, subescapular, suprailíaco, abdominal, muslo anterior, pantorrilla)
- **📐 Circunferencias**: Medición de 8 circunferencias corporales (cuello, pecho, brazo, antebrazo, cintura, cadera, muslo, pantorrilla)

### 🏆 **Evaluación AAHPERD (NUEVO)**
- **📊 Método Oficial AAHPERD**: Evaluación basada en estándares científicos para población universitaria
- **📈 Suma de Pliegues Cutáneos (SPC)**: Cálculo automático usando tríceps + subescapular
- **🎯 Percentilas Poblacionales**: Posición del usuario respecto a población universitaria (18-25 años)
- **🏅 Clasificación Motivacional**: Excelente, Muy Bueno, Bueno, Promedio, Bajo Promedio, Necesita Mejora
- **💡 Interpretación Personalizada**: Mensajes motivacionales y recomendaciones específicas según percentila

### 📊 **Análisis y Estadísticas**
- **📈 Estadísticas Individuales**: Visualización de progreso y estadísticas por usuario
- **📋 Tablas de Clasificación**: Rangos oficiales AAHPERD para hombres y mujeres universitarios
- **🎨 Interfaz Moderna**: Diseño responsive con Bootstrap 5
- **💾 Base de Datos**: SQLite para almacenamiento local con relaciones entre usuarios y registros

### 🔄 **Importación y Exportación (NUEVO)**
- **📤 Exportar CSV**: Descarga completa de registros con todos los datos y cálculos
- **📥 Importar CSV**: Carga masiva de registros desde archivos CSV
- **🏃‍♂️ Compatibilidad Garmin**: Importación directa desde Garmin Connect
- **✅ Validación Robusta**: Manejo de errores y validación de datos

## 🚀 Inicio Rápido

### Usar con Docker (Recomendado)

```bash
# 1. Descargar y ejecutar la imagen
docker run -d -p 5000:5000 -v $(pwd)/data:/app/instance --name registro-fisico sergioscardigno82/registro-fisico:latest

# 2. Abrir en el navegador
# http://localhost:5000
```

### Usar desde GitHub

```bash
# 1. Clonar el repositorio
git clone https://github.com/sergio-scardigno/registro-fisico.git
cd registro-fisico

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python app.py
```

## 📋 Funcionalidades Detalladas

### 🎯 **Gestión de Usuarios**
- ✅ Crear, editar y eliminar usuarios
- ✅ Perfiles individuales con datos personales
- ✅ Historial completo de registros por usuario
- ✅ Estadísticas personalizadas

### 📊 **Registro de Mediciones**
- ✅ **Datos Básicos**: Peso, altura, IMC automático
- ✅ **Pliegues Cutáneos**: 6 mediciones con 3 tomas individuales + promedio
- ✅ **Circunferencias**: 8 mediciones corporales
- ✅ **Validación**: Campos requeridos y rangos válidos
- ✅ **Edición**: Modificar registros existentes

### 🏆 **Evaluación AAHPERD**
- ✅ **SPC (Suma de Pliegues Cutáneos)**: Tríceps + Subescapular
- ✅ **Percentilas**: Posición en población universitaria (5, 10, 25, 50, 75, 90, 95)
- ✅ **Clasificación**: 6 niveles motivacionales con colores
- ✅ **Interpretación**: Mensajes personalizados según percentila
- ✅ **Tablas Oficiales**: Rangos específicos para hombres y mujeres universitarios

### 📈 **Estadísticas Avanzadas**
- ✅ **Progreso de Peso**: Inicial vs actual, diferencias, promedios
- ✅ **Análisis IMC**: Clasificación y tendencias
- ✅ **Evaluación AAHPERD**: SPC, percentilas, clasificación
- ✅ **Interpretación Motivacional**: Recomendaciones personalizadas
- ✅ **Historial Completo**: Tabla con todos los registros

### 🔄 **Importación/Exportación**
- ✅ **Exportar CSV**: Descarga completa con todos los datos
- ✅ **Importar CSV**: Carga masiva desde archivos
- ✅ **Formato Garmin**: Compatibilidad con Garmin Connect
- ✅ **Validación**: Manejo de errores por fila
- ✅ **Respaldos**: Sistema completo de respaldo y migración

## 🚀 Instalación

### Opción 1: Instalación Local

1. **Clonar o descargar el proyecto**
   ```bash
   git clone https://github.com/sergio-scardigno/registro-fisico.git
   cd registro-fisico
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

### Opción 2: Usando Docker

1. **Clonar el proyecto**
   ```bash
   git clone https://github.com/sergio-scardigno/registro-fisico.git
   cd registro-fisico
   ```

2. **Construir y ejecutar con Docker Compose**
   ```bash
   # Producción
   docker-compose up -d
   
   # Desarrollo
   docker-compose --profile dev up -d
   ```

3. **O usar Docker directamente**
   ```bash
   # Construir la imagen
   docker build -t registro-fisico .
   
   # Ejecutar el contenedor
   docker run -p 5000:5000 -v $(pwd)/data:/app/instance registro-fisico
   ```

### Opción 3: Usando Imagen de Docker Hub

1. **Descargar y ejecutar la imagen**
   ```bash
   docker run -d -p 5000:5000 -v $(pwd)/data:/app/instance --name registro-fisico sergioscardigno82/registro-fisico:latest
   ```

### Opción 4: Despliegue en Servidor

1. **Clonar el repositorio en el servidor**
   ```bash
   git clone https://github.com/sergio-scardigno/registro-fisico.git
   cd registro-fisico
   ```

2. **Configurar permisos del directorio de datos**
   ```bash
   # Crear directorio de datos
   mkdir -p ./data
   
   # Configurar permisos (Linux/Ubuntu)
   sudo chown -R $USER:$USER ./data
   chmod -R 775 ./data
   
   # Crear directorio instance en el contenedor
   mkdir -p /app/instance
   ```

3. **Ejecutar con Docker Compose**
   ```bash
   # Producción
   docker-compose -f docker-compose.prod.yml up -d
   
   # O con Docker directamente
   docker run -d -p 5000:5000 -v $(pwd)/data:/app/instance --name registro-fisico sergioscardigno82/registro-fisico:latest
   ```

## 📖 Uso

1. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

2. **Funcionalidades disponibles:**
   - **🏠 Inicio**: Lista de usuarios registrados
   - **👥 Gestión de Usuarios**: Crear, editar y administrar usuarios
   - **👤 Perfil de Usuario**: Ver registros y datos de un usuario específico
   - **➕ Nuevo Registro**: Crear una nueva medición para un usuario
   - **👁️ Ver Registro**: Detalles completos de una medición
   - **✏️ Editar Registro**: Modificar datos existentes
   - **📊 Estadísticas**: Análisis de progreso y tendencias por usuario
   - **📤 Exportar CSV**: Descargar todos los registros
   - **📥 Importar CSV**: Cargar registros desde archivo

## 🏆 Evaluación AAHPERD

### ¿Qué es AAHPERD?
La **American Alliance for Health, Physical Education, Recreation and Dance (AAHPERD)** establece estándares científicos para evaluación de composición corporal en población universitaria.

### Método Implementado
- **Pliegues Utilizados**: Tríceps + Subescapular
- **Población Objetivo**: Universitarios (18-25 años)
- **Cálculo**: Suma de Pliegues Cutáneos (SPC)
- **Clasificación**: 6 niveles motivacionales
- **Percentilas**: Posición respecto a población de referencia

### Tablas de Clasificación

#### Hombres Universitarios (18-25 años)
| Clasificación | SPC (mm) | Percentila |
|---------------|----------|------------|
| Excelente     | ≤ 10     | 5-10       |
| Muy Bueno     | 11-13    | 10-25      |
| Bueno         | 14-17    | 25-50      |
| Promedio      | 18-22    | 50-75      |
| Bajo Promedio | 23-28    | 75-90      |
| Necesita Mejora | > 28   | 90+        |

#### Mujeres Universitarias (18-25 años)
| Clasificación | SPC (mm) | Percentila |
|---------------|----------|------------|
| Excelente     | ≤ 15     | 5-10       |
| Muy Bueno     | 16-19    | 10-25      |
| Bueno         | 20-24    | 25-50      |
| Promedio      | 25-30    | 50-75      |
| Bajo Promedio | 31-37    | 75-90      |
| Necesita Mejora | > 37   | 90+        |

## 📁 Estructura del Proyecto

```
registro-fisico/
├── app.py                    # Aplicación principal Flask
├── init_db.py               # Inicialización de base de datos
├── requirements.txt         # Dependencias del proyecto
├── Dockerfile              # Configuración Docker
├── docker-compose.yml      # Orquestación de contenedores
├── .dockerignore           # Archivos ignorados en Docker
├── README.md               # Este archivo
├── templates/              # Plantillas HTML
│   ├── base.html           # Plantilla base
│   ├── index.html          # Página principal
│   ├── usuarios.html       # Lista de usuarios
│   ├── usuario.html        # Perfil de usuario
│   ├── nuevo_usuario.html  # Crear usuario
│   ├── editar_usuario.html # Editar usuario
│   ├── nuevo_registro.html # Crear registro
│   ├── ver_registro.html   # Ver registro
│   ├── editar_registro.html # Editar registro
│   ├── estadisticas.html   # Estadísticas del usuario
│   ├── importar_csv.html   # Importar desde Garmin
│   ├── importar_registros.html # Importar CSV completo
│   └── guia_mediciones.html # Guía de mediciones
├── static/                 # Archivos estáticos
│   ├── pliegues/           # Imágenes de pliegues
│   └── *.gif               # Animaciones de medición
└── data/                   # Base de datos (volumen Docker)
    └── registro_fisico.db  # Base de datos SQLite
```

## 🔧 Características Técnicas

### Modelo de Datos
- **Usuario**: Modelo para gestionar personas:
  - Datos personales: nombre, apellido, fecha de nacimiento, género, altura
  - Estado activo/inactivo
  - Relación con registros físicos
  
- **RegistroFisico**: Modelo principal que incluye:
  - Asociación con usuario específico
  - Datos básicos: peso, altura, IMC
  - Pliegues cutáneos (6 mediciones con 3 tomas + promedio)
  - Circunferencias (8 mediciones)
  - Cálculos derivados: porcentaje grasa, SPC, percentilas AAHPERD

### Funcionalidades Implementadas
- **Gestión completa de usuarios** con CRUD
- **Cálculo automático de IMC** con clasificación por usuario
- **Evaluación AAHPERD** con percentilas y clasificación motivacional
- **Sumatoria de pliegues** para análisis corporal
- **Estadísticas individuales** (peso inicial vs actual, promedios, etc.)
- **Importación/Exportación** de datos en formato CSV
- **Interfaz responsive** compatible con móviles
- **Validación de formularios** en frontend y backend
- **Confirmación de eliminación** para evitar pérdida de datos
- **Navegación intuitiva** entre usuarios y sus registros

### Clasificación de IMC
- **Bajo peso**: IMC < 18.5
- **Peso normal**: IMC 18.5 - 24.9
- **Sobrepeso**: IMC 25.0 - 29.9
- **Obesidad**: IMC ≥ 30.0

## 🔄 Importación y Exportación

### Exportar Datos
1. Ve a **Estadísticas** del usuario
2. Haz clic en **"Exportar CSV"**
3. El archivo se descarga automáticamente con todos los datos

### Importar Datos
1. Ve a **Estadísticas** del usuario
2. Haz clic en **"Importar CSV"**
3. Selecciona el archivo CSV
4. Haz clic en **"Importar Registros"**

### Formato CSV
El archivo CSV incluye:
- Datos básicos (fecha, peso, altura, IMC)
- Pliegues cutáneos (3 mediciones + promedio)
- Circunferencias corporales
- Cálculos derivados (porcentaje grasa, SPC, percentilas)

## 🚀 Despliegue en Servidor

### Preparación del Servidor

1. **Instalar Docker y Docker Compose**
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

2. **Clonar el repositorio**
   ```bash
   git clone https://github.com/sergio-scardigno/registro-fisico.git
   cd registro-fisico
   ```

3. **Configurar directorios y permisos**
   ```bash
   # Crear directorio de datos
   mkdir -p ./data
   
   # Configurar permisos (Linux/Ubuntu)
   sudo chown -R $USER:$USER ./data
   chmod -R 775 ./data
   
   # Crear directorio instance en el contenedor
   mkdir -p /app/instance
   ```

### Despliegue en SupaBase o Servidores Cloud

Para servidores como SupaBase, DigitalOcean, AWS, etc.:

```bash
# 1. Conectar al servidor
ssh usuario@tu-servidor.com

# 2. Clonar repositorio
git clone https://github.com/sergio-scardigno/registro-fisico.git
cd registro-fisico

# 3. Configurar permisos (IMPORTANTE)
mkdir -p ./data
sudo chown -R $USER:$USER ./data
chmod -R 775 ./data
mkdir -p /app/instance

# 4. Ejecutar con Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# 5. Verificar funcionamiento
curl http://localhost:5000
```

4. **Ejecutar la aplicación**
   ```bash
   # Con Docker Compose (recomendado)
   docker-compose -f docker-compose.prod.yml up -d
   
   # O con Docker directamente
   docker run -d -p 5000:5000 -v $(pwd)/data:/app/instance --name registro-fisico sergioscardigno82/registro-fisico:latest
   ```

5. **Verificar que esté funcionando**
   ```bash
   # Ver estado de contenedores
   docker ps | grep registro-fisico
   
   # Ver logs
   docker logs registro-fisico
   
   # Verificar salud
   curl http://localhost:5000
   ```

### Configuración de Firewall (Opcional)

```bash
# Abrir puerto 5000 (si es necesario)
sudo ufw allow 5000
sudo ufw enable
```

### Configuración de Proxy Reverso (Nginx)

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

### Script de Despliegue Automatizado

Para facilitar el despliegue, se incluye un script automatizado:

```bash
# Hacer ejecutable (Linux/Ubuntu)
chmod +x deploy-server.sh

# Comandos disponibles
./deploy-server.sh install    # Instalar Docker y configurar entorno
./deploy-server.sh setup      # Configurar directorios y permisos
./deploy-server.sh start      # Iniciar la aplicación
./deploy-server.sh stop       # Detener la aplicación
./deploy-server.sh restart    # Reiniciar la aplicación
./deploy-server.sh status     # Ver estado de la aplicación
./deploy-server.sh update     # Actualizar a la última versión
./deploy-server.sh backup     # Crear respaldo de datos
./deploy-server.sh logs       # Ver logs en tiempo real
./deploy-server.sh help       # Mostrar ayuda
```

### Comandos de Mantenimiento Manual

```bash
# Actualizar aplicación
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Reiniciar aplicación
docker-compose -f docker-compose.prod.yml restart

# Detener aplicación
docker-compose -f docker-compose.prod.yml down

# Respaldar datos
tar -czf backup-$(date +%Y%m%d).tar.gz ./data/
```

## 🐳 Docker Hub

### Usar la Imagen desde Docker Hub

```bash
# Descargar y ejecutar (última versión)
docker run -d -p 5000:5000 -v $(pwd)/data:/app/instance --name registro-fisico sergioscardigno82/registro-fisico:latest

# Usar una versión específica
docker run -d -p 5000:5000 -v $(pwd)/data:/app/instance --name registro-fisico sergioscardigno82/registro-fisico:v2.0.0

# Con Docker Compose
version: '3.8'
services:
  registro-fisico:
    image: sergioscardigno82/registro-fisico:latest
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/instance
    restart: unless-stopped
```

### Tags Disponibles

- `latest` - Última versión estable (v2.0.0)
- `v2.0.0` - Versión con evaluación AAHPERD e importación/exportación
- `v1.0.1` - Versión anterior

### Comandos Útiles

```bash
# Ver todas las versiones disponibles
docker search sergioscardigno82/registro-fisico

# Ver información de la imagen
docker inspect sergioscardigno82/registro-fisico:latest

# Ver logs del contenedor
docker logs registro-fisico

# Detener contenedor
docker stop registro-fisico

# Iniciar contenedor
docker start registro-fisico

# Reiniciar contenedor
docker restart registro-fisico
```

## 🚀 Próximas Mejoras

- [ ] **Gráficos de Progreso**: Visualización con Chart.js
- [ ] **Exportación PDF**: Reportes en formato PDF
- [ ] **API REST**: Para integración con apps móviles
- [ ] **Autenticación**: Sistema de usuarios y sesiones
- [ ] **Notificaciones**: Recordatorios de mediciones
- [ ] **Comparación**: Análisis entre usuarios
- [ ] **Objetivos**: Establecimiento de metas personales

## 📚 Referencias Científicas

- **AAHPERD Standards**: [saludmed.com](http://www.saludmed.com/CtrlPeso/Labs/Pliegues.html)
- **Método de Pliegues Cutáneos**: Evaluación de composición corporal
- **Población Universitaria**: Estándares para 18-25 años
- **Percentilas Poblacionales**: Clasificación según estudios científicos

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres contribuir al proyecto:

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

### Reportar Problemas

Si encuentras algún problema o tienes sugerencias:

- **🐛 [Reportar Bug](https://github.com/sergio-scardigno/registro-fisico/issues/new?template=bug_report.md)**
- **💡 [Sugerir Mejora](https://github.com/sergio-scardigno/registro-fisico/issues/new?template=feature_request.md)**
- **❓ [Hacer Pregunta](https://github.com/sergio-scardigno/registro-fisico/discussions)**

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🆘 Soporte

Para reportar problemas o sugerir mejoras, por favor crea un issue en el [repositorio del proyecto](https://github.com/sergio-scardigno/registro-fisico/issues).

---

**Desarrollado con ❤️ por [Sergio Scardigno](https://github.com/sergio-scardigno)**