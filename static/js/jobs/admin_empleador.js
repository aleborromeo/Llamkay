// Funcionalidad para panel de empleador

function toggleMenu() {
  const aside = document.querySelector('.acciones');
  const overlay = document.getElementById('menuOverlay');
  
  aside.classList.toggle('open');
  overlay.classList.toggle('active');
  
  // Prevenir scroll del body cuando el menú está abierto
  if (aside.classList.contains('open')) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
}

document.addEventListener('DOMContentLoaded', function () {
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
  const menuItems = document.querySelectorAll('.menu-item');
  menuItems.forEach(item => {
    item.addEventListener('click', function() {
      if (window.innerWidth <= 768) {
        toggleMenu();
      }
    });
  });

  // Funciones de carga de contenido
  function cargarMisTrabajos() {
    fetch(urlMisTrabajosAjax)
      .then(response => {
        if (!response.ok) throw new Error("Error al cargar los trabajos");
        return response.text();
      })
      .then(html => {
        document.getElementById('contenido-dinamico').innerHTML = html;
        marcarActivo('cargar-trabajos');
      })
      .catch(error => {
        document.getElementById('contenido-dinamico').innerHTML = "<p>Error al cargar trabajos.</p>";
        console.error(error);
      });
  }

  function cargarVerTodos() {
    document.getElementById('contenido-dinamico').innerHTML = "<p>Ver Todos los Trabajos (pendiente de implementación).</p>";
    marcarActivo('ver-todos-trabajos');
  }

  function cargarPostulaciones() {
    document.getElementById('contenido-dinamico').innerHTML = "<p>Gestionar Postulaciones (pendiente de implementación).</p>";
    marcarActivo('gestionar-postulaciones');
  }

  function cargarGuardados() {
    document.getElementById('contenido-dinamico').innerHTML = "<p>Trabajos Guardados (pendiente de implementación).</p>";
    marcarActivo('trabajos-guardados');
  }

  function marcarActivo(idBoton) {
    document.querySelectorAll('.acciones ul li').forEach(li => {
      const btn = li.querySelector('button');
      if (btn && btn.id === idBoton) {
        li.classList.add('activo');
      } else {
        li.classList.remove('activo');
      }
    });
  }

  // Asignar eventos
  document.getElementById('cargar-trabajos')?.addEventListener('click', e => {
    e.preventDefault();
    cargarMisTrabajos();
  });
  
  document.getElementById('ver-todos-trabajos')?.addEventListener('click', e => {
    e.preventDefault();
    cargarVerTodos();
  });
  
  document.getElementById('gestionar-postulaciones')?.addEventListener('click', e => {
    e.preventDefault();
    cargarPostulaciones();
  });
  
  document.getElementById('trabajos-guardados')?.addEventListener('click', e => {
    e.preventDefault();
    cargarGuardados();
  });

  // Cargar mis trabajos por defecto
  cargarMisTrabajos();
});