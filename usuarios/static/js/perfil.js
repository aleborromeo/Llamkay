// static/js/perfil.js - Versión corregida sin conflicto de tabs
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Perfil.js cargado');
    
    // Inicializar componentes del perfil (sin tabs, eso lo maneja tabs.js)
    initializeProfile();
    
    // Esperar a que tabs.js se cargue
    setTimeout(() => {
        initializeProfileSpecificFeatures();
    }, 100);
});

/**
 * Inicializar funcionalidades generales del perfil
 */
function initializeProfile() {
    console.log('👤 Inicializando perfil...');
    
    // Agregar event listeners para botones
    initializeButtons();
    
    // Agregar efectos de hover mejorados
    initializeHoverEffects();
    
    // Inicializar previsualización de foto
    initializePhotoPreview();
    
    // Inicializar tooltips
    initializeTooltips();
}

/**
 * Inicializar características específicas del perfil después de que tabs.js esté listo
 */
function initializeProfileSpecificFeatures() {
    console.log('🔧 Inicializando características específicas del perfil...');
    
    // Verificar que el sistema de tabs esté funcionando
    const activeTab = document.querySelector('.tab.active');
    if (!activeTab) {
        // Si no hay tab activo, activar el general
        const generalTab = document.querySelector('.tab[data-tab="general"]');
        if (generalTab) {
            generalTab.click();
        }
    }
}

/**
 * Inicializar botones del perfil
 */
function initializeButtons() {
    console.log('🔘 Inicializando botones...');
    
    const editButton = document.querySelector('.profile-actions .btn-primary');
        if (editButton) {
            editButton.addEventListener('click', function(e) {
                e.preventDefault();
                openEditProfileModal();
            });
        }

    
    // Botones de compartir
    const shareButtons = document.querySelectorAll('.btn-secondary');
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const buttonText = this.textContent;
            
            if (buttonText.includes('WhatsApp')) {
                shareOnWhatsApp();
            } else if (buttonText.includes('Referencias')) {
                showReferences();
            }
        });
    });
}

/**
 * Abrir modal de edición de perfil
 */
function openEditProfileModal() {
    console.log('✏️ Abriendo modal de edición...');
    
    const modal = document.getElementById('editProfileModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevenir scroll del body
        
        // Agregar event listener para cerrar con ESC
        document.addEventListener('keydown', handleModalKeydown);
        
        // Event listener para cerrar clickeando fuera del modal
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeEditProfileModal();
            }
        });
    } else {
        console.error('❌ No se encontró el modal de edición');
    }
}

/**
 * Cerrar modal de edición de perfil
 */
function closeEditProfileModal() {
    console.log('❌ Cerrando modal de edición...');
    
    const modal = document.getElementById('editProfileModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restaurar scroll del body
        
        // Remover event listeners
        document.removeEventListener('keydown', handleModalKeydown);
    }
}

/**
 * Manejar teclas del modal
 */
function handleModalKeydown(e) {
    if (e.key === 'Escape') {
        closeEditProfileModal();
    }
}

/**
 * Compartir en WhatsApp
 */
