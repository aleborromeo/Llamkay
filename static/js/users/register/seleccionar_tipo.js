// =============================================
// SELECCIONAR TIPO - LLAMKAY.PE
// JS ACCESIBLE + UX + SIN ROMPER FORMULARIO
// =============================================

document.addEventListener('DOMContentLoaded', () => {

    // ==================== ELEMENTOS ====================
    const optionCards = document.querySelectorAll('.option-card');

    if (!optionCards.length) return;

    // ==================== CLICK FEEDBACK ====================
    optionCards.forEach(card => {

        // CLICK
        card.addEventListener('click', (e) => {
            // Feedback visual inmediato (Nielsen)
            optionCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');

            // Microinteracción segura (no bloquea submit)
            card.classList.add('is-clicked');
            setTimeout(() => card.classList.remove('is-clicked'), 150);

            // Ripple solo si hay coordenadas (mouse/touch)
            if (e.clientX && e.clientY) {
                createRipple(e, card);
            }
        });

        // ==================== TECLADO ====================
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                card.click(); // Accesibilidad total
            }
        });
    });

    // ==================== RIPPLE EFFECT ====================
    function createRipple(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);

        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${event.clientX - rect.left - size / 2}px`;
        ripple.style.top = `${event.clientY - rect.top - size / 2}px`;
        ripple.classList.add('ripple');

        element.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }

    // ==================== NAVEGACIÓN CON FLECHAS ====================
    let currentIndex = -1;

    document.addEventListener('keydown', (e) => {
        const keys = ['ArrowRight', 'ArrowDown', 'ArrowLeft', 'ArrowUp'];
        if (!keys.includes(e.key)) return;

        e.preventDefault();

        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            currentIndex = (currentIndex + 1) % optionCards.length;
        } else {
            currentIndex = currentIndex <= 0
                ? optionCards.length - 1
                : currentIndex - 1;
        }

        focusCard(currentIndex);
    });

    function focusCard(index) {
        optionCards.forEach((card, i) => {
            if (i === index) {
                card.focus();
                card.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }
        });
    }

    // ==================== REDUCED MOTION ====================
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        optionCards.forEach(card => {
            card.style.transition = 'none';
        });
    }

});

// =============================================
// CSS DINÁMICO NECESARIO PARA JS
// =============================================
const style = document.createElement('style');
style.textContent = `
.option-card {
    position: relative;
    overflow: hidden;
}

.option-card.selected {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 4px rgba(7, 115, 75, 0.15);
}

.option-card.is-clicked {
    transform: scale(0.97);
}

.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(7, 115, 75, 0.25);
    transform: scale(0);
    animation: ripple-animation 0.6s ease-out;
    pointer-events: none;
    z-index: 0;
}

@keyframes ripple-animation {
    to {
        transform: scale(2);
        opacity: 0;
    }
}
`;
document.head.appendChild(style);
