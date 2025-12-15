// =============================================
// MIS CALIFICACIONES - INTERACTIVIDAD
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ mis_calificaciones.js cargado');

    // ========== SISTEMA DE TABS ==========
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.dataset.tab;

            // Remover active de todos
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Activar el seleccionado
            this.classList.add('active');
            document.getElementById(`tab-${targetTab}`).classList.add('active');

            // Guardar en localStorage (comentado para compatibilidad con Claude.ai)
            // localStorage.setItem('activeTab', targetTab);

            // Log para debug
            console.log(`Tab cambiado a: ${targetTab}`);
        });
    });

    // Restaurar tab activo desde localStorage (comentado)
    // const savedTab = localStorage.getItem('activeTab');
    // if (savedTab) {
    //     const savedButton = document.querySelector(`[data-tab="${savedTab}"]`);
    //     if (savedButton) {
    //         savedButton.click();
    //     }
    // }

    // ========== ANIMACIÓN AL HACER SCROLL ==========
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
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

    // Observar todas las cards
    document.querySelectorAll('.rating-card').forEach(card => {
        observer.observe(card);
    });

    // ========== HOVER EFFECTS EN CARDS ==========
    document.querySelectorAll('.rating-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // ========== COPIAR COMENTARIO ==========
    document.querySelectorAll('.rating-comment').forEach(comment => {
        comment.style.cursor = 'pointer';
        comment.title = 'Click para copiar comentario';

        comment.addEventListener('click', function() {
            const text = this.querySelector('p').textContent;
            
            navigator.clipboard.writeText(text).then(() => {
                // Mostrar feedback visual
                const originalBg = this.style.background;
                this.style.background = 'linear-gradient(135deg, #d1fae5, #a7f3d0)';
                
                setTimeout(() => {
                    this.style.background = originalBg;
                }, 500);

                console.log('✅ Comentario copiado al portapapeles');
            }).catch(err => {
                console.error('❌ Error al copiar:', err);
            });
        });
    });

    // ========== CONTADOR DE CALIFICACIONES ==========
    updateRatingCounts();

    function updateRatingCounts() {
        const recibidasCount = document.querySelectorAll('#tab-recibidas .rating-card').length;
        const dadasCount = document.querySelectorAll('#tab-dadas .rating-card').length;

        console.log(`📊 Recibidas: ${recibidasCount} | Dadas: ${dadasCount}`);
        
        // Opcional: Actualizar badges de conteo si existen en el HTML
        const recibidasBadge = document.querySelector('[data-tab="recibidas"] .badge');
        const dadasBadge = document.querySelector('[data-tab="dadas"] .badge');
        
        if (recibidasBadge) recibidasBadge.textContent = recibidasCount;
        if (dadasBadge) dadasBadge.textContent = dadasCount;
    }

    // ========== ANIMACIÓN DE ENTRADA INICIAL ==========
    setTimeout(() => {
        document.querySelectorAll('.rating-card').forEach((card, index) => {
            setTimeout(() => {
                card.style.animation = 'slideInUp 0.5s ease forwards';
            }, index * 100);
        });
    }, 200);
});

