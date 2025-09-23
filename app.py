from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import csv
import io
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
# Use a more accessible database path for Linux
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "registro_fisico.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.String(10))  # 'M' o 'F'
    altura = db.Column(db.Float)  # Altura en metros para reutilizar en registros
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relación con registros físicos
    registros = db.relationship('RegistroFisico', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Usuario {self.nombre} {self.apellido}>'
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

class RegistroFisico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    imc = db.Column(db.Float, nullable=False)
    
    # Pliegues cutáneos (en mm) - 3 mediciones individuales + promedio
    # Tricipital
    pliegue_tricipital_1 = db.Column(db.Float)
    pliegue_tricipital_2 = db.Column(db.Float)
    pliegue_tricipital_3 = db.Column(db.Float)
    pliegue_tricipital_promedio = db.Column(db.Float)
    
    # Subescapular
    pliegue_subescapular_1 = db.Column(db.Float)
    pliegue_subescapular_2 = db.Column(db.Float)
    pliegue_subescapular_3 = db.Column(db.Float)
    pliegue_subescapular_promedio = db.Column(db.Float)
    
    # Suprailíaco
    pliegue_suprailiaco_1 = db.Column(db.Float)
    pliegue_suprailiaco_2 = db.Column(db.Float)
    pliegue_suprailiaco_3 = db.Column(db.Float)
    pliegue_suprailiaco_promedio = db.Column(db.Float)
    
    # Abdominal
    pliegue_abdominal_1 = db.Column(db.Float)
    pliegue_abdominal_2 = db.Column(db.Float)
    pliegue_abdominal_3 = db.Column(db.Float)
    pliegue_abdominal_promedio = db.Column(db.Float)
    
    # Muslo anterior
    pliegue_muslo_anterior_1 = db.Column(db.Float)
    pliegue_muslo_anterior_2 = db.Column(db.Float)
    pliegue_muslo_anterior_3 = db.Column(db.Float)
    pliegue_muslo_anterior_promedio = db.Column(db.Float)
    
    # Pantorrilla
    pliegue_pantorrilla_1 = db.Column(db.Float)
    pliegue_pantorrilla_2 = db.Column(db.Float)
    pliegue_pantorrilla_3 = db.Column(db.Float)
    pliegue_pantorrilla_promedio = db.Column(db.Float)
    
    # Circunferencias (en cm)
    circunferencia_cuello = db.Column(db.Float)
    circunferencia_pecho = db.Column(db.Float)
    circunferencia_brazo = db.Column(db.Float)
    circunferencia_antebrazo = db.Column(db.Float)
    circunferencia_cintura = db.Column(db.Float)
    circunferencia_cadera = db.Column(db.Float)
    circunferencia_muslo = db.Column(db.Float)
    circunferencia_pantorrilla = db.Column(db.Float)
    
    # Observaciones
    observaciones = db.Column(db.Text)

    def calcular_imc(self):
        """Calcula el IMC basado en peso y altura"""
        if self.altura > 0:
            return round(self.peso / (self.altura ** 2), 2)
        return 0

    def clasificacion_imc(self):
        """Retorna la clasificación del IMC"""
        if self.imc < 18.5:
            return "Bajo peso"
        elif self.imc < 25:
            return "Peso normal"
        elif self.imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"

    def sumatoria_pliegues(self):
        """Calcula la sumatoria de pliegues usando los promedios"""
        pliegues = [
            self.pliegue_tricipital_promedio or 0,
            self.pliegue_subescapular_promedio or 0,
            self.pliegue_suprailiaco_promedio or 0,
            self.pliegue_abdominal_promedio or 0,
            self.pliegue_muslo_anterior_promedio or 0,
            self.pliegue_pantorrilla_promedio or 0
        ]
        return sum(pliegues)
    
    def calcular_porcentaje_grasa(self):
        """Calcula el porcentaje de grasa corporal usando la fórmula de Durnin-Womersley"""
        if not self.usuario:
            return None
            
        # Obtener edad del usuario
        if not self.usuario.fecha_nacimiento:
            return None
            
        from datetime import datetime
        hoy = datetime.now().date()
        edad = hoy.year - self.usuario.fecha_nacimiento.year
        if hoy.month < self.usuario.fecha_nacimiento.month or \
           (hoy.month == self.usuario.fecha_nacimiento.month and hoy.day < self.usuario.fecha_nacimiento.day):
            edad -= 1
        
        # Sumatoria de 4 pliegues (tricipital, subescapular, suprailíaco, abdominal)
        suma_4_pliegues = (
            (self.pliegue_tricipital_promedio or 0) +
            (self.pliegue_subescapular_promedio or 0) +
            (self.pliegue_suprailiaco_promedio or 0) +
            (self.pliegue_abdominal_promedio or 0)
        )
        
        if suma_4_pliegues == 0:
            return None
        
        # Fórmula de Durnin-Womersley
        if self.usuario.genero == 'M':
            # Fórmula para hombres
            if edad >= 16 and edad <= 19:
                densidad = 1.1620 - 0.0630 * (suma_4_pliegues / 10)
            elif edad >= 20 and edad <= 29:
                densidad = 1.1631 - 0.0632 * (suma_4_pliegues / 10)
            elif edad >= 30 and edad <= 39:
                densidad = 1.1422 - 0.0544 * (suma_4_pliegues / 10)
            elif edad >= 40 and edad <= 49:
                densidad = 1.1620 - 0.0700 * (suma_4_pliegues / 10)
            elif edad >= 50:
                densidad = 1.1715 - 0.0779 * (suma_4_pliegues / 10)
            else:
                return None
        else:
            # Fórmula para mujeres
            if edad >= 16 and edad <= 19:
                densidad = 1.1549 - 0.0678 * (suma_4_pliegues / 10)
            elif edad >= 20 and edad <= 29:
                densidad = 1.1599 - 0.0717 * (suma_4_pliegues / 10)
            elif edad >= 30 and edad <= 39:
                densidad = 1.1423 - 0.0632 * (suma_4_pliegues / 10)
            elif edad >= 40 and edad <= 49:
                densidad = 1.1333 - 0.0612 * (suma_4_pliegues / 10)
            elif edad >= 50:
                densidad = 1.1339 - 0.0645 * (suma_4_pliegues / 10)
            else:
                return None
        
        # Convertir densidad a porcentaje de grasa usando la ecuación de Siri
        if densidad > 0:
            porcentaje_grasa = ((4.95 / densidad) - 4.50) * 100
            return round(porcentaje_grasa, 1)
        
        return None
    
    def clasificar_grasa_corporal(self):
        """Clasifica el nivel de grasa corporal según estándares"""
        porcentaje = self.calcular_porcentaje_grasa()
        if not porcentaje or not self.usuario:
            return None, None
            
        edad = self.usuario.fecha_nacimiento
        if not edad:
            return None, None
            
        from datetime import datetime
        hoy = datetime.now().date()
        edad_anos = hoy.year - edad.year
        if hoy.month < edad.month or (hoy.month == edad.month and hoy.day < edad.day):
            edad_anos -= 1
        
        if self.usuario.genero == 'M':
            # Clasificación para hombres
            if edad_anos >= 18 and edad_anos <= 39:
                if porcentaje < 8:
                    return "Muy Bajo", "danger"
                elif porcentaje < 11:
                    return "Bajo", "warning"
                elif porcentaje < 14:
                    return "Aceptable", "info"
                elif porcentaje < 18:
                    return "Promedio", "success"
                elif porcentaje < 25:
                    return "Alto", "warning"
                else:
                    return "Muy Alto", "danger"
            elif edad_anos >= 40 and edad_anos <= 59:
                if porcentaje < 11:
                    return "Muy Bajo", "danger"
                elif porcentaje < 14:
                    return "Bajo", "warning"
                elif porcentaje < 17:
                    return "Aceptable", "info"
                elif porcentaje < 22:
                    return "Promedio", "success"
                elif porcentaje < 28:
                    return "Alto", "warning"
                else:
                    return "Muy Alto", "danger"
            else:  # 60+
                if porcentaje < 13:
                    return "Muy Bajo", "danger"
                elif porcentaje < 16:
                    return "Bajo", "warning"
                elif porcentaje < 20:
                    return "Aceptable", "info"
                elif porcentaje < 25:
                    return "Promedio", "success"
                elif porcentaje < 30:
                    return "Alto", "warning"
                else:
                    return "Muy Alto", "danger"
        else:
            # Clasificación para mujeres
            if edad_anos >= 18 and edad_anos <= 39:
                if porcentaje < 16:
                    return "Muy Bajo", "danger"
                elif porcentaje < 20:
                    return "Bajo", "warning"
                elif porcentaje < 22:
                    return "Aceptable", "info"
                elif porcentaje < 25:
                    return "Promedio", "success"
                elif porcentaje < 32:
                    return "Alto", "warning"
                else:
                    return "Muy Alto", "danger"
            elif edad_anos >= 40 and edad_anos <= 59:
                if porcentaje < 20:
                    return "Muy Bajo", "danger"
                elif porcentaje < 24:
                    return "Bajo", "warning"
                elif porcentaje < 26:
                    return "Aceptable", "info"
                elif porcentaje < 30:
                    return "Promedio", "success"
                elif porcentaje < 35:
                    return "Alto", "warning"
                else:
                    return "Muy Alto", "danger"
            else:  # 60+
                if porcentaje < 22:
                    return "Muy Bajo", "danger"
                elif porcentaje < 26:
                    return "Bajo", "warning"
                elif porcentaje < 29:
                    return "Aceptable", "info"
                elif porcentaje < 33:
                    return "Promedio", "success"
                elif porcentaje < 38:
                    return "Alto", "warning"
                else:
                    return "Muy Alto", "danger"
    
    def calcular_spc_aaherd(self):
        """Calcula la Suma de Pliegues Cutáneos según método AAHPERD para población universitaria"""
        if not self.pliegue_tricipital_promedio or not self.pliegue_subescapular_promedio:
            return None
        return self.pliegue_tricipital_promedio + self.pliegue_subescapular_promedio
    
    def calcular_percentila_spc_aaherd(self):
        """Calcula la percentila de SPC según tablas oficiales AAHPERD para población universitaria"""
        spc = self.calcular_spc_aaherd()
        if not spc or not self.usuario:
            return None
            
        edad = self.usuario.fecha_nacimiento
        if not edad:
            return None
            
        from datetime import datetime
        hoy = datetime.now().date()
        edad_anos = hoy.year - edad.year
        if hoy.month < edad.month or (hoy.month == edad.month and hoy.day < edad.day):
            edad_anos -= 1
        
        # Tablas oficiales AAHPERD para población universitaria (Tríceps + Subescapular)
        if self.usuario.genero == 'M':
            # Hombres universitarios (18-25 años) - Tabla AAHPERD
            if edad_anos >= 18 and edad_anos <= 25:
                # Percentilas: 5, 10, 25, 50, 75, 90, 95
                spc_percentiles = [8, 10, 13, 17, 22, 28, 32]
            else:
                # Para edades fuera del rango universitario, usar aproximación
                spc_percentiles = [10, 12, 15, 19, 24, 30, 34]
        else:
            # Mujeres universitarias (18-25 años) - Tabla AAHPERD
            if edad_anos >= 18 and edad_anos <= 25:
                # Percentilas: 5, 10, 25, 50, 75, 90, 95
                spc_percentiles = [12, 15, 19, 24, 30, 37, 42]
            else:
                # Para edades fuera del rango universitario, usar aproximación
                spc_percentiles = [14, 17, 21, 26, 32, 39, 44]
        
        # Determinar percentila basada en SPC
        if spc <= spc_percentiles[0]:
            return 5
        elif spc <= spc_percentiles[1]:
            return 10
        elif spc <= spc_percentiles[2]:
            return 25
        elif spc <= spc_percentiles[3]:
            return 50
        elif spc <= spc_percentiles[4]:
            return 75
        elif spc <= spc_percentiles[5]:
            return 90
        else:
            return 95
    
    def calcular_percentila_grasa(self):
        """Calcula la percentila de grasa corporal según edad y género"""
        porcentaje = self.calcular_porcentaje_grasa()
        if not porcentaje or not self.usuario:
            return None
            
        edad = self.usuario.fecha_nacimiento
        if not edad:
            return None
            
        from datetime import datetime
        hoy = datetime.now().date()
        edad_anos = hoy.year - edad.year
        if hoy.month < edad.month or (hoy.month == edad.month and hoy.day < edad.day):
            edad_anos -= 1
        
        # Tablas de percentilas basadas en estudios poblacionales
        if self.usuario.genero == 'M':
            # Percentilas para hombres (aproximadas)
            if edad_anos >= 18 and edad_anos <= 39:
                percentilas = [5, 8, 11, 14, 18, 25, 35]
            elif edad_anos >= 40 and edad_anos <= 59:
                percentilas = [8, 11, 14, 17, 22, 28, 38]
            else:  # 60+
                percentilas = [10, 13, 16, 20, 25, 30, 40]
        else:
            # Percentilas para mujeres (aproximadas)
            if edad_anos >= 18 and edad_anos <= 39:
                percentilas = [12, 16, 20, 22, 25, 32, 42]
            elif edad_anos >= 40 and edad_anos <= 59:
                percentilas = [16, 20, 24, 26, 30, 35, 45]
            else:  # 60+
                percentilas = [18, 22, 26, 29, 33, 38, 48]
        
        # Determinar percentila
        if porcentaje <= percentilas[0]:
            return 5
        elif porcentaje <= percentilas[1]:
            return 10
        elif porcentaje <= percentilas[2]:
            return 25
        elif porcentaje <= percentilas[3]:
            return 50
        elif porcentaje <= percentilas[4]:
            return 75
        elif porcentaje <= percentilas[5]:
            return 90
        else:
            return 95
    
    def calcular_progreso_grasa(self):
        """Calcula el progreso hacia el siguiente nivel de clasificación"""
        porcentaje = self.calcular_porcentaje_grasa()
        if not porcentaje or not self.usuario:
            return None, None, None, None
            
        edad = self.usuario.fecha_nacimiento
        if not edad:
            return None, None, None, None
            
        from datetime import datetime
        hoy = datetime.now().date()
        edad_anos = hoy.year - edad.year
        if hoy.month < edad.month or (hoy.month == edad.month and hoy.day < edad.day):
            edad_anos -= 1
        
        # Definir rangos por edad y género
        if self.usuario.genero == 'M':
            if edad_anos >= 18 and edad_anos <= 39:
                rangos = [8, 11, 14, 18, 25, 35]
            elif edad_anos >= 40 and edad_anos <= 59:
                rangos = [11, 14, 17, 22, 28, 38]
            else:  # 60+
                rangos = [13, 16, 20, 25, 30, 40]
        else:
            if edad_anos >= 18 and edad_anos <= 39:
                rangos = [16, 20, 22, 25, 32, 42]
            elif edad_anos >= 40 and edad_anos <= 59:
                rangos = [20, 24, 26, 30, 35, 45]
            else:  # 60+
                rangos = [22, 26, 29, 33, 38, 48]
        
        # Determinar nivel actual y siguiente
        nivel_actual = None
        nivel_siguiente = None
        porcentaje_objetivo = None
        diferencia = None
        
        if porcentaje < rangos[0]:
            nivel_actual = "Muy Bajo"
            nivel_siguiente = "Bajo"
            porcentaje_objetivo = rangos[0]
            diferencia = rangos[0] - porcentaje
        elif porcentaje < rangos[1]:
            nivel_actual = "Bajo"
            nivel_siguiente = "Aceptable"
            porcentaje_objetivo = rangos[1]
            diferencia = rangos[1] - porcentaje
        elif porcentaje < rangos[2]:
            nivel_actual = "Aceptable"
            nivel_siguiente = "Promedio"
            porcentaje_objetivo = rangos[2]
            diferencia = rangos[2] - porcentaje
        elif porcentaje < rangos[3]:
            nivel_actual = "Promedio"
            nivel_siguiente = "Alto"
            porcentaje_objetivo = rangos[3]
            diferencia = rangos[3] - porcentaje
        elif porcentaje < rangos[4]:
            nivel_actual = "Alto"
            nivel_siguiente = "Muy Alto"
            porcentaje_objetivo = rangos[4]
            diferencia = rangos[4] - porcentaje
        else:
            nivel_actual = "Muy Alto"
            nivel_siguiente = None
            porcentaje_objetivo = None
            diferencia = None
        
        return nivel_actual, nivel_siguiente, porcentaje_objetivo, diferencia
    
    def clasificar_spc_aaherd(self):
        """Clasifica el SPC según estándares AAHPERD para población universitaria"""
        spc = self.calcular_spc_aaherd()
        if not spc or not self.usuario:
            return None, None
            
        edad = self.usuario.fecha_nacimiento
        if not edad:
            return None, None
            
        from datetime import datetime
        hoy = datetime.now().date()
        edad_anos = hoy.year - edad.year
        if hoy.month < edad.month or (hoy.month == edad.month and hoy.day < edad.day):
            edad_anos -= 1
        
        # Clasificación AAHPERD para población universitaria (18-25 años)
        if edad_anos >= 18 and edad_anos <= 25:
            if self.usuario.genero == 'M':
                # Hombres universitarios
                if spc <= 10:
                    return "Excelente", "success"
                elif spc <= 13:
                    return "Muy Bueno", "info"
                elif spc <= 17:
                    return "Bueno", "primary"
                elif spc <= 22:
                    return "Promedio", "warning"
                elif spc <= 28:
                    return "Bajo Promedio", "warning"
                else:
                    return "Necesita Mejora", "danger"
            else:
                # Mujeres universitarias
                if spc <= 15:
                    return "Excelente", "success"
                elif spc <= 19:
                    return "Muy Bueno", "info"
                elif spc <= 24:
                    return "Bueno", "primary"
                elif spc <= 30:
                    return "Promedio", "warning"
                elif spc <= 37:
                    return "Bajo Promedio", "warning"
                else:
                    return "Necesita Mejora", "danger"
        else:
            # Para edades fuera del rango universitario, usar clasificación general
            if self.usuario.genero == 'M':
                if spc <= 12:
                    return "Excelente", "success"
                elif spc <= 15:
                    return "Muy Bueno", "info"
                elif spc <= 19:
                    return "Bueno", "primary"
                elif spc <= 24:
                    return "Promedio", "warning"
                elif spc <= 30:
                    return "Bajo Promedio", "warning"
                else:
                    return "Necesita Mejora", "danger"
            else:
                if spc <= 17:
                    return "Excelente", "success"
                elif spc <= 21:
                    return "Muy Bueno", "info"
                elif spc <= 26:
                    return "Bueno", "primary"
                elif spc <= 32:
                    return "Promedio", "warning"
                elif spc <= 39:
                    return "Bajo Promedio", "warning"
                else:
                    return "Necesita Mejora", "danger"
    
    def obtener_interpretacion_motivacional(self):
        """Obtiene interpretación motivacional basada en percentilas AAHPERD"""
        percentila_spc = self.calcular_percentila_spc_aaherd()
        if not percentila_spc:
            return None, None, None
            
        if percentila_spc <= 5:
            mensaje = "¡Excelente! Estás en el top 5% de la población universitaria. Tu composición corporal es excepcional."
            consejo = "Mantén tu rutina actual de ejercicio y alimentación balanceada."
            color = "success"
        elif percentila_spc <= 10:
            mensaje = "¡Muy bien! Estás en el top 10% de la población universitaria. Tu composición corporal es muy buena."
            consejo = "Continúa con tu estilo de vida saludable y considera agregar entrenamiento de fuerza."
            color = "info"
        elif percentila_spc <= 25:
            mensaje = "¡Bien! Estás por encima del promedio de la población universitaria. Tu composición corporal es buena."
            consejo = "Mantén el ejercicio regular y considera optimizar tu alimentación."
            color = "primary"
        elif percentila_spc <= 50:
            mensaje = "Estás en el promedio de la población universitaria. Hay espacio para mejorar tu composición corporal."
            consejo = "Incorpora ejercicio cardiovascular regular y revisa tus hábitos alimentarios."
            color = "warning"
        elif percentila_spc <= 75:
            mensaje = "Estás por debajo del promedio de la población universitaria. Es momento de tomar acción."
            consejo = "Inicia un programa de ejercicio estructurado y consulta con un nutricionista."
            color = "warning"
        elif percentila_spc <= 90:
            mensaje = "Tu composición corporal está significativamente por debajo del promedio. Es importante actuar ahora."
            consejo = "Busca asesoría profesional para crear un plan de ejercicio y nutrición personalizado."
            color = "danger"
        else:
            mensaje = "Tu composición corporal está muy por debajo del promedio. Es crucial buscar ayuda profesional."
            consejo = "Consulta inmediatamente con un médico, nutricionista y entrenador personal certificado."
            color = "danger"
            
        return mensaje, consejo, color

# Funciones de exportación e importación CSV
def export_registros_csv(usuario_id):
    """Exporta los registros de un usuario a formato CSV"""
    usuario = Usuario.query.get_or_404(usuario_id)
    registros = RegistroFisico.query.filter_by(usuario_id=usuario_id).order_by(RegistroFisico.fecha.desc()).all()
    
    if not registros:
        return None
    
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Encabezados del CSV
    headers = [
        'fecha', 'peso', 'altura', 'imc',
        'pliegue_tricipital_1', 'pliegue_tricipital_2', 'pliegue_tricipital_3', 'pliegue_tricipital_promedio',
        'pliegue_subescapular_1', 'pliegue_subescapular_2', 'pliegue_subescapular_3', 'pliegue_subescapular_promedio',
        'pliegue_suprailiaco_1', 'pliegue_suprailiaco_2', 'pliegue_suprailiaco_3', 'pliegue_suprailiaco_promedio',
        'pliegue_abdominal_1', 'pliegue_abdominal_2', 'pliegue_abdominal_3', 'pliegue_abdominal_promedio',
        'pliegue_muslo_anterior_1', 'pliegue_muslo_anterior_2', 'pliegue_muslo_anterior_3', 'pliegue_muslo_anterior_promedio',
        'pliegue_pantorrilla_1', 'pliegue_pantorrilla_2', 'pliegue_pantorrilla_3', 'pliegue_pantorrilla_promedio',
        'circunferencia_cuello', 'circunferencia_pecho', 'circunferencia_brazo', 'circunferencia_antebrazo',
        'circunferencia_cintura', 'circunferencia_cadera', 'circunferencia_muslo', 'circunferencia_pantorrilla',
        'porcentaje_grasa', 'spc_aaherd', 'percentila_spc_aaherd', 'clasificacion_spc_aaherd'
    ]
    
    writer.writerow(headers)
    
    # Datos de los registros
    for registro in registros:
        # Calcular valores derivados
        porcentaje_grasa = registro.calcular_porcentaje_grasa()
        spc_aaherd = registro.calcular_spc_aaherd()
        percentila_spc = registro.calcular_percentila_spc_aaherd()
        clasificacion_spc = registro.clasificar_spc_aaherd()
        
        row = [
            registro.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            registro.peso,
            registro.altura,
            registro.imc,
            registro.pliegue_tricipital_1 or '',
            registro.pliegue_tricipital_2 or '',
            registro.pliegue_tricipital_3 or '',
            registro.pliegue_tricipital_promedio or '',
            registro.pliegue_subescapular_1 or '',
            registro.pliegue_subescapular_2 or '',
            registro.pliegue_subescapular_3 or '',
            registro.pliegue_subescapular_promedio or '',
            registro.pliegue_suprailiaco_1 or '',
            registro.pliegue_suprailiaco_2 or '',
            registro.pliegue_suprailiaco_3 or '',
            registro.pliegue_suprailiaco_promedio or '',
            registro.pliegue_abdominal_1 or '',
            registro.pliegue_abdominal_2 or '',
            registro.pliegue_abdominal_3 or '',
            registro.pliegue_abdominal_promedio or '',
            registro.pliegue_muslo_anterior_1 or '',
            registro.pliegue_muslo_anterior_2 or '',
            registro.pliegue_muslo_anterior_3 or '',
            registro.pliegue_muslo_anterior_promedio or '',
            registro.pliegue_pantorrilla_1 or '',
            registro.pliegue_pantorrilla_2 or '',
            registro.pliegue_pantorrilla_3 or '',
            registro.pliegue_pantorrilla_promedio or '',
            registro.circunferencia_cuello or '',
            registro.circunferencia_pecho or '',
            registro.circunferencia_brazo or '',
            registro.circunferencia_antebrazo or '',
            registro.circunferencia_cintura or '',
            registro.circunferencia_cadera or '',
            registro.circunferencia_muslo or '',
            registro.circunferencia_pantorrilla or '',
            round(porcentaje_grasa, 2) if porcentaje_grasa else '',
            round(spc_aaherd, 2) if spc_aaherd else '',
            percentila_spc or '',
            clasificacion_spc[0] if clasificacion_spc and clasificacion_spc[0] else ''
        ]
        writer.writerow(row)
    
    output.seek(0)
    return output.getvalue()

def import_registros_csv(csv_content, usuario_id):
    """Importa registros desde un CSV al usuario especificado"""
    import csv
    import io
    from datetime import datetime
    
    usuario = Usuario.query.get_or_404(usuario_id)
    registros_importados = []
    errores = []
    
    # Leer el CSV
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    
    for row_num, row in enumerate(csv_reader, start=2):  # Empezar en 2 porque la fila 1 son headers
        try:
            # Validar campos requeridos
            if not row.get('fecha') or not row.get('peso') or not row.get('altura'):
                errores.append(f"Fila {row_num}: Faltan campos requeridos (fecha, peso, altura)")
                continue
            
            # Crear nuevo registro
            registro = RegistroFisico()
            registro.usuario_id = usuario_id
            
            # Fecha
            try:
                registro.fecha = datetime.strptime(row['fecha'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    registro.fecha = datetime.strptime(row['fecha'], '%Y-%m-%d')
                except ValueError:
                    errores.append(f"Fila {row_num}: Formato de fecha inválido: {row['fecha']}")
                    continue
            
            # Datos básicos
            registro.peso = float(row['peso'])
            registro.altura = float(row['altura'])
            registro.imc = float(row['imc']) if row.get('imc') else round(registro.peso / (registro.altura ** 2), 2)
            
            # Pliegues cutáneos - Tricipital
            registro.pliegue_tricipital_1 = float(row['pliegue_tricipital_1']) if row.get('pliegue_tricipital_1') else None
            registro.pliegue_tricipital_2 = float(row['pliegue_tricipital_2']) if row.get('pliegue_tricipital_2') else None
            registro.pliegue_tricipital_3 = float(row['pliegue_tricipital_3']) if row.get('pliegue_tricipital_3') else None
            registro.pliegue_tricipital_promedio = float(row['pliegue_tricipital_promedio']) if row.get('pliegue_tricipital_promedio') else None
            
            # Pliegues cutáneos - Subescapular
            registro.pliegue_subescapular_1 = float(row['pliegue_subescapular_1']) if row.get('pliegue_subescapular_1') else None
            registro.pliegue_subescapular_2 = float(row['pliegue_subescapular_2']) if row.get('pliegue_subescapular_2') else None
            registro.pliegue_subescapular_3 = float(row['pliegue_subescapular_3']) if row.get('pliegue_subescapular_3') else None
            registro.pliegue_subescapular_promedio = float(row['pliegue_subescapular_promedio']) if row.get('pliegue_subescapular_promedio') else None
            
            # Pliegues cutáneos - Suprailíaco
            registro.pliegue_suprailiaco_1 = float(row['pliegue_suprailiaco_1']) if row.get('pliegue_suprailiaco_1') else None
            registro.pliegue_suprailiaco_2 = float(row['pliegue_suprailiaco_2']) if row.get('pliegue_suprailiaco_2') else None
            registro.pliegue_suprailiaco_3 = float(row['pliegue_suprailiaco_3']) if row.get('pliegue_suprailiaco_3') else None
            registro.pliegue_suprailiaco_promedio = float(row['pliegue_suprailiaco_promedio']) if row.get('pliegue_suprailiaco_promedio') else None
            
            # Pliegues cutáneos - Abdominal
            registro.pliegue_abdominal_1 = float(row['pliegue_abdominal_1']) if row.get('pliegue_abdominal_1') else None
            registro.pliegue_abdominal_2 = float(row['pliegue_abdominal_2']) if row.get('pliegue_abdominal_2') else None
            registro.pliegue_abdominal_3 = float(row['pliegue_abdominal_3']) if row.get('pliegue_abdominal_3') else None
            registro.pliegue_abdominal_promedio = float(row['pliegue_abdominal_promedio']) if row.get('pliegue_abdominal_promedio') else None
            
            # Pliegues cutáneos - Muslo anterior
            registro.pliegue_muslo_anterior_1 = float(row['pliegue_muslo_anterior_1']) if row.get('pliegue_muslo_anterior_1') else None
            registro.pliegue_muslo_anterior_2 = float(row['pliegue_muslo_anterior_2']) if row.get('pliegue_muslo_anterior_2') else None
            registro.pliegue_muslo_anterior_3 = float(row['pliegue_muslo_anterior_3']) if row.get('pliegue_muslo_anterior_3') else None
            registro.pliegue_muslo_anterior_promedio = float(row['pliegue_muslo_anterior_promedio']) if row.get('pliegue_muslo_anterior_promedio') else None
            
            # Pliegues cutáneos - Pantorrilla
            registro.pliegue_pantorrilla_1 = float(row['pliegue_pantorrilla_1']) if row.get('pliegue_pantorrilla_1') else None
            registro.pliegue_pantorrilla_2 = float(row['pliegue_pantorrilla_2']) if row.get('pliegue_pantorrilla_2') else None
            registro.pliegue_pantorrilla_3 = float(row['pliegue_pantorrilla_3']) if row.get('pliegue_pantorrilla_3') else None
            registro.pliegue_pantorrilla_promedio = float(row['pliegue_pantorrilla_promedio']) if row.get('pliegue_pantorrilla_promedio') else None
            
            # Circunferencias
            registro.circunferencia_cuello = float(row['circunferencia_cuello']) if row.get('circunferencia_cuello') else None
            registro.circunferencia_pecho = float(row['circunferencia_pecho']) if row.get('circunferencia_pecho') else None
            registro.circunferencia_brazo = float(row['circunferencia_brazo']) if row.get('circunferencia_brazo') else None
            registro.circunferencia_antebrazo = float(row['circunferencia_antebrazo']) if row.get('circunferencia_antebrazo') else None
            registro.circunferencia_cintura = float(row['circunferencia_cintura']) if row.get('circunferencia_cintura') else None
            registro.circunferencia_cadera = float(row['circunferencia_cadera']) if row.get('circunferencia_cadera') else None
            registro.circunferencia_muslo = float(row['circunferencia_muslo']) if row.get('circunferencia_muslo') else None
            registro.circunferencia_pantorrilla = float(row['circunferencia_pantorrilla']) if row.get('circunferencia_pantorrilla') else None
            
            # Agregar a la base de datos
            db.session.add(registro)
            registros_importados.append(registro)
            
        except Exception as e:
            errores.append(f"Fila {row_num}: Error al procesar registro - {str(e)}")
            continue
    
    # Guardar cambios
    if registros_importados:
        db.session.commit()
    
    return registros_importados, errores

# Funciones de importación CSV
def parse_garmin_csv(csv_content):
    """Parsea el contenido CSV de Garmin y retorna una lista de registros"""
    registros = []
    
    # Leer el CSV
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    
    if len(rows) < 2:
        return registros
    
    # Procesar filas de datos (saltar header)
    i = 1
    fecha_actual = None
    
    while i < len(rows):
        row = rows[i]
        
        # Si la fila está vacía o solo tiene comas, saltar
        if not row or all(cell.strip() == '' for cell in row):
            i += 1
            continue
        
        # Verificar si la fila contiene una fecha
        if len(row) > 0 and row[0].strip() and not row[0].strip().endswith('am') and not row[0].strip().endswith('pm'):
            # Esta fila podría contener una fecha
            fecha_str = row[0].strip()
            try:
                # Parsear fecha (formato: " 22 Sep 2025")
                fecha_clean = fecha_str.strip()
                # Convertir mes en español a inglés
                meses_es = {
                    'Ene': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar', 'Abr': 'Apr',
                    'May': 'May', 'Jun': 'Jun', 'Jul': 'Jul', 'Ago': 'Aug',
                    'Sep': 'Sep', 'Oct': 'Oct', 'Nov': 'Nov', 'Dic': 'Dec'
                }
                for es, en in meses_es.items():
                    fecha_clean = fecha_clean.replace(es, en)
                
                fecha_actual = datetime.strptime(fecha_clean.strip(), '%d %b %Y').date()
                i += 1
                continue
            except (ValueError, AttributeError):
                i += 1
                continue
        
        # Si tenemos una fecha y esta fila contiene hora y peso
        if fecha_actual and len(row) >= 2:
            hora_str = row[0].strip()
            peso_str = row[1].strip()
            imc_str = row[3].strip() if len(row) >= 4 else None
            
            try:
                # Parsear hora (formato: "10:12 am")
                hora_clean = hora_str.strip()
                hora = datetime.strptime(hora_clean, '%I:%M %p').time()
                
                # Combinar fecha y hora
                fecha_hora = datetime.combine(fecha_actual, hora)
                
                # Parsear peso (formato: "98.7 kg")
                peso_match = re.search(r'(\d+\.?\d*)\s*kg', peso_str)
                if peso_match:
                    peso = float(peso_match.group(1))
                else:
                    i += 1
                    continue
                
                # Parsear IMC si está disponible
                imc = None
                if imc_str and imc_str.strip() != '--':
                    try:
                        imc = float(imc_str.strip())
                    except ValueError:
                        pass
                
                registros.append({
                    'fecha_hora': fecha_hora,
                    'peso': peso,
                    'imc': imc
                })
                
            except (ValueError, AttributeError) as e:
                # Si hay error parseando esta fila, continuar con la siguiente
                pass
        
        i += 1
    
    return registros

# Rutas
@app.route('/')
def index():
    usuarios = Usuario.query.filter_by(activo=True).all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/usuario/<int:usuario_id>')
def ver_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    registros = RegistroFisico.query.filter_by(usuario_id=usuario_id).order_by(RegistroFisico.fecha.desc()).limit(10).all()
    return render_template('usuario.html', usuario=usuario, registros=registros)

@app.route('/usuarios')
def gestion_usuarios():
    usuarios = Usuario.query.order_by(Usuario.nombre, Usuario.apellido).all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/nuevo_usuario', methods=['GET', 'POST'])
def nuevo_usuario():
    if request.method == 'POST':
        try:
            # Obtener altura si se proporciona
            altura_str = request.form.get('altura')
            altura = None
            if altura_str and altura_str.strip():
                try:
                    altura = float(altura_str)
                except ValueError:
                    pass  # Si no es un número válido, usar None
            
            usuario = Usuario(
                nombre=request.form['nombre'],
                apellido=request.form['apellido'],
                fecha_nacimiento=datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date() if request.form.get('fecha_nacimiento') else None,
                genero=request.form.get('genero'),
                altura=altura
            )
            db.session.add(usuario)
            db.session.commit()
            flash('Usuario creado exitosamente!', 'success')
            return redirect(url_for('gestion_usuarios'))
        except Exception as e:
            flash(f'Error al crear el usuario: {str(e)}', 'error')
    
    return render_template('nuevo_usuario.html')

@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if request.method == 'POST':
        try:
            usuario.nombre = request.form['nombre']
            usuario.apellido = request.form['apellido']
            usuario.fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date() if request.form.get('fecha_nacimiento') else None
            usuario.genero = request.form.get('genero')
            usuario.activo = 'activo' in request.form
            
            # Actualizar altura si se proporciona
            altura_str = request.form.get('altura')
            if altura_str and altura_str.strip():
                try:
                    usuario.altura = float(altura_str)
                except ValueError:
                    pass  # Si no es un número válido, no actualizar
            
            db.session.commit()
            flash('Usuario actualizado exitosamente!', 'success')
            return redirect(url_for('gestion_usuarios'))
        except Exception as e:
            flash(f'Error al actualizar el usuario: {str(e)}', 'error')
    
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/eliminar_usuario/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.activo = False
    db.session.commit()
    flash('Usuario desactivado exitosamente!', 'success')
    return redirect(url_for('gestion_usuarios'))

@app.route('/nuevo_registro/<int:usuario_id>', methods=['GET', 'POST'])
def nuevo_registro(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])
            
            # Función auxiliar para convertir string a float de forma segura
            def safe_float(value):
                if value and value.strip():
                    try:
                        return float(value)
                    except ValueError:
                        return None
                return None
            
            # Función para calcular promedio de 3 mediciones
            def calcular_promedio_pliegue(med1, med2, med3):
                valores = [safe_float(med1), safe_float(med2), safe_float(med3)]
                valores_validos = [v for v in valores if v is not None]
                if len(valores_validos) >= 2:  # Al menos 2 mediciones válidas
                    return sum(valores_validos) / len(valores_validos)
                return None
            
            # Obtener fecha y hora de la muestra
            fecha_muestra = request.form.get('fecha_muestra')
            hora_muestra = request.form.get('hora_muestra')
            
            # Crear datetime combinando fecha y hora
            if fecha_muestra and hora_muestra:
                fecha_hora_muestra = datetime.strptime(f"{fecha_muestra} {hora_muestra}", '%Y-%m-%d %H:%M')
            else:
                fecha_hora_muestra = datetime.utcnow()
            
            # Actualizar la altura del usuario si no la tiene guardada
            if not usuario.altura:
                usuario.altura = altura
                db.session.commit()
            
            # Crear nuevo registro
            registro = RegistroFisico(
                usuario_id=usuario_id,
                fecha=fecha_hora_muestra,
                peso=peso,
                altura=altura,
                # Pliegues cutáneos - Tricipital
                pliegue_tricipital_1=safe_float(request.form.get('pliegue_tricipital_1')),
                pliegue_tricipital_2=safe_float(request.form.get('pliegue_tricipital_2')),
                pliegue_tricipital_3=safe_float(request.form.get('pliegue_tricipital_3')),
                pliegue_tricipital_promedio=calcular_promedio_pliegue(
                    request.form.get('pliegue_tricipital_1'),
                    request.form.get('pliegue_tricipital_2'),
                    request.form.get('pliegue_tricipital_3')
                ),
                # Pliegues cutáneos - Subescapular
                pliegue_subescapular_1=safe_float(request.form.get('pliegue_subescapular_1')),
                pliegue_subescapular_2=safe_float(request.form.get('pliegue_subescapular_2')),
                pliegue_subescapular_3=safe_float(request.form.get('pliegue_subescapular_3')),
                pliegue_subescapular_promedio=calcular_promedio_pliegue(
                    request.form.get('pliegue_subescapular_1'),
                    request.form.get('pliegue_subescapular_2'),
                    request.form.get('pliegue_subescapular_3')
                ),
                # Pliegues cutáneos - Suprailíaco
                pliegue_suprailiaco_1=safe_float(request.form.get('pliegue_suprailiaco_1')),
                pliegue_suprailiaco_2=safe_float(request.form.get('pliegue_suprailiaco_2')),
                pliegue_suprailiaco_3=safe_float(request.form.get('pliegue_suprailiaco_3')),
                pliegue_suprailiaco_promedio=calcular_promedio_pliegue(
                    request.form.get('pliegue_suprailiaco_1'),
                    request.form.get('pliegue_suprailiaco_2'),
                    request.form.get('pliegue_suprailiaco_3')
                ),
                # Pliegues cutáneos - Abdominal
                pliegue_abdominal_1=safe_float(request.form.get('pliegue_abdominal_1')),
                pliegue_abdominal_2=safe_float(request.form.get('pliegue_abdominal_2')),
                pliegue_abdominal_3=safe_float(request.form.get('pliegue_abdominal_3')),
                pliegue_abdominal_promedio=calcular_promedio_pliegue(
                    request.form.get('pliegue_abdominal_1'),
                    request.form.get('pliegue_abdominal_2'),
                    request.form.get('pliegue_abdominal_3')
                ),
                # Pliegues cutáneos - Muslo anterior
                pliegue_muslo_anterior_1=safe_float(request.form.get('pliegue_muslo_anterior_1')),
                pliegue_muslo_anterior_2=safe_float(request.form.get('pliegue_muslo_anterior_2')),
                pliegue_muslo_anterior_3=safe_float(request.form.get('pliegue_muslo_anterior_3')),
                pliegue_muslo_anterior_promedio=calcular_promedio_pliegue(
                    request.form.get('pliegue_muslo_anterior_1'),
                    request.form.get('pliegue_muslo_anterior_2'),
                    request.form.get('pliegue_muslo_anterior_3')
                ),
                # Pliegues cutáneos - Pantorrilla
                pliegue_pantorrilla_1=safe_float(request.form.get('pliegue_pantorrilla_1')),
                pliegue_pantorrilla_2=safe_float(request.form.get('pliegue_pantorrilla_2')),
                pliegue_pantorrilla_3=safe_float(request.form.get('pliegue_pantorrilla_3')),
                pliegue_pantorrilla_promedio=calcular_promedio_pliegue(
                    request.form.get('pliegue_pantorrilla_1'),
                    request.form.get('pliegue_pantorrilla_2'),
                    request.form.get('pliegue_pantorrilla_3')
                ),
                # Circunferencias
                circunferencia_cuello=safe_float(request.form.get('circunferencia_cuello')),
                circunferencia_pecho=safe_float(request.form.get('circunferencia_pecho')),
                circunferencia_brazo=safe_float(request.form.get('circunferencia_brazo')),
                circunferencia_antebrazo=safe_float(request.form.get('circunferencia_antebrazo')),
                circunferencia_cintura=safe_float(request.form.get('circunferencia_cintura')),
                circunferencia_cadera=safe_float(request.form.get('circunferencia_cadera')),
                circunferencia_muslo=safe_float(request.form.get('circunferencia_muslo')),
                circunferencia_pantorrilla=safe_float(request.form.get('circunferencia_pantorrilla')),
                observaciones=request.form.get('observaciones', '')
            )
            
            # Calcular IMC
            registro.imc = registro.calcular_imc()
            
            # Guardar en la base de datos
            db.session.add(registro)
            db.session.commit()
            
            flash('Registro guardado exitosamente!', 'success')
            return redirect(url_for('ver_usuario', usuario_id=usuario_id))
            
        except Exception as e:
            flash(f'Error al guardar el registro: {str(e)}', 'error')
            return redirect(url_for('nuevo_registro', usuario_id=usuario_id))
    
    return render_template('nuevo_registro.html', usuario=usuario)

@app.route('/ver_registro/<int:id>')
def ver_registro(id):
    registro = RegistroFisico.query.get_or_404(id)
    return render_template('ver_registro.html', registro=registro)

@app.route('/editar_registro/<int:id>', methods=['GET', 'POST'])
def editar_registro(id):
    registro = RegistroFisico.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Función auxiliar para convertir string a float de forma segura
            def safe_float(value):
                if value and value.strip():
                    try:
                        return float(value)
                    except ValueError:
                        return None
                return None
            
            # Función para calcular promedio de 3 mediciones
            def calcular_promedio_pliegue(med1, med2, med3):
                valores = [safe_float(med1), safe_float(med2), safe_float(med3)]
                valores_validos = [v for v in valores if v is not None]
                if len(valores_validos) >= 2:  # Al menos 2 mediciones válidas
                    return sum(valores_validos) / len(valores_validos)
                return None
            
            # Obtener fecha y hora de la muestra
            fecha_muestra = request.form.get('fecha_muestra')
            hora_muestra = request.form.get('hora_muestra')
            
            # Crear datetime combinando fecha y hora
            if fecha_muestra and hora_muestra:
                fecha_hora_muestra = datetime.strptime(f"{fecha_muestra} {hora_muestra}", '%Y-%m-%d %H:%M')
                registro.fecha = fecha_hora_muestra
            
            # Actualizar datos
            registro.peso = float(request.form['peso'])
            nueva_altura = float(request.form['altura'])
            registro.altura = nueva_altura
            
            # Actualizar la altura del usuario si no la tiene guardada o si es diferente
            if not registro.usuario.altura or registro.usuario.altura != nueva_altura:
                registro.usuario.altura = nueva_altura
            
            # Pliegues cutáneos - Tricipital
            registro.pliegue_tricipital_1 = safe_float(request.form.get('pliegue_tricipital_1'))
            registro.pliegue_tricipital_2 = safe_float(request.form.get('pliegue_tricipital_2'))
            registro.pliegue_tricipital_3 = safe_float(request.form.get('pliegue_tricipital_3'))
            registro.pliegue_tricipital_promedio = calcular_promedio_pliegue(
                request.form.get('pliegue_tricipital_1'),
                request.form.get('pliegue_tricipital_2'),
                request.form.get('pliegue_tricipital_3')
            )
            
            # Pliegues cutáneos - Subescapular
            registro.pliegue_subescapular_1 = safe_float(request.form.get('pliegue_subescapular_1'))
            registro.pliegue_subescapular_2 = safe_float(request.form.get('pliegue_subescapular_2'))
            registro.pliegue_subescapular_3 = safe_float(request.form.get('pliegue_subescapular_3'))
            registro.pliegue_subescapular_promedio = calcular_promedio_pliegue(
                request.form.get('pliegue_subescapular_1'),
                request.form.get('pliegue_subescapular_2'),
                request.form.get('pliegue_subescapular_3')
            )
            
            # Pliegues cutáneos - Suprailíaco
            registro.pliegue_suprailiaco_1 = safe_float(request.form.get('pliegue_suprailiaco_1'))
            registro.pliegue_suprailiaco_2 = safe_float(request.form.get('pliegue_suprailiaco_2'))
            registro.pliegue_suprailiaco_3 = safe_float(request.form.get('pliegue_suprailiaco_3'))
            registro.pliegue_suprailiaco_promedio = calcular_promedio_pliegue(
                request.form.get('pliegue_suprailiaco_1'),
                request.form.get('pliegue_suprailiaco_2'),
                request.form.get('pliegue_suprailiaco_3')
            )
            
            # Pliegues cutáneos - Abdominal
            registro.pliegue_abdominal_1 = safe_float(request.form.get('pliegue_abdominal_1'))
            registro.pliegue_abdominal_2 = safe_float(request.form.get('pliegue_abdominal_2'))
            registro.pliegue_abdominal_3 = safe_float(request.form.get('pliegue_abdominal_3'))
            registro.pliegue_abdominal_promedio = calcular_promedio_pliegue(
                request.form.get('pliegue_abdominal_1'),
                request.form.get('pliegue_abdominal_2'),
                request.form.get('pliegue_abdominal_3')
            )
            
            # Pliegues cutáneos - Muslo anterior
            registro.pliegue_muslo_anterior_1 = safe_float(request.form.get('pliegue_muslo_anterior_1'))
            registro.pliegue_muslo_anterior_2 = safe_float(request.form.get('pliegue_muslo_anterior_2'))
            registro.pliegue_muslo_anterior_3 = safe_float(request.form.get('pliegue_muslo_anterior_3'))
            registro.pliegue_muslo_anterior_promedio = calcular_promedio_pliegue(
                request.form.get('pliegue_muslo_anterior_1'),
                request.form.get('pliegue_muslo_anterior_2'),
                request.form.get('pliegue_muslo_anterior_3')
            )
            
            # Pliegues cutáneos - Pantorrilla
            registro.pliegue_pantorrilla_1 = safe_float(request.form.get('pliegue_pantorrilla_1'))
            registro.pliegue_pantorrilla_2 = safe_float(request.form.get('pliegue_pantorrilla_2'))
            registro.pliegue_pantorrilla_3 = safe_float(request.form.get('pliegue_pantorrilla_3'))
            registro.pliegue_pantorrilla_promedio = calcular_promedio_pliegue(
                request.form.get('pliegue_pantorrilla_1'),
                request.form.get('pliegue_pantorrilla_2'),
                request.form.get('pliegue_pantorrilla_3')
            )
            
            # Circunferencias
            registro.circunferencia_cuello = safe_float(request.form.get('circunferencia_cuello'))
            registro.circunferencia_pecho = safe_float(request.form.get('circunferencia_pecho'))
            registro.circunferencia_brazo = safe_float(request.form.get('circunferencia_brazo'))
            registro.circunferencia_antebrazo = safe_float(request.form.get('circunferencia_antebrazo'))
            registro.circunferencia_cintura = safe_float(request.form.get('circunferencia_cintura'))
            registro.circunferencia_cadera = safe_float(request.form.get('circunferencia_cadera'))
            registro.circunferencia_muslo = safe_float(request.form.get('circunferencia_muslo'))
            registro.circunferencia_pantorrilla = safe_float(request.form.get('circunferencia_pantorrilla'))
            registro.observaciones = request.form.get('observaciones', '')
            
            # Recalcular IMC
            registro.imc = registro.calcular_imc()
            
            db.session.commit()
            flash('Registro actualizado exitosamente!', 'success')
            return redirect(url_for('ver_registro', id=id))
            
        except Exception as e:
            flash(f'Error al actualizar el registro: {str(e)}', 'error')
    
    return render_template('editar_registro.html', registro=registro)

@app.route('/eliminar_registro/<int:id>', methods=['POST'])
def eliminar_registro(id):
    registro = RegistroFisico.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    flash('Registro eliminado exitosamente!', 'success')
    return redirect(url_for('ver_usuario', usuario_id=registro.usuario_id))

@app.route('/estadisticas/<int:usuario_id>')
def estadisticas(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    registros = RegistroFisico.query.filter_by(usuario_id=usuario_id).order_by(RegistroFisico.fecha.desc()).all()
    
    if not registros:
        return render_template('estadisticas.html', estadisticas=None, usuario=usuario)
    
    # Calcular estadísticas básicas
    pesos = [r.peso for r in registros]
    imcs = [r.imc for r in registros]
    
    # Calcular estadísticas de grasa corporal
    porcentajes_grasa = []
    spc_valores = []
    for registro in registros:
        porcentaje = registro.calcular_porcentaje_grasa()
        if porcentaje:
            porcentajes_grasa.append(porcentaje)
        
        spc = registro.calcular_spc_aaherd()
        if spc:
            spc_valores.append(spc)
    
    # Obtener información AAHPERD del registro más reciente
    registro_actual = registros[0] if registros else None
    spc_actual = registro_actual.calcular_spc_aaherd() if registro_actual else None
    percentila_spc_actual = registro_actual.calcular_percentila_spc_aaherd() if registro_actual else None
    clasificacion_spc_actual = registro_actual.clasificar_spc_aaherd() if registro_actual else (None, None)
    interpretacion_motivacional = registro_actual.obtener_interpretacion_motivacional() if registro_actual else (None, None, None)
    
    estadisticas = {
        'total_registros': len(registros),
        'peso_actual': pesos[0] if pesos else 0,
        'peso_inicial': pesos[-1] if pesos else 0,
        'diferencia_peso': pesos[0] - pesos[-1] if len(pesos) > 1 else 0,
        'peso_promedio': sum(pesos) / len(pesos),
        'peso_minimo': min(pesos),
        'peso_maximo': max(pesos),
        'imc_actual': imcs[0] if imcs else 0,
        'imc_promedio': sum(imcs) / len(imcs),
        'clasificacion_actual': registros[0].clasificacion_imc() if registros else 'N/A',
        'porcentaje_grasa_actual': porcentajes_grasa[0] if porcentajes_grasa else None,
        'porcentaje_grasa_promedio': sum(porcentajes_grasa) / len(porcentajes_grasa) if porcentajes_grasa else None,
        'percentila_grasa_actual': registros[0].calcular_percentila_grasa() if registros else None,
        'clasificacion_grasa_actual': registros[0].clasificar_grasa_corporal() if registros else (None, None),
        'progreso_grasa': registros[0].calcular_progreso_grasa() if registros else (None, None, None, None),
        # Nuevas estadísticas AAHPERD
        'spc_actual': spc_actual,
        'spc_promedio': sum(spc_valores) / len(spc_valores) if spc_valores else None,
        'percentila_spc_actual': percentila_spc_actual,
        'clasificacion_spc_actual': clasificacion_spc_actual,
        'interpretacion_motivacional': interpretacion_motivacional
    }
    
    return render_template('estadisticas.html', estadisticas=estadisticas, registros=registros, usuario=usuario)

@app.route('/api/registros/<int:usuario_id>')
def api_registros(usuario_id):
    registros = RegistroFisico.query.filter_by(usuario_id=usuario_id).order_by(RegistroFisico.fecha.desc()).all()
    return jsonify([{
        'id': r.id,
        'fecha': r.fecha.isoformat(),
        'peso': r.peso,
        'altura': r.altura,
        'imc': r.imc,
        'clasificacion': r.clasificacion_imc()
    } for r in registros])

@app.route('/exportar_registros/<int:usuario_id>')
def exportar_registros(usuario_id):
    """Exporta los registros de un usuario a CSV"""
    usuario = Usuario.query.get_or_404(usuario_id)
    csv_content = export_registros_csv(usuario_id)
    
    if not csv_content:
        flash('No hay registros para exportar', 'warning')
        return redirect(url_for('estadisticas', usuario_id=usuario_id))
    
    from flask import Response
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=registros_{usuario.nombre}_{usuario.apellido}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
    )

@app.route('/importar_registros/<int:usuario_id>', methods=['GET', 'POST'])
def importar_registros(usuario_id):
    """Importa registros desde CSV"""
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if request.method == 'POST':
        if 'archivo_csv' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('importar_registros', usuario_id=usuario_id))
        
        archivo = request.files['archivo_csv']
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('importar_registros', usuario_id=usuario_id))
        
        if archivo and archivo.filename.endswith('.csv'):
            try:
                csv_content = archivo.read().decode('utf-8')
                registros_importados, errores = import_registros_csv(csv_content, usuario_id)
                
                if registros_importados:
                    flash(f'Se importaron {len(registros_importados)} registros exitosamente', 'success')
                
                if errores:
                    for error in errores:
                        flash(error, 'warning')
                
                return redirect(url_for('estadisticas', usuario_id=usuario_id))
                
            except Exception as e:
                flash(f'Error al procesar el archivo: {str(e)}', 'error')
                return redirect(url_for('importar_registros', usuario_id=usuario_id))
        else:
            flash('El archivo debe ser un CSV', 'error')
            return redirect(url_for('importar_registros', usuario_id=usuario_id))
    
    return render_template('importar_registros.html', usuario=usuario)

