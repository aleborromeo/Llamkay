document.addEventListener('DOMContentLoaded', function () {
    const toggleButtons = document.querySelectorAll('.toggle-password');

    toggleButtons.forEach(function (toggle) {
        toggle.addEventListener('click', function () {
            const formGroup = toggle.closest('.form-group');
            const passwordInput = formGroup.querySelector('.password-input') || formGroup.querySelector('input[type="password"], input[type="text"]');
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
            } else {
                console.error('Faltan elementos dentro de .form-group para alternar contraseña');
            }
        });
    });
});
