// Funcionalidad para botones de tipo de usuario
function toggleTipo(btn) {
  document.querySelectorAll('.tipo-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  
  const valor = btn.getAttribute('data-tipo') || '';
  document.getElementById('tipoUsuarioInput').value = valor;
  console.log('Filtro seleccionado:', btn.textContent.trim(), '→', valor);
}

// Funcionalidad de modales
function abrirModal(id) {
  const modal = document.getElementById('modal-' + id);
  if (modal) {
    modal.classList.add('mostrar');
    document.body.style.overflow = 'hidden';
  }
}

function cerrarModal(id) {
  const modal = document.getElementById('modal-' + id);
  if (modal) {
    modal.classList.remove('mostrar');
    document.body.style.overflow = '';
  }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
  // Botones de tipo
  document.querySelectorAll('.tipo-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      toggleTipo(this);
    });
  });

  // Botones "Ver más"
  document.querySelectorAll('.ver-mas-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const modalId = this.getAttribute('data-modal-id');
      abrirModal(modalId.replace('modal-', ''));
    });
  });

  // Botones cerrar modal
  document.querySelectorAll('.cerrar-modal').forEach(btn => {
    btn.addEventListener('click', function() {
      const modalId = this.getAttribute('data-modal-id');
      cerrarModal(modalId.replace('modal-', ''));
    });
  });

  // Cerrar modal al hacer clic fuera
  window.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-trabajo')) {
      e.target.classList.remove('mostrar');
      document.body.style.overflow = '';
    }
  });

  // Iconos de mensajería
  document.querySelectorAll('.mensaje-icon-btn').forEach(img => {
    img.addEventListener('click', function(evt) {
      evt.stopPropagation();
      alert('Funcionalidad de mensajería aún no implementada.');
    });
  });
});