@app.route('/guia_mediciones')
def guia_mediciones():
    return render_template('guia_mediciones.html')

@app.route('/importar_csv/<int:usuario_id>', methods=['GET', 'POST'])
def importar_csv(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if request.method == 'POST':
        try:
            # Verificar que se subió un archivo
            if 'archivo_csv' not in request.files:
                flash('No se seleccionó ningún archivo', 'error')
                return redirect(url_for('importar_csv', usuario_id=usuario_id))
            
            archivo = request.files['archivo_csv']
            if archivo.filename == '':
                flash('No se seleccionó ningún archivo', 'error')
                return redirect(url_for('importar_csv', usuario_id=usuario_id))
            
            if not archivo.filename.lower().endswith('.csv'):
                flash('El archivo debe ser un CSV', 'error')
                return redirect(url_for('importar_csv', usuario_id=usuario_id))
            
            # Leer el contenido del archivo
            contenido = archivo.read().decode('utf-8')
            
            # Parsear el CSV
            registros_csv = parse_garmin_csv(contenido)
            
            if not registros_csv:
                flash('No se pudieron extraer datos válidos del archivo CSV', 'error')
                return redirect(url_for('importar_csv', usuario_id=usuario_id))
            
            # Verificar que el usuario tenga altura guardada
            if not usuario.altura:
                flash('El usuario debe tener una altura configurada antes de importar datos. Por favor, edita el usuario y agrega su altura.', 'error')
                return redirect(url_for('editar_usuario', usuario_id=usuario_id))
            
            # Crear registros en la base de datos
            registros_creados = 0
            registros_duplicados = 0
            
            for datos in registros_csv:
                # Verificar si ya existe un registro para esta fecha/hora
                registro_existente = RegistroFisico.query.filter_by(
                    usuario_id=usuario_id,
                    fecha=datos['fecha_hora']
                ).first()
                
                if registro_existente:
                    registros_duplicados += 1
                    continue
                
                # Crear nuevo registro
                registro = RegistroFisico(
                    usuario_id=usuario_id,
                    fecha=datos['fecha_hora'],
                    peso=datos['peso'],
                    altura=usuario.altura,
                    imc=datos['imc'] if datos['imc'] else None
                )
                
                # Calcular IMC si no se proporcionó
                if not registro.imc:
                    registro.imc = registro.calcular_imc()
                
                db.session.add(registro)
                registros_creados += 1
            
            db.session.commit()
            
            # Mensaje de éxito
            mensaje = f'Importación completada: {registros_creados} registros creados'
            if registros_duplicados > 0:
                mensaje += f', {registros_duplicados} registros duplicados omitidos'
            
            flash(mensaje, 'success')
            return redirect(url_for('ver_usuario', usuario_id=usuario_id))
            
        except Exception as e:
            flash(f'Error al importar el archivo: {str(e)}', 'error')
            return redirect(url_for('importar_csv', usuario_id=usuario_id))
    
    return render_template('importar_csv.html', usuario=usuario)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Configuración para Docker
    host = '0.0.0.0' if os.environ.get('FLASK_ENV') == 'production' else '0.0.0.0'
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host=host, debug=debug)
