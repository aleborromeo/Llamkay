// === Función para obtener el token CSRF ===
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// === Función para buscar RUC ===
function buscarRUC(event) {
    const ruc = document.getElementById('id_ruc').value;

    if (!ruc || ruc.length !== 11) {
        alert('Por favor ingresa un RUC válido de 11 dígitos');
        return;
    }

    const btnBuscar = event.target;
    const textoOriginal = btnBuscar.textContent;
    btnBuscar.textContent = 'Buscando...';
    btnBuscar.disabled = true;

    const csrftoken = getCookie('csrftoken');

    fetch(`/usuarios/buscar-ruc/?ruc=${ruc}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                const razonSocialInput = document.getElementById('id_razon_social');
                if (razonSocialInput && razonSocialInput.actualizarValor) {
                    razonSocialInput.actualizarValor(data.razon_social || '');
                } else {
                    razonSocialInput.value = data.razon_social || '';
                }
                mostrarMensaje('Datos de la empresa cargados correctamente', 'success');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarMensaje('Error al buscar el RUC. Intenta nuevamente.', 'error');
        })
        .finally(() => {
            btnBuscar.textContent = textoOriginal;
            btnBuscar.disabled = false;
        });
}

// === Función para buscar DNI ===
function buscarDNI(event) {
    const dni = document.getElementById('id_dni').value;

    if (!dni || dni.length !== 8) {
        alert('Por favor ingresa un DNI válido de 8 dígitos');
        return;
    }

    const btnBuscar = event.target;
    const textoOriginal = btnBuscar.textContent;
    btnBuscar.textContent = 'Buscando...';
    btnBuscar.disabled = true;

    const csrftoken = getCookie('csrftoken');

    fetch(`/usuarios/buscar-dni/?dni=${dni}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                const nombreInput = document.getElementById('id_nombre');
                const apellidoInput = document.getElementById('id_apellido');

                let apellidos = '';
                if (data.apellido_paterno) apellidos += data.apellido_paterno;
                if (data.apellido_materno) apellidos += ' ' + data.apellido_materno;

                if (nombreInput && nombreInput.actualizarValor) {
                    nombreInput.actualizarValor(data.nombres || '');
                } else {
                    nombreInput.value = data.nombres || '';
                }

                if (apellidoInput && apellidoInput.actualizarValor) {
                    apellidoInput.actualizarValor(apellidos.trim());
                } else {
                    apellidoInput.value = apellidos.trim();
                }

                mostrarMensaje('Datos del DNI cargados correctamente', 'success');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarMensaje('Error al buscar el DNI. Intenta nuevamente.', 'error');
        })
        .finally(() => {
            btnBuscar.textContent = textoOriginal;
            btnBuscar.disabled = false;
        });
}

// === Función para mostrar mensajes flotantes ===
function mostrarMensaje(mensaje, tipo) {
    const mensajeAnterior = document.querySelector('.mensaje-temporal');
    if (mensajeAnterior) {
        mensajeAnterior.remove();
    }

    const div = document.createElement('div');
    div.className = `mensaje-temporal alert-${tipo}`;
    div.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 4px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        ${tipo === 'success' ? 'background-color: #28a745;' : 'background-color: #dc3545;'}
    `;
    div.textContent = mensaje;

    if (!document.querySelector('#mensaje-styles')) {
        const style = document.createElement('style');
        style.id = 'mensaje-styles';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(div);
    setTimeout(() => div.remove(), 3000);
}

// === Validación de solo números para campos DNI y RUC ===
document.addEventListener('DOMContentLoaded', function () {
    const dniInput = document.getElementById('id_dni');
    const rucInput = document.getElementById('id_ruc');

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
    }

    if (rucInput) {
        rucInput.addEventListener('keydown', soloNumeros);
        rucInput.addEventListener('input', function () {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 11);
        });
    }
});