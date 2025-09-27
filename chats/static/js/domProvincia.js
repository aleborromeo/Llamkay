document.addEventListener('DOMContentLoaded', () => {
    const departamentoSelect = document.getElementById('departamento');
    const provinciaSelect = document.getElementById('provincia');

    departamentoSelect.addEventListener('change', async (event) => {
        const departamentoId = event.target.value; // 1
        console.log(departamentoId);

        provinciaSelect.innerHTML = '<option value="">Selecciona tu provincia</option>';

        if (departamentoId) {
            try {
                const response = await fetch(`/ajax/cargar-provincias/?departamento_id=${departamentoId}`);
                if (!response.ok) throw new Error('Error en la respuesta');

                const data = await response.json();

                data.forEach(provincia => {
                    const option = document.createElement('option');
                    option.value = provincia.id_provincia;
                    option.textContent = provincia.nombre;
                    provinciaSelect.appendChild(option);
                });
            } catch (error) {
                console.error('Error al cargar provincias:', error);
            }
        }
    });
});