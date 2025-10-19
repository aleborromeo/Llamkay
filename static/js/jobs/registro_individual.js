// Funcionalidad para registro individual

document.addEventListener('DOMContentLoaded', function () {
  // Botón volver
  const btnVolver = document.getElementById('btn-volver');
  if (btnVolver && typeof urlVolver !== 'undefined') {
    btnVolver.addEventListener('click', function() {
      window.location.href = urlVolver;
    });
  }

  // Preview de imagen
  const fotoInput = document.querySelector('input[type="file"]');
  const previewImagen = document.getElementById('preview-imagen');
  
  if (fotoInput && previewImagen) {
    fotoInput.addEventListener('change', function(event) {
      const archivo = event.target.files[0];
      if (archivo) {
        const lector = new FileReader();
        lector.onload = function(e) {
          previewImagen.src = e.target.result;
          previewImagen.style.display = 'block';
        };
        lector.readAsDataURL(archivo);
      } else {
        previewImagen.src = '';
        previewImagen.style.display = 'none';
      }
    });
  }

  // Ubicación AJAX
  cargarUbicacionAjax();

  // Validación número de WhatsApp
  validarNumeroWhatsApp();
});

function cargarUbicacionAjax() {
  const departamentoSelect = document.getElementById('id_id_departamento');
  const provinciaSelect = document.getElementById('id_id_provincia');
  const distritoSelect = document.getElementById('id_id_distrito');
  const comunidadSelect = document.getElementById('id_id_comunidad');

  if (!departamentoSelect) return;

  departamentoSelect.addEventListener('change', function () {
    const departamentoId = this.value;
    if (!departamentoId) return;

    fetch(`${urlCargarProvincias}?departamento_id=${departamentoId}`)
      .then(response => response.json())
      .then(data => {
        provinciaSelect.innerHTML = '<option value="">Seleccione</option>';
        data.forEach(function (provincia) {
          provinciaSelect.innerHTML += `<option value="${provincia.id_provincia}">${provincia.nombre}</option>`;
        });
        distritoSelect.innerHTML = '<option value="">Seleccione</option>';
        comunidadSelect.innerHTML = '<option value="">Seleccione</option>';
      })
      .catch(error => console.error('Error:', error));
  });

  provinciaSelect.addEventListener('change', function () {
    const provinciaId = this.value;
    if (!provinciaId) return;

    fetch(`${urlCargarDistritos}?provincia_id=${provinciaId}`)
      .then(response => response.json())
      .then(data => {
        distritoSelect.innerHTML = '<option value="">Seleccione</option>';
        data.forEach(function (distrito) {
          distritoSelect.innerHTML += `<option value="${distrito.id_distrito}">${distrito.nombre}</option>`;
        });
        comunidadSelect.innerHTML = '<option value="">Seleccione</option>';
      })
      .catch(error => console.error('Error:', error));
  });

  distritoSelect.addEventListener('change', function () {
    const distritoId = this.value;
    if (!distritoId) return;

    fetch(`${urlCargarComunidades}?distrito_id=${distritoId}`)
      .then(response => response.json())
      .then(data => {
        comunidadSelect.innerHTML = '<option value="">Seleccione</option>';
        data.forEach(function (comunidad) {
          comunidadSelect.innerHTML += `<option value="${comunidad.id_comunidad}">${comunidad.nombre}</option>`;
        });
      })
      .catch(error => console.error('Error:', error));
  });
}

function validarNumeroWhatsApp() {
  const numeroContacto = document.getElementById('id_numero_contacto');
  const formTrabajo = document.getElementById('form-trabajo');
  
  if (!numeroContacto) return;

  numeroContacto.addEventListener('input', function() {
    let valor = this.value;
    
    // Remover caracteres no válidos excepto + y números
    valor = valor.replace(/[^\d+]/g, '');
    
    // Asegurar que empiece con +
    if (valor && !valor.startsWith('+')) {
      valor = '+' + valor;
    }
    
    this.value = valor;
    
    // Validar formato
    const isValid = /^\+?[1-9]\d{8,14}$/.test(valor);
    
    if (valor && !isValid) {
      this.style.borderColor = '#f44336';
      this.style.backgroundColor = '#ffebee';
    } else {
      this.style.borderColor = '#4caf50';
      this.style.backgroundColor = '#e8f5e8';
    }
  });
  
  // Validación al enviar el formulario
  if (formTrabajo) {
    formTrabajo.addEventListener('submit', function(e) {
      const numero = numeroContacto.value;
      if (!numero || !/^\+?[1-9]\d{8,14}$/.test(numero)) {
        e.preventDefault();
        alert('Por favor, ingrese un número de WhatsApp válido. Formato: +51999123456');
        numeroContacto.focus();
      }
    });
  }
}