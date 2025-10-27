/**
 * disputas.js
 * JavaScript para el módulo de disputas
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== VALIDACIÓN DE FORMULARIO ====================
    const disputaForm = document.querySelector('.disputa-form');
    if (disputaForm) {
        initDisputaFormValidation();
    }
    
    // ==================== CONFIRMACIONES DE ACCIONES ====================
    const accionForms = document.querySelectorAll('.accion-form');
    accionForms.forEach(form => {
        form.addEventListener('submit', handleDisputaAccionSubmit);
    });
    
    // ==================== CONTADOR DE CARACTERES ====================
    const motivoTextarea = document.getElementById('motivo');
    if (motivoTextarea) {
        initDisputaCharacterCounter();
    }
    
    // ==================== VALIDACIÓN DE MONTO ====================
    const montoInput = document.querySelector('input[name="monto_resolucion"]');
    if (montoInput) {
        initMontoValidation();
    }
    
    // ==================== EVIDENCIAS MÚLTIPLES ====================
    const evidenciasTextarea = document.getElementById('evidencias');
    if (evidenciasTextarea) {
        initEvidenciasHelper();
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
    
    // ==================== ANIMACIONES DE ENTRADA ====================
    initAnimations();
});

/**
 * Inicializar validación del formulario de disputa
 */
function initDisputaFormValidation() {
    const form = document.querySelector('.disputa-form');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', function(e) {
        const idContrato = document.querySelector('input[name="id_contrato"]');
        const motivo = document.getElementById('motivo');
        
        let isValid = true;
        let errorMsg = '';
        
        // Validar ID contrato
        if (!idContrato || !idContrato.value || parseInt(idContrato.value) <= 0) {
            isValid = false;
            errorMsg = 'Por favor ingresa un ID de contrato válido';
            if (idContrato) idContrato.focus();
        }
        
        // Validar motivo (mínimo 100 caracteres)
        else if (!motivo.value || motivo.value.trim().length < 100) {
            isValid = false;
            errorMsg = 'El motivo debe tener al menos 100 caracteres. Sé específico y detallado.';
            motivo.focus();
        }
        
        if (!isValid) {
            e.preventDefault();
            showNotification(errorMsg, 'error');
            return false;
        }
        
        // Deshabilitar botón y mostrar loading
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
            Iniciando disputa...
        `;
    });
}

/**
 * Manejar envío de formularios de acción de disputa
 */
function handleDisputaAccionSubmit(e) {
    const form = e.target;
    const accion = form.querySelector('input[name="accion"]').value;
    
    let confirmMsg = '';
    let isValid = true;
    
    switch(accion) {
        case 'asignar':
            confirmMsg = '¿Deseas asignarte esta disputa? Serás el mediador responsable de resolverla.';
            break;
            
        case 'resolver':
            // Validar campos de resolución
            const resolucion = form.querySelector('textarea[name="resolucion"]');
            const idFavorece = form.querySelector('select[name="id_favorece_a"]');
            
            if (!resolucion || !resolucion.value.trim()) {
                isValid = false;
                showNotification('Por favor describe la resolución en detalle', 'error');
                if (resolucion) resolucion.focus();
            } else if (!idFavorece || !idFavorece.value) {
                isValid = false;
                showNotification('Por favor selecciona a quién favorece la resolución', 'error');
                if (idFavorece) idFavorece.focus();
            } else if (resolucion.value.trim().length < 50) {
                isValid = false;
                showNotification('La resolución debe ser más detallada (mínimo 50 caracteres)', 'error');
                resolucion.focus();
            }
            
            if (!isValid) {
                e.preventDefault();
                return false;
            }
            
            confirmMsg = '¿Confirmas que quieres resolver esta disputa con esta decisión? Esta acción es definitiva y se notificará a ambas partes.';
            break;
            
        case 'cerrar':
            confirmMsg = '¿Deseas cerrar esta disputa sin resolución? Esto significa que no se tomará ninguna acción adicional.';
            break;
    }
    
    if (!isValid) {
        e.preventDefault();
        return false;
    }
    
    if (confirmMsg && !confirm(confirmMsg)) {
        e.preventDefault();
        return false;
    }
    
    // Deshabilitar botón para evitar doble envío
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = `
            <svg class="spin" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
            </svg>
            Procesando...
        `;
    }
}

/**
 * Contador de caracteres para motivo de disputa
 */
function initDisputaCharacterCounter() {
    const textarea = document.getElementById('motivo');
    const minChars = 100;
    
    // Crear elemento contador
    const counter = document.createElement('div');
    counter.className = 'char-counter';
    counter.style.cssText = `
        display: flex;
        justify-content: space-between;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    `;
    
    const charCount = document.createElement('span');
    charCount.className = 'char-count';
    
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        flex: 1;
        height: 4px;
        background: #e2e3e5;
        border-radius: 4px;
        margin: 0 1rem;
        overflow: hidden;
    `;
    
    const progressFill = document.createElement('div');
    progressFill.style.cssText = `
        height: 100%;
        background: linear-gradient(90deg, #dc3545, #ffc107, #198754);
        width: 0%;
        transition: width 0.3s ease, background 0.3s ease;
    `;
    
    progressBar.appendChild(progressFill);
    counter.appendChild(charCount);
    counter.appendChild(progressBar);
    
    textarea.parentNode.insertBefore(counter, textarea.nextSibling);
    
    // Actualizar contador
    function updateCounter() {
        const length = textarea.value.trim().length;
        const percentage = Math.min((length / minChars) * 100, 100);
        
        progressFill.style.width = percentage + '%';
        
        if (length < minChars) {
            const remaining = minChars - length;
            charCount.textContent = `${length} / ${minChars} (faltan ${remaining})`;
            charCount.style.color = '#dc3545';
        } else {
            charCount.textContent = `${length} caracteres`;
            charCount.style.color = '#198754';
        }
    }
    
    textarea.addEventListener('input', updateCounter);
    updateCounter();
}

