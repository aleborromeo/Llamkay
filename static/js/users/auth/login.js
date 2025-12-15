// =============================================
// LOGIN - LLAMKAY.PE
// JavaScript Optimizado con Validaciones
// =============================================

(function() {
    'use strict';

    // ==================== ELEMENTOS DEL DOM ====================
    const form = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const submitBtn = form?.querySelector('.btn-submit');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');

    // ==================== MENSAJES DE ERROR (i18n ready) ====================
    const errorMessages = {
        email: {
            required: 'El correo electrónico es obligatorio',
            invalid: 'Por favor ingresa un correo electrónico válido',
            format: 'El formato del correo no es correcto'
        },
        password: {
            required: 'La contraseña es obligatoria',
            minLength: 'La contraseña debe tener al menos 6 caracteres',
            weak: 'La contraseña es demasiado débil'
        }
    };

    // ==================== UTILIDADES ====================
    
    /**
     * Valida formato de email
     * @param {string} email
     * @returns {boolean}
     */
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email.trim());
    }

    /**
     * Muestra mensaje de error en un campo
     * @param {HTMLElement} input
     * @param {HTMLElement} errorElement
     * @param {string} message
     */
    function showError(input, errorElement, message) {
        input.setAttribute('aria-invalid', 'true');
        input.style.borderColor = 'var(--color-danger)';
        
        errorElement.textContent = message;
        errorElement.classList.add('active');
        
        // Animación de shake
        input.style.animation = 'shake 0.5s';
        setTimeout(() => {
            input.style.animation = '';
        }, 500);
    }

    /**
     * Limpia error de un campo
     * @param {HTMLElement} input
     * @param {HTMLElement} errorElement
     */
    function clearError(input, errorElement) {
        input.setAttribute('aria-invalid', 'false');
        input.style.borderColor = '';
        
        errorElement.textContent = '';
        errorElement.classList.remove('active');
    }

    /**
     * Valida el campo de email
     * @returns {boolean}
     */
    function validateEmail() {
        const email = emailInput.value.trim();
        
        if (!email) {
            showError(emailInput, emailError, errorMessages.email.required);
            return false;
        }
        
        if (!isValidEmail(email)) {
            showError(emailInput, emailError, errorMessages.email.invalid);
            return false;
        }
        
        clearError(emailInput, emailError);
        return true;
    }

    /**
     * Valida el campo de contraseña
     * @returns {boolean}
     */
    function validatePassword() {
        const password = passwordInput.value;
        
        if (!password) {
            showError(passwordInput, passwordError, errorMessages.password.required);
            return false;
        }
        
        if (password.length < 6) {
            showError(passwordInput, passwordError, errorMessages.password.minLength);
            return false;
        }
        
        clearError(passwordInput, passwordError);
        return true;
    }

    /**
     * Establece estado de carga en el botón
     * @param {boolean} loading
     */
    function setLoadingState(loading) {
        if (loading) {
            submitBtn.setAttribute('aria-busy', 'true');
            submitBtn.disabled = true;
        } else {
            submitBtn.setAttribute('aria-busy', 'false');
            submitBtn.disabled = false;
        }
    }

    // ==================== TOGGLE DE CONTRASEÑA ====================
    
    if (togglePasswordBtn && passwordInput) {
        const eyeOpen = togglePasswordBtn.querySelector('.eye-open');
        const eyeClosed = togglePasswordBtn.querySelector('.eye-closed');
        
        togglePasswordBtn.addEventListener('click', function() {
            const isPassword = passwordInput.type === 'password';
            
            // Cambiar tipo de input
            passwordInput.type = isPassword ? 'text' : 'password';
            
            // Cambiar icono
            if (isPassword) {
                eyeOpen.style.display = 'none';
                eyeClosed.style.display = 'block';
            } else {
                eyeOpen.style.display = 'block';
                eyeClosed.style.display = 'none';
            }
            
            // Actualizar ARIA
            this.setAttribute('aria-label', 
                isPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'
            );
            this.setAttribute('aria-pressed', isPassword ? 'true' : 'false');
            
            // Mantener foco en el input
            passwordInput.focus();
        });
    }

    // ==================== VALIDACIÓN EN TIEMPO REAL ====================
    
    // Email: validar al perder foco
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            if (this.value.trim()) {
                validateEmail();
            }
        });
        
        // Limpiar error al escribir
        emailInput.addEventListener('input', function() {
            if (this.getAttribute('aria-invalid') === 'true') {
                clearError(this, emailError);
            }
        });
    }

    // Password: validar al perder foco
    if (passwordInput) {
        passwordInput.addEventListener('blur', function() {
            if (this.value) {
                validatePassword();
            }
        });
        
        // Limpiar error al escribir
        passwordInput.addEventListener('input', function() {
            if (this.getAttribute('aria-invalid') === 'true') {
                clearError(this, passwordError);
            }
        });
    }

    // ==================== VALIDACIÓN DEL FORMULARIO ====================
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Validar campos
            const isEmailValid = validateEmail();
            const isPasswordValid = validatePassword();
            
            // Si hay errores, prevenir envío
            if (!isEmailValid || !isPasswordValid) {
                e.preventDefault();
                
                // Enfocar primer campo con error
                if (!isEmailValid) {
                    emailInput.focus();
                } else if (!isPasswordValid) {
                    passwordInput.focus();
                }
                
                return false;
            }
            
            // Activar estado de carga
            setLoadingState(true);
        });
    }

    // ==================== SOPORTE PARA ENTER ====================
    
    // Enviar con Enter en cualquier campo
    [emailInput, passwordInput].forEach(input => {
        if (input) {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    form.dispatchEvent(new Event('submit', { cancelable: true }));
                }
            });
        }
    });

    // ==================== ANIMACIONES DE ENTRADA ====================
    
    const formElements = document.querySelectorAll('.form-group, .form-options, .btn-submit, .form-footer');
    formElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.4s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100 * index);
    });

    // ==================== EFECTO HOVER EN INPUTS ====================
    
    const allInputs = document.querySelectorAll('.form-input');
    allInputs.forEach(input => {
        const parent = input.closest('.form-group');
        
        input.addEventListener('focus', function() {
            if (parent) {
                parent.style.transform = 'translateY(-2px)';
                parent.style.transition = 'transform 0.2s ease';
            }
        });
        
        input.addEventListener('blur', function() {
            if (parent) {
                parent.style.transform = 'translateY(0)';
            }
        });
    });

    // ==================== AUTO-GUARDAR EMAIL (OPCIONAL) ====================
    
    if (emailInput) {
        // Cargar email guardado
        const savedEmail = localStorage.getItem('llamkay_last_email');
        if (savedEmail && !emailInput.value) {
            emailInput.value = savedEmail;
        }
        
        // Guardar email al cambiar
        emailInput.addEventListener('change', function() {
            if (this.value && isValidEmail(this.value)) {
                localStorage.setItem('llamkay_last_email', this.value);
            }
        });
    }

    // ==================== MANEJO DE ERRORES DEL SERVIDOR ====================
    
    // Si hay un alert de error, hacer scroll hacia él
    const alert = document.querySelector('.alert-error');
    if (alert) {
        alert.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Animación de atención
        alert.style.animation = 'pulse 0.5s ease 2';
    }

    // ==================== ESTILOS CSS DINÁMICOS ====================
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .form-input.error {
            animation: shake 0.5s;
        }
        
        .checkbox-wrapper:hover .checkbox-custom {
            transform: scale(1.05);
        }
        
        .form-input:focus + .password-toggle {
            color: var(--color-primary);
        }
    `;
    document.head.appendChild(style);

    // ==================== ACCESIBILIDAD: ANUNCIAR ERRORES ====================
    
    /**
     * Anuncia un mensaje a lectores de pantalla
     * @param {string} message
     */
    function announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('role', 'status');
        announcement.setAttribute('aria-live', 'polite');
        announcement.className = 'sr-only';
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            announcement.remove();
        }, 3000);
    }

    // ==================== DETECCIÓN DE CAMPOS VACÍOS AL SALIR ====================
    
    window.addEventListener('beforeunload', function(e) {
        // Si hay datos en el formulario pero no se envió
        if ((emailInput?.value || passwordInput?.value) && !form?.dataset.submitted) {
            e.preventDefault();
            e.returnValue = '¿Seguro que quieres salir? Los datos del formulario se perderán.';
        }
    });

    // Marcar como enviado al hacer submit
    if (form) {
        form.addEventListener('submit', function() {
            this.dataset.submitted = 'true';
        });
    }

    // ==================== LOG DE INICIALIZACIÓN ====================
    
    console.log('✅ Login JS completamente cargado');
    console.log('📋 Validaciones activas:', {
        email: !!emailInput,
        password: !!passwordInput,
        toggle: !!togglePasswordBtn,
        form: !!form
    });
    
})();