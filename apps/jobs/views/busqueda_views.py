"""
Vistas de Búsqueda de Trabajos
Responsabilidad: Controladores para búsqueda y visualización
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

from apps.jobs.services import BusquedaService
from apps.users.models import Usuario, Departamento, Provincia, Distrito


class BusquedaViews:
    """
    Vistas para búsqueda de trabajos
    Principio de Responsabilidad Única (SOLID)
    """
    
    def __init__(self):
        self.service = BusquedaService()
    
    def buscar_trabajos(self, request):
        """Vista principal de búsqueda de trabajos"""
        # Obtener parámetros de búsqueda
        busqueda = request.GET.get('buscar', '').strip()
        departamento_id = request.GET.get('departamento_id')
        provincia_id = request.GET.get('provincia_id')
        distrito_id = request.GET.get('distrito_id')
        tipo_usuario = request.GET.get('tipo_usuario', '')
        categoria_id = request.GET.get('categoria_id')
        page = request.GET.get('page', 1)
        
        # Construir filtros
        filtros = {}
        if busqueda:
            filtros['busqueda'] = busqueda
        if departamento_id:
            filtros['departamento'] = departamento_id
        if provincia_id:
            filtros['provincia'] = provincia_id
        if distrito_id:
            filtros['distrito'] = distrito_id
        if tipo_usuario:
            filtros['tipo'] = tipo_usuario
        if categoria_id:
            filtros['categoria'] = categoria_id
        
        # Obtener usuario actual
        usuario_actual = None
        if request.user.is_authenticated:
            try:
                usuario_actual = Usuario.objects.get(user=request.user)
            except Usuario.DoesNotExist:
                pass
        
        # Buscar trabajos
        trabajos = self.service.buscar_trabajos(filtros, usuario_actual)
        
        # Marcar guardados y postulados si hay usuario
        if usuario_actual:
            trabajos = self.service.marcar_trabajos_guardados(
                trabajos,
                usuario_actual.id_usuario
            )
            trabajos = self.service.marcar_trabajos_postulados(
                trabajos,
                usuario_actual.id_usuario
            )
        
        # Paginar resultados
        paginator = Paginator(trabajos, 12)
        trabajos_paginados = paginator.get_page(page)
        
        # Datos para filtros
        departamentos = Departamento.objects.all().order_by('nombre')
        provincias = Provincia.objects.none()
        distritos = Distrito.objects.none()
        
        if departamento_id:
            provincias = Provincia.objects.filter(
                id_departamento=departamento_id
            ).order_by('nombre')
        
        if provincia_id:
            distritos = Distrito.objects.filter(
                id_provincia=provincia_id
            ).order_by('nombre')
        
        context = {
            'trabajos': trabajos_paginados,
            'departamentos': departamentos,
            'provincias': provincias,
            'distritos': distritos,
            'filtros': {
                'buscar': busqueda,
                'departamento_id': departamento_id,
                'provincia_id': provincia_id,
                'distrito_id': distrito_id,
                'tipo_usuario': tipo_usuario,
                'categoria_id': categoria_id,
            },
            'total_resultados': len(trabajos),
        }
        
        return render(request, 'jobs/busqueda/lista.html', context)
    
    def all_trabajos(self, request):
        """Vista que muestra todos los trabajos (alias)"""
        return self.buscar_trabajos(request)
    
    def detalle_trabajo(self, request, tipo, trabajo_id):
        """Ver detalle de un trabajo específico"""
        # Validar tipo
        if tipo not in ['usuario', 'empresa']:
            return JsonResponse({'error': 'Tipo inválido'}, status=400)
        
        # Obtener usuario actual
        usuario_actual = None
        if request.user.is_authenticated:
            try:
                usuario_actual = Usuario.objects.get(user=request.user)
            except Usuario.DoesNotExist:
                pass
        
        # Obtener detalle
        detalle = self.service.get_detalle_trabajo(tipo, trabajo_id, usuario_actual)
        
        if not detalle:
            messages.error(request, "Trabajo no encontrado o no disponible.")
            return redirect('jobs:buscar_trabajos')
        
        context = detalle
        
        return render(request, 'jobs/busqueda/detalle.html', context)
    
    def filtrar_trabajos(self, request):
        """Vista AJAX para filtrar trabajos dinámicamente"""
        if request.method == 'GET':
            return self.buscar_trabajos(request)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Implementar respuesta AJAX si es necesario
            pass
        
        return JsonResponse({'error': 'Método no permitido'}, status=405)


# Instancia global para usar en urls.py
busqueda_views = BusquedaViews()