// =============================================
// DASHBOARD JAVASCRIPT - LLAMKAY.PE
// Aplicando Principios de Nielsen y Responsividad
// =============================================

/**
 * PRINCIPIOS APLICADOS:
 * ✓ NIELSEN #1 - Visibilidad del estado del sistema
 * ✓ NIELSEN #3 - Control y libertad del usuario
 * ✓ NIELSEN #5 - Prevención de errores
 * ✓ NIELSEN #8 - Estética y diseño minimalista
 * ✓ NIELSEN #9 - Ayuda a reconocer y recuperarse de errores
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
    
    console.log('✅ Dashboard cargado con principios de usabilidad aplicados! 🚀');
});

/**
 * ═══════════════════════════════════════════════════════════
 * MENÚ MÓVIL RESPONSIVO
 * NIELSEN #1: Visibilidad del estado (abierto/cerrado)
 * NIELSEN #3: Control del usuario (abrir/cerrar fácilmente)
 * ═══════════════════════════════════════════════════════════
 */
function initMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (!navToggle || !navMenu) return;
    
    // Toggle del menú
    navToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleMenu();
    });
    
    // Cerrar menú al hacer click en un enlace (excepto mobile actions)
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (!link.closest('.nav-mobile-actions')) {
                closeMenu();
            }
        });
    });
    
    // Cerrar menú al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            if (navMenu.classList.contains('active')) {
                closeMenu();
            }
        }
    });
    
    // Cerrar con tecla ESC - NIELSEN #3: Control del usuario
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            closeMenu();
            navToggle.focus(); // Devolver foco para accesibilidad
        }
    });
    
    // NIELSEN #5: Prevención de errores - No cerrar si se está scrolleando
    let isScrolling = false;
    navMenu.addEventListener('scroll', () => {
        isScrolling = true;
        setTimeout(() => isScrolling = false, 100);
    });
    
    function toggleMenu() {
        const isExpanded = navMenu.classList.toggle('active');
        
        // NIELSEN #1: Visibilidad del estado - Actualizar ARIA
        navToggle.setAttribute('aria-expanded', isExpanded);
        
        // Animar hamburger
        animateHamburger(isExpanded);
        
        // Prevenir scroll del body cuando menú está abierto
        document.body.style.overflow = isExpanded ? 'hidden' : '';
        
        // NIELSEN #1: Feedback visual en consola (solo dev)
        console.log('Menú móvil:', isExpanded ? 'Abierto' : 'Cerrado');
    }
    
    function closeMenu() {
        if (isScrolling) return; // No cerrar si está scrolleando
        
        navMenu.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
        animateHamburger(false);
    }
    
    function animateHamburger(isOpen) {
        const spans = navToggle.querySelectorAll('span');
        if (isOpen) {
            spans[0].style.transform = 'rotate(45deg) translate(8px, 8px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
        } else {
            spans.forEach(span => {
                span.style.transform = '';
                span.style.opacity = '';
            });
        }
    }
    
    // Hacer closeMenu accesible globalmente
    window.closeMenu = closeMenu;
}

/**
 * ═══════════════════════════════════════════════════════════
 * USER DROPDOWN
 * NIELSEN #1: Visibilidad del estado
 * NIELSEN #3: Control del usuario
 * ═══════════════════════════════════════════════════════════
 */
function initUserDropdown() {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    
    if (!userMenuBtn || !userDropdown) return;
    
    // Toggle dropdown
    userMenuBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const isActive = userDropdown.classList.toggle('active');
        userMenuBtn.classList.toggle('active');
        
        // NIELSEN #1: Actualizar ARIA para accesibilidad
        userMenuBtn.setAttribute('aria-expanded', isActive);
        
        console.log('User menu:', isActive ? 'Abierto' : 'Cerrado');
    });
    
    // Cerrar dropdown cuando se hace click fuera
    document.addEventListener('click', function(e) {
        if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
            closeDropdown();
        }
    });
    
    // NIELSEN #3: Cerrar con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeDropdown();
            
            // También cerrar menú móvil si está abierto
            const navMenu = document.querySelector('.nav-menu');
            if (navMenu && navMenu.classList.contains('active')) {
                window.closeMenu();
            }
        }
    });
    
    // Cerrar dropdown al hacer click en un enlace
    const dropdownLinks = userDropdown.querySelectorAll('a');
    dropdownLinks.forEach(link => {
        link.addEventListener('click', () => {
            setTimeout(closeDropdown, 100); // Pequeño delay para UX
        });
    });
    
    function closeDropdown() {
        userDropdown.classList.remove('active');
        userMenuBtn.classList.remove('active');
        userMenuBtn.setAttribute('aria-expanded', 'false');
    }
}

