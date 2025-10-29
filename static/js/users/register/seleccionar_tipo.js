// =============================================
// SELECCIONAR TIPO - LLAMKAY.PE (JAVASCRIPT)
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('🎯 Seleccionar Tipo JS iniciado');

    // ==================== ELEMENTOS ====================
    const optionCards = document.querySelectorAll('.option-card');
    const selectorForm = document.getElementById('selectorForm');
    const tipoUsuarioInput = document.getElementById('tipo_usuario_input');

    // ==================== MANEJO DE CLICKS ====================
    optionCards.forEach(card => {
        card.addEventListener('click', function(e) {
            const tipoUsuario = this.getAttribute('data-tipo');
            console.log('📌 Tipo seleccionado:', tipoUsuario);
            
            // Establecer el valor en el input hidden
            if (tipoUsuarioInput) {
                tipoUsuarioInput.value = tipoUsuario;
            }
            
            // Añadir clase de selección
            optionCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            
            // Animación de click
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 100);

            // Crear efecto ripple
            createRipple(e, this);
            
            // Enviar el formulario después de un breve delay
            setTimeout(() => {
                console.log('📤 Enviando formulario con tipo:', tipoUsuario);
                if (selectorForm) {
                    selectorForm.submit();
                }
            }, 300);
        });
        
        // Soporte para Enter y Espacio
        card.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });

    // ==================== HOVER EFFECTS ====================
    optionCards.forEach(card => {
        // Efecto hover con mouse tracking
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `
                perspective(1000px) 
                rotateX(${rotateX}deg) 
                rotateY(${rotateY}deg) 
                translateY(-5px)
                scale(1.02)
            `;
        });

        card.addEventListener('mouseleave', function() {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0) scale(1)';
        });
    });

    // ==================== EFECTO RIPPLE ====================
    function createRipple(event, element) {
        // Validar que el evento tiene las propiedades necesarias
        if (!event.clientX || !event.clientY) {
            console.log('⚠️ Evento sin coordenadas, saltando ripple');
            return;
        }
        
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            border-radius: 50%;
            background: rgba(7, 115, 75, 0.3);
            top: ${y}px;
            left: ${x}px;
            pointer-events: none;
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            z-index: 10;
        `;

        element.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    // ==================== NAVEGACIÓN CON TECLADO ====================
    let currentIndex = -1;

    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
            e.preventDefault();
            currentIndex = (currentIndex + 1) % optionCards.length;
            focusCard(currentIndex);
        } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
            e.preventDefault();
            currentIndex = currentIndex <= 0 ? optionCards.length - 1 : currentIndex - 1;
            focusCard(currentIndex);
        } else if (e.key === 'Enter' && currentIndex >= 0) {
            e.preventDefault();
            optionCards[currentIndex].click();
        }
    });

    function focusCard(index) {
        optionCards.forEach((card, i) => {
            if (i === index) {
                card.style.outline = '3px solid var(--color-primary)';
                card.style.outlineOffset = '2px';
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                card.style.outline = 'none';
            }
        });
    }

    // ==================== ANIMACIONES CSS ====================
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple-animation {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }

        .option-card.selected {
            border-color: var(--color-primary) !important;
            box-shadow: 0 0 0 4px rgba(7, 115, 75, 0.1) !important;
        }

        .option-card:focus-visible {
            outline: 3px solid var(--color-primary);
            outline-offset: 2px;
        }

        @media (prefers-reduced-motion: reduce) {
            .option-card,
            .option-icon,
            * {
                animation: none !important;
                transition: none !important;
            }
        }
    `;
    document.head.appendChild(style);

    // ==================== TOOLTIPS INFORMATIVOS ====================
    const tooltips = {
        'trabajador': 'Ideal para buscar trabajos temporales o freelance',
        'trabajador_empleador': 'La opción más flexible y popular entre usuarios',
        'empleador': 'Perfecto si solo necesitas contratar',
        'empresa': 'Para negocios con RUC y necesidades corporativas'
    };

    optionCards.forEach(card => {
        const tipoUsuario = card.getAttribute('data-tipo');
        if (tipoUsuario && tooltips[tipoUsuario]) {
            card.setAttribute('title', tooltips[tipoUsuario]);
        }
    });

    // ==================== ANALYTICS (opcional) ====================
    optionCards.forEach(card => {
        card.addEventListener('click', function() {
            const optionName = this.querySelector('h3')?.textContent || 'Unknown';
            console.log(`📊 Opción seleccionada: ${optionName}`);
        });
    });

    console.log('✅ Seleccionar Tipo JS completamente cargado');
    console.log(`📋 ${optionCards.length} opciones disponibles`);
});