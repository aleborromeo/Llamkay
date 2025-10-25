// =============================================
//  PERFIL DE USUARIO - JAVASCRIPT MODERNO
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Perfil JS cargado');
    
    initializeTabs();
    initializeModal();
    initializeMobileMenu();
    initializeForm();
});

// ==================== TABS NAVIGATION ====================
function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    if (!tabBtns.length || !tabContents.length) {
        console.warn('⚠️ No se encontraron tabs');
        return;
    }
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.dataset.tab;
            
            // Remove active class from all tabs and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
            }
            
            console.log(`📑 Tab activado: ${targetTab}`);
        });
    });
    
    console.log('✅ Tabs inicializados');
}

// ==================== MODAL MANAGEMENT ====================
function initializeModal() {
    const modal = document.getElementById('editModal');
    if (!modal) {
        console.warn('⚠️ Modal no encontrado');
        return;
    }
    
    // Close modal on overlay click
    const overlay = modal.querySelector('.modal-overlay');
    if (overlay) {
        overlay.addEventListener('click', closeEditModal);
    }
    
    // Close modal on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeEditModal();
        }
    });
    
    console.log('✅ Modal inicializado');
}

function openEditModal() {
    const modal = document.getElementById('editModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        console.log('✏️ Modal abierto');
    }
}

function closeEditModal() {
    const modal = document.getElementById('editModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
        console.log('❌ Modal cerrado');
    }
}

// Make functions globally available
window.openEditModal = openEditModal;
window.closeEditModal = closeEditModal;

// ==================== MOBILE MENU ====================
function initializeMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (!navToggle || !navMenu) {
        return;
    }
    
    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        this.classList.toggle('active');
    });
    
    // Close menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });
    
    console.log('✅ Menú móvil inicializado');
}

// ==================== FORM HANDLING ====================
function initializeForm() {
    const form = document.getElementById('editProfileForm');
    if (!form) {
        console.warn('⚠️ Formulario no encontrado');
        return;
    }
    
    // Preview image on file select
    const fotoInput = document.getElementById('foto');
    if (fotoInput) {
        fotoInput.addEventListener('change', handleImagePreview);
    }
    
    // Form submission
    form.addEventListener('submit', handleFormSubmit);
    
    console.log('✅ Formulario inicializado');
}

function handleImagePreview(e) {
    const file = e.target.files[0];
    
    if (!file) return;
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showNotification('Por favor selecciona una imagen válida', 'error');
        e.target.value = '';
        return;
    }
    
    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
        showNotification('La imagen no debe superar los 5MB', 'error');
        e.target.value = '';
        return;
    }
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(event) {
        console.log('📸 Imagen cargada para previsualización');
        // You can add preview logic here if needed
    };
    reader.readAsDataURL(file);
    
    console.log('✅ Imagen válida seleccionada');
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (!submitBtn) return;
    
    // Validate form
    if (!validateForm(form)) {
        return;
    }
    
    // Disable button and show loading
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Guardando...';
    submitBtn.disabled = true;
    
    // Get form data
    const formData = new FormData(form);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Submit form
    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => {
        return response.json().then(data => ({
            ok: response.ok,
            status: response.status,
            data: data
        }));
    })
    .then(({ ok, status, data }) => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        
        if (ok && data.status === 'ok') {
            showNotification('✅ Perfil actualizado correctamente', 'success');
            closeEditModal();
            
            // Reload page after short delay
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            const message = data.message || `Error desconocido. Código ${status}`;
            showNotification('❌ ' + message, 'error');
        }
    })
    .catch(error => {
        console.error('❌ Error en fetch:', error);
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        showNotification('❌ Error de conexión con el servidor', 'error');
    });
}

function validateForm(form) {
    // Validate phone (9 digits)
    const telefono = form.querySelector('[name="telefono"]')?.value.trim();
    if (telefono && !/^\d{9}$/.test(telefono)) {
        showNotification('El teléfono debe tener 9 dígitos', 'error');
        return false;
    }
    
    // Validate price per hour
    const tarifaHora = form.querySelector('[name="tarifa_hora"]')?.value;
    if (tarifaHora && (isNaN(tarifaHora) || parseFloat(tarifaHora) < 0)) {
        showNotification('El precio por hora debe ser un número válido', 'error');
        return false;
    }
    
    return true;
}

// ==================== NOTIFICATIONS ====================
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem 1.5rem',
        background: type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6',
        color: 'white',
        borderRadius: '12px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
        zIndex: '9999',
        fontWeight: '600',
        animation: 'slideInRight 0.3s ease',
        maxWidth: '400px'
    });
    
    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        @keyframes slideOutRight {
            from {
                opacity: 1;
                transform: translateX(0);
            }
            to {
                opacity: 0;
                transform: translateX(100px);
            }
        }
    `;
    if (!document.querySelector('style[data-notification-styles]')) {
        style.setAttribute('data-notification-styles', 'true');
        document.head.appendChild(style);
    }
    
    // Add to document
    document.body.appendChild(notification);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 4000);
    
    console.log(`📢 Notificación: ${message}`);
}

// Make notification function globally available
window.showNotification = showNotification;

console.log('🎉 Perfil.js completamente inicializado');