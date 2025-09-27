document.addEventListener('DOMContentLoaded', function () {
    const departamentoSelect = document.getElementById('id_departamento');
    const provinciaSelect = document.getElementById('id_provincia');
    const distritoSelect = document.getElementById('id_distrito');

    departamentoSelect.addEventListener('change', function () {
        const departamentoId = this.value;
        fetch(`/usuarios/cargar_provincias/?id_departamento=${departamentoId}`)
            .then(response => response.json())
            .then(data => {
                provinciaSelect.innerHTML = '<option value="">Selecciona tu provincia</option>';
                distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
                data.forEach(function (provincia) {
                    const option = document.createElement('option');
                    option.value = provincia.id_provincia;
                    option.textContent = provincia.nombre;
                    provinciaSelect.appendChild(option);
                });
            });
    });

    provinciaSelect.addEventListener('change', function () {
        const provinciaId = this.value;
        fetch(`/usuarios/cargar_distritos/?id_provincia=${provinciaId}`)
            .then(response => response.json())
            .then(data => {
                distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
                data.forEach(function (distrito) {
                    const option = document.createElement('option');
                    option.value = distrito.id_distrito;
                    option.textContent = distrito.nombre;
                    distritoSelect.appendChild(option);
                });
            });
    });

     const emailInput = document.getElementById('id_email');

    // Crea el contenedor del mensaje si no existe
    let emailMessage = document.createElement('div');
    emailMessage.id = 'email-error-message';
    emailMessage.style.color = 'red';
    emailMessage.style.marginTop = '5px';
    emailInput.parentNode.insertBefore(emailMessage, emailInput.nextSibling);

    emailInput.addEventListener('blur', function () {
        const email = emailInput.value;
        if (email.trim() === '') return;

        fetch(`/usuarios/validar_correo/?email=${encodeURIComponent(email)}`)
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    emailMessage.textContent = '⚠️ El correo electrónico ya está en uso.';
                } else {
                    emailMessage.textContent = '';
                }
            })
            .catch(() => {
                emailMessage.textContent = 'Error al verificar el correo.';
            });
    });
});

