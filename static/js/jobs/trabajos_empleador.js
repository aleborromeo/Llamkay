// Funcionalidad para trabajos del empleador

document.addEventListener('DOMContentLoaded', function() {
  // Confirmación para eliminar trabajos
  const enlacesEliminar = document.querySelectorAll('.icon-eliminar');
  
  enlacesEliminar.forEach(enlace => {
    enlace.addEventListener('click', function(e) {
      const mensaje = this.getAttribute('data-confirm') || '¿Estás seguro de que deseas eliminar este trabajo?';
      if (!confirm(mensaje)) {
        e.preventDefault();
      }
    });
  });
});