// Funcionalidad para panel de empresa

function toggleMenu() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('menuOverlay');
  
  sidebar.classList.toggle('open');
  overlay.classList.toggle('active');
  
  // Prevenir scroll del body cuando el menú está abierto
  if (sidebar.classList.contains('open')) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // Event listener para el toggle del menú
  const menuToggle = document.getElementById('menuToggle');
  if (menuToggle) {
    menuToggle.addEventListener('click', toggleMenu);
  }

  // Cerrar menú al hacer clic en overlay
  const menuOverlay = document.getElementById('menuOverlay');
  if (menuOverlay) {
    menuOverlay.addEventListener('click', toggleMenu);
  }

  // Cerrar menú al hacer clic en cualquier enlace del menú en móvil
  const menuItems = document.querySelectorAll('.nav-item');
  menuItems.forEach(item => {
    item.addEventListener('click', function() {
      if (window.innerWidth <= 768) {
        toggleMenu();
      }
    });
  });

  // Manejar navegación sin salir del dashboard para "Mis trabajos"
  const btnMisTrabajos = document.getElementById('btn-mis-trabajos');
  if (btnMisTrabajos) {
    btnMisTrabajos.addEventListener('click', function(e) {
      e.preventDefault();
      // Remover active de todos los botones
      document.querySelectorAll('.nav-item').forEach(btn => {
        btn.classList.remove('active', 'mis-trabajos-active');
      });
      // Activar el botón actual
      this.classList.add('mis-trabajos-active');
      
      // Cargar contenido
      cargarMisTrabajos();
    });
  }

  // Cargar por defecto los trabajos
  cargarMisTrabajos();
});

function cargarMisTrabajos() {
  // Mostrar indicador de carga
  const contenidoDashboard = document.getElementById('contenido-dashboard');
  contenidoDashboard.innerHTML = '<div class="main-content"><div class="loader">Cargando trabajos...</div></div>';

  // Usar jQuery si está disponible, sino fetch
  if (typeof $ !== 'undefined') {
    $.ajax({
      url: urlMisTrabajosAjax,
      method: "GET",
      success: function(data) {
        $('#contenido-dashboard').html(data);
      },
      error: function() {
        $('#contenido-dashboard').html('<div class="main-content"><p style="text-align: center; color: #e74c3c; padding: 2rem;">Error al cargar los trabajos. Intenta nuevamente.</p></div>');
      }
    });
  } else {
    fetch(urlMisTrabajosAjax)
      .then(response => {
        if (!response.ok) throw new Error('Error al cargar');
        return response.text();
      })
      .then(html => {
        contenidoDashboard.innerHTML = html;
      })
      .catch(error => {
        contenidoDashboard.innerHTML = '<div class="main-content"><p style="text-align: center; color: #e74c3c; padding: 2rem;">Error al cargar los trabajos. Intenta nuevamente.</p></div>';
        console.error(error);
      });
  }
}