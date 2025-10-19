// ===== DASHBOARD LLAMKAY - Gestor de Dropdowns y Carrusel =====

/**
 * Gestor de Dropdowns
 */
class DropdownManager {
    constructor() {
        this.activeDropdown = null;
        this.overlay = document.getElementById('dropdownOverlay');
        this.init();
    }

    init() {
        console.log('🔧 Inicializando DropdownManager...');
        
        // Notificaciones
        const notificationsBtn = document.getElementById('notificationsBtn');
        if (notificationsBtn) {
            console.log('✅ Botón de notificaciones encontrado');
            notificationsBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                console.log('🔔 Click en notificaciones');
                this.toggleDropdown('notificationsDropdown');
            });
        }

        // Mensajes
        const messagesBtn = document.getElementById('messagesBtn');
        if (messagesBtn) {
            console.log('✅ Botón de mensajes encontrado');
            messagesBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                console.log('💬 Click en mensajes');
                this.toggleDropdown('messagesDropdown');
            });
        }

        // Usuario
        const userMenuBtn = document.getElementById('userMenuBtn');
        if (userMenuBtn) {
            console.log('✅ Menú de usuario encontrado');
            userMenuBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                console.log('👤 Click en menú de usuario');
                this.toggleDropdown('userDropdown');
            });
        }

        // Overlay para cerrar dropdowns
        if (this.overlay) {
            console.log('✅ Overlay encontrado');
            this.overlay.addEventListener('click', () => {
                console.log('🖱️ Click en overlay - cerrando dropdowns');
                this.closeAllDropdowns();
            });
        }

        // ✅ CORRECCIÓN CRÍTICA: NO interferir con los enlaces
        // Los enlaces deben funcionar naturalmente sin prevenir nada
        
        // Cerrar al hacer clic FUERA (pero NO dentro de dropdowns)
        document.addEventListener('click', (e) => {
            // Si el click es en un botón que abre dropdown, NO hacer nada
            if (e.target.closest('#notificationsBtn') || 
                e.target.closest('#messagesBtn') || 
                e.target.closest('#userMenuBtn')) {
                return;
            }
            
            // Si el click es DENTRO de un dropdown visible, NO hacer nada
            if (e.target.closest('.dropdown.show')) {
                return;
            }
            
            // En cualquier otro lugar, cerrar todos los dropdowns
            this.closeAllDropdowns();
        }, false); // ← false = fase de burbuja (después de que los enlaces se procesen)

        // Cerrar con tecla ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllDropdowns();
            }
        });

        console.log('✅ Event listeners configurados');
    }

    toggleDropdown(dropdownId) {
        const dropdown = document.getElementById(dropdownId);
        if (!dropdown) {
            console.error(`❌ Dropdown no encontrado: ${dropdownId}`);
            return;
        }

        console.log(`🔄 Toggle dropdown: ${dropdownId}`);

        if (this.activeDropdown === dropdownId) {
            console.log(`🔥 Cerrando dropdown activo: ${dropdownId}`);
            this.closeAllDropdowns();
        } else {
            console.log(`🔤 Abriendo dropdown: ${dropdownId}`);
            this.closeAllDropdowns();
            this.openDropdown(dropdownId);
        }
    }

    openDropdown(dropdownId) {
        const dropdown = document.getElementById(dropdownId);
        if (!dropdown) {
            console.error(`❌ No se puede abrir - Dropdown no encontrado: ${dropdownId}`);
            return;
        }

        console.log(`📂 Abriendo dropdown: ${dropdownId}`);
        
        dropdown.classList.add('show');
        
        if (this.overlay) {
            this.overlay.classList.add('active');
        }
        
        this.activeDropdown = dropdownId;

        // Añadir clase active al contenedor padre
        const parentItem = dropdown.closest('.navbar-item');
        if (parentItem) {
            parentItem.classList.add('active');
        }

        // Añadir clase active al botón de usuario si corresponde
        if (dropdownId === 'userDropdown') {
            const userMenuBtn = document.getElementById('userMenuBtn');
            if (userMenuBtn) {
                userMenuBtn.classList.add('active');
            }
        }
    }

    closeAllDropdowns() {
        console.log('🔒 Cerrando todos los dropdowns');
        
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            dropdown.classList.remove('show');
        });
        
        if (this.overlay) {
            this.overlay.classList.remove('active');
        }
        
        // Remover clase active de todos los contenedores
        document.querySelectorAll('.navbar-item').forEach(item => {
            item.classList.remove('active');
        });

        // Remover clase active del botón de usuario
        const userMenuBtn = document.getElementById('userMenuBtn');
        if (userMenuBtn) {
            userMenuBtn.classList.remove('active');
        }
        
        this.activeDropdown = null;
    }
}

