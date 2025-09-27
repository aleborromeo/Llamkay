function toggleFormFields() {
    const tipo = document.getElementById('tipoUsuario').value;
    const camposPersona = document.querySelector('.campos-persona');
    const camposEmpresa = document.querySelector('.campos-empresa');
    
    if (tipo === 'empresa') {
        if (camposPersona) camposPersona.style.display = 'none';
        if (camposEmpresa) camposEmpresa.style.display = 'block';
    } else {
        if (camposPersona) camposPersona.style.display = 'block';
        if (camposEmpresa) camposEmpresa.style.display = 'none';
    }
}

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', toggleFormFields);