// =============================================
// LLAMKAY LANDING PAGE JAVASCRIPT
// 
// PRINCIPIOS APLICADOS:
// - Nielsen: Visibilidad del estado del sistema, Control y libertad del usuario
// - Nielsen: Prevención de errores
// - Responsividad: Interacciones táctiles y desktop
// - I18n: Manejo de envío de formulario para cambio de idioma (Backend/Django)
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // ==================== I18N LOGIC (CORREGIDA) ====================
    
    const langForm = document.getElementById('language-form');
    const langInput = document.getElementById('language-input');
    const navMenu = document.querySelector('.nav-menu');
    const langSelector = document.querySelector('.language-selector'); 
    const navMobileActions = document.querySelector('.nav-mobile-actions'); 

    // Función para manejar el evento de cambio de idioma
    function handleLanguageChange(e) {
        e.preventDefault();
        const newLang = this.getAttribute('data-lang');
        
        // 1. Actualizar el input con el nuevo idioma
        if (langInput) langInput.value = newLang;
        
        // 2. Enviar el formulario
        if (langForm) langForm.submit();
        
        console.log('Solicitando cambio de idioma a:', newLang); 
    }
    
    if (langForm && langInput) {
        
        // 1. Asignar listeners a los botones originales (Desktop Header)
        document.querySelectorAll('.language-selector .lang-btn').forEach(btn => {
            btn.addEventListener('click', handleLanguageChange);
        });
        
        // 2. Lógica para el botón en el menú móvil (Responsividad)
        if (langSelector && navMobileActions && navMenu && window.innerWidth < 1024) { 
            // CLONACIÓN: Clonamos el selector
            const clonedLangSelector = langSelector.cloneNode(true);
            clonedLangSelector.classList.add('mobile-clone'); 
            
            // Re-asignar event listeners al CLON (Crucial: cloning descarta listeners)
            clonedLangSelector.querySelectorAll('.lang-btn').forEach(btn => {
                 btn.addEventListener('click', handleLanguageChange);
            });
            
            // Insertar el clon antes de las acciones móviles
            navMenu.insertBefore(clonedLangSelector, navMobileActions);
        }
    }

    // ==================== MOBILE MENU ====================
    // Nielsen: Control y libertad del usuario
    
    const navToggle = document.querySelector('.nav-toggle');
    
    if (navToggle && navMenu) { // navMenu ya está definido arriba
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Actualizar aria-expanded para accesibilidad
            const isExpanded = navMenu.classList.contains('active');
            navToggle.setAttribute('aria-expanded', isExpanded);
            
            // Animar hamburger
            const spans = navToggle.querySelectorAll('span');
            if (isExpanded) {
                spans[0].style.transform = 'rotate(45deg) translate(8px, 8px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans.forEach(span => {
                    span.style.transform = '';
                    span.style.opacity = '';
                });
            }
            
            // Nielsen: Visibilidad del estado - feedback visual
            console.log('Menu móvil toggled:', isExpanded);
        });
        
        // Cerrar menu al hacer click fuera
        document.addEventListener('click', function(e) {
            if (navMenu && !navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
                
                const spans = navToggle.querySelectorAll('span');
                spans.forEach(span => {
                    span.style.transform = '';
                    span.style.opacity = '';
                });
            }
        });
        
        // Cerrar con tecla ESC
        // Nielsen: Control y libertad del usuario
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
                navToggle.focus(); // Devolver focus al botón
            }
        });
    }
    
    // ==================== SMOOTH SCROLL ====================
    // Nielsen: Flexibilidad y eficiencia de uso
    // Gestalt: Continuidad - transiciones suaves
    
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    // Cerrar menu móvil si está abierto
                    if (navMenu && navMenu.classList.contains('active')) {
                        navMenu.classList.remove('active');
                    }
                    
                    // Scroll suave
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Focus en el elemento para accesibilidad
                    targetElement.setAttribute('tabindex', '-1');
                    targetElement.focus();
                }
            }
        });
    });
    
    // ==================== INTERSECTION OBSERVER ====================
    // Nielsen: Visibilidad del estado
    // Gestalt: Continuidad - animaciones de entrada
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Añadir clase de animación
                entry.target.classList.add('is-visible');
                
                // Dejar de observar una vez visible
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observar elementos animables
    const animatedElements = document.querySelectorAll(
        '.benefit-card, .step, .category-card, .hero-card'
    );
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Añadir estilos para elementos visibles
    const style = document.createElement('style');
    style.textContent = `
        .is-visible {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
    
    // ==================== BUTTON RIPPLE EFFECT ====================
    // Nielsen: Visibilidad del estado - feedback táctil
    // Responsividad: Mejorar interacciones táctiles
    
    const buttons = document.querySelectorAll('.btn, .btn-nav, .category-card');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Crear efecto ripple
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.appendChild(ripple);
            
            // Remover después de la animación
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Estilos para ripple effect
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        .btn, .btn-nav, .category-card {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
    
    // ==================== HEADER SCROLL EFFECT ====================
    // Nielsen: Visibilidad del estado
    // Gestalt: Figura y fondo - contraste adaptativo
    
    const header = document.querySelector('.header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        // Auto-hide en scroll down (opcional)
        if (scrollTop > lastScrollTop && scrollTop > 500) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Estilos para header scrolled
    const headerStyle = document.createElement('style');
    headerStyle.textContent = `
        .header {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .header.scrolled {
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
    `;
    document.head.appendChild(headerStyle);
    
    // ==================== LAZY LOADING IMAGES ====================
    // Nielsen: Flexibilidad y eficiencia - optimización de rendimiento
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        img.classList.add('loaded');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // ==================== FORM VALIDATION ====================
    // Nielsen: Prevención de errores
    // Nielsen: Ayuda a recuperarse de errores
    
    const forms = document.querySelectorAll('form:not(#language-form)'); // Excluir el formulario de idioma
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                    
                    // Crear mensaje de error si no existe
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('error-message')) {
                        const errorMsg = document.createElement('span');
                        errorMsg.className = 'error-message';
                        errorMsg.textContent = 'Este campo es requerido'; 
                        errorMsg.style.color = 'var(--color-danger, #dc2626)';
                        errorMsg.style.fontSize = '0.875rem';
                        errorMsg.style.marginTop = '0.25rem';
                        errorMsg.style.display = 'block';
                        input.parentNode.insertBefore(errorMsg, input.nextSibling);
                    }
                } else {
                    input.classList.remove('error');
                    const errorMsg = input.nextElementSibling;
                    if (errorMsg && errorMsg.classList.contains('error-message')) {
                        errorMsg.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Focus en el primer campo con error
                const firstError = form.querySelector('.error');
                if (firstError) {
                    firstError.focus();
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
        
        // Validación en tiempo real
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('error');
                } else {
                    this.classList.remove('error');
                    const errorMsg = this.nextElementSibling;
                    if (errorMsg && errorMsg.classList.contains('error-message')) {
                        errorMsg.remove();
                    }
                }
            });
        });
    });
    
    // ==================== ACCESSIBILITY ENHANCEMENTS ====================
    // Nielsen: Ayuda y documentación
    
    // Skip link para navegación por teclado
    const body = document.body;
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Saltar al contenido principal';
    body.insertBefore(skipLink, body.firstChild);
    
    // Añadir ID al contenido principal si no existe
    const mainContent = document.querySelector('main, [role="main"]');
    if (mainContent && !mainContent.id) {
        mainContent.id = 'main-content';
    }
    
    // ==================== PERFORMANCE MONITORING ====================
    // Opcional: Monitorear métricas de rendimiento
    
    if ('PerformanceObserver' in window) {
        try {
            const perfObserver = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.entryType === 'largest-contentful-paint') {
                        console.log('LCP:', entry.renderTime || entry.loadTime);
                    }
                }
            });
            
            perfObserver.observe({ entryTypes: ['largest-contentful-paint'] });
        } catch (e) {
            console.log('Performance Observer no soportado');
        }
    }
    
    // ==================== CONSOLE LOG ====================
    console.log('✅ Llamkay Landing Page loaded successfully!');
    console.log('📱 Responsive: ' + (window.innerWidth <= 768 ? 'Mobile' : 'Desktop'));
});

// ==================== UTILITY FUNCTIONS ====================

// Debounce function para optimizar eventos de scroll/resize
// Nielsen: Flexibilidad y eficiencia de uso
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

// Throttle function para limitar frecuencia de ejecución
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Uso de debounce en resize
window.addEventListener('resize', debounce(function() {
    console.log('Window resized:', window.innerWidth + 'x' + window.innerHeight);
    // Recalcular layouts si es necesario
}, 250));