/**
 * Gestor del Carrusel
 */
class CarouselManager {
    constructor() {
        this.currentIndex = 0;
        this.images = document.querySelectorAll('.carousel-image');
        this.prevBtn = document.querySelector('.carousel-btn.prev');
        this.nextBtn = document.querySelector('.carousel-btn.next');
        this.autoPlayInterval = null;
        this.autoPlayDelay = 5000;
        
        if (this.images.length > 0) {
            console.log(`🎠 Carrusel inicializado con ${this.images.length} imágenes`);
            this.init();
        } else {
            console.warn('⚠️ No se encontraron imágenes para el carrusel');
        }
    }

    init() {
        // Botones de navegación
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.prev();
            });
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.next();
            });
        }

        // Buscar botones con data-action también
        document.querySelectorAll('[data-action="prev-slide"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.prev();
            });
        });

        document.querySelectorAll('[data-action="next-slide"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.next();
            });
        });

        // Auto-play
        this.startAutoPlay();

        // Pausar auto-play al hacer hover
        const carousel = document.querySelector('.carousel');
        if (carousel) {
            carousel.addEventListener('mouseenter', () => this.stopAutoPlay());
            carousel.addEventListener('mouseleave', () => this.startAutoPlay());
        }

        // Soporte táctil
        this.initTouchSupport();

        // Pausar cuando la pestaña no está visible
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopAutoPlay();
            } else {
                this.startAutoPlay();
            }
        });
    }

    showImage(index) {
        this.images.forEach((img, i) => {
            img.classList.remove('active');
            if (i === index) {
                img.classList.add('active');
            }
        });
        this.currentIndex = index;
    }

    next() {
        let newIndex = (this.currentIndex + 1) % this.images.length;
        this.showImage(newIndex);
    }

    prev() {
        let newIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
        this.showImage(newIndex);
    }

    startAutoPlay() {
        this.stopAutoPlay();
        this.autoPlayInterval = setInterval(() => this.next(), this.autoPlayDelay);
    }

    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }

    initTouchSupport() {
        const carousel = document.querySelector('.carousel');
        if (!carousel) return;

        let touchStartX = 0;
        let touchEndX = 0;

        carousel.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        carousel.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe(touchStartX, touchEndX);
        }, { passive: true });
    }

    handleSwipe(startX, endX) {
        const swipeThreshold = 50;
        if (endX < startX - swipeThreshold) {
            this.next();
        }
        if (endX > startX + swipeThreshold) {
            this.prev();
        }
    }
}

/**
 * Inicializar Dashboard
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎯 Dashboard JS iniciado');
    console.log('📍 Ubicación:', window.location.pathname);
    
    // Verificar elementos críticos
    const elementos = {
        overlay: document.getElementById('dropdownOverlay'),
        notificationsBtn: document.getElementById('notificationsBtn'),
        messagesBtn: document.getElementById('messagesBtn'),
        userMenuBtn: document.getElementById('userMenuBtn'),
        notificationsDropdown: document.getElementById('notificationsDropdown'),
        messagesDropdown: document.getElementById('messagesDropdown'),
        userDropdown: document.getElementById('userDropdown')
    };
    
    console.log('📋 Verificando elementos críticos:');
    Object.entries(elementos).forEach(([key, value]) => {
        console.log(`  ${key}: ${value ? '✅ OK' : '❌ FALTA'}`);
    });
    
    // Inicializar gestor de dropdowns
    const dropdownManager = new DropdownManager();
    
    // Inicializar carrusel
    const carouselManager = new CarouselManager();
    
    console.log('✅ Dashboard completamente listo');
    
    // Hacer disponibles globalmente para debugging
    window.dropdownManager = dropdownManager;
    window.carouselManager = carouselManager;
});