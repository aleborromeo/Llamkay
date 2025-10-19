// ===== REGISTRO PASO 1 - DNI/RUC + Toggle Contraseña =====

console.log('🚀 Script step_1.js cargado');

/**
 * Mostrar notificación
 */
function showNotification(message, type = 'info') {
    const oldNotif = document.querySelector('.notification-toast');
    if (oldNotif) oldNotif.remove();
    
    const notification = document.createElement('div');
    notification.className = `notification-toast ${type}`;
    notification.textContent = message;
    
    const styles = {
        success: { bg: '#d4edda', color: '#155724', border: '#c3e6cb' },
        error: { bg: '#f8d7da', color: '#721c24', border: '#f5c6cb' },
        warning: { bg: '#fff3cd', color: '#856404', border: '#ffeaa7' },
        info: { bg: '#d1ecf1', color: '#0c5460', border: '#bee5eb' }
    };
    
    const style = styles[type] || styles.info;
    
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 20px',
        backgroundColor: style.bg,
        color: style.color,
        borderLeft: `4px solid ${style.border}`,
        borderRadius: '4px',
        boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
        zIndex: '10000',
        animation: 'slideIn 0.3s ease',
        maxWidth: '400px'
    });
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

/**
 * Buscar DNI en API
 */
async function buscarDNI(event) {
    console.log('🔍 === INICIO BÚSQUEDA DNI ===');
    
    const dniInput = document.querySelector('input[name="dni"]');
    if (!dniInput) {
        console.error('❌ No se encontró el campo DNI');
        showNotification('Error: Campo DNI no encontrado', 'error');
        return;
    }
    
    const dni = dniInput.value.trim();
    console.log('📝 DNI ingresado:', dni);

    if (!dni || dni.length !== 8) {
        showNotification('Por favor ingresa un DNI válido de 8 dígitos', 'error');
        return;
    }

    const btnBuscar = event.target;
    const textoOriginal = btnBuscar.textContent;
    btnBuscar.textContent = 'Buscando...';
    btnBuscar.disabled = true;

    try {
        console.log('🌐 Llamando a la API...');
        const url = `/users/api/consultar-dni/?dni=${dni}`;
        console.log('📡 URL:', url);
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            },
        });

        console.log('📡 Status:', response.status);
        const data = await response.json();
        console.log('📦 Datos recibidos:', data);

        if (response.ok && data.success) {
            const nombreInput = document.querySelector('input[name="nombre"]');
            const apellidoInput = document.querySelector('input[name="apellido"]');

            console.log('🎯 Campos encontrados:', {
                nombre: !!nombreInput,
                apellido: !!apellidoInput
            });

            if (!nombreInput || !apellidoInput) {
                console.error('❌ No se encontraron los campos nombre/apellido');
                showNotification('Error: Campos no encontrados', 'error');
                return;
            }

            // Construir apellidos
            let apellidos = '';
            if (data.data.apellido_paterno) apellidos += data.data.apellido_paterno;
            if (data.data.apellido_materno) apellidos += ' ' + data.data.apellido_materno;

            console.log('📝 Valores a asignar:', {
                nombres: data.data.nombres,
                apellidos: apellidos.trim()
            });

            // ACTUALIZAR CAMPOS - QUITAR READONLY TEMPORALMENTE
            nombreInput.removeAttribute('readonly');
            nombreInput.value = data.data.nombres || '';
            nombreInput.dataset.valorValido = 'true'; // Marcar como válido
            
            apellidoInput.removeAttribute('readonly');
            apellidoInput.value = apellidos.trim();
            apellidoInput.dataset.valorValido = 'true'; // Marcar como válido

            // NO volver a poner readonly para permitir el submit
            console.log('✅ Campos actualizados y desbloqueados para submit');

            showNotification(`✅ Datos encontrados: ${data.data.nombre_completo}`, 'success');
            console.log('🎉 === BÚSQUEDA EXITOSA ===');
        } else {
            console.warn('⚠️ No se encontraron datos');
            showNotification('⚠️ ' + (data.error || 'DNI no encontrado'), 'error');
        }
    } catch (error) {
        console.error('❌ Error completo:', error);
        console.error('Stack:', error.stack);
        showNotification('Error al buscar el DNI. Intenta nuevamente.', 'error');
    } finally {
        btnBuscar.textContent = textoOriginal;
        btnBuscar.disabled = false;
        console.log('📚 === FIN BÚSQUEDA DNI ===');
    }
}

/**
 * Buscar RUC en API
 */
async function buscarRUC(event) {
    console.log('🔍 === INICIO BÚSQUEDA RUC ===');
    
    const rucInput = document.querySelector('input[name="ruc"]');
    if (!rucInput) {
        console.error('❌ No se encontró el campo RUC');
        showNotification('Error: Campo RUC no encontrado', 'error');
        return;
    }
    
    const ruc = rucInput.value.trim();
    console.log('📝 RUC ingresado:', ruc);

    if (!ruc || ruc.length !== 11) {
        showNotification('Por favor ingresa un RUC válido de 11 dígitos', 'error');
        return;
    }

    const btnBuscar = event.target;
    const textoOriginal = btnBuscar.textContent;
    btnBuscar.textContent = 'Buscando...';
    btnBuscar.disabled = true;

    try {
        console.log('🌐 Llamando a la API...');
        const url = `/users/api/consultar-ruc/?ruc=${ruc}`;
        console.log('📡 URL:', url);
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            },
        });

        console.log('📡 Status:', response.status);
        const data = await response.json();
        console.log('📦 Datos recibidos:', data);

        if (response.ok && data.success) {
            const razonSocialInput = document.querySelector('input[name="razon_social"]');
            
            if (!razonSocialInput) {
                console.error('❌ No se encontró el campo razón social');
                showNotification('Error: Campo razón social no encontrado', 'error');
                return;
            }

            // ACTUALIZAR CAMPO - QUITAR READONLY TEMPORALMENTE
            razonSocialInput.removeAttribute('readonly');
            razonSocialInput.value = data.data.razon_social || '';
            razonSocialInput.dataset.valorValido = 'true'; // Marcar como válido
            
            // NO volver a poner readonly para permitir el submit
            console.log('✅ Razón social actualizada y desbloqueada para submit');
            
            showNotification(`✅ Empresa encontrada: ${data.data.razon_social}`, 'success');
            console.log('🎉 === BÚSQUEDA EXITOSA ===');
        } else {
            console.warn('⚠️ No se encontraron datos');
            showNotification('⚠️ ' + (data.error || 'RUC no encontrado'), 'error');
        }
    } catch (error) {
        console.error('❌ Error completo:', error);
        console.error('Stack:', error.stack);
        showNotification('Error al buscar el RUC. Intenta nuevamente.', 'error');
    } finally {
        btnBuscar.textContent = textoOriginal;
        btnBuscar.disabled = false;
        console.log('📚 === FIN BÚSQUEDA RUC ===');
    }
}

