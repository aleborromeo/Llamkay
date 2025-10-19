// ===== REGISTRO PASO 2 - Ubicación (Departamento, Provincia, Distrito) =====

document.addEventListener('DOMContentLoaded', function () {
    console.log('📍 Registro Step 2 - Ubicación iniciado');
    
    const departamentoSelect = document.getElementById('id_departamento');
    const provinciaSelect = document.getElementById('id_provincia');
    const distritoSelect = document.getElementById('id_distrito');

    if (!departamentoSelect || !provinciaSelect || !distritoSelect) {
        console.warn('⚠️ No se encontraron todos los selectores de ubicación');
        return;
    }

    // Cargar provincias al cambiar departamento
    departamentoSelect.addEventListener('change', function () {
        const departamentoId = this.value;
        
        if (!departamentoId) {
            provinciaSelect.innerHTML = '<option value="">Selecciona tu provincia</option>';
            distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
            return;
        }
        
        // Mostrar loading
        provinciaSelect.innerHTML = '<option value="">Cargando provincias...</option>';
        provinciaSelect.disabled = true;
        distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
        distritoSelect.disabled = true;
        
        fetch(`/users/cargar-provincias/?id_departamento=${departamentoId}`)
            .then(response => response.json())
            .then(data => {
                provinciaSelect.innerHTML = '<option value="">Selecciona tu provincia</option>';
                data.forEach(function (provincia) {
                    const option = document.createElement('option');
                    option.value = provincia.id_provincia;
                    option.textContent = provincia.nombre;
                    provinciaSelect.appendChild(option);
                });
                provinciaSelect.disabled = false;
                console.log(`✅ ${data.length} provincias cargadas`);
            })
            .catch(error => {
                console.error('❌ Error al cargar provincias:', error);
                provinciaSelect.innerHTML = '<option value="">Error al cargar provincias</option>';
                if (window.showNotification) {
                    window.showNotification('Error al cargar provincias', 'error');
                }
            });
    });

    // Cargar distritos al cambiar provincia
    provinciaSelect.addEventListener('change', function () {
        const provinciaId = this.value;
        
        if (!provinciaId) {
            distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
            return;
        }
        
        // Mostrar loading
        distritoSelect.innerHTML = '<option value="">Cargando distritos...</option>';
        distritoSelect.disabled = true;
        
        fetch(`/users/cargar-distritos/?id_provincia=${provinciaId}`)
            .then(response => response.json())
            .then(data => {
                distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
                data.forEach(function (distrito) {
                    const option = document.createElement('option');
                    option.value = distrito.id_distrito;
                    option.textContent = distrito.nombre;
                    distritoSelect.appendChild(option);
                });
                distritoSelect.disabled = false;
                console.log(`✅ ${data.length} distritos cargados`);
            })
            .catch(error => {
                console.error('❌ Error al cargar distritos:', error);
                distritoSelect.innerHTML = '<option value="">Error al cargar distritos</option>';
                if (window.showNotification) {
                    window.showNotification('Error al cargar distritos', 'error');
                }
            });
    });

    // Validación de email en tiempo real
    const emailInput = document.getElementById('id_email');
    if (emailInput) {
        let emailMessage = document.getElementById('email-error-message');
        
        if (!emailMessage) {
            emailMessage = document.createElement('div');
            emailMessage.id = 'email-error-message';
            emailMessage.style.cssText = `
                color: red;
                margin-top: 5px;
                font-size: 0.9rem;
                font-weight: 500;
            `;
            emailInput.parentNode.insertBefore(emailMessage, emailInput.nextSibling);
        }

        emailInput.addEventListener('blur', function () {
            const email = emailInput.value;
            if (email.trim() === '') {
                emailMessage.textContent = '';
                return;
            }

            // Validar formato
            if (!validateEmail(email)) {
                emailMessage.textContent = '⚠️ Formato de email inválido';
                emailMessage.style.color = '#dc2626';
                return;
            }

            // Verificar si existe
            fetch(`/users/validar-correo/?email=${encodeURIComponent(email)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        emailMessage.textContent = '⚠️ El correo electrónico ya está en uso.';
                        emailMessage.style.color = '#dc2626';
                    } else {
                        emailMessage.textContent = '✅ Email disponible';
                        emailMessage.style.color = '#22c55e';
                    }
                })
                .catch(error => {
                    console.error('Error al verificar email:', error);
                    emailMessage.textContent = 'Error al verificar el correo.';
                    emailMessage.style.color = '#f59e0b';
                });
        });
    }
    
    // Función de validación de email
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    console.log('✅ Registro Step 2 listo');
});