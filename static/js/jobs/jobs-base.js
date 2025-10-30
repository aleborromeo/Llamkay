// =============================================
// JOBS MODULE - LLAMKAY.PE
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    initializeLocationSelects();
    initializeTabs();
    initializeFormValidation();
});

// ==================== LOCATION SELECTS ====================
function initializeLocationSelects() {
    const departamentoSelect = document.getElementById('departamento');
    const provinciaSelect = document.getElementById('provincia');
    const distritoSelect = document.getElementById('distrito');
    
    if (!departamentoSelect || !provinciaSelect || !distritoSelect) return;
    
    // Cargar provincias cuando cambia departamento
    departamentoSelect.addEventListener('change', function() {
        const departamentoId = this.value;
        
        provinciaSelect.innerHTML = '<option value="">Cargando...</option>';
        distritoSelect.innerHTML = '<option value="">Seleccione distrito</option>';
        
        if (departamentoId) {
            fetch(`/jobs/ajax/cargar-provincias/?id_departamento=${departamentoId}`)
                .then(response => response.json())
                .then(data => {
                    provinciaSelect.innerHTML = '<option value="">Todas</option>';
                    data.forEach(prov => {
                        const option = document.createElement('option');
                        option.value = prov.id_provincia;
                        option.textContent = prov.nombre;
                        provinciaSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    provinciaSelect.innerHTML = '<option value="">Error al cargar</option>';
                });
        } else {
            provinciaSelect.innerHTML = '<option value="">Todas</option>';
        }
    });
    
    // Cargar distritos cuando cambia provincia
    provinciaSelect.addEventListener('change', function() {
        const provinciaId = this.value;
        
        distritoSelect.innerHTML = '<option value="">Cargando...</option>';
        
        if (provinciaId) {
            fetch(`/jobs/ajax/cargar-distritos/?id_provincia=${provinciaId}`)
                .then(response => response.json())
                .then(data => {
                    distritoSelect.innerHTML = '<option value="">Todos</option>';
                    data.forEach(dist => {
                        const option = document.createElement('option');
                        option.value = dist.id_distrito;
                        option.textContent = dist.nombre;
                        distritoSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    distritoSelect.innerHTML = '<option value="">Error al cargar</option>';
                });
        } else {
            distritoSelect.innerHTML = '<option value="">Todos</option>';
        }
    });
}

// ==================== TABS ====================
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            document.getElementById(targetId).classList.add('active');
        });
    });
}

// ==================== FORM VALIDATION ====================
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showMessage('error', 'Por favor completa todos los campos requeridos');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });
}

// ==================== UTILITY FUNCTIONS ====================
function showMessage(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    
    const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    icon.setAttribute('viewBox', '0 0 24 24');
    icon.setAttribute('fill', 'none');
    icon.setAttribute('stroke', 'currentColor');
    icon.setAttribute('stroke-width', '2');
    
    if (type === 'success') {
        icon.innerHTML = '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>';
    } else if (type === 'error') {
        icon.innerHTML = '<circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line>';
    }
    
    alertDiv.appendChild(icon);
    alertDiv.appendChild(document.createTextNode(message));
    
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.transition = 'opacity 0.3s';
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 300);
    }, 3000);
}

// ==================== AJAX ACTIONS ====================
function cambiarEstado(ofertaId, nuevoEstado, tipo) {
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCsrfToken());
    formData.append('estado', nuevoEstado);
    
    fetch(`/jobs/cambiar-estado/${ofertaId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('success', data.message);
            setTimeout(() => location.reload(), 1000);
        } else {
            showMessage('error', data.message || 'Error al cambiar estado');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('error', 'Error al procesar la solicitud');
    });
}

function cerrarOferta(ofertaId, titulo) {
    if (!confirm(`¿Estás seguro de cerrar "${titulo}"?\n\nLa oferta ya no aparecerá en las búsquedas.`)) {
        return;
    }
    
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCsrfToken());
    
    fetch(`/jobs/eliminar/${ofertaId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('success', 'Oferta cerrada correctamente');
            setTimeout(() => location.reload(), 1000);
        } else {
            showMessage('error', data.message || 'Error al cerrar oferta');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('error', 'Error al procesar la solicitud');
    });
}

function aceptarPostulante(postulacionId, nombreTrabajador) {
    if (!confirm(`¿Estás seguro de aceptar a ${nombreTrabajador}?`)) {
        return;
    }
    
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCsrfToken());
    
    fetch(`/jobs/aceptar-postulante/${postulacionId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('success', data.message);
            setTimeout(() => location.reload(), 1500);
        } else {
            showMessage('error', data.message || 'Error al aceptar postulante');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('error', 'Error al procesar la solicitud');
    });
}

function rechazarPostulante(postulacionId, nombreTrabajador) {
    if (!confirm(`¿Estás seguro de rechazar a ${nombreTrabajador}?`)) {
        return;
    }
    
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCsrfToken());
    
    fetch(`/jobs/rechazar-postulante/${postulacionId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('success', data.message);
            setTimeout(() => location.reload(), 1500);
        } else {
            showMessage('error', data.message || 'Error al rechazar postulante');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('error', 'Error al procesar la solicitud');
    });
}

function confirmarQuitar(event, titulo) {
    event.preventDefault();
    const form = event.target;
    
    if (confirm(`¿Estás seguro de que deseas quitar "${titulo}" de tus guardados?`)) {
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const card = form.closest('.job-card, .guardado-card');
                card.style.transition = 'all 0.3s';
                card.style.opacity = '0';
                card.style.transform = 'translateX(-20px)';
                
                setTimeout(() => {
                    card.remove();
                    
                    const remainingCards = document.querySelectorAll('.job-card, .guardado-card');
                    if (remainingCards.length === 0) {
                        location.reload();
                    }
                }, 300);
                
                showMessage('success', data.message);
            } else {
                showMessage('error', data.message || 'Error al quitar de guardados');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('error', 'Error al procesar la solicitud');
        });
    }
    
    return false;
}

// ==================== HELPER FUNCTIONS ====================
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Make functions available globally for inline onclick handlers
window.cambiarEstado = cambiarEstado;
window.cerrarOferta = cerrarOferta;
window.aceptarPostulante = aceptarPostulante;
window.rechazarPostulante = rechazarPostulante;
window.confirmarQuitar = confirmarQuitar;