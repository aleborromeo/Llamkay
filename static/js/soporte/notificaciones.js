/**
 * Notificaciones - Interactividad
 */

document.addEventListener('DOMContentLoaded', () => {
    // Obtener CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Marcar como leída
    document.querySelectorAll('.marcar-leida').forEach(btn => {
        btn.addEventListener('click', async function() {
            const id = this.dataset.id;
            const card = document.querySelector(`.notificacion-card[data-id="${id}"]`);
            
            try {
                const response = await fetch(`/soporte/notificaciones/${id}/leer/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Remover clase no-leida
                    card.classList.remove('no-leida');
                    
                    // Remover indicador
                    const indicator = card.querySelector('.notificacion-indicator');
                    if (indicator) {
                        indicator.style.animation = 'fadeOut 0.3s';
                        setTimeout(() => indicator.remove(), 300);
                    }
                    
                    // Remover botón
                    this.style.animation = 'fadeOut 0.3s';
                    setTimeout(() => this.remove(), 300);
                    
                    // Actualizar contador
                    actualizarContador();
                    
                    mostrarNotificacion('Notificación marcada como leída', 'success');
                } else {
                    mostrarNotificacion('Error al marcar como leída', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                mostrarNotificacion('Error de conexión', 'error');
            }
        });
    });
    
    // Eliminar notificación
    document.querySelectorAll('.eliminar-notificacion').forEach(btn => {
        btn.addEventListener('click', async function() {
            if (!confirm('¿Estás seguro de eliminar esta notificación?')) {
                return;
            }
            
            const id = this.dataset.id;
            const card = document.querySelector(`.notificacion-card[data-id="${id}"]`);
            
            try {
                const response = await fetch(`/soporte/notificaciones/${id}/eliminar/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Animar salida
                    card.style.animation = 'slideOut 0.3s ease-out';
                    setTimeout(() => {
                        card.remove();
                        
                        // Verificar si quedan notificaciones
                        const remaining = document.querySelectorAll('.notificacion-card').length;
                        if (remaining === 0) {
                            mostrarEmptyState();
                        }
                        
                        actualizarContador();
                    }, 300);
                    
                    mostrarNotificacion('Notificación eliminada', 'success');
                } else {
                    mostrarNotificacion('Error al eliminar', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                mostrarNotificacion('Error de conexión', 'error');
            }
        });
    });
    
    // Actualizar contador
    function actualizarContador() {
        const noLeidas = document.querySelectorAll('.notificacion-card.no-leida').length;
        const total = document.querySelectorAll('.notificacion-card').length;
        
        const contadorNoLeidas = document.querySelector('.stat-badge .stat-number');
        const contadorTotal = document.querySelector('.stat-badge.stat-secondary .stat-number');
        
        if (contadorNoLeidas) {
            contadorNoLeidas.textContent = noLeidas;
        }
        
        if (contadorTotal) {
            contadorTotal.textContent = total;
        }
        
        // Ocultar botón "Marcar todas" si no hay no leídas
        if (noLeidas === 0) {
            const btnMarcarTodas = document.querySelector('.header-actions');
            if (btnMarcarTodas) {
                btnMarcarTodas.style.animation = 'fadeOut 0.3s';
                setTimeout(() => btnMarcarTodas.remove(), 300);
            }
        }
    }
    
    // Mostrar empty state
    function mostrarEmptyState() {
        const container = document.querySelector('.notificaciones-list');
        container.innerHTML = `
            <div class="empty-state" style="animation: fadeIn 0.5s;">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                    <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
                <h2>No tienes notificaciones</h2>
                <p>Cuando recibas notificaciones, aparecerán aquí</p>
                <a href="/" class="btn btn-primary">Ir al inicio</a>
            </div>
        `;
    }
    
    // Mostrar notificación toast
    function mostrarNotificacion(mensaje, tipo = 'info') {
        // Remover toast anterior si existe
        const existente = document.querySelector('.toast-notification');
        if (existente) {
            existente.remove();
        }
        
        // Crear toast
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${tipo}`;
        toast.innerHTML = `
            <div class="toast-content">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    ${tipo === 'success' ? '<polyline points="20 6 9 17 4 12"></polyline>' : '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>'}
                </svg>
                <span>${mensaje}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Animar entrada
        setTimeout(() => toast.classList.add('show'), 10);
        
        // Remover después de 3 segundos
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
});

// Agregar estilos para animaciones y toast
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        to { opacity: 0; transform: scale(0.95); }
    }
    
    @keyframes slideOut {
        to { opacity: 0; transform: translateX(100%); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .toast-notification {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
        z-index: 10000;
        transform: translateY(100px);
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .toast-notification.show {
        transform: translateY(0);
        opacity: 1;
    }
    
    .toast-content {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #1a1a1a;
        font-weight: 500;
    }
    
    .toast-success {
        border-left: 4px solid #07734B;
    }
    
    .toast-success svg {
        color: #07734B;
    }
    
    .toast-error {
        border-left: 4px solid #dc3545;
    }
    
    .toast-error svg {
        color: #dc3545;
    }
    
    @media (max-width: 768px) {
        .toast-notification {
            bottom: 1rem;
            right: 1rem;
            left: 1rem;
        }
    }
`;
document.head.appendChild(style);