// =============================================
// BASE JS - USERS APP
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ Base Users JS cargado');
    
    // Preview de imagen al seleccionar foto
    const fotoInput = document.querySelector('input[type="file"][name="foto"]');
    if (fotoInput) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tamaño
                if (file.size > 5 * 1024 * 1024) {
                    alert('La imagen no puede pesar más de 5MB');
                    this.value = '';
                    return;
                }
                
                // Preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.querySelector('.profile-pic-placeholder img') ||
                                  document.querySelector('.current-photo img');
                    if (preview) {
                        preview.src = e.target.result;
                    }
                };
                reader.readAsDataURL(file);
                
                console.log(`📷 Foto seleccionada: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`);
            }
        });
    }
    
    // Manejo de formularios con AJAX opcional
    const forms = document.querySelectorAll('form[data-ajax="true"]');
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            
            // Deshabilitar botón
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner"></span> Guardando...';
            }
            
            try {
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (data.status === 'ok') {
                    alert(data.message || 'Guardado correctamente');
                    window.location.reload();
                } else {
                    alert(data.message || 'Error al guardar');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error de conexión');
            } finally {
                // Rehabilitar botón
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Guardar';
                }
            }
        });
    });
});