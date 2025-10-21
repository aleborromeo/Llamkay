import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from apps.users.models import Provincia, Distrito, Comunidad

# -------------------------------------------------
# 🔹 Token de API PERÚ
# -------------------------------------------------
APIPERU_TOKEN = "b6bcd92e240859cbaf2a08b008e357b250fbe17f7c950501bcdb1262e837140b"


# -------------------------------------------------
# 🔹 Consultar DNI (RENIEC)
# -------------------------------------------------
@csrf_exempt
@require_GET
def consultar_dni_api(request):
    dni = request.GET.get('dni', '').strip()
    
    print(f"🔍 === CONSULTA DNI INICIADA ===")
    print(f"📋 DNI recibido: {dni}")
    
    # 🧪 MODO DE PRUEBA - Datos ficticios para desarrollo
    # Descomenta esto si el token no funciona y quieres probar el frontend
    """
    DATOS_PRUEBA = {
        '72768256': {'nombres': 'JUAN CARLOS', 'apellidoPaterno': 'PEREZ', 'apellidoMaterno': 'GARCIA'},
        '12345678': {'nombres': 'MARIA', 'apellidoPaterno': 'LOPEZ', 'apellidoMaterno': 'TORRES'},
    }
    
    if dni in DATOS_PRUEBA:
        data = DATOS_PRUEBA[dni]
        return JsonResponse({
            'success': True,
            'dni': dni,
            'nombres': data['nombres'],
            'apellido_paterno': data['apellidoPaterno'],
            'apellido_materno': data['apellidoMaterno'],
            'nombre_completo': f"{data['nombres']} {data['apellidoPaterno']} {data['apellidoMaterno']}"
        })
    """

    if not dni or len(dni) != 8:
        print(f"❌ Error: DNI debe tener 8 dígitos")
        return JsonResponse({'success': False, 'error': 'El DNI debe tener 8 dígitos'}, status=400)

    if not dni.isdigit():
        print(f"❌ Error: DNI debe contener solo números")
        return JsonResponse({'success': False, 'error': 'El DNI debe contener solo números'}, status=400)

    url = f"https://api.apis.net.pe/v2/reniec/dni?numero={dni}"
    headers = {
        "Authorization": f"Bearer {APIPERU_TOKEN}", 
        "Accept": "application/json"
    }
    
    print(f"🌐 URL de consulta: {url}")
    print(f"🔐 Token (primeros 20 chars): {APIPERU_TOKEN[:20]}...")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📦 Response Text: {response.text[:200]}...")  # Primeros 200 caracteres

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Datos obtenidos: {data}")
            
            return JsonResponse({
                'success': True,
                'dni': data.get('numeroDocumento', ''),
                'nombres': data.get('nombres', ''),
                'apellido_paterno': data.get('apellidoPaterno', ''),
                'apellido_materno': data.get('apellidoMaterno', ''),
                'nombre_completo': f"{data.get('nombres', '')} {data.get('apellidoPaterno', '')} {data.get('apellidoMaterno', '')}"
            })
        elif response.status_code == 401:
            print(f"❌ Error 401: Token inválido o sin autorización")
            return JsonResponse({
                'success': False, 
                'error': 'Token de API inválido. Contacta al administrador.'
            }, status=500)
        elif response.status_code == 404:
            print(f"⚠️ Error 404: DNI no encontrado en RENIEC")
            return JsonResponse({
                'success': False, 
                'error': 'DNI no encontrado en la base de datos de RENIEC'
            }, status=404)
        else:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return JsonResponse({
                'success': False, 
                'error': f'Error al consultar DNI (Código: {response.status_code})'
            }, status=response.status_code)

    except requests.exceptions.Timeout:
        print(f"⏱️ Error: Timeout al consultar API")
        return JsonResponse({'success': False, 'error': 'Tiempo de espera agotado'}, status=500)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de requests: {str(e)}")
        return JsonResponse({'success': False, 'error': f'Error de conexión: {str(e)}'}, status=500)
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return JsonResponse({'success': False, 'error': f'Error inesperado: {str(e)}'}, status=500)


