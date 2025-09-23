#!/usr/bin/env python3
"""
Script de inicialización de base de datos para Docker
"""

import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, '/app')

from app import app, db, Usuario

def init_database():
    """Inicializa la base de datos y crea un usuario por defecto"""
    
    with app.app_context():
        try:
            # Crear directorio instance si no existe
            instance_dir = Path('/app/instance')
            instance_dir.mkdir(exist_ok=True)
            
            # Verificar que el directorio existe
            if not instance_dir.exists():
                print(f"❌ Error: No se pudo crear el directorio {instance_dir}")
                sys.exit(1)
            
            print(f"✅ Directorio {instance_dir} creado correctamente")
            
            # Crear todas las tablas
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
            
            # Verificar si ya existe un usuario
            if Usuario.query.first() is None:
                # Crear usuario por defecto
                usuario_default = Usuario(
                    nombre="Usuario",
                    apellido="Por Defecto",
                    fecha_nacimiento=None,
                    genero="M",
                    activo=False
                )
                db.session.add(usuario_default)
                db.session.commit()
                print("✅ Usuario por defecto creado")
            else:
                print("ℹ️  Usuarios ya existen en la base de datos")
                
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
            print(f"Directorio actual: {os.getcwd()}")
            print(f"Directorio instance: {instance_dir}")
            print(f"Existe: {instance_dir.exists()}")
            if instance_dir.exists():
                print(f"Permisos: {oct(instance_dir.stat().st_mode)[-3:]}")
            sys.exit(1)

if __name__ == "__main__":
    init_database()
