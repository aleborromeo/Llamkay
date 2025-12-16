// mis-trabajos.js - Gestión de ofertas del empleador

document.addEventListener('DOMContentLoaded', function() {
    console.log("📋 Inicializando mis-trabajos.js");
    
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
    console.log(`🔘 Botones de cambio de estado encontrados: ${botonesEstado.length}`);

    botonesEstado.forEach((boton, index) => {
        boton.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            const url = this.dataset.url;
            const nuevoEstado = this.dataset.estado;

            console.log(`Botón ${index + 1}:`, { url, nuevoEstado });

            if (!url) {
                console.error("❌ Botón sin data-url:", this);
                mostrarMensaje('error', 'Error interno: URL no definida');
                return;
            }

            cambiarEstadoOferta(url, nuevoEstado);
        });
    });
}



/**
 * Cambiar estado de una oferta
 */
function cambiarEstadoOferta(url, nuevoEstado) {
    console.log("🔄 Cambiando estado:", { url, nuevoEstado });

    const csrftoken = getCookie('csrftoken');

    const formData = new FormData();
    formData.append('estado', nuevoEstado);

    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            mostrarMensaje('success', data.message);
            setTimeout(() => location.reload(), 1000);
        } else {
            mostrarMensaje('error', data.message);
        }
    })
    .catch(error => {
        console.error(error);
        mostrarMensaje('error', 'Error al cambiar el estado');
    });
}


/**
 * Mostrar mensaje toast
 */
function mostrarMensaje(tipo, mensaje) {
    console.log(`📢 Mostrando mensaje [${tipo}]:`, mensaje);
    
    // Crear contenedor de mensajes si no existe
    let container = document.querySelector('.toast-container');
    
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    // Crear toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    toast.style.backgroundColor = tipo === 'success' ? '#d4edda' : '#f8d7da';
    toast.style.color = tipo === 'success' ? '#155724' : '#721c24';
    toast.style.padding = '15px 20px';
    toast.style.marginBottom = '10px';
    toast.style.borderRadius = '8px';
    toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    toast.style.minWidth = '300px';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(400px)';
    toast.style.transition = 'all 0.3s ease';
    
    const icon = tipo === 'success' ? '✓' : '✕';
    toast.innerHTML = `
        <span class="toast-icon" style="font-weight: bold; margin-right: 10px;">${icon}</span>
        <span class="toast-message">${mensaje}</span>
    `;
    
    container.appendChild(toast);
    
    // Animar entrada
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 10);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(400px)';
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
    console.log("🗑️ Intentando eliminar oferta:", ofertaId);
    
    if (!confirm('¿Estás seguro de eliminar esta oferta? Esta acción no se puede deshacer.')) {
        console.log("❌ Usuario canceló la eliminación");
        return;
    }
    
    const csrftoken = getCookie('csrftoken');
    const url = `/empleadores/ofertas/eliminar/${ofertaId}/`;
    
    console.log("📤 Eliminando oferta en:", url);
    
    const formData = new FormData();
    
    fetch(url, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    .then(response => {
        console.log("📥 Respuesta recibida:", response.status);
        
        const contentType = response.headers.get("content-type") || "";
        if (!contentType.includes("application/json")) {
            return response.text().then(text => {
                console.error("Respuesta no JSON:", text.substring(0, 500));
                throw new Error("El servidor no devolvió JSON");
            });
        }
        
        return response.json();
    })
    .then(data => {
        console.log("📦 Datos:", data);
        
        if (data && data.success) {
            console.log("✅ Oferta eliminada");
            mostrarMensaje('success', data.message);
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            console.error("❌ Error:", data ? data.message : 'Sin datos');
            mostrarMensaje('error', data ? data.message : 'Error desconocido');
        }
    })
    .catch(error => {
        console.error('💥 Error al eliminar:', error);
        mostrarMensaje('error', 'Error al eliminar la oferta: ' + error.message);
    });
}

// Exponer funciones globalmente si es necesario
window.cambiarEstadoOferta = cambiarEstadoOferta;
window.eliminarOferta = eliminarOferta;