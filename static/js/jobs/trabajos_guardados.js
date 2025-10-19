// Funcionalidad para trabajos guardados

document.addEventListener('DOMContentLoaded', function() {
  // Confirmación para quitar trabajos guardados
  const formsQuitar = document.querySelectorAll('.form-quitar-guardado');
  
  formsQuitar.forEach(form => {
    form.addEventListener('submit', function(e) {
      const btnQuitar = this.querySelector('.btn-quitar');
      const mensaje = btnQuitar?.getAttribute('data-confirm') || '¿Estás seguro de que deseas quitar este trabajo guardado?';
      
      if (!confirm(mensaje)) {
        e.preventDefault();
      }
    });
  });

  // Funcionalidad para iconos de mensajería
  const mensajeIcons = document.querySelectorAll('.mensaje-icon-btn');
  mensajeIcons.forEach(icon => {
    icon.addEventListener('click', function(e) {
      e.stopPropagation();
      alert('Funcionalidad de mensajería aún no implementada.');
    });
  });
});