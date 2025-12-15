// =============================================
// DASHBOARD JAVASCRIPT - LLAMKAY.PE
// Mejorado: Responsividad, Accesibilidad e i18n
// =============================================

/**
 * PRINCIPIOS APLICADOS:
 * ✓ Nielsen #1 - Visibilidad del estado del sistema
 * ✓ Nielsen #3 - Control y libertad del usuario
 * ✓ Nielsen #5 - Prevención de errores
 * ✓ Nielsen #8 - Estética y diseño minimalista
 * ✓ Nielsen #9 - Ayuda a reconocer y recuperarse de errores
 * ✓ Nielsen #10 - Accesibilidad
 * ✓ Internacionalización (i18n) completa
 */

document.addEventListener('DOMContentLoaded', function() {
    // ==================== INICIALIZACIÓN ====================
    initMobileMenu();
    initUserDropdown();
    initSmoothScroll();
    initAnimations();
    initLazyLoading();
    updateWelcomeMessage();
    initAccessibility();
    initResponsiveChecks();
    initLanguageSwitcher();
    initKeyboardNavigation();
    initTouchOptimization();
    
    console.log('✅ Dashboard cargado con principios de usabilidad aplicados! 🚀');
});

/* =========================================================
   LANGUAGE SWITCHER (i18n)
   Manejo de cambio de idioma sin recargar
   ========================================================= */
function initLanguageSwitcher() {
    const languageForm = document.getElementById('language-form');
    const languageInput = document.getElementById('language-input');
    
    if (!languageForm || !languageInput) return;
    
    // Delegación de eventos para los botones de idioma
    document.addEventListener('click', function(e) {
        const langBtn = e.target.closest('.lang-btn');
        if (!langBtn) return;
        
        e.preventDefault();
        
        const selectedLang = langBtn.dataset.lang;
        
        // Actualizar visualmente botones activos
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-checked', 'false');
        });
        
        langBtn.classList.add('active');
        langBtn.setAttribute('aria-checked', 'true');
        
        // Establecer el idioma y enviar formulario
        languageInput.value = selectedLang;
        
        // Feedback visual antes de enviar
        langBtn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            langBtn.style.transform = '';
            languageForm.submit();
        }, 150);
        
        // Anunciar cambio para lectores de pantalla
        announceToScreenReader(`Idioma cambiado a ${selectedLang === 'es' ? 'Español' : 'English'}`);
    });
}

/* ==================== MENÚ MÓVIL ==================== */
function initMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (!navToggle || !navMenu) return;
    
    // Toggle del menú
    navToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleMenu();
    });
    
    // Cerrar menú al hacer clic en enlaces (excepto acciones móviles)
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            if (!link.closest('.nav-mobile-actions')) {
                closeMenu();
            }
        });
    });
    
    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            closeMenu();
        }
    });
    
    // Cerrar con tecla Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            closeMenu();
            navToggle.focus();
        }
    });
    
    // Funciones auxiliares
    function toggleMenu() {
        const isExpanded = navMenu.classList.toggle('active');
        navToggle.setAttribute('aria-expanded', isExpanded);
        document.body.style.overflow = isExpanded ? 'hidden' : '';
        
        // Anunciar estado para lectores de pantalla
        announceToScreenReader(isExpanded ? 'Menú abierto' : 'Menú cerrado');
        
        // Enfocar primer elemento del menú cuando se abre
        if (isExpanded) {
            const firstLink = navMenu.querySelector('a');
            if (firstLink) {
                setTimeout(() => firstLink.focus(), 100);
            }
        }
    }
    
    function closeMenu() {
        navMenu.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }
    
    // Hacer accesible globalmente
    window.closeMenu = closeMenu;
}