/**
 * Validación de monto de resolución
 */
function initMontoValidation() {
    const montoInput = document.querySelector('input[name="monto_resolucion"]');
    
    montoInput.addEventListener('input', function() {
        let value = this.value;
        
        // Permitir solo números y punto decimal
        value = value.replace(/[^\d.]/g, '');
        
        // Permitir solo un punto decimal
        const parts = value.split('.');
        if (parts.length > 2) {
            value = parts[0] + '.' + parts.slice(1).join('');
        }
        
        // Limitar a 2 decimales
        if (parts[1] && parts[1].length > 2) {
            value = parts[0] + '.' + parts[1].substring(0, 2);
        }
        
        this.value = value;
        
        // Validar que no sea negativo
        if (parseFloat(value) < 0) {
            this.value = '0';
        }
    });
    
    montoInput.addEventListener('blur', function() {
        if (this.value && !this.value.includes('.')) {
            this.value = parseFloat(this.value).toFixed(2);
        }
    });
}

/**
 * Helper para evidencias múltiples
 */
function initEvidenciasHelper() {
    const textarea = document.getElementById('evidencias');
    
    // Crear helper de formato
    const helper = document.createElement('div');
    helper.className = 'evidencias-helper';
    helper.style.cssText = `
        margin-top: 0.5rem;
        padding: 0.75rem;
        background: #e7f3ff;
        border-left: 4px solid #0d6efd;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #084298;
    `;
    
    helper.innerHTML = `
        <strong>💡 Formato de evidencias:</strong><br>
        Una URL por línea. Ejemplo:<br>
        <code style="display: block; margin-top: 0.5rem; padding: 0.5rem; background: white; border-radius: 4px;">
        https://drive.google.com/file/d/123...<br>
        https://dropbox.com/s/abc...<br>
        https://imgur.com/xyz...
        </code>
    `;
    
    textarea.parentNode.insertBefore(helper, textarea.nextSibling);
    
    // Validar URLs al escribir
    textarea.addEventListener('blur', function() {
        const lines = this.value.split('\n').filter(line => line.trim());
        const invalidUrls = [];
        
        lines.forEach((line, index) => {
            try {
                new URL(line.trim());
            } catch {
                if (line.trim()) {
                    invalidUrls.push(index + 1);
                }
            }
        });
        
        if (invalidUrls.length > 0) {
            showNotification(
                `URL inválida en línea(s): ${invalidUrls.join(', ')}. Verifica el formato.`,
                'warning'
            );
        }
    });
}

/**
 * Animaciones de entrada
 */
function initAnimations() {
    // Observar elementos para animarlos al entrar en viewport
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Elementos a animar
    const elements = document.querySelectorAll('.disputa-card, .info-card, .contrato-info-card, .timeline-card');
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.animationDelay = `${index * 0.1}s`;
        observer.observe(el);
    });
}

/**
 * Mostrar notificación
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const colors = {
        error: '#dc3545',
        success: '#198754',
        warning: '#ffc107',
        info: '#0dcaf0'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        padding: 1rem 1.5rem;
        background: ${colors[type] || colors.info};
        color: ${type === 'warning' ? '#000' : '#fff'};
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
        font-weight: 500;
    `;
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                ${getIconForType(type)}
            </svg>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-eliminar
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
    
    // Click para cerrar
    notification.addEventListener('click', () => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    });
}

function getIconForType(type) {
    const icons = {
        error: '<circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line>',
        success: '<polyline points="20 6 9 17 4 12"></polyline>',
        warning: '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line>',
        info: '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>'
    };
    return icons[type] || icons.info;
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
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
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
    
    .notification {
        cursor: pointer;
    }
    
    .notification:hover {
        transform: translateX(-5px);
        transition: transform 0.2s ease;
    }
`;
document.head.appendChild(style);

/**
 * Auto-expandir textareas
 */
document.querySelectorAll('textarea.form-control').forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Expandir al cargar si tiene contenido
    if (textarea.value) {
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
    }
});

/**
 * Copiar ID de contrato al clipboard
 */
const contratoLinks = document.querySelectorAll('.disputa-contrato a, .contrato-badge');
contratoLinks.forEach(link => {
    link.addEventListener('dblclick', function(e) {
        e.preventDefault();
        const text = this.textContent.trim();
        const idMatch = text.match(/\d+/);
        
        if (idMatch) {
            navigator.clipboard.writeText(idMatch[0]).then(() => {
                showNotification('ID copiado al portapapeles', 'success');
            });
        }
    });
});