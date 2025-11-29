// mis-trabajos.js - Gestión de ofertas del empleador

document.addEventListener('DOMContentLoaded', function() {
    // Manejo de tabs
    initTabs();
    
    // Manejo de cambio de estados
    initCambioEstado();
    
    // Manejo de dropdowns
    initDropdowns();
});

/**
 * Inicializar sistema de tabs
 */
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remover clase active de todos los botones y contenidos
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Agregar clase active al botón clickeado y su contenido
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

/**
 * Inicializar dropdowns manualmente
 */
function initDropdowns() {
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const dropdown = this.parentElement;
            const menu = dropdown.querySelector('.dropdown-menu');
            
            // Cerrar otros dropdowns abiertos
            document.querySelectorAll('.dropdown-menu.show').forEach(otherMenu => {
                if (otherMenu !== menu) {
                    otherMenu.classList.remove('show');
                }
            });
            
            // Toggle del dropdown actual
            menu.classList.toggle('show');
        });
    });
    
    // Cerrar dropdowns al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
}

/**
 * Inicializar cambio de estado de ofertas
 */
function initCambioEstado() {
    const botonesEstado = document.querySelectorAll('.cambiar-estado');
    
    botonesEstado.forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            
            const ofertaId = this.getAttribute('data-id');
            const nuevoEstado = this.getAttribute('data-estado');
            
            cambiarEstadoOferta(ofertaId, nuevoEstado);
        });
    });
}

/**
 * Cambiar estado de una oferta
 */
function cambiarEstadoOferta(ofertaId, nuevoEstado) {
    // Confirmación para cierre de oferta
    if (nuevoEstado === 'cerrada') {
        if (!confirm('¿Estás seguro de cerrar esta oferta? No podrás reactivarla después.')) {
            return;
        }
    }
    
    // Mostrar indicador de carga
    const card = document.querySelector(`.oferta-card[data-oferta-id="${ofertaId}"]`) || 
                 document.querySelector('.oferta-card'); // Fallback
    
    if (card) {
        card.style.opacity = '0.6';
        card.style.pointerEvents = 'none';
    }
    
    // Obtener CSRF token
    const csrftoken = getCookie('csrftoken');
    
    // Hacer petición AJAX
    fetch(`/empleadores/ofertas/cambiar-estado/${ofertaId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: `estado=${nuevoEstado}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarMensaje('success', data.message);
            
            // Recargar la página después de un breve delay
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            mostrarMensaje('error', data.message);
            
            if (card) {
                card.style.opacity = '1';
                card.style.pointerEvents = 'auto';
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarMensaje('error', 'Error al cambiar el estado de la oferta');
        
        if (card) {
            card.style.opacity = '1';
            card.style.pointerEvents = 'auto';
        }
    });
}

/**
 * Mostrar mensaje toast
 */
function mostrarMensaje(tipo, mensaje) {
    // Crear contenedor de mensajes si no existe
    let container = document.querySelector('.toast-container');
    
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    // Crear toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    
    const icon = tipo === 'success' ? '✓' : '✕';
    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-message">${mensaje}</span>
    `;
    
    container.appendChild(toast);
    
    // Animar entrada
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

/**
 * Obtener cookie por nombre (para CSRF token)
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Eliminar oferta (cerrarla permanentemente)
 */
function eliminarOferta(ofertaId) {
    if (!confirm('¿Estás seguro de eliminar esta oferta? Esta acción no se puede deshacer.')) {
        return;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    fetch(`/empleadores/ofertas/eliminar/${ofertaId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarMensaje('success', data.message);
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            mostrarMensaje('error', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarMensaje('error', 'Error al eliminar la oferta');
    });
}

// Exponer funciones globalmente si es necesario
window.cambiarEstadoOferta = cambiarEstadoOferta;
window.eliminarOferta = eliminarOferta;