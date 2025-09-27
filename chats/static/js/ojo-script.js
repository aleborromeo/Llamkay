document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.querySelector('.toggle-password');
    const passwordInput = document.getElementById('password');
    const eyeOpen = toggleButton.querySelector('.eye-open');
    const eyeClosed = toggleButton.querySelector('.eye-closed');

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
    } else {
        console.error("No se encontraron elementos necesarios para el toggle de contraseña");
    }
});
