from django.http import JsonResponse
from apps.users.models import Provincia, Distrito 
from django.views.decorators.http import require_GET

@require_GET
def cargar_provincias(request):
    id_departamento = request.GET.get('id_departamento')
    if not id_departamento:
        return JsonResponse([], safe=False)
    
    provincias = Provincia.objects.filter(id_departamento=id_departamento).values('id_provincia', 'nombre')
    return JsonResponse(list(provincias), safe=False)


@require_GET
def cargar_distritos(request):
    id_provincia = request.GET.get('id_provincia')
    if not id_provincia:
        return JsonResponse([], safe=False)
    
    distritos = Distrito.objects.filter(id_provincia=id_provincia).values('id_distrito', 'nombre')
    return JsonResponse(list(distritos), safe=False)
