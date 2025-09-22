# Registro Físico - Aplicación Flask

Una aplicación web desarrollada en Python con Flask para registrar y gestionar mediciones corporales de múltiples personas, incluyendo peso, IMC, pliegues cutáneos y circunferencias.

## Características

- **👥 Múltiples Usuarios**: Gestión completa de usuarios con perfiles individuales
- **📊 Registro de Peso e IMC**: Calcula automáticamente el Índice de Masa Corporal por usuario
- **📏 Pliegues Cutáneos**: Registro de 6 pliegues corporales (tricipital, subescapular, suprailíaco, abdominal, muslo anterior, pantorrilla)
- **📐 Circunferencias**: Medición de 8 circunferencias corporales (cuello, pecho, brazo, antebrazo, cintura, cadera, muslo, pantorrilla)
- **📈 Estadísticas Individuales**: Visualización de progreso y estadísticas por usuario
- **🎨 Interfaz Moderna**: Diseño responsive con Bootstrap 5
- **💾 Base de Datos**: SQLite para almacenamiento local con relaciones entre usuarios y registros

## Instalación

### Opción 1: Instalación Local

1. **Clonar o descargar el proyecto**
   ```bash
   git clone <url-del-repositorio>
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
   git clone <url-del-repositorio>
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
   docker run -p 5000:5000 -v $(pwd)/data:/app/instance tu-usuario/registro-fisico:latest
   ```

## Uso

1. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

3. **Funcionalidades disponibles:**
   - **Inicio**: Lista de usuarios registrados
   - **Gestión de Usuarios**: Crear, editar y administrar usuarios
   - **Perfil de Usuario**: Ver registros y datos de un usuario específico
   - **Nuevo Registro**: Crear una nueva medición para un usuario
   - **Ver Registro**: Detalles completos de una medición
   - **Editar Registro**: Modificar datos existentes
   - **Estadísticas**: Análisis de progreso y tendencias por usuario

## Estructura del Proyecto

```
registro-fisico/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── nuevo_registro.html
│   ├── ver_registro.html
│   ├── editar_registro.html
│   └── estadisticas.html
└── static/               # Archivos estáticos (CSS, JS)
```

## Características Técnicas

### Modelo de Datos
- **Usuario**: Modelo para gestionar personas:
  - Datos personales: nombre, apellido, fecha de nacimiento, género
  - Estado activo/inactivo
  - Relación con registros físicos
  
- **RegistroFisico**: Modelo principal que incluye:
  - Asociación con usuario específico
  - Datos básicos: peso, altura, IMC
  - Pliegues cutáneos (6 mediciones)
  - Circunferencias (8 mediciones)
  - Observaciones y fecha

### Funcionalidades Implementadas
- **Gestión completa de usuarios** con CRUD
- **Cálculo automático de IMC** con clasificación por usuario
- **Sumatoria de pliegues** para análisis corporal
- **Estadísticas individuales** (peso inicial vs actual, promedios, etc.)
- **Interfaz responsive** compatible con móviles
- **Validación de formularios** en frontend y backend
- **Confirmación de eliminación** para evitar pérdida de datos
- **Navegación intuitiva** entre usuarios y sus registros

### Clasificación de IMC
- **Bajo peso**: IMC < 18.5
- **Peso normal**: IMC 18.5 - 24.9
- **Sobrepeso**: IMC 25.0 - 29.9
- **Obesidad**: IMC ≥ 30.0

## Personalización

### Cambiar la Base de Datos
Para usar una base de datos diferente (PostgreSQL, MySQL), modifica la configuración en `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:password@localhost/registro_fisico'
```

### Agregar Nuevas Mediciones
Para agregar nuevos campos de medición:

1. Modifica el modelo `RegistroFisico` en `app.py`
2. Actualiza los formularios en los templates
3. Ejecuta una migración de base de datos

## Desarrollo

### Estructura de la Aplicación
- **Rutas**: Definidas en `app.py` con decoradores Flask
- **Modelos**: SQLAlchemy ORM para manejo de base de datos
- **Templates**: Jinja2 para renderizado de HTML
- **Estilos**: Bootstrap 5 + CSS personalizado

### Próximas Mejoras
- [ ] Gráficos de progreso con Chart.js
- [ ] Exportación de datos a Excel/PDF
- [ ] Sistema de usuarios y autenticación
- [ ] API REST para integración con apps móviles
- [ ] Cálculos de composición corporal avanzados

## Docker Hub

### Subir a Docker Hub

1. **Crear cuenta en Docker Hub** (https://hub.docker.com)

2. **Hacer login en Docker**
   ```bash
   docker login
   ```

3. **Usar los scripts incluidos**
   ```bash
   # Linux/Mac
   ./build-and-push.sh [version] [tu-usuario-dockerhub]
   
   # Windows
   build-and-push.bat [version] [tu-usuario-dockerhub]
   ```

4. **O manualmente**
   ```bash
   # Construir la imagen
   docker build -t tu-usuario/registro-fisico:latest .
   
   # Subir a Docker Hub
   docker push tu-usuario/registro-fisico:latest
   ```

### Usar la Imagen desde Docker Hub

```bash
# Descargar y ejecutar
docker run -p 5000:5000 -v $(pwd)/data:/app/instance tu-usuario/registro-fisico:latest

# Con Docker Compose
version: '3.8'
services:
  registro-fisico:
    image: tu-usuario/registro-fisico:latest
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/instance
    restart: unless-stopped
```

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Soporte

Para reportar problemas o sugerir mejoras, por favor crea un issue en el repositorio del proyecto.
