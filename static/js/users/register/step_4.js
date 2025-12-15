// =============================================
// REGISTRO PASO 3 - PERFIL DEL USUARIO
// UX/UI + Nielsen + Gestalt + Accesibilidad
// =============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ step_3.js cargado');

    // =========================
    // ELEMENTOS
    // =========================
    const form = document.getElementById('profileForm');
    const tituloInput = document.getElementById('id_titulo');
    const descripcionInput = document.getElementById('id_descripcion');
    const experienciaSelect = document.getElementById('id_experiencia');
    const disponibilidadRadios = document.querySelectorAll('input[name="disponibilidad"]');
    const submitBtn = form?.querySelector('button[type="submit"]');

    if (!form) return;

    // =========================
    // HELPERS UX
    // =========================

    function setFieldState(field, valid) {
        if (!field) return;
        field.style.borderColor = valid ? '#10b981' : '#dc2626';
    }

    function clearFieldState(field) {
        if (!field) return;
        field.style.borderColor = '';
    }

    function getSelectedRadioValue(radios) {
        let value = null;
        radios.forEach(radio => {
            if (radio.checked) value = radio.value;
        });
        return value;
    }

    function showInlineError(field, message) {
        let error = field.parentElement.querySelector('.form-error-inline');
        if (!error) {
            error = document.createElement('span');
            error.className = 'form-error-inline';
            error.style.cssText = `
                font-size: 0.85rem;
                color: #dc2626;
                margin-top: 0.25rem;
                display: block;
            `;
            field.parentElement.appendChild(error);
        }
        error.textContent = message;
    }

    function clearInlineError(field) {
        const error = field.parentElement.querySelector('.form-error-inline');
        if (error) error.remove();
    }

    // =========================
    // VALIDACIONES EN VIVO
    // =========================

    if (tituloInput) {
        tituloInput.addEventListener('input', () => {
            if (tituloInput.value.trim().length >= 3) {
                setFieldState(tituloInput, true);
                clearInlineError(tituloInput);
            } else {
                setFieldState(tituloInput, false);
            }
        });
    }

    if (descripcionInput) {
        descripcionInput.addEventListener('input', () => {
            if (descripcionInput.value.trim().length >= 20) {
                setFieldState(descripcionInput, true);
                clearInlineError(descripcionInput);
            } else {
                setFieldState(descripcionInput, false);
            }
        });
    }

    if (experienciaSelect) {
        experienciaSelect.addEventListener('change', () => {
            if (experienciaSelect.value) {
                setFieldState(experienciaSelect, true);
                clearInlineError(experienciaSelect);
            }
        });
    }

    // =========================
    // SUBMIT FORM
    // =========================

    form.addEventListener('submit', (e) => {
        let hasErrors = false;

        // ---- TÍTULO ----
        if (!tituloInput || tituloInput.value.trim().length < 3) {
            showInlineError(tituloInput, tituloInput.dataset.error || 'Campo requerido');
            setFieldState(tituloInput, false);
            hasErrors = true;
        }

        // ---- DESCRIPCIÓN ----
        if (!descripcionInput || descripcionInput.value.trim().length < 20) {
            showInlineError(descripcionInput, descripcionInput.dataset.error || 'Campo requerido');
            setFieldState(descripcionInput, false);
            hasErrors = true;
        }

        // ---- EXPERIENCIA ----
        if (!experienciaSelect || !experienciaSelect.value) {
            showInlineError(experienciaSelect, experienciaSelect.dataset.error || 'Campo requerido');
            setFieldState(experienciaSelect, false);
            hasErrors = true;
        }

        // ---- DISPONIBILIDAD ----
        const disponibilidad = getSelectedRadioValue(disponibilidadRadios);
        if (!disponibilidad) {
            disponibilidadRadios[0]?.closest('.form-group')?.classList.add('error');
            hasErrors = true;
        } else {
            disponibilidadRadios[0]?.closest('.form-group')?.classList.remove('error');
        }

        if (hasErrors) {
            e.preventDefault();
            return false;
        }

        // =========================
        // ESTADO DE CARGA
        // =========================
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
        }
    });

    // =========================
    // ACCESIBILIDAD TECLADO
    // =========================
    disponibilidadRadios.forEach(radio => {
        radio.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                radio.checked = true;
            }
        });
    });

    console.log('🎯 step_3.js inicializado correctamente');
});
