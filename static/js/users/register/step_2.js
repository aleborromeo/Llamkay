document.addEventListener('DOMContentLoaded', function () {
    console.log('🗺️ Registro Step 2 - Ubicación iniciado');

    // Selectores
    const departamentoSelect = document.getElementById('id_departamento');
    const provinciaSelect = document.getElementById('id_provincia');
    const distritoSelect = document.getElementById('id_distrito');
    const emailInput = document.getElementById('id_email');

    if (!departamentoSelect || !provinciaSelect || !distritoSelect) {
        console.warn('⚠️ No se encontraron todos los selectores de ubicación');
        return;
    }

    // ✅ Las URLs ya están definidas en el HTML por Django
    console.log('📍 URLs configuradas:', {
        provincias: urlProvincias,
        distritos: urlDistritos,
        validarCorreo: urlValidarCorreo
    });

    // ===== Cargar provincias cuando cambia el departamento =====
    departamentoSelect.addEventListener('change', async function () {
        const departamentoId = this.value;
        console.log(`🟢 Departamento seleccionado: ${departamentoId}`);

        // Resetear selects
        provinciaSelect.innerHTML = '<option value="">Selecciona tu provincia</option>';
        distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
        distritoSelect.disabled = true;

        if (!departamentoId) {
            provinciaSelect.disabled = false;
            return;
        }

        provinciaSelect.innerHTML = '<option value="">Cargando provincias...</option>';
        provinciaSelect.disabled = true;

        try {
            const url = `${urlProvincias}?id_departamento=${departamentoId}`;
            console.log('📡 Consultando:', url);
            
            const response = await fetch(url);
            
            console.log('📊 Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log('📦 Datos recibidos:', data);

            provinciaSelect.innerHTML = '<option value="">Selecciona tu provincia</option>';
            
            if (Array.isArray(data) && data.length > 0) {
                data.forEach(p => {
                    const option = document.createElement('option');
                    option.value = p.id_provincia;
                    option.textContent = p.nombre;
                    provinciaSelect.appendChild(option);
                });
                provinciaSelect.disabled = false;
                console.log(`✅ Provincias cargadas (${data.length})`);
            } else {
                provinciaSelect.innerHTML = '<option value="">No hay provincias disponibles</option>';
                provinciaSelect.disabled = false;
                console.warn('⚠️ Respuesta vacía de provincias');
            }
        } catch (error) {
            console.error('❌ Error al cargar provincias:', error);
            provinciaSelect.innerHTML = '<option value="">Error al cargar provincias</option>';
            provinciaSelect.disabled = false;
            alert('Error al cargar las provincias. Por favor, intenta de nuevo.');
        }
    });

    // ===== Cargar distritos cuando cambia la provincia =====
    provinciaSelect.addEventListener('change', async function () {
        const provinciaId = this.value;
        console.log(`🟢 Provincia seleccionada: ${provinciaId}`);

        distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
        distritoSelect.disabled = true;
        
        if (!provinciaId) {
            return;
        }

        distritoSelect.innerHTML = '<option value="">Cargando distritos...</option>';

        try {
            const url = `${urlDistritos}?id_provincia=${provinciaId}`;
            console.log('📡 Consultando:', url);
            
            const response = await fetch(url);
            
            console.log('📊 Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log('📦 Datos recibidos:', data);

            distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
            
            if (Array.isArray(data) && data.length > 0) {
                data.forEach(d => {
                    const option = document.createElement('option');
                    option.value = d.id_distrito;
                    option.textContent = d.nombre;
                    distritoSelect.appendChild(option);
                });
                distritoSelect.disabled = false;
                console.log(`✅ Distritos cargados (${data.length})`);
            } else {
                distritoSelect.innerHTML = '<option value="">No hay distritos disponibles</option>';
                distritoSelect.disabled = false;
                console.warn('⚠️ Respuesta vacía de distritos');
            }
        } catch (error) {
            console.error('❌ Error al cargar distritos:', error);
            distritoSelect.innerHTML = '<option value="">Error al cargar distritos</option>';
            distritoSelect.disabled = false;
            alert('Error al cargar los distritos. Por favor, intenta de nuevo.');
        }
    });

    // ===== Validación de email en tiempo real =====
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
            emailInput.insertAdjacentElement('afterend', emailMessage);
        }

        emailInput.addEventListener('blur', async function () {
            const email = emailInput.value.trim();
            if (!email) {
                emailMessage.textContent = '';
                return;
            }

            // Validar formato
            if (!validateEmail(email)) {
                emailMessage.textContent = '⚠️ Formato de email inválido';
                emailMessage.style.color = '#dc2626';
                return;
            }

            // Verificar existencia
            try {
                const response = await fetch(`${urlValidarCorreo}?email=${encodeURIComponent(email)}`);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();

                if (data.exists) {
                    emailMessage.textContent = '⚠️ El correo electrónico ya está en uso.';
                    emailMessage.style.color = '#dc2626';
                } else {
                    emailMessage.textContent = '✅ Email disponible';
                    emailMessage.style.color = '#22c55e';
                }
            } catch (error) {
                console.error('❌ Error al verificar email:', error);
                emailMessage.textContent = 'Error al verificar el correo.';
                emailMessage.style.color = '#f59e0b';
            }
        });
    }

    // ===== Función de validación de email =====
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // ===== Validación del formulario antes de enviar =====
    const form = document.getElementById('location-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('📤 Enviando formulario...');
            
            // Validar que todos los campos estén llenos
            const direccion = document.querySelector('input[name="direccion"]');
            const departamento = departamentoSelect;
            const provincia = provinciaSelect;
            const distrito = distritoSelect;
            
            if (!direccion || !direccion.value.trim()) {
                e.preventDefault();
                alert('Por favor ingresa tu dirección');
                direccion?.focus();
                return false;
            }
            
            if (!departamento.value) {
                e.preventDefault();
                alert('Por favor selecciona un departamento');
                departamento.focus();
                return false;
            }
            
            if (!provincia.value) {
                e.preventDefault();
                alert('Por favor selecciona una provincia');
                provincia.focus();
                return false;
            }
            
            if (!distrito.value) {
                e.preventDefault();
                alert('Por favor selecciona un distrito');
                distrito.focus();
                return false;
            }
            
            console.log('✅ Formulario válido, enviando...');
            console.log('📋 Datos:', {
                direccion: direccion.value,
                departamento: departamento.value,
                provincia: provincia.value,
                distrito: distrito.value
            });
        });
    }

    console.log('✅ Registro Step 2 listo');
});