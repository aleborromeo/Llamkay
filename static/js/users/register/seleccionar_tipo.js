// =============================================
// SELECCIONAR TIPO - LLAMKAY.PE MEJORADO
// Cambio de idioma + UX + Accesibilidad
// =============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ seleccionar_tipo.js iniciado');

    // ==================== ELEMENTOS ====================
    const optionCards = document.querySelectorAll('.option-card-new');
    const langButtons = document.querySelectorAll('.lang-btn');
    const form = document.getElementById('selectorForm');

    // ==================== TRADUCCIONES ====================
    const translations = {
        es: {
            step: 'Paso 1 de 5',
            title: '¿Cómo deseas registrarte?',
            subtitle: 'Selecciona tu rol en la plataforma para continuar',
            trabajador_title: 'Buscar trabajo',
            trabajador_desc: 'Encuentra oportunidades laborales en tu zona',
            dual_title: 'Buscar y publicar trabajos',
            dual_desc: 'Trabaja y contrata según tus necesidades',
            empleador_title: 'Publicar trabajos',
            empleador_desc: 'Contrata profesionales verificados',
            empresa_title: 'Soy una empresa',
            empresa_desc: 'Registro corporativo con RUC',
            popular: 'Popular',
            recommended: 'Recomendado',
            corporate: 'Corporativo',
            have_account: '¿Ya tienes una cuenta?',
            login: 'Inicia sesión aquí',
            back: 'Volver al inicio',
            info_title: '¿No estás seguro?',
            info_desc: 'Puedes cambiar tu tipo de cuenta después del registro desde tu perfil.'
        },
        en: {
            step: 'Step 1 of 5',
            title: 'How do you want to register?',
            subtitle: 'Select your role on the platform to continue',
            trabajador_title: 'Find work',
            trabajador_desc: 'Find job opportunities in your area',
            dual_title: 'Find and post jobs',
            dual_desc: 'Work and hire according to your needs',
            empleador_title: 'Post jobs',
            empleador_desc: 'Hire verified professionals',
            empresa_title: 'I am a company',
            empresa_desc: 'Corporate registration with RUC',
            popular: 'Popular',
            recommended: 'Recommended',
            corporate: 'Corporate',
            have_account: 'Already have an account?',
            login: 'Log in here',
            back: 'Back to home',
            info_title: 'Not sure?',
            info_desc: 'You can change your account type after registration from your profile.'
        }
    };

    // ==================== CAMBIO DE IDIOMA ====================
    let currentLang = 'es';

    function changeLanguage(lang) {
        currentLang = lang;
        
        // Actualizar botones activos
        langButtons.forEach(btn => {
            if (btn.dataset.lang === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Actualizar textos
        const t = translations[lang];

        // Header
        const stepBadge = document.querySelector('.step-badge');
        const title = document.querySelector('.selector-title');
        const subtitle = document.querySelector('.selector-subtitle');
        
        if (stepBadge) stepBadge.textContent = t.step;
        if (title) title.textContent = t.title;
        if (subtitle) subtitle.textContent = t.subtitle;

        // Cards
        const cards = document.querySelectorAll('.option-card-new');
        cards.forEach((card, index) => {
            const h3 = card.querySelector('h3');
            const p = card.querySelector('p');
            
            if (index === 0) { // Trabajador
                if (h3) h3.textContent = t.trabajador_title;
                if (p) p.textContent = t.trabajador_desc;
            } else if (index === 1) { // Dual
                if (h3) h3.textContent = t.dual_title;
                if (p) p.textContent = t.dual_desc;
            } else if (index === 2) { // Empleador
                if (h3) h3.textContent = t.empleador_title;
                if (p) p.textContent = t.empleador_desc;
            } else if (index === 3) { // Empresa
                if (h3) h3.textContent = t.empresa_title;
                if (p) p.textContent = t.empresa_desc;
            }
        });

        // Badges
        const popularBadge = document.querySelector('.popular-badge');
        const featuredCorner = document.querySelector('.featured-corner span');
        const corporateBadge = document.querySelector('.corporate-badge');
        
        if (popularBadge) popularBadge.textContent = t.popular;
        if (featuredCorner) featuredCorner.textContent = t.recommended;
        if (corporateBadge) corporateBadge.textContent = t.corporate;

        // Footer
        const footerP = document.querySelector('.selector-footer-new p');
        const loginLink = document.querySelector('.selector-footer-new p a');
        const backLink = document.querySelector('.back-link-new');
        
        if (footerP) {
            footerP.innerHTML = `${t.have_account} <a href="${loginLink?.href || '#'}">${t.login}</a>`;
        }
        if (backLink) {
            backLink.innerHTML = `← ${t.back}`;
        }

        // Info banner
        const infoTitle = document.querySelector('.info-text-new strong');
        const infoDesc = document.querySelector('.info-text-new span');
        
        if (infoTitle) infoTitle.textContent = t.info_title;
        if (infoDesc) infoDesc.textContent = t.info_desc;

        // Guardar preferencia
        localStorage.setItem('llamkay_lang', lang);
    }

    // Event listeners para cambio de idioma
    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            changeLanguage(btn.dataset.lang);
        });
    });

    // Cargar idioma guardado
    const savedLang = localStorage.getItem('llamkay_lang');
    if (savedLang && savedLang !== 'es') {
        changeLanguage(savedLang);
    }

    // ==================== INTERACCIONES DE CARDS ====================
    if (optionCards.length) {
        optionCards.forEach(card => {
            // Click feedback
            card.addEventListener('click', (e) => {
                optionCards.forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');

                // Microinteracción
                card.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    card.style.transform = '';
                }, 100);

                // Ripple
                if (e.clientX && e.clientY) {
                    createRipple(e, card);
                }
            });

            // Teclado
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    card.click();
                }
            });
        });
    }

    // ==================== RIPPLE EFFECT ====================
    function createRipple(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);

        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${event.clientX - rect.left - size / 2}px`;
        ripple.style.top = `${event.clientY - rect.top - size / 2}px`;
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(7, 115, 75, 0.3)';
        ripple.style.transform = 'scale(0)';
        ripple.style.animation = 'ripple-anim 0.6s ease-out';
        ripple.style.pointerEvents = 'none';

        element.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    }

    // ==================== NAVEGACIÓN CON TECLADO ====================
    let currentIndex = -1;

    document.addEventListener('keydown', (e) => {
        if (!['ArrowRight', 'ArrowDown', 'ArrowLeft', 'ArrowUp'].includes(e.key)) return;
        
        e.preventDefault();

        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            currentIndex = (currentIndex + 1) % optionCards.length;
        } else {
            currentIndex = currentIndex <= 0 ? optionCards.length - 1 : currentIndex - 1;
        }

        optionCards[currentIndex]?.focus();
        optionCards[currentIndex]?.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    });

    // ==================== ANIMACIÓN DE CARGA ====================
    optionCards.forEach((card, i) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, i * 100);
    });

    console.log('🎉 seleccionar_tipo.js listo');
});

// ==================== ESTILOS DINÁMICOS ====================
const style = document.createElement('style');
style.textContent = `
@keyframes ripple-anim {
    to {
        transform: scale(2);
        opacity: 0;
    }
}

.option-card-new.selected {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(7, 115, 75, 0.1);
}
`;
document.head.appendChild(style);