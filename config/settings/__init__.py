"""
Settings package initialization.
Carga explícita de la configuración base primero.
"""

import os

# CARGAR BASE PRIMERO (OBLIGATORIO)
from .base import *

# Determinar qué configuración adicional usar
ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *

# VERIFICAR QUE EL TOKEN ESTÁ DISPONIBLE
print("\n" + "="*60)
print("🔍 VERIFICACIÓN FINAL DE TOKEN EN __init__.py")
print("="*60)
print(f"APIPERU_TOKEN existe: {bool(APIPERU_TOKEN)}")
if APIPERU_TOKEN:
    print(f"APIPERU_TOKEN valor: {APIPERU_TOKEN[:20]}...")
else:
    print("❌ APIPERU_TOKEN NO ESTÁ DEFINIDO")
print("="*60 + "\n")