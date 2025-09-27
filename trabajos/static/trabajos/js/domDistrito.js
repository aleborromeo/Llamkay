document.addEventListener('DOMContentLoaded', () => {
    const provinciaSelect = document.getElementById('provincia');
    const distritoSelect = document.getElementById('distrito');

    if (!provinciaSelect || !distritoSelect) return;

    provinciaSelect.addEventListener('change', async (event) => {
        const provinciaId = event.target.value;
        distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';

        if (provinciaId) {
            try {
                const response = await fetch(`${urlCargarDistritos}?provincia_id=${provinciaId}`);
                if (!response.ok) throw new Error('Error al cargar distritos');
                const data = await response.json();

                data.forEach(distrito => {
                    const option = document.createElement('option');
                    option.value = distrito.id_distrito;
                    option.textContent = distrito.nombre;
                    distritoSelect.appendChild(option);
                });
            } catch (error) {
                console.error(error);
            }
        }
    });
});
