"""
Vistas de API - REFACTORIZADAS
Responsabilidad: Exponer endpoints REST simples
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from apps.users.services import APIService
from apps.users.models import Provincia, Distrito, Comunidad

import traceback


# -------------------------------------------------
# 🔹 Consultar DNI (RENIEC)
# -------------------------------------------------
@csrf_exempt
@require_GET
def consultar_dni_api(request):
    """
    Endpoint para consultar DNI en RENIEC
    Usa el servicio APIService con patrón Strategy
    """
    print("\n" + "="*60)
    print("🔍 INICIO - consultar_dni_api")
    print("="*60)
    
    dni = request.GET.get('dni', '').strip()
    print(f"📝 DNI recibido: '{dni}'")
    
    if not dni:
        print("❌ DNI vacío")
        return JsonResponse({
            'success': False,
            'error': 'DNI es requerido'
        }, status=400)
    
    # ✅ VALIDAR LONGITUD
    if len(dni) != 8:
        print(f"❌ Longitud incorrecta: {len(dni)} (esperado: 8)")
        return JsonResponse({
            'success': False,
            'error': f'DNI debe tener 8 dígitos (recibido: {len(dni)})'
        }, status=400)
    
    if not dni.isdigit():
        print(f"❌ Contiene caracteres no numéricos")
        return JsonResponse({
            'success': False,
            'error': 'DNI debe contener solo números'
        }, status=400)
    
    try:
        print(f"✅ Validaciones pasadas")
        print(f"🔑 Token en settings: {settings.APIPERU_TOKEN[:20]}..." if hasattr(settings, 'APIPERU_TOKEN') else "❌ APIPERU_TOKEN no está en settings")
        
        # Crear servicio
        print("🏗️ Creando APIService...")
        api_service = APIService()
        
        print(f"📞 Llamando a api_service.consultar('dni', '{dni}')...")
        resultado = api_service.consultar('dni', dni)
        
        print(f"📦 Resultado recibido del servicio:")
        print(f"   - success: {resultado.get('success')}")
        print(f"   - error: {resultado.get('error')}")
        print(f"   - datos: {list(resultado.keys())}")
        
        # ✅ FORMATEAR RESPUESTA CORRECTAMENTE
        if resultado['success']:
            print("✅ Consulta exitosa, formateando respuesta...")
            respuesta = {
                'success': True,
                'data': {
                    'dni': resultado.get('dni', ''),
                    'nombres': resultado.get('nombres', ''),
                    'apellido_paterno': resultado.get('apellido_paterno', ''),
                    'apellido_materno': resultado.get('apellido_materno', ''),
                    'nombre_completo': resultado.get('nombre_completo', '')
                }
            }
            print(f"📤 Enviando respuesta: {respuesta}")
            return JsonResponse(respuesta)
        else:
            print(f"❌ Consulta falló: {resultado.get('error')}")
            return JsonResponse({
                'success': False,
                'error': resultado.get('error', 'Error desconocido')
            }, status=400)
            
    except Exception as e:
        print(f"\n❌❌❌ EXCEPCIÓN CAPTURADA ❌❌❌")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print(f"Traceback:")
        print(traceback.format_exc())
        print("="*60 + "\n")
        
        return JsonResponse({
            'success': False,
            'error': f'Error inesperado: {str(e)}'
        }, status=500)


# -------------------------------------------------
# 🔹 Consultar RUC (SUNAT)
# -------------------------------------------------
@csrf_exempt
@require_GET
def consultar_ruc_api(request):
    """
    Endpoint para consultar RUC en SUNAT
    Usa el servicio APIService con patrón Strategy
    """
    print("\n" + "="*60)
    print("🔍 INICIO - consultar_ruc_api")
    print("="*60)
    
    ruc = request.GET.get('ruc', '').strip()
    print(f"📝 RUC recibido: '{ruc}'")
    
    if not ruc:
        print("❌ RUC vacío")
        return JsonResponse({
            'success': False,
            'error': 'RUC es requerido'
        }, status=400)
    
    # ✅ VALIDAR LONGITUD
    if len(ruc) != 11:
        print(f"❌ Longitud incorrecta: {len(ruc)} (esperado: 11)")
        return JsonResponse({
            'success': False,
            'error': f'RUC debe tener 11 dígitos (recibido: {len(ruc)})'
        }, status=400)
    
    if not ruc.isdigit():
        print(f"❌ Contiene caracteres no numéricos")
        return JsonResponse({
            'success': False,
            'error': 'RUC debe contener solo números'
        }, status=400)
    
    try:
        print(f"✅ Validaciones pasadas")
        
        # Crear servicio
        print("🏗️ Creando APIService...")
        api_service = APIService()
        
        print(f"📞 Llamando a api_service.consultar('ruc', '{ruc}')...")
        resultado = api_service.consultar('ruc', ruc)
        
        print(f"📦 Resultado recibido: {resultado}")
        
        # ✅ FORMATEAR RESPUESTA CORRECTAMENTE
        if resultado['success']:
            print("✅ Consulta exitosa")
            return JsonResponse({
                'success': True,
                'data': {
                    'ruc': resultado.get('ruc', ''),
                    'razon_social': resultado.get('razon_social', ''),
                    'nombre_comercial': resultado.get('nombre_comercial', ''),
                    'direccion': resultado.get('direccion', ''),
                    'estado': resultado.get('estado', ''),
                    'condicion': resultado.get('condicion', ''),
                    'departamento': resultado.get('departamento', ''),
                    'provincia': resultado.get('provincia', ''),
                    'distrito': resultado.get('distrito', '')
                }
            })
        else:
            print(f"❌ Consulta falló: {resultado.get('error')}")
            return JsonResponse({
                'success': False,
                'error': resultado.get('error', 'Error desconocido')
            }, status=400)
            
    except Exception as e:
        print(f"\n❌❌❌ EXCEPCIÓN CAPTURADA ❌❌❌")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print(traceback.format_exc())
        print("="*60 + "\n")
        
        return JsonResponse({
            'success': False,
            'error': f'Error inesperado: {str(e)}'
        }, status=500)


# -------------------------------------------------
# 🔹 Cargar Provincias por Departamento
# -------------------------------------------------
@csrf_exempt
@require_GET
def cargar_provincias(request):
    """API para cargar provincias de un departamento"""
    id_departamento = request.GET.get('id_departamento')
    
    if not id_departamento:
        return JsonResponse([], safe=False)
    
    try:
        provincias = Provincia.objects.filter(
            id_departamento=id_departamento
        ).values('id_provincia', 'nombre').order_by('nombre')
        
        return JsonResponse(list(provincias), safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)


@csrf_exempt
@require_GET
def cargar_distritos(request):
    """API para cargar distritos de una provincia"""
    id_provincia = request.GET.get('id_provincia')
    
    if not id_provincia:
        return JsonResponse([], safe=False)
    
    try:
        distritos = Distrito.objects.filter(
            id_provincia=id_provincia
        ).values('id_distrito', 'nombre').order_by('nombre')
        
        return JsonResponse(list(distritos), safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)


@csrf_exempt
@require_GET
def cargar_comunidades(request):
    """API para cargar comunidades de un distrito"""
    id_distrito = request.GET.get('id_distrito')
    
    if not id_distrito:
        return JsonResponse([], safe=False)
    
    try:
        comunidades = Comunidad.objects.filter(
            id_distrito=id_distrito
        ).values('id_comunidad', 'nombre').order_by('nombre')
        
        return JsonResponse(list(comunidades), safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)