/**
 * ═══════════════════════════════════════════════════════════
 * SMOOTH SCROLL
 * NIELSEN #8: Estética y experiencia fluida
 * ═══════════════════════════════════════════════════════════
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    // NIELSEN #1: Feedback visual del scroll
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Actualizar foco para accesibilidad
                    target.setAttribute('tabindex', '-1');
                    target.focus();
                }
            }
        });
    });
}

/**
 * ═══════════════════════════════════════════════════════════
 * ANIMACIONES Y FEEDBACK VISUAL
 * NIELSEN #1: Visibilidad del estado
 * NIELSEN #8: Estética minimalista
 * ═══════════════════════════════════════════════════════════
 */
function initAnimations() {
    // Animación de botones de aplicación
    const applyButtons = document.querySelectorAll('.job-card .btn-small.btn-primary');
    
    applyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // NIELSEN #1: Feedback táctil visual
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
    
    // Intersection Observer para animaciones al scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // NIELSEN #8: Animaciones sutiles y elegantes
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    entry.target.style.transition = 'all 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observar elementos para animación
    document.querySelectorAll('.activity-item, .job-card, .stat-card').forEach(item => {
        observer.observe(item);
    });
    
    // Animación de barra de progreso
    animateProgressBar();
}

/**
 * NIELSEN #1: Visibilidad del estado - Barra de progreso animada
 */
function animateProgressBar() {
    const progressBar = document.querySelector('.progress-fill');
    if (progressBar) {
        const targetWidth = progressBar.style.width;
        progressBar.style.width = '0%';
        
        // NIELSEN #1: Feedback visual del progreso
        setTimeout(() => {
            progressBar.style.transition = 'width 1s ease';
            progressBar.style.width = targetWidth;
        }, 500);
    }
}

/**
 * ═══════════════════════════════════════════════════════════
 * LAZY LOADING DE IMÁGENES
 * RESPONSIVIDAD: Optimización de rendimiento
 * ═══════════════════════════════════════════════════════════
 */
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        // Cargar imagen con fade-in
                        img.style.opacity = '0';
                        img.src = img.dataset.src;
                        
                        img.onload = () => {
                            img.style.transition = 'opacity 0.3s ease';
                            img.style.opacity = '1';
                            img.removeAttribute('data-src');
                        };
                        
                        imageObserver.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback para navegadores sin IntersectionObserver
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
    }
}

/**
 * ═══════════════════════════════════════════════════════════
 * WELCOME MESSAGE BASADO EN HORA
 * NIELSEN #2: Concordancia entre sistema y mundo real
 * ═══════════════════════════════════════════════════════════
 */
function updateWelcomeMessage() {
    const hour = new Date().getHours();
    const welcomeTitle = document.querySelector('.welcome-content h1');
    
    if (welcomeTitle) {
        let greeting = '¡Bienvenido de vuelta';
        
        // NIELSEN #2: Lenguaje natural según hora del día
        if (hour >= 5 && hour < 12) {
            greeting = '¡Buenos días';
        } else if (hour >= 12 && hour < 19) {
            greeting = '¡Buenas tardes';
        } else {
            greeting = '¡Buenas noches';
        }
        
        const nameSpan = welcomeTitle.querySelector('.text-highlight');
        if (nameSpan) {
            const userName = nameSpan.textContent;
            welcomeTitle.innerHTML = `${greeting}, <span class="text-highlight">${userName}</span>!`;
        }
    }
}

/**
 * ═══════════════════════════════════════════════════════════
 * ACCESIBILIDAD
 * NIELSEN #10: Ayuda y documentación
 * ═══════════════════════════════════════════════════════════
 */