/* ==================== USER DROPDOWN ==================== */
function initUserDropdown() {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    
    if (!userMenuBtn || !userDropdown) return;
    
    // Toggle dropdown
    userMenuBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const isActive = userDropdown.classList.toggle('active');
        userMenuBtn.setAttribute('aria-expanded', isActive);
        userMenuBtn.classList.toggle('active', isActive);
        
        // Anunciar para lectores de pantalla
        announceToScreenReader(isActive ? 'Menú de usuario abierto' : 'Menú de usuario cerrado');
        
        // Enfocar primer elemento cuando se abre
        if (isActive) {
            const firstItem = userDropdown.querySelector('.dropdown-item');
            if (firstItem) {
                setTimeout(() => firstItem.focus(), 100);
            }
        }
    });
    
    // Cerrar al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
            userDropdown.classList.remove('active');
            userMenuBtn.setAttribute('aria-expanded', 'false');
            userMenuBtn.classList.remove('active');
        }
    });
    
    // Cerrar con Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && userDropdown.classList.contains('active')) {
            userDropdown.classList.remove('active');
            userMenuBtn.setAttribute('aria-expanded', 'false');
            userMenuBtn.classList.remove('active');
            userMenuBtn.focus();
        }
    });
}

/* ==================== SMOOTH SCROLL ==================== */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#' && href !== '#!') {
                e.preventDefault();
                
                const target = document.querySelector(href);
                if (target) {
                    // Smooth scroll
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Hacer el elemento enfocable y enfocarlo
                    target.setAttribute('tabindex', '-1');
                    target.focus();
                    
                    // Anunciar navegación
                    const targetText = target.getAttribute('aria-label') || 
                                     target.querySelector('h1, h2, h3')?.textContent || 
                                     'Sección';
                    announceToScreenReader(`Navegado a ${targetText}`);
                }
            }
        });
    });
}

