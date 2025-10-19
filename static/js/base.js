// ===== LLAMKAY BASE JS - Funcionalidades Globales =====

/**
 * Obtener token CSRF de las cookies
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
 * Mostrar notificación flotante
 */
function showNotification(message, type = 'info', duration = 4000) {
    // Remover notificación anterior si existe
    const existingNotification = document.querySelector('.global-notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    const notification = document.createElement('div');
    notification.className = `global-notification notification-${type}`;

    const colors = {
        success: { bg: '#07734B', shadow: 'rgba(7, 115, 75, 0.3)' },
        error: { bg: '#dc2626', shadow: 'rgba(220, 38, 38, 0.3)' },
        warning: { bg: '#f59e0b', shadow: 'rgba(245, 158, 11, 0.3)' },
        info: { bg: '#024959', shadow: 'rgba(2, 73, 89, 0.3)' }
    };

    const color = colors[type] || colors.info;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${color.bg};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 6px 20px ${color.shadow};
        z-index: 10000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
        font-weight: 500;
        max-width: 350px;
        transform: translateX(400px);
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255,255,255,0.2);
        display: flex;
        align-items: center;
        gap: 12px;
    `;

    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };

    notification.innerHTML = `
        <span style="font-size: 18px;">${icons[type] || icons.info}</span>
        <span>${message}</span>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

/**
 * Validar email
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

/**
 * Validar teléfono peruano (9 dígitos)
 */
function validatePhone(phone) {
    const re = /^[0-9]{9}$/;
    return re.test(phone);
}

/**
 * Formatear número con separadores de miles
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Debounce para optimizar eventos
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Smooth scroll a un elemento
 */
function smoothScrollTo(elementId, offset = 0) {
    const element = document.getElementById(elementId);
    if (element) {
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

/**
 * Lazy loading de imágenes
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

/**
 * Inicializar funcionalidades globales al cargar el DOM
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Llamkay Base JS iniciado');
    
    // Inicializar lazy loading
    initLazyLoading();
    
    // Agregar animaciones de scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    console.log('✅ Base JS listo');
});

// Exponer funciones globalmente
window.getCookie = getCookie;
window.showNotification = showNotification;
window.validateEmail = validateEmail;
window.validatePhone = validatePhone;
window.formatNumber = formatNumber;
window.debounce = debounce;
window.smoothScrollTo = smoothScrollTo;