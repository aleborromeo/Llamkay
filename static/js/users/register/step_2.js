// =============================================
// REGISTRO PASO 2 - UBICACIÓN (CASCADA)
// Version 3.0 - Completamente funcional
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ step_2.js cargado correctamente');

    // ==================== ELEMENTOS DEL DOM ====================
    const departamentoSelect = document.getElementById('id_departamento');
    const provinciaSelect = document.getElementById('id_provincia');
    const distritoSelect = document.getElementById('id_distrito');
    const direccionInput = document.querySelector('input[name="direccion"]');
    const form = document.getElementById('location-form');

    // Validar que existen los elementos
    if (!departamentoSelect || !provinciaSelect || !distritoSelect) {
        console.error('⚠️ No se encontraron todos los selectores de ubicación');
        return;
    }

    // Verificar que las URLs están definidas (vienen del template)
    if (typeof urlProvincias === 'undefined' || typeof urlDistritos === 'undefined') {
        console.error('⚠️ URLs de API no definidas');
        return;
    }

    console.log('📍 URLs configuradas:', {
        provincias: urlProvincias,
        distritos: urlDistritos
    });

    // ==================== FUNCIONES HELPER ====================

    /**
     * Muestra notificación
     */
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#dc2626' : '#3b82f6'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    /**
     * Resetea un select y lo deshabilita
     */
    function resetSelect(select, placeholderText, disabled = true) {
        select.innerHTML = `<option value="">${placeholderText}</option>`;
        select.disabled = disabled;
        select.value = '';
    }

    /**
     * Llena un select con opciones
     */
    function populateSelect(select, options, valueKey, textKey, enableAfter = true) {
        select.innerHTML = '<option value="">Selecciona una opción</option>';
        
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option[valueKey];
            optionElement.textContent = option[textKey];
            select.appendChild(optionElement);
        });
        
        if (enableAfter) {
            select.disabled = false;
        }
    }

    /**
     * Muestra estado de carga en select
     */
    function setSelectLoading(select, loading = true) {
        if (loading) {
            select.disabled = true;
            select.innerHTML = '<option value="">Cargando...</option>';
        }
    }

    // ==================== CARGAR PROVINCIAS ====================

    departamentoSelect.addEventListener('change', async function () {
        const departamentoId = this.value;
        console.log(`🟢 Departamento seleccionado: ${departamentoId}`);

        // Resetear selects dependientes
        resetSelect(provinciaSelect, 'Selecciona tu provincia', true);
        resetSelect(distritoSelect, 'Primero selecciona una provincia', true);

        if (!departamentoId) {
            return;
        }

        // Mostrar loading
        setSelectLoading(provinciaSelect, true);

        try {
            const url = `${urlProvincias}?id_departamento=${departamentoId}`;
            console.log('📡 Consultando:', url);
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            console.log('📊 Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log('📦 Datos recibidos:', data);

            if (Array.isArray(data) && data.length > 0) {
                populateSelect(provinciaSelect, data, 'id_provincia', 'nombre', true);
                console.log(`✅ ${data.length} provincias cargadas`);
            } else {
                resetSelect(provinciaSelect, 'No hay provincias disponibles', false);
                console.warn('⚠️ Respuesta vacía de provincias');
                showNotification('No se encontraron provincias', 'error');
            }
            
        } catch (error) {
            console.error('❌ Error al cargar provincias:', error);
            resetSelect(provinciaSelect, 'Error al cargar provincias', false);
            showNotification('Error al cargar provincias. Intenta de nuevo.', 'error');
        }
    });

    // ==================== CARGAR DISTRITOS ====================

    provinciaSelect.addEventListener('change', async function () {
        const provinciaId = this.value;
        console.log(`🟢 Provincia seleccionada: ${provinciaId}`);

        // Resetear distrito
        resetSelect(distritoSelect, 'Selecciona tu distrito', true);
        
        if (!provinciaId) {
            return;
        }

        // Mostrar loading
        setSelectLoading(distritoSelect, true);

        try {
            const url = `${urlDistritos}?id_provincia=${provinciaId}`;
            console.log('📡 Consultando:', url);
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            console.log('📊 Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log('📦 Datos recibidos:', data);

            if (Array.isArray(data) && data.length > 0) {
                populateSelect(distritoSelect, data, 'id_distrito', 'nombre', true);
                console.log(`✅ ${data.length} distritos cargados`);
            } else {
                resetSelect(distritoSelect, 'No hay distritos disponibles', false);
                console.warn('⚠️ Respuesta vacía de distritos');
                showNotification('No se encontraron distritos', 'error');
            }
            
        } catch (error) {
            console.error('❌ Error al cargar distritos:', error);
            resetSelect(distritoSelect, 'Error al cargar distritos', false);
            showNotification('Error al cargar distritos. Intenta de nuevo.', 'error');
        }
    });

    // ==================== VALIDACIÓN DEL FORMULARIO ====================

    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('📤 Enviando formulario...');
            
            const errors = [];

            // Validar dirección
            if (!direccionInput || !direccionInput.value.trim()) {
                errors.push('Por favor ingresa tu dirección');
            }
            
            // Validar departamento
            if (!departamentoSelect.value) {
                errors.push('Por favor selecciona un departamento');
            }
            
            // Validar provincia
            if (!provinciaSelect.value) {
                errors.push('Por favor selecciona una provincia');
            }
            
            // Validar distrito
            if (!distritoSelect.value) {
                errors.push('Por favor selecciona un distrito');
            }
            
            if (errors.length > 0) {
                e.preventDefault();
                errors.forEach(error => showNotification(error, 'error'));
                
                // Enfocar el primer campo con error
                if (!direccionInput.value.trim()) {
                    direccionInput.focus();
                } else if (!departamentoSelect.value) {
                    departamentoSelect.focus();
                } else if (!provinciaSelect.value) {
                    provinciaSelect.focus();
                } else if (!distritoSelect.value) {
                    distritoSelect.focus();
                }
                
                return false;
            }
            
            console.log('✅ Formulario válido, enviando...');
            console.log('📋 Datos:', {
                direccion: direccionInput.value,
                departamento: departamentoSelect.value,
                provincia: provinciaSelect.value,
                distrito: distritoSelect.value
            });

            // Mostrar loading en botón
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                submitBtn.innerHTML = `
                    <svg style="animation: spin 1s linear infinite;" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="12" y1="2" x2="12" y2="6"></line>
                        <line x1="12" y1="18" x2="12" y2="22"></line>
                        <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
                        <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
                        <line x1="2" y1="12" x2="6" y2="12"></line>
                        <line x1="18" y1="12" x2="22" y2="12"></line>
                        <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
                        <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
                    </svg>
                    Procesando...
                `;
            }
        });
    }

    // ==================== VALIDACIÓN EN TIEMPO REAL ====================

    // Validar dirección mientras escribe
    if (direccionInput) {
        direccionInput.addEventListener('input', function() {
            if (this.value.trim().length > 0) {
                this.style.borderColor = '#10b981';
            } else {
                this.style.borderColor = '#e2e8f0';
            }
        });
    }

    // ==================== AUTO-GUARDAR PROGRESO (OPCIONAL) ====================

    // Guardar en localStorage para no perder datos
    function saveProgress() {
        const progress = {
            direccion: direccionInput?.value || '',
            departamento: departamentoSelect?.value || '',
            provincia: provinciaSelect?.value || '',
            distrito: distritoSelect?.value || ''
        };
        localStorage.setItem('registro_step2', JSON.stringify(progress));
    }

    // Recuperar progreso
    function loadProgress() {
        try {
            const saved = localStorage.getItem('registro_step2');
            if (saved) {
                const progress = JSON.parse(saved);
                if (direccionInput && progress.direccion) {
                    direccionInput.value = progress.direccion;
                }
                // Los selects se recargarán dinámicamente
            }
        } catch (e) {
            console.error('Error al cargar progreso:', e);
        }
    }

    // Cargar progreso al iniciar
    loadProgress();

    // Guardar progreso en cada cambio
    [direccionInput, departamentoSelect, provinciaSelect, distritoSelect].forEach(element => {
        if (element) {
            element.addEventListener('change', saveProgress);
        }
    });

    console.log('✅ step_2.js listo');
});

// Agregar estilos de animación
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;
if (!document.getElementById('step2-animations')) {
    style.id = 'step2-animations';
    document.head.appendChild(style);
}