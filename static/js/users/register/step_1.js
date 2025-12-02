// =============================================
// REGISTRO PASO 1 - DNI/RUC Y VALIDACIONES
// Version 3.0 - Completamente funcional
// =============================================

document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ step_1.js cargado correctamente");

    // ==================== ELEMENTOS DEL DOM ====================
    const btnBuscarDNI = document.querySelector('button[data-action="buscar-dni"]');
    const btnBuscarRUC = document.querySelector('button[data-action="buscar-ruc"]');
    const form = document.getElementById('registerForm');
    
    // Inputs DNI
    const dniInput = document.querySelector('input[name="dni"]');
    const nombreInput = document.querySelector('input[name="nombre"]');
    const apellidoInput = document.querySelector('input[name="apellido"]');
    
    // Inputs RUC
    const rucInput = document.querySelector('input[name="ruc"]');
    const razonSocialInput = document.querySelector('input[name="razon_social"]');
    
    // Password toggles
    const passwordToggles = document.querySelectorAll('.password-toggle');

    // ==================== FUNCIONES HELPER ====================
    
    /**
     * Muestra notificación toast
     */
    function showNotification(message, type = 'error') {
        // Crear o usar sistema de notificaciones
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#dc2626' : '#f59e0b'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
            z-index: 9999;
            animation: slideIn 0.3s ease;
            max-width: 400px;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    /**
     * Deshabilita un botón durante la carga
     */
    function setButtonLoading(button, loading = true) {
        if (loading) {
            button.disabled = true;
            button.classList.add('loading');
            button.dataset.originalText = button.textContent;
            button.textContent = 'Buscando...';
        } else {
            button.disabled = false;
            button.classList.remove('loading');
            button.textContent = button.dataset.originalText || 'Buscar';
        }
    }

    /**
     * Limpia un input y lo hace editable
     */
    function unlockInput(input) {
        input.removeAttribute('readonly');
        input.classList.remove('readonly-field');
        input.style.background = 'white';
    }

    /**
     * Bloquea un input
     */
    function lockInput(input) {
        input.setAttribute('readonly', 'readonly');
        input.classList.add('readonly-field');
    }

    /**
     * Valida formato de DNI
     */
    function validarDNI(dni) {
        if (!dni || dni.trim().length === 0) {
            return { valid: false, error: 'El DNI no puede estar vacío' };
        }
        if (dni.length !== 8) {
            return { valid: false, error: 'El DNI debe tener exactamente 8 dígitos' };
        }
        if (!/^\d+$/.test(dni)) {
            return { valid: false, error: 'El DNI solo debe contener números' };
        }
        return { valid: true };
    }

    /**
     * Valida formato de RUC
     */
    function validarRUC(ruc) {
        if (!ruc || ruc.trim().length === 0) {
            return { valid: false, error: 'El RUC no puede estar vacío' };
        }
        if (ruc.length !== 11) {
            return { valid: false, error: 'El RUC debe tener exactamente 11 dígitos' };
        }
        if (!/^\d+$/.test(ruc)) {
            return { valid: false, error: 'El RUC solo debe contener números' };
        }
        return { valid: true };
    }

    // ==================== CONSULTAR DNI ====================
    
    if (btnBuscarDNI && dniInput && nombreInput && apellidoInput) {
        btnBuscarDNI.addEventListener("click", async function () {
            const dni = dniInput.value.trim();

            // Validaciones locales
            const validation = validarDNI(dni);
            if (!validation.valid) {
                showNotification(validation.error, 'error');
                dniInput.focus();
                return;
            }

            // Deshabilitar botón
            setButtonLoading(btnBuscarDNI, true);

            try {
                console.log("🔍 Consultando DNI:", dni);
                
                const response = await fetch(`/users/api/consultar-dni/?dni=${dni}`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();
                console.log("📦 Respuesta:", data);

                if (response.ok && data.success && data.data) {
                    const info = data.data;

                    // Llenar campos
                    nombreInput.value = info.nombres || "";
                    apellidoInput.value = `${info.apellido_paterno || ""} ${info.apellido_materno || ""}`.trim();

                    // Hacer campos editables
                    unlockInput(nombreInput);
                    unlockInput(apellidoInput);

                    showNotification('✅ Datos cargados correctamente', 'success');
                    
                    // Enfocar siguiente campo
                    const telefonoInput = document.querySelector('input[name="telefono"]');
                    if (telefonoInput) telefonoInput.focus();
                    
                } else {
                    const errorMsg = data.error || "No se encontró información para el DNI ingresado";
                    showNotification(errorMsg, 'error');
                    
                    // Permitir edición manual
                    unlockInput(nombreInput);
                    unlockInput(apellidoInput);
                    nombreInput.focus();
                }

            } catch (error) {
                console.error("❌ Error en consulta DNI:", error);
                showNotification("Error de conexión. Intenta nuevamente.", 'error');
                
                // Permitir edición manual
                unlockInput(nombreInput);
                unlockInput(apellidoInput);
                
            } finally {
                setButtonLoading(btnBuscarDNI, false);
            }
        });

        // Enter key en DNI
        dniInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                btnBuscarDNI.click();
            }
        });
    }

    // ==================== CONSULTAR RUC ====================
    
    if (btnBuscarRUC && rucInput && razonSocialInput) {
        btnBuscarRUC.addEventListener("click", async function () {
            const ruc = rucInput.value.trim();

            // Validaciones locales
            const validation = validarRUC(ruc);
            if (!validation.valid) {
                showNotification(validation.error, 'error');
                rucInput.focus();
                return;
            }

            // Deshabilitar botón
            setButtonLoading(btnBuscarRUC, true);

            try {
                console.log("🔍 Consultando RUC:", ruc);
                
                const response = await fetch(`/users/api/consultar-ruc/?ruc=${ruc}`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();
                console.log("📦 Respuesta:", data);

                if (response.ok && data.success && data.data) {
                    const info = data.data;
                    
                    // Llenar campo
                    razonSocialInput.value = info.razon_social || "";
                    
                    // Hacer campo editable
                    unlockInput(razonSocialInput);
                    
                    showNotification('✅ Razón social cargada correctamente', 'success');
                    
                    // Enfocar siguiente campo
                    const telefonoInput = document.querySelector('input[name="telefono"]');
                    if (telefonoInput) telefonoInput.focus();
                    
                } else {
                    const errorMsg = data.error || "No se encontró información para el RUC ingresado";
                    showNotification(errorMsg, 'error');
                    
                    // Permitir edición manual
                    unlockInput(razonSocialInput);
                    razonSocialInput.focus();
                }

            } catch (error) {
                console.error("❌ Error en consulta RUC:", error);
                showNotification("Error de conexión. Intenta nuevamente.", 'error');
                
                // Permitir edición manual
                unlockInput(razonSocialInput);
                
            } finally {
                setButtonLoading(btnBuscarRUC, false);
            }
        });

        // Enter key en RUC
        rucInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                btnBuscarRUC.click();
            }
        });
    }

    // ==================== PASSWORD TOGGLE ====================
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.dataset.target;
            const input = document.getElementById(targetId);
            
            if (input) {
                if (input.type === 'password') {
                    input.type = 'text';
                    this.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                            <line x1="1" y1="1" x2="23" y2="23"></line>
                        </svg>
                    `;
                } else {
                    input.type = 'password';
                    this.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                    `;
                }
            }
        });
    });

    // ==================== VALIDACIÓN DE FORMULARIO ====================
    
    if (form) {
        form.addEventListener('submit', function(e) {
            let hasErrors = false;
            const errors = [];

            // Validar campos según tipo
            if (nombreInput && !nombreInput.value.trim()) {
                errors.push('Por favor busca el DNI primero o completa tu nombre');
                hasErrors = true;
            }

            if (apellidoInput && !apellidoInput.value.trim()) {
                errors.push('Por favor completa tus apellidos');
                hasErrors = true;
            }

            if (razonSocialInput && !razonSocialInput.value.trim()) {
                errors.push('Por favor busca el RUC primero o completa la razón social');
                hasErrors = true;
            }

            // Validar email
            const emailInput = document.querySelector('input[name="email"]');
            if (emailInput && emailInput.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(emailInput.value)) {
                    errors.push('El formato del correo electrónico no es válido');
                    hasErrors = true;
                }
            }

            // Validar contraseñas
            const password1 = document.getElementById('id_password1');
            const password2 = document.getElementById('id_password2');
            
            if (password1 && password2) {
                if (password1.value !== password2.value) {
                    errors.push('Las contraseñas no coinciden');
                    hasErrors = true;
                }
                if (password1.value.length < 8) {
                    errors.push('La contraseña debe tener al menos 8 caracteres');
                    hasErrors = true;
                }
            }

            // Validar términos
            const terminosCheckbox = document.getElementById('acepto_terminos');
            if (terminosCheckbox && !terminosCheckbox.checked) {
                errors.push('Debes aceptar los términos y condiciones');
                hasErrors = true;
            }

            if (hasErrors) {
                e.preventDefault();
                errors.forEach(error => showNotification(error, 'error'));
                return false;
            }

            // Mostrar loading en botón submit
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                setButtonLoading(submitBtn, true);
            }
        });
    }

    // ==================== VALIDACIÓN EN TIEMPO REAL ====================
    
    // Email validation
    const emailInput = document.querySelector('input[name="email"]');
    if (emailInput) {
        let emailTimeout;
        emailInput.addEventListener('input', function() {
            clearTimeout(emailTimeout);
            emailTimeout = setTimeout(() => {
                const email = this.value.trim();
                if (email) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (emailRegex.test(email)) {
                        // Validar si existe (opcional)
                        fetch(`/users/validar-correo/?email=${encodeURIComponent(email)}`)
                            .then(r => r.json())
                            .then(data => {
                                if (data.exists) {
                                    this.style.borderColor = '#dc2626';
                                    showNotification('Este correo ya está registrado', 'error');
                                } else {
                                    this.style.borderColor = '#10b981';
                                }
                            })
                            .catch(() => {});
                    }
                }
            }, 500);
        });
    }

    // Password strength indicator (opcional)
    const password1 = document.getElementById('id_password1');
    if (password1) {
        password1.addEventListener('input', function() {
            const value = this.value;
            if (value.length < 8) {
                this.style.borderColor = '#dc2626';
            } else if (value.length < 12) {
                this.style.borderColor = '#f59e0b';
            } else {
                this.style.borderColor = '#10b981';
            }
        });
    }

    console.log("✅ Todas las funcionalidades de step_1.js inicializadas");
});

// Agregar estilos de animación
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);