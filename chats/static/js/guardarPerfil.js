function editProfile() {
  document.getElementById('editProfileModal').style.display = 'flex';
}

function cerrarModalEdicion() {
  document.getElementById('editProfileModal').style.display = 'none';
}

document.getElementById('form-editar-perfil').addEventListener('submit', function(e) {
  e.preventDefault();
  const formData = new FormData(this);

  fetch('{% url "usuarios:actualizar_perfil" %}', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': '{{ csrf_token }}'
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert('Perfil actualizado correctamente');
      location.reload();
    } else {
      alert('Error al actualizar: ' + (data.error || 'Intenta de nuevo.'));
    }
  })
  .catch(err => alert('Error en la petición.'));
});