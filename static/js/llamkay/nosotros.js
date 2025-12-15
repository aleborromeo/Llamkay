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
    'use strict';

    // ==================== I18N ====================
    const langForm = document.getElementById('language-form');
    const langInput = document.getElementById('language-input');

    if (langForm && langInput) {
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.lang-btn');
            if (!btn) return;

            e.preventDefault();
            const lang = btn.dataset.lang;

            if (!lang) return;

            langInput.value = lang;
            langForm.submit();
        });
    }

    // ==================== MOBILE MENU ====================
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');

            const expanded = navMenu.classList.contains('active');
            navToggle.setAttribute('aria-expanded', expanded);

            const spans = navToggle.querySelectorAll('span');
            if (expanded) {
                spans[0].style.transform = 'rotate(45deg) translate(6px, 6px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(6px, -6px)';
            } else {
                spans.forEach(s => {
                    s.style.transform = '';
                    s.style.opacity = '';
                });
            }
        });

        // Cerrar al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!navMenu.contains(e.target) && !navToggle.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');

                navToggle.querySelectorAll('span').forEach(s => {
                    s.style.transform = '';
                    s.style.opacity = '';
                });
            }
        });

        // Cerrar con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
                navToggle.focus();
            }
        });
    }

    // ==================== SCROLL TO TOP ====================
    const scrollBtn = document.getElementById('scrollToTop');

    if (scrollBtn) {
        window.addEventListener('scroll', () => {
            scrollBtn.style.opacity = window.scrollY > 300 ? '1' : '0';
            scrollBtn.style.visibility = window.scrollY > 300 ? 'visible' : 'hidden';
        });

        scrollBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ==================== AOS ====================
    if (window.AOS) {
        AOS.init({ duration: 800, once: true });
    }

    console.log('✅ Idioma, menú y UX funcionando correctamente');
});
