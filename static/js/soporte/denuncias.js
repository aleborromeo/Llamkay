/**
 * denuncias.js
 * JavaScript para el módulo de denuncias
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== VALIDACIÓN DE FORMULARIO ====================
    const denunciaForm = document.querySelector('.denuncia-form');
    if (denunciaForm) {
        initFormValidation();
    }
    
    // ==================== CONFIRMACIONES ====================
    const accionForms = document.querySelectorAll('.accion-form');
    accionForms.forEach(form => {
        form.addEventListener('submit', handleAccionSubmit);
    });
    
    // ==================== CONTADOR DE CARACTERES ====================
    const descripcionTextarea = document.getElementById('descripcion');
    if (descripcionTextarea) {
        initCharacterCounter();
    }
    
    // ==================== SMOOTH SCROLL ====================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

/**
 * Inicializar validación del formulario
 */
function initFormValidation() {
    const form = document.querySelector('.denuncia-form');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', function(e) {
        // Validar campos requeridos
        const idDenunciado = document.getElementById('id_denunciado');
        const motivo = document.getElementById('motivo');
        const descripcion = document.getElementById('descripcion');
        
        let isValid = true;
        let errorMsg = '';
        
        // Validar ID denunciado
        if (!idDenunciado.value || idDenunciado.value <= 0) {
            isValid = false;
            errorMsg = 'Por favor ingresa un ID de usuario válido';
            idDenunciado.focus();
        }
        
        // Validar motivo
        else if (!motivo.value) {
            isValid = false;
            errorMsg = 'Por favor selecciona un motivo';
            motivo.focus();
        }
        
        // Validar descripción (mínimo 50 caracteres)
        else if (!descripcion.value || descripcion.value.trim().length < 50) {
            isValid = false;
            errorMsg = 'La descripción debe tener al menos 50 caracteres';
            descripcion.focus();
        }
        
        if (!isValid) {
            e.preventDefault();
            showNotification(errorMsg, 'error');
            return false;
        }
        
        // Deshabilitar botón para evitar doble envío
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <svg class="spin" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="2" x2="12" y2="6"></line>
                <line x1="12" y1="18" x2="12" y2="22"></line>
                <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
                <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
                <line x1="2" y1="12" x2="6" y2="12"></line>
                <line x1="18" y1="12" x2="22" y2="12"></line>
                <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
                <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
            </svg>
            Enviando...
        `;
    });
}

/**
 * Manejar envío de formularios de acción
 */
function handleAccionSubmit(e) {
    const form = e.target;
    const accion = form.querySelector('input[name="accion"]').value;
    
    let confirmMsg = '';
    
    switch(accion) {
        case 'asignar':
            confirmMsg = '¿Deseas asignarte esta denuncia? Serás responsable de su revisión.';
            break;
        case 'resolver':
            const resolucion = form.querySelector('textarea[name="resolucion"]');
            if (!resolucion || !resolucion.value.trim()) {
                e.preventDefault();
                showNotification('Por favor describe la resolución', 'error');
                if (resolucion) resolucion.focus();
                return false;
            }
            confirmMsg = '¿Confirmas que quieres resolver esta denuncia? Esta acción no se puede deshacer.';
            break;
        case 'rechazar':
            const motivoRechazo = form.querySelector('textarea[name="motivo_rechazo"]');
            if (!motivoRechazo || !motivoRechazo.value.trim()) {
                e.preventDefault();
                showNotification('Por favor explica el motivo del rechazo', 'error');
                if (motivoRechazo) motivoRechazo.focus();
                return false;
            }
            confirmMsg = '¿Estás seguro de rechazar esta denuncia?';
            break;
        case 'cerrar':
            confirmMsg = '¿Deseas cerrar esta denuncia sin tomar acción?';
            break;
    }
    
    if (confirmMsg && !confirm(confirmMsg)) {
        e.preventDefault();
        return false;
    }
}

/**
 * Contador de caracteres para descripción
 */
function initCharacterCounter() {
    const textarea = document.getElementById('descripcion');
    const minChars = 50;
    
    // Crear elemento contador
    const counter = document.createElement('small');
    counter.className = 'char-counter';
    counter.style.cssText = 'display: block; margin-top: 0.5rem; color: #666;';
    textarea.parentNode.insertBefore(counter, textarea.nextSibling);
    
    // Actualizar contador
    function updateCounter() {
        const length = textarea.value.trim().length;
        const remaining = minChars - length;
        
        if (remaining > 0) {
            counter.textContent = `Faltan ${remaining} caracteres (mínimo ${minChars})`;
            counter.style.color = '#dc3545';
        } else {
            counter.textContent = `${length} caracteres`;
            counter.style.color = '#198754';
        }
    }
    
    textarea.addEventListener('input', updateCounter);
    updateCounter();
}

/**
 * Mostrar notificación
 */
function showNotification(message, type = 'info') {
    // Crear notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        padding: 1rem 1.5rem;
        background: ${type === 'error' ? '#dc3545' : type === 'success' ? '#198754' : '#0dcaf0'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                ${type === 'error' ? 
                    '<circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line>' :
                type === 'success' ?
                    '<polyline points="20 6 9 17 4 12"></polyline>' :
                    '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>'
                }
            </svg>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-eliminar después de 5 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Agregar estilos de animación
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
    
    .spin {
        animation: spin 1s linear infinite;
    }
    
    .char-counter {
        transition: color 0.3s ease;
    }
`;
document.head.appendChild(style);

/**
 * Filtros en lista de denuncias
 */
if (document.querySelector('.denuncias-grid')) {
    const filtros = document.querySelectorAll('.filtro-badge a');
    filtros.forEach(filtro => {
        filtro.addEventListener('click', function(e) {
            // Agregar efecto de loading
            const denunciasGrid = document.querySelector('.denuncias-grid');
            if (denunciasGrid) {
                denunciasGrid.style.opacity = '0.5';
                denunciasGrid.style.transition = 'opacity 0.3s ease';
            }
        });
    });
}

/**
 * Confirmación al eliminar desde detalle
 */
const deleteButtons = document.querySelectorAll('.btn-danger');
deleteButtons.forEach(btn => {
    if (btn.textContent.includes('Eliminar') || btn.textContent.includes('Rechazar')) {
        btn.addEventListener('click', function(e) {
            const form = this.closest('form');
            if (form && !form.dataset.confirmed) {
                e.preventDefault();
                if (confirm('¿Estás seguro? Esta acción no se puede deshacer.')) {
                    form.dataset.confirmed = 'true';
                    form.submit();
                }
            }
        });
    }
});

/**
 * Auto-expandir textareas
 */
document.querySelectorAll('textarea.form-control').forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});

