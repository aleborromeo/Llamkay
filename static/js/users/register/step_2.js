// =============================================
// REGISTRO PASO 2 - UBICACIÓN (CASCADA)
// i18n + UX + Accesibilidad + Responsividad
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ step_2.js iniciado');

    // ==================== I18N ====================
    const i18n = {
        errorDireccion: document.body.dataset.i18nErrorDireccion,
        errorDepartamento: document.body.dataset.i18nErrorDepartamento,
        errorProvincia: document.body.dataset.i18nErrorProvincia,
        errorDistrito: document.body.dataset.i18nErrorDistrito,
        loading: document.body.dataset.i18nLoading || 'Cargando...',
        processing: document.body.dataset.i18nProcessing || 'Procesando...'
    };

    // ==================== ELEMENTOS ====================
    const departamentoSelect = document.getElementById('id_departamento');
    const provinciaSelect = document.getElementById('id_provincia');
    const distritoSelect = document.getElementById('id_distrito');
    const direccionInput = document.getElementById('id_direccion');
    const form = document.getElementById('location-form');

    if (!departamentoSelect || !provinciaSelect || !distritoSelect) {
        console.error('❌ Elementos de ubicación no encontrados');
        return;
    }

    if (typeof urlProvincias === 'undefined' || typeof urlDistritos === 'undefined') {
        console.error('❌ URLs de backend no definidas');
        return;
    }

    // ==================== NOTIFICACIONES ====================
    function showNotification(message, type = 'info') {
        const div = document.createElement('div');
        div.className = `notification ${type}`;
        div.setAttribute('role', 'alert');
        div.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#dc2626' : '#10b981'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,.2);
            z-index: 9999;
        `;
        div.textContent = message;
        document.body.appendChild(div);
        setTimeout(() => div.remove(), 3000);
    }

    // ==================== HELPERS ====================
    function resetSelect(select, text, disabled = true) {
        select.innerHTML = `<option value="">${text}</option>`;
        select.disabled = disabled;
    }

    function setLoading(select) {
        resetSelect(select, i18n.loading, true);
    }

    function populateSelect(select, items, idKey, labelKey) {
        resetSelect(select, '—', false);
        items.forEach(item => {
            const opt = document.createElement('option');
            opt.value = item[idKey];
            opt.textContent = item[labelKey];
            select.appendChild(opt);
        });
        select.disabled = false;
    }

    // ==================== DEPARTAMENTO → PROVINCIA ====================
    departamentoSelect.addEventListener('change', async function () {
        resetSelect(provinciaSelect, i18n.loading);
        resetSelect(distritoSelect, i18n.errorProvincia);

        if (!this.value) return;

        setLoading(provinciaSelect);

        try {
            const res = await fetch(`${urlProvincias}?id_departamento=${this.value}`);
            const data = await res.json();

            if (Array.isArray(data) && data.length) {
                populateSelect(provinciaSelect, data, 'id_provincia', 'nombre');
            } else {
                resetSelect(provinciaSelect, i18n.errorProvincia, true);
            }
        } catch {
            showNotification(i18n.errorProvincia, 'error');
        }
    });

    // ==================== PROVINCIA → DISTRITO ====================
    provinciaSelect.addEventListener('change', async function () {
        resetSelect(distritoSelect, i18n.loading);

        if (!this.value) return;

        setLoading(distritoSelect);

        try {
            const res = await fetch(`${urlDistritos}?id_provincia=${this.value}`);
            const data = await res.json();

            if (Array.isArray(data) && data.length) {
                populateSelect(distritoSelect, data, 'id_distrito', 'nombre');
            } else {
                resetSelect(distritoSelect, i18n.errorDistrito, true);
            }
        } catch {
            showNotification(i18n.errorDistrito, 'error');
        }
    });

    // ==================== VALIDACIÓN ====================
    form.addEventListener('submit', function (e) {
        const errors = [];

        if (!direccionInput.value.trim()) errors.push(i18n.errorDireccion);
        if (!departamentoSelect.value) errors.push(i18n.errorDepartamento);
        if (!provinciaSelect.value) errors.push(i18n.errorProvincia);
        if (!distritoSelect.value) errors.push(i18n.errorDistrito);

        if (errors.length) {
            e.preventDefault();
            errors.forEach(msg => showNotification(msg, 'error'));
            return;
        }

        const btn = form.querySelector('button[type="submit"]');
        if (btn) {
            btn.disabled = true;
            btn.innerText = i18n.processing;
        }
    });

    console.log('✅ step_2.js listo (i18n + UX)');
});
