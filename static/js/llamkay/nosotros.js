/**
 * ═══════════════════════════════════════════════════════════════════════════
 * LLAMKAY.PE - PÁGINA SOBRE NOSOTROS
 * JavaScript aplicando Principios de Usabilidad de Nielsen
 * Menú Sandwich ELEGANTE solo en móvil (como index.html)
 * 
 * PRINCIPIOS APLICADOS:
 * ✓ NIELSEN #1 - Visibilidad del estado del sistema
 * ✓ NIELSEN #3 - Control y libertad para el usuario
 * ✓ NIELSEN #5 - Prevención de errores
 * ✓ NIELSEN #7 - Flexibilidad y eficiencia de uso
 * ✓ RESPONSIVIDAD - Menú sandwich solo en móvil
 * ═══════════════════════════════════════════════════════════════════════════
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initScrollToTop();
    initSmoothScroll();
    initAnimationsOnScroll();
    initAccessibility();
});

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * MENÚ MÓVIL RESPONSIVO (IGUAL QUE INDEX.HTML)
 * 
 * PRINCIPIOS:
 * ✓ NIELSEN #1 - Visibilidad: El menú muestra su estado (abierto/cerrado)
 * ✓ NIELSEN #3 - Control: Usuario puede abrir/cerrar fácilmente
 * ✓ Responsividad: Solo activo en móvil (< 768px)
 * ═══════════════════════════════════════════════════════════════════════════
 */
function initMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (!navToggle || !navMenu) return;
    
    // Toggle del menú
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
        
        // NIELSEN #1: Visibilidad del estado - feedback visual
        console.log('Menú móvil toggled:', isExpanded);
    });
    
    // Cerrar menú al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
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
    // NIELSEN #3: Control y libertad del usuario
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
            navToggle.focus(); // Devolver focus al botón
            
            const spans = navToggle.querySelectorAll('span');
            spans.forEach(span => {
                span.style.transform = '';
                span.style.opacity = '';
            });
        }
    });
}

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * BOTÓN SCROLL TO TOP
 * 
 * PRINCIPIOS:
 * ✓ NIELSEN #3 - Control y libertad: Navegación rápida
 * ✓ NIELSEN #7 - Flexibilidad: Atajo para usuarios frecuentes
 * ✓ NIELSEN #1 - Visibilidad: Aparece solo cuando es útil
 * ═══════════════════════════════════════════════════════════════════════════
 */
function initScrollToTop() {
    const scrollBtn = document.getElementById('scrollToTop');
    
    if (!scrollBtn) return;
    
    // Mostrar/ocultar botón según scroll
    window.addEventListener('scroll', () => {
        // NIELSEN #1: Visibilidad del estado
        if (window.scrollY > 300) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    });
    
    // NIELSEN #3: Control - Click para volver arriba
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * SMOOTH SCROLL
 * 
 * PRINCIPIOS:
 * ✓ NIELSEN #1 - Visibilidad: Usuario ve el movimiento
 * ✓ GESTALT - Continuidad: Transición fluida entre secciones
 * ═══════════════════════════════════════════════════════════════════════════
 */
function initSmoothScroll() {
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    // Cerrar menú móvil si está abierto
                    const navMenu = document.querySelector('.nav-menu');
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
}

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * ANIMACIONES AL HACER SCROLL
 * 
 * PRINCIPIOS:
 * ✓ NIELSEN #1 - Visibilidad: Feedback visual progresivo
 * ✓ GESTALT - Continuidad: Elementos aparecen fluidamente
 * ✓ Responsividad: Animaciones adaptadas al dispositivo
 * ═══════════════════════════════════════════════════════════════════════════
 */
function initAnimationsOnScroll() {
    // Verificar si el usuario prefiere reducir movimiento
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (prefersReducedMotion) return;
    
    // Elementos con atributos data-aos
    const animatedElements = document.querySelectorAll('[data-aos]');
    
    if (animatedElements.length === 0) return;
    
    // Opciones del Intersection Observer
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    // Callback del observer
    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.getAttribute('data-aos-delay') || 0;
                
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, delay);
                
                observer.unobserve(entry.target);
            }
        });
    };
    
    // Crear observer
    const observer = new IntersectionObserver(observerCallback, observerOptions);
    
    // Observar cada elemento
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        observer.observe(element);
    });
}

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * MEJORAS DE ACCESIBILIDAD
 * 
 * PRINCIPIOS:
 * ✓ NIELSEN #10 - Ayuda y documentación: Tooltips informativos
 * ✓ NIELSEN #5 - Prevención de errores: Validación de enlaces
 * ✓ Accesibilidad: WCAG 2.1 compliance
 * ═══════════════════════════════════════════════════════════════════════════
 */
function initAccessibility() {
    // Añadir títulos descriptivos a enlaces sin texto
    const links = document.querySelectorAll('a');
    
    links.forEach(link => {
        if (!link.hasAttribute('title') && !link.textContent.trim()) {
            const href = link.getAttribute('href');
            if (href) {
                link.setAttribute('title', `Ir a ${href}`);
            }
        }
        
        // Enlaces externos: abrir en nueva pestaña con seguridad
        if (link.hasAttribute('href')) {
            const href = link.getAttribute('href');
            
            if (href.startsWith('http') && !href.includes(window.location.hostname)) {
                link.setAttribute('target', '_blank');
                link.setAttribute('rel', 'noopener noreferrer');
                
                if (!link.textContent.includes('↗')) {
                    link.setAttribute('aria-label', `${link.textContent} (se abre en nueva ventana)`);
                }
            }
        }
    });
    
    // Manejar errores de carga de imágenes
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (!img.hasAttribute('alt')) {
            console.warn('Imagen sin alt text:', img.src);
            img.setAttribute('alt', '');
        }
        
        img.addEventListener('error', function() {
            this.style.display = 'none';
            console.error('Error al cargar imagen:', this.src);
        });
    });
}

// Logs para debugging
console.log('✅ Nosotros page loaded successfully! 🚀');
console.log('📱 Viewport:', window.innerWidth + 'x' + window.innerHeight);