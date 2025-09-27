class DropdownManager {
    constructor() {
        this.activeDropdown = null;
        this.overlay = document.getElementById('dropdownOverlay');
        this.init();
    }

    init() {
        // Notificaciones
        document.getElementById('notificationsBtn').addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleDropdown('notificationsDropdown');
        });

        // Mensajes
        document.getElementById('messagesBtn').addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleDropdown('messagesDropdown');
        });

        // Usuario
        document.getElementById('userMenuBtn').addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleDropdown('userDropdown');
        });

        // Overlay para cerrar dropdowns
        this.overlay.addEventListener('click', () => {
            this.closeAllDropdowns();
        });

        // Cerrar al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dropdown') && !e.target.closest('.icon-button') && !e.target.closest('.user-menu')) {
                this.closeAllDropdowns();
            }
        });

        // NO manejar clics dentro del dropdown - dejar que los enlaces funcionen naturalmente
        // Solo prevenir el cierre del dropdown cuando se hace clic en áreas que no son enlaces
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            dropdown.addEventListener('click', (e) => {
                // Si es un enlace, dejar que funcione normalmente y cerrar el dropdown
                if (e.target.closest('a')) {
                    this.closeAllDropdowns();
                    return; // No prevenir nada, dejar que el enlace funcione
                }
                // Solo prevenir propagación si NO es un enlace
                e.stopPropagation();
            });
        });
    }

    toggleDropdown(dropdownId) {
        const dropdown = document.getElementById(dropdownId);
                    
        if (this.activeDropdown === dropdownId) {
            this.closeAllDropdowns();
        } else {
            this.closeAllDropdowns();
            this.openDropdown(dropdownId);
        }
    }

    openDropdown(dropdownId) {
        const dropdown = document.getElementById(dropdownId);
        dropdown.classList.add('show');
        this.overlay.classList.add('active');
        this.activeDropdown = dropdownId;

        // Añadir clase active al botón de usuario si corresponde
        if (dropdownId === 'userDropdown') {
            document.getElementById('userMenuBtn').parentElement.classList.add('active');
        }
    }

    closeAllDropdowns() {
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            dropdown.classList.remove('show');
        });
        this.overlay.classList.remove('active');
        this.activeDropdown = null;

        // Remover clase active del botón de usuario
        const userMenuContainer = document.getElementById('userMenuBtn').parentElement;
        if (userMenuContainer) {
            userMenuContainer.classList.remove('active');
        }
    }
}

// Inicializar el gestor de dropdowns
document.addEventListener('DOMContentLoaded', () => {
    new DropdownManager();
});

// Animación de notificaciones (opcional)
function simulateNotification() {
    const badge = document.querySelector('.notification-badge');
    if (badge) {
        const currentCount = parseInt(badge.textContent) || 0;
        badge.textContent = currentCount + 1;
        
        // Animación de pulso
        badge.style.animation = 'none';
        setTimeout(() => {
            badge.style.animation = 'pulse 0.5s ease-in-out';
        }, 10);
    }
}

// CSS para animación de pulso
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);