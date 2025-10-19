// Funcionalidad para registro de empresa

document.addEventListener('DOMContentLoaded', function () {
  // Preview de imagen
  const fotoInput = document.getElementById('id_foto');
  const preview = document.getElementById('preview');
  
  if (fotoInput && preview) {
    fotoInput.addEventListener('change', previewImage);
  }

  // Ubicación AJAX
  cargarUbicacionEmpresa();
});

function previewImage(event) {
  const preview = document.getElementById('preview');
  const file = event.target.files[0];
  
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      preview.src = e.target.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  } else {
    preview.style.display = 'none';
    preview.src = '';
  }
}

function validarUbicacion() {
  const dpto = document.getElementById('id_id_departamento').value;
  const prov = document.getElementById('id_id_provincia').value;
  const dist = document.getElementById('id_id_distrito').value;
  const comu = document.getElementById('id_id_comunidad').value;
  
  if (!dpto && !prov && !dist && !comu) {
    alert("Debe completar al menos uno de los campos de ubicación.");
    return false;
  }
  return true;
}

function cargarUbicacionEmpresa() {
  const departamentoSelect = document.getElementById('id_id_departamento');
  const provinciaSelect = document.getElementById('id_id_provincia');
  const distritoSelect = document.getElementById('id_id_distrito');
  const comunidadSelect = document.getElementById('id_id_comunidad');

  if (!departamentoSelect) return;

  departamentoSelect.addEventListener('change', function () {
    const departamentoId = this.value;
    fetch(`${urlCargarProvincias}?departamento_id=${departamentoId}`)
      .then(response => response.json())
      .then(data => {
        provinciaSelect.innerHTML = '<option value="">Seleccione</option>';
        data.forEach(function (provincia) {
          provinciaSelect.innerHTML += `<option value="${provincia.id_provincia}">${provincia.nombre}</option>`;
        });
        distritoSelect.innerHTML = '<option value="">Seleccione</option>';
        comunidadSelect.innerHTML = '<option value="">Seleccione</option>';
      });
  });

  provinciaSelect.addEventListener('change', function () {
    const provinciaId = this.value;
    fetch(`${urlCargarDistritos}?provincia_id=${provinciaId}`)
      .then(response => response.json())
      .then(data => {
        distritoSelect.innerHTML = '<option value="">Seleccione</option>';
        data.forEach(function (distrito) {
          distritoSelect.innerHTML += `<option value="${distrito.id_distrito}">${distrito.nombre}</option>`;
        });
        comunidadSelect.innerHTML = '<option value="">Seleccione</option>';
      });
  });

  distritoSelect.addEventListener('change', function () {
    const distritoId = this.value;
    fetch(`${urlCargarComunidades}?distrito_id=${distritoId}`)
      .then(response => response.json())
      .then(data => {
        comunidadSelect.innerHTML = '<option value="">Seleccione</option>';
        data.forEach(function (comunidad) {
          comunidadSelect.innerHTML += `<option value="${comunidad.id_comunidad}">${comunidad.nombre}</option>`;
        });
      });
  });

  // Validación del formulario
  const formEmpresa = document.getElementById('form-empresa');
  if (formEmpresa) {
    formEmpresa.addEventListener('submit', function(e) {
      if (!validarUbicacion()) {
        e.preventDefault();
      }
    });
  }
}