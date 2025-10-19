// Gestión de ubicación (Departamento -> Provincia -> Distrito -> Comunidad)

document.addEventListener('DOMContentLoaded', function () {
  const departamentoSelect = document.getElementById('departamento');
  const provinciaSelect = document.getElementById('provincia');
  const distritoSelect = document.getElementById('distrito');
  const comunidadSelect = document.getElementById('comunidad');

  if (!departamentoSelect) return;

  // Cargar provincias al cambiar departamento
  departamentoSelect.addEventListener('change', function () {
    const departamentoId = this.value;
    
    if (!departamentoId) {
      resetSelect(provinciaSelect, 'Ciudad');
      resetSelect(distritoSelect, 'Distrito');
      resetSelect(comunidadSelect, 'Comunidad');
      return;
    }

    fetch(`/trabajos/ajax/cargar-provincias/?departamento_id=${departamentoId}`)
      .then(response => response.json())
      .then(data => {
        populateSelect(provinciaSelect, data, 'id_provincia', 'nombre', 'Ciudad');
        resetSelect(distritoSelect, 'Distrito');
        resetSelect(comunidadSelect, 'Comunidad');
      })
      .catch(error => console.error('Error al cargar provincias:', error));
  });

  // Cargar distritos al cambiar provincia
  provinciaSelect.addEventListener('change', function () {
    const provinciaId = this.value;
    
    if (!provinciaId) {
      resetSelect(distritoSelect, 'Distrito');
      resetSelect(comunidadSelect, 'Comunidad');
      return;
    }

    fetch(`/trabajos/ajax/cargar-distritos/?provincia_id=${provinciaId}`)
      .then(response => response.json())
      .then(data => {
        populateSelect(distritoSelect, data, 'id_distrito', 'nombre', 'Distrito');
        resetSelect(comunidadSelect, 'Comunidad');
      })
      .catch(error => console.error('Error al cargar distritos:', error));
  });

  // Cargar comunidades al cambiar distrito
  distritoSelect.addEventListener('change', function () {
    const distritoId = this.value;
    
    if (!distritoId) {
      resetSelect(comunidadSelect, 'Comunidad');
      return;
    }

    fetch(`/trabajos/ajax/cargar-comunidades/?distrito_id=${distritoId}`)
      .then(response => response.json())
      .then(data => {
        populateSelect(comunidadSelect, data, 'id_comunidad', 'nombre', 'Comunidad');
      })
      .catch(error => console.error('Error al cargar comunidades:', error));
  });
});

// Función auxiliar para resetear un select
function resetSelect(selectElement, placeholder) {
  selectElement.innerHTML = `<option value="">${placeholder}</option>`;
}

// Función auxiliar para poblar un select
function populateSelect(selectElement, data, idKey, nameKey, placeholder) {
  selectElement.innerHTML = `<option value="">${placeholder}</option>`;
  data.forEach(function (item) {
    const option = document.createElement('option');
    option.value = item[idKey];
    option.textContent = item[nameKey];
    selectElement.appendChild(option);
  });
}