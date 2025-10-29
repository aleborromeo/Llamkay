// =============================================
// LOGIN - LLAMKAY.PE (JAVASCRIPT MODERNO)
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('🔐 Login JS iniciado');
    
    // ==================== TOGGLE DE CONTRASEÑA ====================
    const togglePasswordBtn = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const eyeOpen = document.querySelector('.eye-open');
    const eyeClosed = document.querySelector('.eye-closed');

    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener('click', function () {
            const type = passwordInput.type === 'password' ? 'text' : 'password';
            passwordInput.type = type;
            
            if (type === 'text') {
                eyeOpen.style.display = 'none';
                eyeClosed.style.display = 'block';
            } else {
                eyeOpen.style.display = 'block';
                eyeClosed.style.display = 'none';
            }
        });
        console.log('✅ Toggle de contraseña configurado');
    }

    // ==================== VALIDACIÓN DE FORMULARIO ====================
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');

    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            let isValid = true;
            
            // Validar email
            if (!emailInput.value.trim()) {
                e.preventDefault();
                showError(emailInput, 'Por favor ingresa tu email');
                isValid = false;
            } else if (!isValidEmail(emailInput.value)) {
                e.preventDefault();
                showError(emailInput, 'Por favor ingresa un email válido');
                isValid = false;
            } else {
                removeError(emailInput);
            }
            
            // Validar contraseña
            if (!passwordInput.value.trim()) {
                e.preventDefault();
                showError(passwordInput, 'Por favor ingresa tu contraseña');
                isValid = false;
            } else if (passwordInput.value.length < 6) {
                e.preventDefault();
                showError(passwordInput, 'La contraseña debe tener al menos 6 caracteres');
                isValid = false;
            } else {
                removeError(passwordInput);
            }
            
            if (!isValid) {
                return false;
            }
        });
        
        // Validación en tiempo real
        emailInput.addEventListener('blur', function () {
            if (this.value.trim() && !isValidEmail(this.value)) {
                showError(this, 'Email inválido');
            } else {
                removeError(this);
            }
        });
        
        emailInput.addEventListener('input', function () {
            if (this.classList.contains('error')) {
                removeError(this);
            }
        });
        
        passwordInput.addEventListener('input', function () {
            if (this.classList.contains('error')) {
                removeError(this);
            }
        });
        
        console.log('✅ Validación de formulario configurada');
    }

    // ==================== FUNCIONES AUXILIARES ====================
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function showError(input, message) {
        input.classList.add('error');
        input.style.borderColor = 'var(--color-danger)';
        
        // Remover mensaje de error anterior si existe
        const existingError = input.parentElement.querySelector('.error-text');
        if (existingError) {
            existingError.remove();
        }
        
        // Crear nuevo mensaje de error
        const errorText = document.createElement('span');
        errorText.className = 'error-text';
        errorText.style.color = 'var(--color-danger)';
        errorText.style.fontSize = '0.85rem';
        errorText.style.marginTop = '0.25rem';
        errorText.style.display = 'block';
        errorText.textContent = message;
        
        if (input.parentElement.classList.contains('password-wrapper')) {
            input.parentElement.parentElement.appendChild(errorText);
        } else {
            input.parentElement.appendChild(errorText);
        }
        
        // Shake animation
        input.style.animation = 'shake 0.5s';
        setTimeout(() => {
            input.style.animation = '';
        }, 500);
    }

    function removeError(input) {
        input.classList.remove('error');
        input.style.borderColor = '';
        
        const errorText = input.parentElement.querySelector('.error-text') || 
                         input.parentElement.parentElement.querySelector('.error-text');
        if (errorText) {
            errorText.remove();
        }
    }

    // ==================== ANIMACIÓN DE ENTRADA ====================
    const formElements = document.querySelectorAll('.form-group, .form-options, .btn-submit');
    formElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.4s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100 * index);
    });

    // ==================== ANIMACIÓN DEL BOTÓN AL ENVIAR ====================
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            const submitBtn = this.querySelector('.btn-submit');
            if (submitBtn && !this.querySelector('.error')) {
                submitBtn.innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10" stroke-dasharray="63" stroke-dashoffset="63">
                            <animate attributeName="stroke-dashoffset" from="63" to="0" dur="1s" repeatCount="indefinite"/>
                        </circle>
                    </svg>
                    <span>Iniciando sesión...</span>
                `;
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
            }
        });
    }

    // ==================== EFECTO HOVER EN INPUTS ====================
    const allInputs = document.querySelectorAll('.form-input');
    allInputs.forEach(input => {
        input.addEventListener('focus', function () {
            this.parentElement.style.transform = 'translateY(-2px)';
            this.parentElement.style.transition = 'transform 0.2s ease';
        });
        
        input.addEventListener('blur', function () {
            this.parentElement.style.transform = 'translateY(0)';
        });
    });

    // ==================== ANIMACIÓN CSS ADICIONAL ====================
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        .form-input.error {
            animation: shake 0.5s;
        }
        
        .btn-submit:disabled {
            cursor: not-allowed;
        }
        
        .checkbox-wrapper:hover .checkbox-custom {
            border-color: var(--color-primary);
            transform: scale(1.05);
        }
        
        .form-input:focus + .password-toggle {
            color: var(--color-primary);
        }
    `;
    document.head.appendChild(style);

    console.log('✅ Login JS completamente cargado');
});