function initAccessibility() {
    // Mejorar navegación por teclado
    const focusableElements = document.querySelectorAll(
        'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    // Trap focus en dropdown cuando está abierto
    const userDropdown = document.getElementById('userDropdown');
    if (userDropdown) {
        userDropdown.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                const focusable = this.querySelectorAll('a, button');
                const first = focusable[0];
                const last = focusable[focusable.length - 1];
                
                if (e.shiftKey && document.activeElement === first) {
                    e.preventDefault();
                    last.focus();
                } else if (!e.shiftKey && document.activeElement === last) {
                    e.preventDefault();
                    first.focus();
                }
            }
        });
    }
    
    // Anunciar cambios de estado para lectores de pantalla
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('role', 'status');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    document.body.appendChild(liveRegion);
    
    window.announceToScreenReader = function(message) {
        liveRegion.textContent = message;
        setTimeout(() => liveRegion.textContent = '', 1000);
    };
}

/**
 * ═══════════════════════════════════════════════════════════
 * RESPONSIVE CHECKS
 * RESPONSIVIDAD: Adaptación según dispositivo
 * ═══════════════════════════════════════════════════════════
 */
function initResponsiveChecks() {
    // Detectar tamaño de pantalla y ajustar comportamiento
    const checkViewport = () => {
        const width = window.innerWidth;
        const isMobile = width < 768;
        const isTablet = width >= 768 && width < 1024;
        const isDesktop = width >= 1024;
        
        // Ajustar dropdown según dispositivo
        const userDropdown = document.getElementById('userDropdown');
        if (userDropdown) {
            if (isMobile) {
                userDropdown.style.maxHeight = '80vh';
            } else {
                userDropdown.style.maxHeight = '';
            }
        }
        
        // Log para desarrollo
        console.log('Viewport:', { isMobile, isTablet, isDesktop, width });
    };
    
    // Check inicial
    checkViewport();
    
    // Check en resize con debounce
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(checkViewport, 250);
    });
    
    // Detectar orientación en móviles
    if (window.matchMedia) {
        const orientationChange = (e) => {
            console.log('Orientación:', e.matches ? 'Portrait' : 'Landscape');
            // Cerrar menús al cambiar orientación
            if (window.closeMenu) window.closeMenu();
        };
        
        const portraitQuery = window.matchMedia('(orientation: portrait)');
        portraitQuery.addListener(orientationChange);
    }
}

/**
 * ═══════════════════════════════════════════════════════════
 * UTILIDADES ADICIONALES
 * ═══════════════════════════════════════════════════════════
 */

// NIELSEN #9: Manejo de errores en imágenes
document.addEventListener('error', function(e) {
    if (e.target.tagName === 'IMG') {
        console.warn('Error cargando imagen:', e.target.src);
        // Imagen placeholder
        e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23f0f0f0" width="100" height="100"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" fill="%23999" dy=".3em"%3E?%3C/text%3E%3C/svg%3E';
        e.target.alt = 'Imagen no disponible';
    }
}, true);

// Detectar si hay soporte táctil
const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
if (isTouchDevice) {
    document.body.classList.add('touch-device');
    console.log('Dispositivo táctil detectado');
}

// NIELSEN #5: Prevención de errores - Confirmar acciones destructivas
document.querySelectorAll('a[href*="logout"], a[href*="delete"]').forEach(link => {
    link.addEventListener('click', function(e) {
        const action = this.href.includes('logout') ? 'cerrar sesión' : 'eliminar';
        if (!confirm(`¿Estás seguro que deseas ${action}?`)) {
            e.preventDefault();
        }
    });
});

// Performance monitoring (solo en desarrollo)
if (window.performance && console.table) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = window.performance.timing;
            const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
            const connectTime = perfData.responseEnd - perfData.requestStart;
            const renderTime = perfData.domComplete - perfData.domLoading;
            
            console.table({
                'Carga Total': `${pageLoadTime}ms`,
                'Conexión': `${connectTime}ms`,
                'Renderizado': `${renderTime}ms`
            });
        }, 0);
    });
}

/**
 * ═══════════════════════════════════════════════════════════
 * EXPORT PARA TESTING (opcional)
 * ═══════════════════════════════════════════════════════════
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initMobileMenu,
        initUserDropdown,
        updateWelcomeMessage,
        initAccessibility
    };
}