function shareOnWhatsApp() {
    console.log('📱 Compartiendo en WhatsApp...');
    
    const userName = document.querySelector('.profile-info h1')?.textContent || 'Perfil';
    const message = `¡Conoce mi perfil profesional en LLamkay.pe! ${userName} - ${window.location.href}`;
    const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(message)}`;
    
    window.open(whatsappUrl, '_blank');
}

/**
 * Mostrar referencias
 */
function showReferences() {
    console.log('📋 Mostrando referencias...');
    
    // Cambiar a la pestaña de experiencia que contiene las calificaciones
    if (window.showTab) {
        window.showTab('experience');
    }
    
    // Scroll hacia las calificaciones si existen
    setTimeout(() => {
        const calificaciones = document.querySelector('#experience .calificaciones');
        if (calificaciones) {
            calificaciones.scrollIntoView({ behavior: 'smooth' });
        }
    }, 300);
}

/**
 * Inicializar previsualización de foto
 */
function initializePhotoPreview() {
    console.log('📸 Inicializando previsualización de foto...');
    
    const fotoInput = document.getElementById('foto');
    if (fotoInput) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tipo de archivo
                if (!file.type.startsWith('image/')) {
                    alert('Por favor selecciona un archivo de imagen válido.');
                    return;
                }
                
                // Validar tamaño (máximo 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('La imagen es demasiado grande. Por favor selecciona una imagen menor a 5MB.');
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    const profilePhoto = document.querySelector('.profile-photo');
                    const initialsSpan = document.querySelector('.profile-avatar .initials');
                    
                    if (profilePhoto) {
                        profilePhoto.src = e.target.result;
                        profilePhoto.style.display = 'block';
                        if (initialsSpan) {
                            initialsSpan.style.display = 'none';
                        }
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

/**
 * Inicializar efectos de hover mejorados
 */
function initializeHoverEffects() {
    console.log('✨ Inicializando efectos de hover...');
    
    // Efectos para cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 12px 40px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 8px 32px rgba(0,0,0,0.1)';
        });
    });
    
    // Efectos para stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(stat => {
        stat.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
            this.style.transform = 'scale(1.05)';
            this.style.borderColor = '#07734B';
            this.style.background = 'linear-gradient(135deg, #fff7ed, #fef3e2)';
        });
        
        stat.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.borderColor = '#DEF9C4';
            this.style.background = '#fef7ed';
        });
    });
    
    // Efectos para badges
    const badges = document.querySelectorAll('.profile-badge');
    badges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
            this.style.transform = 'scale(1.1)';
            this.style.boxShadow = '0 4px 12px rgba(7, 115, 75, 0.3)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = 'none';
        });
    });
}

/**
 * Inicializar tooltips
 */
function initializeTooltips() {
    console.log('💬 Inicializando tooltips...');
    
    // Agregar tooltips a elementos con título
    const elementsWithTitle = document.querySelectorAll('[title]');
    elementsWithTitle.forEach(element => {
        element.addEventListener('mouseenter', function() {
            console.log(`💡 Tooltip: ${this.getAttribute('title')}`);
        });
    });
    
    // Tooltip personalizado para estadísticas
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach((stat, index) => {
        const labels = ['trabajos totales', 'trabajos activos', 'completados', 'estrellas promedio', 'satisfacción', 'ingresos mensuales'];
        stat.setAttribute('title', `${stat.textContent} ${labels[index] || 'estadística'}`);
    });
}

/**
 * Manejar envío del formulario de edición
 */
function handleEditFormSubmit() {
    const form = document.getElementById('form-editar-perfil');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('📤 Enviando formulario de edición...');
            
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            // Mostrar estado de carga
            submitButton.textContent = 'Guardando...';
            submitButton.disabled = true;
            
            // Simular envío (reemplazar con lógica real)
            const formData = new FormData(form);
            
            // Aquí harías la petición AJAX real
            fetch(form.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    console.log('✅ Perfil actualizado correctamente');
                    closeEditProfileModal();
                    
                    // Mostrar mensaje de éxito
                    showSuccessMessage('Perfil actualizado correctamente');
                    
                    // Actualizar la página después de un breve delay
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                } else {
                    throw new Error(data.message || 'Error al actualizar perfil');
                }
            })
            .catch(error => {
                console.error('❌ Error al actualizar perfil:', error);
                showErrorMessage('Error al actualizar el perfil: ' + error.message);
            })
            .finally(() => {
                // Restaurar botón
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            });
        });
    }
}

/**
 * Mostrar mensaje de éxito
 */
function showSuccessMessage(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success';
    alert.textContent = message;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #d4edda;
        color: #155724;
        padding: 12px 20px;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 3000);
}

/**
 * Mostrar mensaje de error
 */
function showErrorMessage(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-error';
    alert.textContent = message;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f8d7da;
        color: #721c24;
        padding: 12px 20px;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Inicializar el manejo del formulario cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        handleEditFormSubmit();
    }, 500);
});

// Funciones globales para mantener compatibilidad
window.openEditProfileModal = openEditProfileModal;
window.closeEditProfileModal = closeEditProfileModal;
window.cerrarModalEdicion = closeEditProfileModal; // Alias para compatibilidad

// Agregar estilos CSS para el modal y animaciones
const modalStyles = `
    .edit-profile-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        backdrop-filter: blur(5px);
    }
    
    .edit-profile-modal form {
        background: white;
        padding: 30px;
        border-radius: 15px;
        max-width: 500px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        animation: modalSlideIn 0.3s ease;
    }
    
    @keyframes modalSlideIn {
        from {
            opacity: 0;
            transform: translateY(-30px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .modal-buttons {
        display: flex;
        gap: 10px;
        margin-top: 20px;
    }
    
    .modal-buttons button {
        flex: 1;
        padding: 12px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .modal-buttons button[type="submit"] {
        background: #07734B;
        color: white;
    }
    
    .modal-buttons button[type="submit"]:hover {
        background: #05592f;
        transform: translateY(-2px);
    }
    
    .modal-buttons button[type="button"] {
        background: #6c757d;
        color: white;
    }
    
    .modal-buttons button[type="button"]:hover {
        background: #545b62;
        transform: translateY(-2px);
    }
    
    .modal-buttons button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
        transform: none !important;
    }
`;

// Inyectar estilos del modal
const styleSheet = document.createElement('style');
styleSheet.textContent = modalStyles;
document.head.appendChild(styleSheet);

console.log('🎉 Perfil.js completamente inicializado (sin conflictos de tabs)');