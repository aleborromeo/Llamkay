// =============================================
// DASHBOARD JAVASCRIPT - LLAMKAY.PE
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== USER MENU DROPDOWN ====================
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
    
    // Cerrar dropdown cuando se hace click fuera
    document.addEventListener('click', function(e) {
        if (userDropdown && userMenuBtn && 
            !userMenuBtn.contains(e.target) && 
            !userDropdown.contains(e.target)) {
            userDropdown.classList.remove('active');
            userMenuBtn.classList.remove('active');
        }
    });
    
    // Cerrar dropdown con tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && userDropdown && userMenuBtn) {
            userDropdown.classList.remove('active');
            userMenuBtn.classList.remove('active');
        }
    });
    
    // Los links dentro del dropdown navegarán normalmente
    if (userDropdown) {
        const dropdownLinks = userDropdown.querySelectorAll('.dropdown-item');
        dropdownLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Permitir navegación normal de los links
                console.log('Navegando a:', this.href);
            });
        });
    }
    
    // ==================== SMOOTH SCROLL ====================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ==================== APPLY BUTTON ANIMATION ====================
    const applyButtons = document.querySelectorAll('.job-card .btn-small.btn-primary');
    
    applyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Animación de click
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
    
    // ==================== NOTIFICATION SYSTEM ====================
    function showNotification(message, type = 'info') {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Estilos inline
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#dc2626' : '#3b82f6'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
            z-index: 9999;
            animation: slideInRight 0.3s ease;
            max-width: 300px;
        `;
        
        document.body.appendChild(notification);
        
        // Remover después de 3 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    // Agregar animaciones CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // ==================== ACTIVITY ITEMS ANIMATION ====================
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
    
    // Observar elementos de actividad
    document.querySelectorAll('.activity-item, .job-card, .stat-card').forEach(item => {
        observer.observe(item);
    });
    
    // ==================== PROGRESS BAR ANIMATION ====================
    const progressBar = document.querySelector('.progress-fill');
    if (progressBar) {
        const targetWidth = progressBar.style.width;
        progressBar.style.width = '0%';
        
        setTimeout(() => {
            progressBar.style.transition = 'width 1s ease';
            progressBar.style.width = targetWidth;
        }, 500);
    }
    
    // ==================== RESPONSIVE MENU ====================
    const menuToggle = document.querySelector('.menu-toggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            document.querySelector('.nav-menu').classList.toggle('active');
        });
    }
    
    // ==================== LAZY LOADING DE IMÁGENES ====================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // ==================== WELCOME MESSAGE BASED ON TIME ====================
    function updateWelcomeMessage() {
        const hour = new Date().getHours();
        const welcomeTitle = document.querySelector('.welcome-content h1');
        
        if (welcomeTitle) {
            let greeting = '¡Bienvenido de vuelta';
            
            if (hour >= 5 && hour < 12) {
                greeting = '¡Buenos días';
            } else if (hour >= 12 && hour < 19) {
                greeting = '¡Buenas tardes';
            } else {
                greeting = '¡Buenas noches';
            }
            
            // Mantener el nombre del usuario
            const nameSpan = welcomeTitle.querySelector('.text-highlight');
            if (nameSpan) {
                const userName = nameSpan.textContent;
                welcomeTitle.innerHTML = `${greeting}, <span class="text-highlight">${userName}</span>!`;
            }
        }
    }
    
    updateWelcomeMessage();
    
    // ==================== FORMATO DE FECHAS RELATIVAS ====================
    function formatRelativeTime(date) {
        const now = new Date();
        const diff = now - date;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (seconds < 60) return 'Hace un momento';
        if (minutes < 60) return `Hace ${minutes} ${minutes === 1 ? 'minuto' : 'minutos'}`;
        if (hours < 24) return `Hace ${hours} ${hours === 1 ? 'hora' : 'horas'}`;
        if (days < 7) return `Hace ${days} ${days === 1 ? 'día' : 'días'}`;
        
        return date.toLocaleDateString('es-PE');
    }
    
    // Actualizar timestamps relativos
    document.querySelectorAll('[data-timestamp]').forEach(element => {
        const timestamp = parseInt(element.dataset.timestamp);
        const date = new Date(timestamp);
        element.textContent = formatRelativeTime(date);
    });
    
    // ==================== CONSOLE LOG ====================
    console.log('✅ Dashboard loaded successfully! 🚀');
});