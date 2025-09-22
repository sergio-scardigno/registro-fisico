# Demo - Registro Físico Multi-Usuario

## 🚀 Inicio Rápido

### 1. Ejecutar la Aplicación
```bash
python run.py
```

### 2. Acceder a la Aplicación
Abre tu navegador en: `http://localhost:5000`

## 📋 Flujo de Trabajo

### Paso 1: Crear Usuarios
1. **Página Principal**: Verás la lista de usuarios (inicialmente vacía)
2. **Crear Usuario**: Haz clic en "Nuevo Usuario"
3. **Completar Datos**:
   - Nombre: "Juan"
   - Apellido: "Pérez"
   - Fecha de Nacimiento: "1990-05-15"
   - Género: "Masculino"
4. **Guardar**: Haz clic en "Crear Usuario"

### Paso 2: Agregar Registros Físicos
1. **Seleccionar Usuario**: En la página principal, haz clic en "Ver Perfil" del usuario
2. **Nuevo Registro**: Haz clic en "Nuevo Registro"
3. **Completar Mediciones**:
   - Peso: 75.5 kg
   - Altura: 1.80 m
   - Pliegues (opcional): Tricipital: 12, Subescapular: 15, etc.
   - Circunferencias (opcional): Cintura: 85, Cadera: 95, etc.
4. **Guardar**: El IMC se calcula automáticamente

### Paso 3: Ver Estadísticas
1. **Estadísticas**: Desde el perfil del usuario, haz clic en "Estadísticas"
2. **Análisis**: Ve el progreso, promedios y tendencias

## 👥 Gestión de Múltiples Usuarios

### Crear Más Usuarios
1. **Gestión de Usuarios**: Haz clic en "Usuarios" en el menú
2. **Nuevo Usuario**: Crea usuarios adicionales
3. **Ejemplo**:
   - María García (Femenino, 1985-03-20)
   - Carlos López (Masculino, 1992-11-10)

### Navegación Entre Usuarios
- **Página Principal**: Lista todos los usuarios activos
- **Perfil Individual**: Cada usuario tiene su propio perfil
- **Registros Separados**: Los datos están completamente separados por usuario

## 📊 Características Destacadas

### Cálculos Automáticos
- **IMC**: Se calcula automáticamente al ingresar peso y altura
- **Clasificación**: Bajo peso, Normal, Sobrepeso, Obesidad
- **Sumatoria de Pliegues**: Total de todos los pliegues medidos

### Estadísticas por Usuario
- Peso actual vs inicial
- Diferencia de peso
- Promedios de peso e IMC
- Historial completo de registros

### Interfaz Intuitiva
- **Tarjetas de Usuario**: Vista clara de cada persona
- **Botones de Acción Rápida**: Nuevo registro, estadísticas, editar
- **Navegación Clara**: Siempre sabes en qué usuario estás trabajando

## 🔧 Funciones Avanzadas

### Editar Usuarios
1. **Gestión de Usuarios** → **Editar Usuario**
2. **Modificar Datos**: Cambiar nombre, apellido, etc.
3. **Activar/Desactivar**: Controlar el estado del usuario

### Editar Registros
1. **Perfil del Usuario** → **Editar Registro**
2. **Modificar Mediciones**: Cambiar cualquier dato
3. **Recálculo Automático**: El IMC se actualiza automáticamente

### Eliminar Datos
- **Registros**: Se pueden eliminar individualmente
- **Usuarios**: Se desactivan (no se eliminan permanentemente)

## 📱 Uso en Móviles

La aplicación es completamente responsive:
- **Navegación táctil**: Botones grandes y fáciles de tocar
- **Formularios adaptados**: Campos optimizados para móviles
- **Vista de tarjetas**: Perfecta para pantallas pequeñas

## 🎯 Casos de Uso

### Para Entrenadores Personales
- Gestionar múltiples clientes
- Seguimiento individual de progreso
- Comparar estadísticas entre clientes

### Para Familias
- Registrar mediciones de todos los miembros
- Seguimiento de salud familiar
- Historial individual por persona

### Para Gimnasios
- Control de socios
- Seguimiento de objetivos
- Reportes individuales

## 🚨 Notas Importantes

- **Datos Separados**: Cada usuario tiene sus propios registros
- **Privacidad**: Los datos están completamente aislados por usuario
- **Backup**: La base de datos se guarda en `instance/registro_fisico.db`
- **Seguridad**: No hay autenticación (uso local recomendado)

## 🔄 Migración de Datos

Si tenías datos anteriores:
1. **Backup**: Guarda tu base de datos anterior
2. **Recrear**: Ejecuta `python recrear_bd.py`
3. **Usuario por Defecto**: Se crea automáticamente un usuario "Por Defecto"

¡Disfruta usando tu aplicación de registro físico multi-usuario! 🎉
