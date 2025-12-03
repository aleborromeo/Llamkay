// =============================================
// DASHBOARD JAVASCRIPT - LLAMKAY.PE
// (Control y Libertad, Visibilidad del Estado)
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== USER MENU DROPDOWN (Control y Libertad) ====================
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    
    // Toggle user menu dropdown
    if (userMenuBtn && userDropdown) {
        userMenuBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Toggle dropdown
            userDropdown.classList.toggle('active');
            userMenuBtn.classList.toggle('active');
            
            console.log('User menu toggled');
        });
    }
    
    // Cerrar dropdown cuando se hace click fuera (Control y Libertad)
    document.addEventListener('click', function(e) {
        if (userDropdown && userMenuBtn && 
            !userMenuBtn.contains(e.target) && 
            !userDropdown.contains(e.target)) {
            userDropdown.classList.remove('active');
            userMenuBtn.classList.remove('active');
        }
    });
    
    // Cerrar dropdown con tecla ESC (Control y Libertad)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && userDropdown && userMenuBtn) {
            userDropdown.classList.remove('active');
            userMenuBtn.classList.remove('active');
        }
    });
    
    // ==================== ANIMACIÓN DE PROGRESO (Visibilidad del Estado) ====================
    const progressBar = document.querySelector('.progress-fill');
    if (progressBar) {
        const targetWidth = progressBar.style.width;
        progressBar.style.width = '0%';
        
        // Animación al cargar para mostrar el progreso
        setTimeout(() => {
            progressBar.style.transition = 'width 1s ease';
            progressBar.style.width = targetWidth;
        }, 500);
    }
    
    // ==================== ANIMACIÓN DE INTERSECCIÓN (Estética/Flexibilidad) ====================
    // Animación de aparición para las tarjetas y actividades
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
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
    
    // Observar elementos clave para animar la carga (Estética Minimalista)
    document.querySelectorAll('.activity-item, .job-card, .stat-card, .sidebar-card').forEach(item => {
        observer.observe(item);
    });

    // ... (El resto de funciones como formatRelativeTime y updateWelcomeMessage se mantienen) ...
    
    console.log('✅ Dashboard loaded successfully! 🚀');
});