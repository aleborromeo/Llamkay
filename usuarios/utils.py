
import os
import easyocr
import requests

from pdf2image import convert_from_path
from tempfile import NamedTemporaryFile

from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from .forms import MultipleCertificacionesForm

from usuarios.models import (
    Provincia, Distrito, Certificacion
)


# --- FUNCIONES UTILITARIAS ---

def extract_text_from_file(uploaded_file):
    """
    Extrae texto de una imagen o PDF usando EasyOCR.
    Soporta: PDF, JPG, PNG, JPEG.
    """
    # Obtener extensión
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    # Guardar archivo temporalmente
    with NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        temp_path = temp_file.name

    texto = ""
    reader = easyocr.Reader(['es'], gpu=False)

    try:
        if ext == ".pdf":
            # Convertir PDF a imágenes (una por página)
            paginas = convert_from_path(temp_path, dpi=300, fmt='jpeg')
            for img in paginas:
                with NamedTemporaryFile(delete=False, suffix='.jpg') as img_temp:
                    img.save(img_temp.name, 'JPEG')
                    resultado = reader.readtext(img_temp.name)
                    texto += " ".join([linea[1] for linea in resultado]) + " "
                    os.remove(img_temp.name)  # eliminar imagen temporal

        else:
            # Imagen directamente (JPG, PNG, etc.)
            resultado = reader.readtext(temp_path)
            texto = " ".join([linea[1] for linea in resultado])

    except Exception as e:
        texto = f"ERROR: {str(e)}"

    finally:
        # Limpieza del archivo temporal original
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return texto

def subir_certificaciones(request):
    if request.method == 'POST':
        form = MultipleCertificacionesForm(request.POST, request.FILES)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            archivos = request.FILES.getlist('archivos')
            for archivo in archivos:
                Certificacion.objects.create(usuario=request.user, archivo=archivo, descripcion=descripcion)
            messages.success(request, "Certificaciones subidas con éxito.")
            return redirect('usuarios:perfil')
    else:
        form = MultipleCertificacionesForm()

    return render(request, 'usuarios/subir_certificaciones.html', {'form': form})


@csrf_exempt
def buscar_dni(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    dni = request.GET.get('dni')
    if not dni or len(dni) != 8 or not dni.isdigit():
        return JsonResponse({'error': 'DNI inválido'}, status=400)

    try:
        token = 'apis-token-15994.QTKH6OudufG0IiLw5plIH9ucJ6MqNQSd'
        url = f"https://api.apis.net.pe/v1/dni?numero={dni}"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse({
                'nombres': data.get('nombres', ''),
                'apellido_paterno': data.get('apellidoPaterno', ''),
                'apellido_materno': data.get('apellidoMaterno', '')
            })
        else:
            return JsonResponse({'error': 'No se encontró el DNI'}, status=response.status_code)

    except Exception as e:
        return JsonResponse({'error': f'Error al consultar el DNI: {str(e)}'}, status=500)


@csrf_exempt
def buscar_ruc(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    ruc = request.GET.get('ruc')
    if not ruc or len(ruc) != 11 or not ruc.isdigit():
        return JsonResponse({'error': 'RUC inválido'}, status=400)

    try:
        token = 'apis-token-15994.QTKH6OudufG0IiLw5plIH9ucJ6MqNQSd'
        url = f'https://api.apis.net.pe/v1/ruc?numero={ruc}'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse({'razon_social': data.get('nombre', '')})
        else:
            return JsonResponse({'error': 'No se encontró el RUC'}, status=response.status_code)

    except Exception as e:
        return JsonResponse({'error': f'Error al consultar el RUC: {str(e)}'}, status=500)


def cargar_provincias(request):
    id_departamento = request.GET.get('id_departamento')
    provincias = Provincia.objects.filter(id_departamento=id_departamento).values('id_provincia', 'nombre')
    return JsonResponse(list(provincias), safe=False)

def cargar_distritos(request):
    id_provincia = request.GET.get('id_provincia')
    distritos = Distrito.objects.filter(id_provincia=id_provincia).values('id_distrito', 'nombre')
    return JsonResponse(list(distritos), safe=False)


