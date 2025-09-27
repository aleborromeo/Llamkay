from django.shortcuts import render
from trabajos.utils import obtener_trabajos_unificados

def index(request):
    trabajos_destacados = obtener_trabajos_unificados(limit=6)

    return render(request, 'trabajo_llamkay/index.html', {
        'trabajos': trabajos_destacados,
    })
def nosotros (request):
    return render(request,'trabajo_llamkay/nosotros.html')


def medios(request):
    return render(request,'trabajo_llamkay/medios.html')

def contactanos(request):
    return render(request,'trabajo_llamkay/contactanos.html')


