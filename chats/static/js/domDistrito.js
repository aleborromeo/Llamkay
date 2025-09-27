document.addEventListener('DOMContentLoaded', () => {
    const distritoSelect = document.getElementById('distrito');
    const provinciaSelect = document.getElementById('provincia');

    provinciaSelect.addEventListener('change', async (event) => {
        const provinciaId = event.target.value;
        console.log(provinciaId);
        distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';

        if (provinciaId) {
            try {
                const response = await fetch(`/ajax/cargar-distritos/?provincia_id=${provinciaId}`);
                if (!response.ok) throw new Error('No se capturaron correctamente los datos');

                const data = await response.json();

                data.forEach(distrito => {
                    const option = document.createElement('option');
                    option.value = distrito.id_distrito;
                    option.textContent = distrito.nombre;
                    distritoSelect.appendChild(option);
                });

            } catch (error) {
                console.error('Error al cargar distritos:', error);
            }
        }
    });
});