/**
 * Inicializar
 */
document.addEventListener('DOMContentLoaded', function () {
    console.log('🔧 === INICIALIZANDO STEP 1 ===');
    
    // Validación de solo números para DNI y RUC
    const dniInput = document.querySelector('input[name="dni"]');
    const rucInput = document.querySelector('input[name="ruc"]');

    function soloNumeros(event) {
        const key = event.key;
        if (!/[0-9]/.test(key) && !['Backspace', 'Delete', 'Tab', 'ArrowLeft', 'ArrowRight'].includes(key)) {
            event.preventDefault();
        }
    }

    if (dniInput) {
        dniInput.addEventListener('keydown', soloNumeros);
        dniInput.addEventListener('input', function () {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 8);
        });
        console.log('✅ DNI input configurado');
    }

    if (rucInput) {
        rucInput.addEventListener('keydown', soloNumeros);
        rucInput.addEventListener('input', function () {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 11);
        });
        console.log('✅ RUC input configurado');
    }
    
    // Toggle de contraseña
    const toggleButtons = document.querySelectorAll('.toggle-password');
    console.log(`🔑 Encontrados ${toggleButtons.length} botones de toggle`);
    
    toggleButtons.forEach(function (toggle) {
        toggle.addEventListener('click', function () {
            const formGroup = toggle.closest('.form-group');
            const passwordInput = formGroup?.querySelector('.password-input') || 
                                 formGroup?.querySelector('input[type="password"], input[type="text"]');
            const eyeOpen = toggle.querySelector('.eye-open');
            const eyeClosed = toggle.querySelector('.eye-closed');

            if (passwordInput && eyeOpen && eyeClosed) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    eyeOpen.style.display = 'none';
                    eyeClosed.style.display = 'inline';
                } else {
                    passwordInput.type = 'password';
                    eyeOpen.style.display = 'inline';
                    eyeClosed.style.display = 'none';
                }
            }
        });
    });
    
    // Configurar botones de búsqueda
    const botonesDNI = document.querySelectorAll('[data-action="buscar-dni"]');
    const botonesRUC = document.querySelectorAll('[data-action="buscar-ruc"]');
    
    console.log(`🔍 Encontrados ${botonesDNI.length} botones de DNI`);
    console.log(`🔍 Encontrados ${botonesRUC.length} botones de RUC`);
    
    botonesDNI.forEach(btn => {
        btn.addEventListener('click', buscarDNI);
        console.log('✅ Botón buscar DNI configurado');
    });
    
    botonesRUC.forEach(btn => {
        btn.addEventListener('click', buscarRUC);
        console.log('✅ Botón buscar RUC configurado');
    });
    
    // IMPORTANTE: Handler para SUBMIT del formulario
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            console.log('📤 === SUBMIT DEL FORMULARIO ===');
            
            // Quitar readonly de todos los campos antes del submit
            const readonlyFields = registerForm.querySelectorAll('[readonly]');
            readonlyFields.forEach(field => {
                console.log('🔓 Desbloqueando campo:', field.name);
                field.removeAttribute('readonly');
            });
            
            // Validar que los campos requeridos estén llenos
            const nombre = document.querySelector('input[name="nombre"]');
            const apellido = document.querySelector('input[name="apellido"]');
            const razonSocial = document.querySelector('input[name="razon_social"]');
            
            if (nombre && apellido) {
                // Validar persona natural
                if (!nombre.value.trim() || !apellido.value.trim()) {
                    e.preventDefault();
                    showNotification('Por favor busca tu DNI primero', 'error');
                    console.log('❌ Campos nombre/apellido vacíos');
                    return false;
                }
            }
            
            if (razonSocial) {
                // Validar empresa
                if (!razonSocial.value.trim()) {
                    e.preventDefault();
                    showNotification('Por favor busca tu RUC primero', 'error');
                    console.log('❌ Campo razón social vacío');
                    return false;
                }
            }
            
            console.log('✅ Formulario válido, enviando...');
            console.log('📦 FormData:', new FormData(registerForm));
        });
        
        console.log('✅ Submit handler configurado');
    }
    
    // Agregar estilos de animación
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        
        .readonly-field {
            background-color: #f3f4f6 !important;
            cursor: not-allowed;
        }
    `;
    document.head.appendChild(style);
    
    console.log('✅ === STEP 1 INICIALIZADO COMPLETAMENTE ===');
});

// Exponer funciones globalmente
window.buscarDNI = buscarDNI;
window.buscarRUC = buscarRUC;
window.showNotification = showNotification;

console.log('✅ Funciones expuestas globalmente');