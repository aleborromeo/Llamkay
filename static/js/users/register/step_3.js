// ===== REGISTRO PASO 3 - Perfil Profesional =====

document.addEventListener('DOMContentLoaded', function () {
    console.log('💼 Registro Step 3 - Perfil Profesional iniciado');
    
    // Toggle campo de carrera según nivel de estudios
    const estudiosSelect = document.getElementById('id_estudios');
    const carreraField = document.getElementById('field-carrera');
    
    function toggleCarrera() {
        if (!estudiosSelect || !carreraField) return;
        
        const nivel = estudiosSelect.value;
        
        if (nivel === 'universitario' || nivel === 'posgrado') {
            carreraField.style.display = 'block';
            carreraField.querySelector('input')?.setAttribute('required', 'required');
        } else {
            carreraField.style.display = 'none';
            carreraField.querySelector('input')?.removeAttribute('required');
        }
    }
    
    if (estudiosSelect) {
        estudiosSelect.addEventListener('change', toggleCarrera);
        toggleCarrera(); // Ejecutar al cargar
    }
    
    // Validación de certificaciones
    const certificacionesInput = document.getElementById('id_certificaciones');
    if (certificacionesInput) {
        certificacionesInput.addEventListener('change', function(e) {
            const files = Array.from(e.target.files);
            
            if (files.length === 0) return;
            
            const maxSize = 5 * 1024 * 1024; // 5MB
            const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
            
            let hasError = false;
            
            files.forEach(file => {
                if (file.size > maxSize) {
                    showNotification(`${file.name} excede el tamaño máximo de 5MB`, 'error');
                    hasError = true;
                }
                
                if (!allowedTypes.includes(file.type)) {
                    showNotification(`${file.name} no es un formato válido`, 'error');
                    hasError = true;
                }
            });
            
            if (hasError) {
                this.value = '';
            } else {
                showNotification(`${files.length} archivo(s) seleccionado(s)`, 'success');
            }
        });
    }
    
    // Validación del formulario antes de enviar
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const habilidades = document.getElementById('id_habilidades');
            const disponibilidad = document.getElementById('id_disponibilidad');
            const estudios = document.getElementById('id_estudios');
            
            if (habilidades && !habilidades.value.trim()) {
                e.preventDefault();
                showNotification('Por favor describe tus habilidades', 'error');
                habilidades.focus();
                return false;
            }
            
            if (disponibilidad && !disponibilidad.value) {
                e.preventDefault();
                showNotification('Por favor selecciona tu disponibilidad', 'error');
                disponibilidad.focus();
                return false;
            }
            
            if (estudios && !estudios.value) {
                e.preventDefault();
                showNotification('Por favor selecciona tu nivel de estudios', 'error');
                estudios.focus();
                return false;
            }
        });
    }
    
    console.log('✅ Registro Step 3 listo');
});