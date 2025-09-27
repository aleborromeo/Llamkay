document.addEventListener('DOMContentLoaded', () => {
    const distritoSelect = document.getElementById('distrito');
    const comunidadSelect = document.getElementById('comunidad');

    if (!distritoSelect || !comunidadSelect) return;

    distritoSelect.addEventListener('change', async (event) => {
        const distritoId = event.target.value;
        comunidadSelect.innerHTML = '<option value="">Selecciona tu comunidad</option>';

        if (distritoId) {
            try {
                const response = await fetch(`${urlCargarComunidades}?distrito_id=${distritoId}`);
                if (!response.ok) throw new Error('Error al cargar comunidades');
                const data = await response.json();

                data.forEach(comunidad => {
                    const option = document.createElement('option');
                    option.value = comunidad.id_comunidad;
                    option.textContent = comunidad.nombre;
                    comunidadSelect.appendChild(option);
                });
            } catch (error) {
                console.error(error);
            }
        }
    });
});