/**
 * Validación en tiempo real
 */
const formInputs = document.querySelectorAll('.form-control');
formInputs.forEach(input => {
    input.addEventListener('blur', function() {
        validateInput(this);
    });
    
    input.addEventListener('input', function() {
        if (this.classList.contains('error')) {
            validateInput(this);
        }
    });
});

function validateInput(input) {
    const value = input.value.trim();
    const isRequired = input.hasAttribute('required');
    
    // Limpiar error previo
    input.classList.remove('error');
    const errorMsg = input.parentNode.querySelector('.error-message');
    if (errorMsg) errorMsg.remove();
    
    // Validar si es requerido
    if (isRequired && !value) {
        showInputError(input, 'Este campo es requerido');
        return false;
    }
    
    // Validaciones específicas
    if (input.type === 'number' && value) {
        if (parseInt(value) <= 0) {
            showInputError(input, 'Debe ser un número positivo');
            return false;
        }
    }
    
    if (input.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showInputError(input, 'Email inválido');
            return false;
        }
    }
    
    if (input.type === 'url' && value) {
        try {
            new URL(value);
        } catch {
            showInputError(input, 'URL inválida');
            return false;
        }
    }
    
    return true;
}

function showInputError(input, message) {
    input.classList.add('error');
    
    const errorDiv = document.createElement('small');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = 'color: #dc3545; display: block; margin-top: 0.25rem; font-size: 0.85rem;';
    errorDiv.textContent = message;
    
    input.parentNode.appendChild(errorDiv);
}

// Agregar estilos para inputs con error
const errorStyles = document.createElement('style');
errorStyles.textContent = `
    .form-control.error {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 4px rgba(220, 53, 69, 0.1) !important;
    }
`;
document.head.appendChild(errorStyles);