# -------------------------------------------------
# 🔹 Consultar RUC (SUNAT)
# -------------------------------------------------
@csrf_exempt
@require_GET
def consultar_ruc_api(request):
    ruc = request.GET.get('ruc', '').strip()
    
    print(f"🔍 === CONSULTA RUC INICIADA ===")
    print(f"📋 RUC recibido: {ruc}")

    if not ruc or len(ruc) != 11:
        print(f"❌ Error: RUC debe tener 11 dígitos")
        return JsonResponse({'success': False, 'error': 'El RUC debe tener 11 dígitos'}, status=400)

    if not ruc.isdigit():
        print(f"❌ Error: RUC debe contener solo números")
        return JsonResponse({'success': False, 'error': 'El RUC debe contener solo números'}, status=400)

    url = f"https://api.apis.net.pe/v2/sunat/ruc?numero={ruc}"
    headers = {
        "Authorization": f"Bearer {APIPERU_TOKEN}", 
        "Accept": "application/json"
    }
    
    print(f"🌐 URL de consulta: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📦 Response Text: {response.text[:200]}...")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Datos obtenidos: {data}")
            
            return JsonResponse({
                'success': True,
                'ruc': data.get('numeroDocumento', ''),
                'razon_social': data.get('razonSocial', ''),
                'nombre_comercial': data.get('nombreComercial', ''),
                'direccion': data.get('direccion', ''),
                'estado': data.get('estado', ''),
                'condicion': data.get('condicion', ''),
                'departamento': data.get('departamento', ''),
                'provincia': data.get('provincia', ''),
                'distrito': data.get('distrito', '')
            })
        elif response.status_code == 401:
            print(f"❌ Error 401: Token inválido")
            return JsonResponse({
                'success': False, 
                'error': 'Token de API inválido. Contacta al administrador.'
            }, status=500)
        elif response.status_code == 404:
            print(f"⚠️ Error 404: RUC no encontrado")
            return JsonResponse({
                'success': False, 
                'error': 'RUC no encontrado en SUNAT'
            }, status=404)
        else:
            print(f"❌ Error HTTP {response.status_code}")
            return JsonResponse({
                'success': False, 
                'error': f'Error al consultar RUC (Código: {response.status_code})'
            }, status=response.status_code)

    except requests.exceptions.Timeout:
        print(f"⏱️ Error: Timeout")
        return JsonResponse({'success': False, 'error': 'Tiempo de espera agotado'}, status=500)
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# -------------------------------------------------
# 🔹 Cargar Provincias por Departamento
# -------------------------------------------------
@require_GET
def cargar_provincias(request):
    id_departamento = request.GET.get('id_departamento')

    if not id_departamento:
        return JsonResponse([], safe=False)

    provincias = Provincia.objects.filter(
        id_departamento=id_departamento
    ).values('id_provincia', 'nombre').order_by('nombre')

    return JsonResponse(list(provincias), safe=False)


# -------------------------------------------------
# 🔹 Cargar Distritos por Provincia
# -------------------------------------------------
@require_GET
def cargar_distritos(request):
    id_provincia = request.GET.get('id_provincia')

    if not id_provincia:
        return JsonResponse([], safe=False)

    distritos = Distrito.objects.filter(
        id_provincia=id_provincia
    ).values('id_distrito', 'nombre').order_by('nombre')

    return JsonResponse(list(distritos), safe=False)


# -------------------------------------------------
# 🔹 Cargar Comunidades por Distrito
# -------------------------------------------------
@require_GET
def cargar_comunidades(request):
    id_distrito = request.GET.get('id_distrito')

    if not id_distrito:
        return JsonResponse([], safe=False)

    comunidades = Comunidad.objects.filter(
        id_distrito=id_distrito
    ).values('id_comunidad', 'nombre').order_by('nombre')

    return JsonResponse(list(comunidades), safe=False)