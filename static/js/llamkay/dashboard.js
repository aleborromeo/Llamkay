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
 * ✓ NIELSEN #10 - Accesibilidad
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
    initLanguageSwitcher(); // ✅ AÑADIDO

    console.log('✅ Dashboard cargado con principios de usabilidad aplicados! 🚀');
});

/* =========================================================
   LANGUAGE SWITCHER (i18n)
   NO rompe nada existente
   ========================================================= */
function initLanguageSwitcher() {
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.lang-btn');
        if (!btn) return;

        const form = document.getElementById('language-form');
        const input = document.getElementById('language-input');
        if (!form || !input) return;

        input.value = btn.dataset.lang;
        form.submit();
    });
}

/* ==================== MENÚ MÓVIL ==================== */
function initMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (!navToggle || !navMenu) return;

    navToggle.addEventListener('click', function (e) {
        e.stopPropagation();
        toggleMenu();
    });

    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (!link.closest('.nav-mobile-actions')) closeMenu();
        });
    });

    document.addEventListener('click', function (e) {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            closeMenu();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            closeMenu();
            navToggle.focus();
        }
    });

    function toggleMenu() {
        const expanded = navMenu.classList.toggle('active');
        navToggle.setAttribute('aria-expanded', expanded);
        document.body.style.overflow = expanded ? 'hidden' : '';
    }

    function closeMenu() {
        navMenu.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }

    window.closeMenu = closeMenu;
}

/* ==================== USER DROPDOWN ==================== */
function initUserDropdown() {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    if (!userMenuBtn || !userDropdown) return;

    userMenuBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        const isActive = userDropdown.classList.toggle('active');
        userMenuBtn.setAttribute('aria-expanded', isActive);
    });

    document.addEventListener('click', function (e) {
        if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
            userDropdown.classList.remove('active');
            userMenuBtn.setAttribute('aria-expanded', 'false');
        }
    });
}

/* ==================== SMOOTH SCROLL ==================== */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                    target.setAttribute('tabindex', '-1');
                    target.focus();
                }
            }
        });
    });
}

/* ==================== ANIMACIONES ==================== */
function initAnimations() {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.activity-item, .job-card, .stat-card')
        .forEach(el => observer.observe(el));

    animateProgressBar();
}

function animateProgressBar() {
    const progressBar = document.querySelector('.progress-fill');
    if (!progressBar) return;
    const width = progressBar.style.width;
    progressBar.style.width = '0%';
    setTimeout(() => progressBar.style.width = width, 400);
}

/* ==================== LAZY LOAD ==================== */
function initLazyLoading() {
    if (!('IntersectionObserver' in window)) return;
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.target.dataset.src) {
                entry.target.src = entry.target.dataset.src;
                entry.target.removeAttribute('data-src');
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
}

/* ==================== WELCOME ==================== */
function updateWelcomeMessage() {
    const title = document.querySelector('.welcome-content h1');
    if (!title) return;

    const hour = new Date().getHours();
    let greeting = '¡Bienvenido de vuelta';

    if (hour < 12) greeting = '¡Buenos días';
    else if (hour < 19) greeting = '¡Buenas tardes';
    else greeting = '¡Buenas noches';

    const name = title.querySelector('.text-highlight')?.textContent || '';
    title.innerHTML = `${greeting}, <span class="text-highlight">${name}</span>!`;
}

/* ==================== ACCESIBILIDAD ==================== */
function initAccessibility() {
    const live = document.createElement('div');
    live.setAttribute('role', 'status');
    live.setAttribute('aria-live', 'polite');
    live.className = 'sr-only';
    document.body.appendChild(live);

    window.announceToScreenReader = msg => {
        live.textContent = msg;
        setTimeout(() => live.textContent = '', 1000);
    };
}

/* ==================== RESPONSIVE ==================== */
function initResponsiveChecks() {
    const check = () => {
        const dropdown = document.getElementById('userDropdown');
        if (!dropdown) return;
        dropdown.style.maxHeight = window.innerWidth < 768 ? '80vh' : '';
    };
    check();
    window.addEventListener('resize', check);
}
