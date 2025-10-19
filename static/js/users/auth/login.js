// ===== LOGIN - Toggle de Contraseña =====

document.addEventListener('DOMContentLoaded', function () {
    console.log('🔐 Login JS iniciado');
    
    const toggleButton = document.querySelector('.toggle-password');
    const passwordInput = document.getElementById('password');
    const eyeOpen = toggleButton?.querySelector('.eye-open');
    const eyeClosed = toggleButton?.querySelector('.eye-closed');

    if (toggleButton && passwordInput && eyeOpen && eyeClosed) {
        toggleButton.addEventListener('click', function () {
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                eyeOpen.style.display = 'none';
                eyeClosed.style.display = 'inline';
            } else {
                passwordInput.type = 'password';
                eyeOpen.style.display = 'inline';
                eyeClosed.style.display = 'none';
            }
        });
        
        console.log('✅ Toggle de contraseña configurado');
    } else {
        console.warn('⚠️ No se encontraron elementos para toggle de contraseña');
    }
    
    // Validación de formulario
    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            
            if (!email.value.trim()) {
                e.preventDefault();
                showNotification('Por favor ingresa tu email', 'error');
                email.focus();
                return false;
            }
            
            if (!password.value.trim()) {
                e.preventDefault();
                showNotification('Por favor ingresa tu contraseña', 'error');
                password.focus();
                return false;
            }
        });
    }
    
    console.log('✅ Login JS listo');
});