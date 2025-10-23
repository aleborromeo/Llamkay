// ===== PERFIL DE USUARIO - Gestión Completa =====

document.addEventListener('DOMContentLoaded', function() {
    console.log('👤 Perfil JS cargado');
    
    initializeProfile();
    
    setTimeout(() => {
        initializeProfileSpecificFeatures();
    }, 100);
});

/**
 * Inicializar funcionalidades del perfil
 */
function initializeProfile() {
    console.log('🔧 Inicializando perfil...');
    
    initializeButtons();
    initializeHoverEffects();
    initializePhotoPreview();
    setupImagePreview();
    handleEditFormSubmit();
}

/**
 * Características específicas del perfil
 */
function initializeProfileSpecificFeatures() {
    console.log('📋 Inicializando características específicas...');
    
    const activeTab = document.querySelector('.tab.active');
    if (!activeTab) {
        const generalTab = document.querySelector('.tab[data-tab="general"]');
        if (generalTab) {
            generalTab.click();
        }
    }
}

/**
 * Inicializar botones
 */
function initializeButtons() {
    console.log('🔘 Inicializando botones...');
    
    // Botón de editar con data-action
    document.querySelectorAll('[data-action="editar-perfil"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            openEditProfileModal();
        });
    });
    
    // Botón de editar tradicional
    const editButton = document.querySelector('.profile-actions .btn-primary');
    if (editButton && !editButton.hasAttribute('data-action')) {
        editButton.addEventListener('click', function(e) {
            e.preventDefault();
            openEditProfileModal();
        });
    }
    
    // Botón de cerrar modal
    document.querySelectorAll('[data-action="cerrar-modal"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            closeEditProfileModal();
        });
    });
}

/**
 * Abrir modal de edición
 */
function openEditProfileModal() {
    console.log('✏️ Abriendo modal de edición...');
    
    const modal = document.getElementById('editProfileModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        document.addEventListener('keydown', handleModalKeydown);
        
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
 * Cerrar modal de edición
 */
function closeEditProfileModal() {
    console.log('❌ Cerrando modal de edición...');
    
    const modal = document.getElementById('editProfileModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
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
 * Validar formulario
 */
function validateForm(form) {
    const telefono = form.querySelector('[name="telefono"]')?.value.trim();
    if (telefono && !/^\d{9}$/.test(telefono)) {
        showNotification('El teléfono debe tener 9 dígitos', 'error');
        return false;
    }

    const precioHora = form.querySelector('[name="precio_hora"]')?.value;
    if (precioHora && (isNaN(precioHora) || parseFloat(precioHora) < 0)) {
        showNotification('El precio por hora debe ser un número válido', 'error');
        return false;
    }

    return true;
}

/**
 * Configurar previsualización de imagen
 */
function setupImagePreview() {
    const fileInput = document.querySelector('input[name="foto"]');
    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                if (!file.type.startsWith('image/')) {
                    showNotification('Por favor selecciona una imagen válida', 'error');
                    this.value = '';
                    return;
                }

                if (file.size > 5 * 1024 * 1024) {
                    showNotification('La imagen no debe superar los 5MB', 'error');
                    this.value = '';
                    return;
                }

                console.log('📸 Imagen válida seleccionada');
                
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
 * Manejar envío del formulario
 */
function handleEditFormSubmit() {
    const form = document.getElementById('form-editar-perfil');
    if (!form) {
        console.warn('⚠️ No se encontró el formulario de edición');
        return;
    }

    const modal = document.getElementById('editProfileModal');

    if (modal) {
        modal.addEventListener('click', function (e) {
            if (e.target === modal) closeEditProfileModal();
        });
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal?.style.display === 'flex') {
            closeEditProfileModal();
        }
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        if (!validateForm(form)) return;

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Guardando...';
        submitBtn.disabled = true;
        submitBtn.style.background = '#9CDBA6';
        submitBtn.style.cursor = 'not-allowed';

        const formData = new FormData(form);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/users/perfil/actualizar/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(res => res.json().then(data => ({ ok: res.ok, status: res.status, data })))
        .then(({ ok, data, status }) => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.background = '';
            submitBtn.style.cursor = '';

            if (ok && data.status === 'ok') {
                showNotification('✅ Perfil actualizado correctamente', 'success');
                closeEditProfileModal();
                setTimeout(() => location.reload(), 1000);
            } else {
                const msg = data.message || `Error desconocido. Código ${status}`;
                showNotification('❌ ' + msg, 'error');
            }
        })
        .catch(err => {
            console.error('❌ Error en fetch:', err);
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.background = '';
            submitBtn.style.cursor = '';
            showNotification('❌ Error de conexión con el servidor', 'error');
        });
    });

    console.log('✅ Form submit handler configurado');
}

/**
 * Inicializar previsualización de foto
 */
function initializePhotoPreview() {
    const fotoInput = document.getElementById('foto');
    if (fotoInput) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                if (!file.type.startsWith('image/')) {
                    showNotification('Por favor selecciona un archivo de imagen válido', 'error');
                    return;
                }
                
                if (file.size > 5 * 1024 * 1024) {
                    showNotification('La imagen es demasiado grande. Por favor selecciona una imagen menor a 5MB', 'error');
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
 * Efectos de hover
 */
function initializeHoverEffects() {
    console.log('✨ Inicializando efectos de hover...');
    
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
}

// Funciones globales para compatibilidad
window.openEditProfileModal = openEditProfileModal;
window.closeEditProfileModal = closeEditProfileModal;
window.cerrarModalEdicion = closeEditProfileModal;
window.editProfile = openEditProfileModal;

console.log('🎉 Perfil.js completamente inicializado');