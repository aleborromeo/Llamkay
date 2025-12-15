// =============================================
// REGISTRO PASO 3 - PERFIL Y DISPONIBILIDAD
// UX Avanzada + Nielsen + Gestalt
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ step_3.js cargado correctamente');

    // =========================
    // ELEMENTOS DEL DOM
    // =========================
    const form = document.querySelector('.register-form');

    const experienciaSelect = document.getElementById('id_experiencia_anios');
    const nivelSelect = document.getElementById('id_nivel');
    const modalidadSelect = document.getElementById('id_modalidad');
    const horarioSelect = document.getElementById('id_horario');
    const perfilPublicoCheckbox = document.getElementById('id_perfil_publico');

    // =========================
    // HELPERS
    // =========================

    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#dc2626' : '#3b82f6'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,.16);
            z-index: 9999;
            animation: slideIn .3s ease;
            max-width: 360px;
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut .3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    function markValid(element) {
        element.style.borderColor = '#10b981';
    }

    function resetBorder(element) {
        element.style.borderColor = '#e2e8f0';
    }

    // =========================
    // VALIDACIÓN SUAVE (UX)
    // =========================

    const trackedSelects = [
        experienciaSelect,
        nivelSelect,
        modalidadSelect,
        horarioSelect
    ];

    trackedSelects.forEach(select => {
        if (!select) return;

        select.addEventListener('change', function () {
            if (this.value) {
                markValid(this);
            } else {
                resetBorder(this);
            }
            saveProgress();
        });
    });

    if (perfilPublicoCheckbox) {
        perfilPublicoCheckbox.addEventListener('change', saveProgress);
    }

    // =========================
    // VALIDACIÓN AL ENVIAR
    // Nielsen: Prevención de errores
    // =========================

    if (form) {
        form.addEventListener('submit', function (e) {
            const errors = [];

            if (!experienciaSelect.value) {
                errors.push('Selecciona tus años de experiencia');
            }

            if (!nivelSelect.value) {
                errors.push('Selecciona tu nivel');
            }

            if (!modalidadSelect.value) {
                errors.push('Selecciona una modalidad');
            }

            if (!horarioSelect.value) {
                errors.push('Selecciona un horario');
            }

            if (errors.length > 0) {
                e.preventDefault();
                errors.forEach(err => showNotification(err, 'error'));

                // Enfocar el primer error
                if (!experienciaSelect.value) experienciaSelect.focus();
                else if (!nivelSelect.value) nivelSelect.focus();
                else if (!modalidadSelect.value) modalidadSelect.focus();
                else if (!horarioSelect.value) horarioSelect.focus();

                return false;
            }

            // Loading visual
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                submitBtn.innerHTML = `
                    <svg style="animation: spin 1s linear infinite"
                         xmlns="http://www.w3.org/2000/svg"
                         width="16" height="16"
                         viewBox="0 0 24 24"
                         fill="none"
                         stroke="currentColor"
                         stroke-width="2">
                        <line x1="12" y1="2" x2="12" y2="6"></line>
                        <line x1="12" y1="18" x2="12" y2="22"></line>
                        <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
                        <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
                        <line x1="2" y1="12" x2="6" y2="12"></line>
                        <line x1="18" y1="12" x2="22" y2="12"></line>
                    </svg>
                    Procesando...
                `;
            }
        });
    }

    // =========================
    // AUTOGUARDADO
    // Nielsen: Recuperación ante errores
    // =========================

    function saveProgress() {
        const data = {
            experiencia: experienciaSelect?.value || '',
            nivel: nivelSelect?.value || '',
            modalidad: modalidadSelect?.value || '',
            horario: horarioSelect?.value || '',
            perfil_publico: perfilPublicoCheckbox?.checked ?? true
        };
        localStorage.setItem('registro_step3', JSON.stringify(data));
    }

    function loadProgress() {
        try {
            const saved = localStorage.getItem('registro_step3');
            if (!saved) return;

            const data = JSON.parse(saved);

            if (experienciaSelect && data.experiencia) experienciaSelect.value = data.experiencia;
            if (nivelSelect && data.nivel) nivelSelect.value = data.nivel;
            if (modalidadSelect && data.modalidad) modalidadSelect.value = data.modalidad;
            if (horarioSelect && data.horario) horarioSelect.value = data.horario;
            if (perfilPublicoCheckbox) perfilPublicoCheckbox.checked = data.perfil_publico;

        } catch (err) {
            console.warn('No se pudo restaurar el progreso', err);
        }
    }

    loadProgress();

    console.log('✅ step_3.js inicializado correctamente');
});

// =========================
// ANIMACIONES
// =========================
const style = document.createElement('style');
style.textContent = `
@keyframes slideIn {
    from { transform: translateX(400px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(400px); opacity: 0; }
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
`;
document.head.appendChild(style);
