/**
 * =============================================
 * PERFIL - LLAMKAY.PE
 * JavaScript para funcionalidad del perfil
 * =============================================
 */

document.addEventListener('DOMContentLoaded', function() {
    // ========== ELEMENTOS DEL DOM ==========
    const editProfileModal = document.getElementById('editProfileModal');
    const btnEditarPerfil = document.querySelector('[data-action="editar-perfil"]');
    const btnCerrarModal = document.querySelector('[data-action="cerrar-modal"]');
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const formEditarPerfil = document.getElementById('form-editar-perfil');

    // ========== SISTEMA DE TABS ==========
    function initTabs() {
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const targetTab = this.getAttribute('data-tab');
                
                // Remover clase active de todos los tabs
                tabs.forEach(t => t.classList.remove('active'));
                
                // Remover clase active de todos los contenidos
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Agregar clase active al tab clickeado
                this.classList.add('active');
                
                // Mostrar el contenido correspondiente
                const targetContent = document.getElementById(targetTab);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
                
                // Guardar tab activo en localStorage
                localStorage.setItem('activeProfileTab', targetTab);
            });
        });

        // Restaurar tab activo si existe
        const savedTab = localStorage.getItem('activeProfileTab');
        if (savedTab) {
            const tabToActivate = document.querySelector(`[data-tab="${savedTab}"]`);
            if (tabToActivate) {
                tabToActivate.click();
            }
        }
    }

    // ========== MODAL DE EDICIÓN ==========
    function openModal() {
        if (editProfileModal) {
            editProfileModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            
            // Animación de entrada
            setTimeout(() => {
                editProfileModal.style.opacity = '1';
            }, 10);
        }
    }

    function closeModal() {
        if (editProfileModal) {
            editProfileModal.style.opacity = '0';
            
            setTimeout(() => {
                editProfileModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }, 300);
        }
    }

    // Event listeners para abrir/cerrar modal
    if (btnEditarPerfil) {
        btnEditarPerfil.addEventListener('click', openModal);
    }

    if (btnCerrarModal) {
        btnCerrarModal.addEventListener('click', closeModal);
    }

    // Cerrar modal al hacer click fuera
    if (editProfileModal) {
        editProfileModal.addEventListener('click', function(e) {
            if (e.target === editProfileModal) {
                closeModal();
            }
        });
    }

    // Cerrar modal con tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && editProfileModal && editProfileModal.style.display === 'flex') {
            closeModal();
        }
    });

    // ========== VALIDACIÓN DEL FORMULARIO ==========
    if (formEditarPerfil) {
        formEditarPerfil.addEventListener('submit', function(e) {
            // Validaciones básicas
            const telefono = document.getElementById('telefono');
            const tarifaHora = document.getElementById('tarifa_hora');
            
            let isValid = true;
            let errorMessage = '';

            // Validar teléfono (9 dígitos)
            if (telefono && telefono.value) {
                const telefonoRegex = /^9\d{8}$/;
                if (!telefonoRegex.test(telefono.value)) {
                    isValid = false;
                    errorMessage = 'El teléfono debe tener 9 dígitos y comenzar con 9';
                    telefono.style.borderColor = 'var(--color-danger)';
                } else {
                    telefono.style.borderColor = '';
                }
            }

            // Validar tarifa por hora (debe ser positiva)
            if (tarifaHora && tarifaHora.value) {
                if (parseFloat(tarifaHora.value) < 0) {
                    isValid = false;
                    errorMessage = 'La tarifa por hora debe ser un valor positivo';
                    tarifaHora.style.borderColor = 'var(--color-danger)';
                } else {
                    tarifaHora.style.borderColor = '';
                }
            }

            if (!isValid) {
                e.preventDefault();
                showNotification(errorMessage, 'error');
            }
        });
    }

    // ========== PREVIEW DE IMAGEN ==========
    const inputFoto = document.getElementById('foto');
    if (inputFoto) {
        inputFoto.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tipo de archivo
                const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
                if (!allowedTypes.includes(file.type)) {
                    showNotification('Solo se permiten imágenes (JPG, PNG, GIF)', 'error');
                    inputFoto.value = '';
                    return;
                }

                // Validar tamaño (máximo 5MB)
                const maxSize = 5 * 1024 * 1024; // 5MB
                if (file.size > maxSize) {
                    showNotification('La imagen no debe superar los 5MB', 'error');
                    inputFoto.value = '';
                    return;
                }

                // Mostrar preview (opcional)
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Aquí podrías mostrar un preview de la imagen
                    showNotification('Imagen seleccionada correctamente', 'success');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ========== ANIMACIONES DE SCROLL ==========
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observar cards
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        });
    }

    // ========== SISTEMA DE NOTIFICACIONES ==========
    function showNotification(message, type = 'info') {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">
                    ${getNotificationIcon(type)}
                </span>
                <span class="notification-message">${message}</span>
            </div>
        `;

        // Estilos inline para la notificación
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            zIndex: '10000',
            padding: '1rem 1.5rem',
            borderRadius: '12px',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
            backgroundColor: getNotificationColor(type),
            color: 'white',
            fontWeight: '600',
            opacity: '0',
            transform: 'translateX(100px)',
            transition: 'all 0.3s ease'
        });

        document.body.appendChild(notification);

        // Animar entrada
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 10);

        // Remover después de 3 segundos
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100px)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    function getNotificationIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        return icons[type] || icons.info;
    }

    function getNotificationColor(type) {
        const colors = {
            success: '#10b981',
            error: '#dc2626',
            warning: '#f59e0b',
            info: '#3b82f6'
        };
        return colors[type] || colors.info;
    }

    // ========== TOOLTIPS ==========
    function initTooltips() {
        const elements = document.querySelectorAll('[data-tooltip]');
        
        elements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                const tooltipText = this.getAttribute('data-tooltip');
                const tooltip = document.createElement('div');
                tooltip.className = 'tooltip';
                tooltip.textContent = tooltipText;
                
                Object.assign(tooltip.style, {
                    position: 'absolute',
                    bottom: 'calc(100% + 10px)',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    padding: '0.5rem 1rem',
                    background: '#1a1a1a',
                    color: 'white',
                    borderRadius: '8px',
                    fontSize: '0.875rem',
                    whiteSpace: 'nowrap',
                    zIndex: '1000',
                    pointerEvents: 'none'
                });
                
                this.style.position = 'relative';
                this.appendChild(tooltip);
            });
            
            element.addEventListener('mouseleave', function() {
                const tooltip = this.querySelector('.tooltip');
                if (tooltip) {
                    tooltip.remove();
                }
            });
        });
    }

    // ========== CONFIRMACIÓN ANTES DE SALIR ==========
    let formChanged = false;

    if (formEditarPerfil) {
        const inputs = formEditarPerfil.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                formChanged = true;
            });
        });

        // Advertir si hay cambios no guardados
        btnCerrarModal?.addEventListener('click', function(e) {
            if (formChanged) {
                if (!confirm('Tienes cambios sin guardar. ¿Estás seguro de cerrar?')) {
                    e.preventDefault();
                    e.stopPropagation();
                    return;
                }
            }
        });
    }

    // ========== SMOOTH SCROLL ==========
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

    // ========== INICIALIZACIÓN ==========
    initTabs();
    initScrollAnimations();
    initTooltips();

    // Log de inicialización
    console.log('✓ Perfil inicializado correctamente');
});

// ========== FUNCIONES GLOBALES ==========

// Función para actualizar el avatar en tiempo real (si se usa)
function updateAvatarPreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const avatars = document.querySelectorAll('.profile-photo, .dropdown-avatar img');
        avatars.forEach(avatar => {
            if (avatar.tagName === 'IMG') {
                avatar.src = e.target.result;
            }
        });
    };
    reader.readAsDataURL(file);
}

// Función para formatear números
function formatNumber(num) {
    return new Intl.NumberFormat('es-PE').format(num);
}

// Función para formatear moneda
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-PE', {
        style: 'currency',
        currency: 'PEN'
    }).format(amount);
}