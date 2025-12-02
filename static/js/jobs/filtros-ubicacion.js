// ===========================================================
// FILTROS UBICACIÓN - BUSCAR TRABAJOS
// Versión 3.0 - Cascada dinámica (Departamento → Provincia → Distrito)
// ===========================================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ filtros_ubicacion.js cargado correctamente');

    // ==================== ELEMENTOS ====================
    const departamentoSelect = document.getElementById('departamento');
    const provinciaSelect = document.getElementById('provincia');
    const distritoSelect = document.getElementById('distrito');

    if (!departamentoSelect || !provinciaSelect || !distritoSelect) {
        console.error('⚠️ No se encontraron los selectores de ubicación');
        return;
    }

    // ==================== CONFIGURACIÓN ====================
    // Estas URLs deben ser definidas en el template con {% url 'api:provincias' %}, etc.
    if (typeof urlProvincias === 'undefined' || typeof urlDistritos === 'undefined') {
        console.error('⚠️ URLs de provincias/distritos no definidas.');
        return;
    }

    // ==================== FUNCIONES UTILITARIAS ====================
    function resetSelect(select, placeholder, disabled = true) {
        select.innerHTML = `<option value="">${placeholder}</option>`;
        select.disabled = disabled;
    }

    function populateSelect(select, data, valueKey, textKey) {
        select.innerHTML = '<option value="">Selecciona una opción</option>';
        data.forEach(item => {
            const opt = document.createElement('option');
            opt.value = item[valueKey];
            opt.textContent = item[textKey];
            select.appendChild(opt);
        });
        select.disabled = false;
    }

    function setLoading(select) {
        select.disabled = true;
        select.innerHTML = '<option value="">Cargando...</option>';
    }

    // ==================== EVENTOS ====================

    // 🔹 Cargar provincias al cambiar departamento
    departamentoSelect.addEventListener('change', async function () {
        const departamentoId = this.value;
        console.log('📍 Departamento seleccionado:', departamentoId);

        resetSelect(provinciaSelect, 'Selecciona una provincia', true);
        resetSelect(distritoSelect, 'Selecciona un distrito', true);

        if (!departamentoId) return;

        try {
            setLoading(provinciaSelect);
            const url = `${urlProvincias}?id_departamento=${departamentoId}`;
            const response = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
            const data = await response.json();

            if (Array.isArray(data) && data.length > 0) {
                populateSelect(provinciaSelect, data, 'id_provincia', 'nombre');
                console.log(`✅ ${data.length} provincias cargadas`);
            } else {
                resetSelect(provinciaSelect, 'No hay provincias disponibles');
            }
        } catch (error) {
            console.error('❌ Error al cargar provincias:', error);
            resetSelect(provinciaSelect, 'Error al cargar provincias');
        }
    });

    // 🔹 Cargar distritos al cambiar provincia
    provinciaSelect.addEventListener('change', async function () {
        const provinciaId = this.value;
        console.log('📍 Provincia seleccionada:', provinciaId);

        resetSelect(distritoSelect, 'Selecciona un distrito', true);

        if (!provinciaId) return;

        try {
            setLoading(distritoSelect);
            const url = `${urlDistritos}?id_provincia=${provinciaId}`;
            const response = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
            const data = await response.json();

            if (Array.isArray(data) && data.length > 0) {
                populateSelect(distritoSelect, data, 'id_distrito', 'nombre');
                console.log(`✅ ${data.length} distritos cargados`);
            } else {
                resetSelect(distritoSelect, 'No hay distritos disponibles');
            }
        } catch (error) {
            console.error('❌ Error al cargar distritos:', error);
            resetSelect(distritoSelect, 'Error al cargar distritos');
        }
    });

    console.log('✅ filtros_ubicacion.js listo');
});