/* ==================== ANIMACIONES ==================== */
function initAnimations() {
    // Intersection Observer para animaciones al scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);
    
    // Observar elementos animables
    document.querySelectorAll('.activity-item, .job-card, .stat-card, .sidebar-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
    
    // Animar barra de progreso
    animateProgressBar();
}

function animateProgressBar() {
    const progressBar = document.querySelector('.progress-fill');
    if (!progressBar) return;
    
    const targetWidth = progressBar.style.width;
    progressBar.style.width = '0%';
    
    setTimeout(() => {
        progressBar.style.width = targetWidth;
        
        // Anunciar progreso para lectores de pantalla
        const percentage = parseInt(targetWidth);
        if (!isNaN(percentage)) {
            setTimeout(() => {
                announceToScreenReader(`Perfil completado al ${percentage} por ciento`);
            }, 600);
        }
    }, 400);
}

/* ==================== LAZY LOADING ==================== */
function initLazyLoading() {
    if (!('IntersectionObserver' in window)) {
        // Fallback para navegadores antiguos
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
        return;
    }
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    
                    // Añadir clase cuando la imagen se carga
                    img.addEventListener('load', () => {
                        img.classList.add('loaded');
                    });
                    
                    imageObserver.unobserve(img);
                }
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

function updateWelcomeMessage() {
    const waitForGreeting = setInterval(() => {
        const greetingEl = document.getElementById('welcome-greeting');

        if (!greetingEl || !window.DASHBOARD_I18N) return;

        clearInterval(waitForGreeting);

        const hour = new Date().getHours();
        let greeting;

        if (hour >= 5 && hour < 12) {
            greeting = window.DASHBOARD_I18N.morning;
        } else if (hour >= 12 && hour < 19) {
            greeting = window.DASHBOARD_I18N.afternoon;
        } else {
            greeting = window.DASHBOARD_I18N.night;
        }

        greetingEl.textContent = greeting;
        console.log('✅ Greeting aplicado:', greeting);
    }, 50);
}


/* ==================== ACCESIBILIDAD ==================== */
function initAccessibility() {
    // Crear región live para anuncios
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('role', 'status');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.id = 'live-region';
    document.body.appendChild(liveRegion);
    
    // Función global para anuncios
    window.announceToScreenReader = function(message) {
        const liveRegion = document.getElementById('live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    };
    
    // Añadir skip link si no existe
    if (!document.querySelector('.skip-link')) {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-link';
        skipLink.textContent = document.documentElement.lang === 'es' ? 
            'Saltar al contenido principal' : 
            'Skip to main content';
        document.body.insertBefore(skipLink, document.body.firstChild);
    }
}

/* ==================== NAVEGACIÓN POR TECLADO ==================== */
function initKeyboardNavigation() {
    // Navegación en dropdowns con flechas
    const dropdowns = document.querySelectorAll('.dropdown-menu, .nav-menu');
    
    dropdowns.forEach(dropdown => {
        const items = Array.from(dropdown.querySelectorAll('a, button'));
        
        dropdown.addEventListener('keydown', function(e) {
            const currentIndex = items.indexOf(document.activeElement);
            
            switch(e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    const nextIndex = (currentIndex + 1) % items.length;
                    items[nextIndex].focus();
                    break;
                    
                case 'ArrowUp':
                    e.preventDefault();
                    const prevIndex = currentIndex - 1 < 0 ? items.length - 1 : currentIndex - 1;
                    items[prevIndex].focus();
                    break;
                    
                case 'Home':
                    e.preventDefault();
                    items[0].focus();
                    break;
                    
                case 'End':
                    e.preventDefault();
                    items[items.length - 1].focus();
                    break;
            }
        });
    });
}

/* ==================== OPTIMIZACIÓN TÁCTIL ==================== */
function initTouchOptimization() {
    // Detectar si es dispositivo táctil
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    if (isTouchDevice) {
        document.body.classList.add('touch-device');
        
        // Aumentar áreas de toque para elementos pequeños
        const smallButtons = document.querySelectorAll('.icon-button, .nav-toggle, .lang-btn');
        smallButtons.forEach(btn => {
            if (btn.offsetWidth < 44 || btn.offsetHeight < 44) {
                btn.style.minWidth = '44px';
                btn.style.minHeight = '44px';
            }
        });
    }
}

/* ==================== RESPONSIVE CHECKS ==================== */
function initResponsiveChecks() {
    function checkResponsive() {
        const dropdown = document.getElementById('userDropdown');
        if (!dropdown) return;
        
        const isMobile = window.innerWidth < 768;
        
        // Ajustar altura máxima del dropdown en móvil
        if (isMobile) {
            dropdown.style.maxHeight = '80vh';
        } else {
            dropdown.style.maxHeight = '';
        }
        
        // Actualizar espaciado del container
        const containers = document.querySelectorAll('.container');
        containers.forEach(container => {
            if (window.innerWidth < 768) {
                container.style.padding = '0 1rem';
            } else {
                container.style.padding = '';
            }
        });
    }
    
    // Check inicial
    checkResponsive();
    
    // Check en resize con debounce
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(checkResponsive, 250);
    });
}

/* ==================== MANEJO DE ERRORES ==================== */
window.addEventListener('error', function(e) {
    console.error('Error capturado:', e.error);
    
    // Anunciar error para usuarios
    if (window.announceToScreenReader) {
        const lang = document.documentElement.lang || 'es';
        const errorMsg = lang === 'es' ? 
            'Ha ocurrido un error. Por favor, recarga la página.' : 
            'An error occurred. Please reload the page.';
        announceToScreenReader(errorMsg);
    }
});

/* ==================== UTILIDADES ==================== */

// Debounce para optimizar eventos
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

// Throttle para scroll events
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

// Detectar preferencia de movimiento reducido
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (prefersReducedMotion) {
    document.documentElement.style.setProperty('--transition', '0.01ms');
    document.documentElement.style.setProperty('--transition-fast', '0.01ms');
    document.documentElement.style.setProperty('--transition-slow', '0.01ms');
}

console.log('📱 Dashboard optimizado para todos los dispositivos');
console.log('♿ Accesibilidad mejorada con ARIA y navegación por teclado');
console.log('🌍 Soporte completo de internacionalización (i18n)');