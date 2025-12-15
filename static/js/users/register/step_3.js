// =============================================
// REGISTRO PASO 3 - PERFIL MEJORADO
// i18n + UX Avanzada + Nielsen + Gestalt
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ step_3.js cargado correctamente');

    /* ==================== TRADUCCIONES ==================== */
    const translations = {
        es: {
            // Sidebar
            'sidebar-title': 'Construye tu perfil profesional',
            'sidebar-description': 'Tu perfil es lo primero que verán los empleadores y trabajadores. Hazlo claro, honesto y completo.',
            'benefit-1-title': 'Más confianza',
            'benefit-1-desc': 'Un perfil completo genera mayor credibilidad',
            'benefit-2-title': 'Mejores oportunidades',
            'benefit-2-desc': 'Aparecerás en más búsquedas relevantes',
            'benefit-3-title': 'Control total',
            'benefit-3-desc': 'Puedes editar tu perfil cuando quieras',
            'help-link': '¿Necesitas ayuda para completar tu perfil?',

            // Main
            'main-title': 'Tu perfil',
            'main-subtitle': 'Cuéntanos quién eres y qué sabes hacer',
            'step-1-label': 'Información',
            'step-2-label': 'Ubicación',
            'step-3-label': 'Perfil',
            'step-4-label': 'Verificación',

            // Form
            'legend-identity': 'Identidad pública',
            'legend-about': 'Sobre ti',
            'legend-skills': 'Habilidades principales',
            'legend-experience': 'Experiencia',
            'legend-availability': 'Disponibilidad',
            'legend-privacy': 'Privacidad',

            'label-public-name': 'Nombre público',
            'label-role': '¿Qué haces?',
            'label-bio': 'Descripción',
            'label-skills': 'Habilidades',
            'label-years': 'Años de experiencia',
            'label-level': 'Nivel',
            'label-modality': 'Modalidad',
            'label-schedule': 'Horario disponible',
            'label-public-profile': 'Quiero que mi perfil sea visible para otros usuarios',

            'placeholder-public-name': 'Ej: Juan Pérez',
            'placeholder-bio': 'Describe brevemente tu experiencia, habilidades y lo que ofreces...',
            'placeholder-skills': 'Ej: Carpintería, Plomería, Diseño gráfico',

            'help-public-name': 'Este nombre será visible para otros usuarios',
            'help-bio': 'Máximo 500 caracteres. Sé claro y directo.',
            'help-skills': 'Sepáralas por comas para facilitar la búsqueda',
            'help-privacy': 'Podrás cambiar esto más adelante desde tu perfil',

            'option-select-role': 'Selecciona una opción',
            'option-worker': 'Ofrezco servicios',
            'option-employer': 'Busco contratar',
            'option-both': 'Ambos',

            'option-select': 'Selecciona',
            'option-years-0-1': 'Menos de 1 año',
            'option-years-1-3': '1 a 3 años',
            'option-years-3-5': '3 a 5 años',
            'option-years-5+': 'Más de 5 años',

            'option-basic': 'Básico',
            'option-intermediate': 'Intermedio',
            'option-advanced': 'Avanzado',

            'option-onsite': 'Presencial',
            'option-remote': 'Remoto',
            'option-hybrid': 'Mixto',

            'option-morning': 'Mañanas',
            'option-afternoon': 'Tardes',
            'option-evening': 'Noches',
            'option-flexible': 'Flexible',

            'btn-back': 'Anterior',
            'btn-continue': 'Continuar',

            'footer-have-account': '¿Ya tienes una cuenta?',
            'footer-login': 'Inicia sesión aquí',

            // Mensajes
            'msg-error-name': 'El nombre debe tener al menos 3 caracteres',
            'msg-error-role': 'Por favor selecciona tu rol',
            'msg-error-bio': 'La descripción debe tener al menos 20 caracteres',
            'msg-processing': 'Procesando...',
            'msg-saved': 'Progreso guardado'
        },
        en: {
            // Sidebar
            'sidebar-title': 'Build your professional profile',
            'sidebar-description': 'Your profile is the first thing employers and workers will see. Make it clear, honest and complete.',
            'benefit-1-title': 'More trust',
            'benefit-1-desc': 'A complete profile generates greater credibility',
            'benefit-2-title': 'Better opportunities',
            'benefit-2-desc': 'You will appear in more relevant searches',
            'benefit-3-title': 'Total control',
            'benefit-3-desc': 'You can edit your profile whenever you want',
            'help-link': 'Need help completing your profile?',

            // Main
            'main-title': 'Your profile',
            'main-subtitle': 'Tell us who you are and what you do',
            'step-1-label': 'Information',
            'step-2-label': 'Location',
            'step-3-label': 'Profile',
            'step-4-label': 'Verification',

            // Form
            'legend-identity': 'Public Identity',
            'legend-about': 'About You',
            'legend-skills': 'Main Skills',
            'legend-experience': 'Experience',
            'legend-availability': 'Availability',
            'legend-privacy': 'Privacy',

            'label-public-name': 'Public Name',
            'label-role': 'What do you do?',
            'label-bio': 'Description',
            'label-skills': 'Skills',
            'label-years': 'Years of experience',
            'label-level': 'Level',
            'label-modality': 'Modality',
            'label-schedule': 'Available schedule',
            'label-public-profile': 'I want my profile to be visible to other users',

            'placeholder-public-name': 'E.g.: John Doe',
            'placeholder-bio': 'Briefly describe your experience, skills and what you offer...',
            'placeholder-skills': 'E.g.: Carpentry, Plumbing, Graphic Design',

            'help-public-name': 'This name will be visible to other users',
            'help-bio': 'Maximum 500 characters. Be clear and direct.',
            'help-skills': 'Separate them with commas to facilitate search',
            'help-privacy': 'You can change this later from your profile',

            'option-select-role': 'Select an option',
            'option-worker': 'I offer services',
            'option-employer': 'I want to hire',
            'option-both': 'Both',

            'option-select': 'Select',
            'option-years-0-1': 'Less than 1 year',
            'option-years-1-3': '1 to 3 years',
            'option-years-3-5': '3 to 5 years',
            'option-years-5+': 'More than 5 years',

            'option-basic': 'Basic',
            'option-intermediate': 'Intermediate',
            'option-advanced': 'Advanced',

            'option-onsite': 'On-site',
            'option-remote': 'Remote',
            'option-hybrid': 'Hybrid',

            'option-morning': 'Mornings',
            'option-afternoon': 'Afternoons',
            'option-evening': 'Evenings',
            'option-flexible': 'Flexible',

            'btn-back': 'Previous',
            'btn-continue': 'Continue',

            'footer-have-account': 'Already have an account?',
            'footer-login': 'Log in here',

            // Messages
            'msg-error-name': 'Name must be at least 3 characters',
            'msg-error-role': 'Please select your role',
            'msg-error-bio': 'Description must be at least 20 characters',
            'msg-processing': 'Processing...',
            'msg-saved': 'Progress saved'
        }
    };

    let currentLang = localStorage.getItem('llamkay_lang') || 'es';

    function t(key) {
        return translations[currentLang][key] || key;
    }

    /* ==================== CAMBIO DE IDIOMA ==================== */
    const langButtons = document.querySelectorAll('.lang-btn');

    function changeLanguage(lang) {
        currentLang = lang;
        localStorage.setItem('llamkay_lang', lang);

        langButtons.forEach(btn => {
            if (btn.dataset.lang === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Actualizar textos
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.dataset.i18n;
            el.textContent = t(key);
        });

        // Actualizar placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.dataset.i18nPlaceholder;
            el.placeholder = t(key);
        });
    }

    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            changeLanguage(btn.dataset.lang);
        });
    });

    // Aplicar idioma guardado
    changeLanguage(currentLang);

    /* ==================== ELEMENTOS DEL DOM ==================== */
    const form = document.querySelector('.register-form');
    const nombrePublicoInput = document.getElementById('id_nombre_publico');
    const rolSelect = document.getElementById('id_rol_principal');
    const biografiaTextarea = document.getElementById('id_biografia');
    const experienciaSelect = document.getElementById('id_experiencia_anios');
    const nivelSelect = document.getElementById('id_nivel');
    const modalidadSelect = document.getElementById('id_modalidad');
    const horarioSelect = document.getElementById('id_horario');
    const perfilPublicoCheckbox = document.getElementById('id_perfil_publico');

    /* ==================== NOTIFICACIONES ==================== */
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 80px;
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

    /* ==================== HELPERS UX ==================== */
    function setFieldState(field, valid) {
        if (!field) return;
        field.style.borderColor = valid ? '#10b981' : '#dc2626';
    }

    function clearFieldState(field) {
        if (!field) return;
        field.style.borderColor = '';
    }

    /* ==================== VALIDACIÓN EN VIVO ==================== */
    if (nombrePublicoInput) {
        nombrePublicoInput.addEventListener('input', () => {
            if (nombrePublicoInput.value.trim().length >= 3) {
                setFieldState(nombrePublicoInput, true);
            } else {
                clearFieldState(nombrePublicoInput);
            }
            saveProgress();
        });
    }

    if (biografiaTextarea) {
        biografiaTextarea.addEventListener('input', () => {
            if (biografiaTextarea.value.trim().length >= 20) {
                setFieldState(biografiaTextarea, true);
            } else {
                clearFieldState(biografiaTextarea);
            }
            saveProgress();
        });
    }

    const trackedSelects = [
        experienciaSelect,
        nivelSelect,
        modalidadSelect,
        horarioSelect,
        rolSelect
    ];

    trackedSelects.forEach(select => {
        if (!select) return;

        select.addEventListener('change', function () {
            if (this.value) {
                setFieldState(this, true);
            } else {
                clearFieldState(this);
            }
            saveProgress();
        });
    });

    if (perfilPublicoCheckbox) {
        perfilPublicoCheckbox.addEventListener('change', saveProgress);
    }

    /* ==================== VALIDACIÓN AL ENVIAR ==================== */
    if (form) {
        form.addEventListener('submit', function (e) {
            const errors = [];

            // Validar nombre público
            if (!nombrePublicoInput || nombrePublicoInput.value.trim().length < 3) {
                errors.push(t('msg-error-name'));
                if (nombrePublicoInput) {
                    setFieldState(nombrePublicoInput, false);
                    nombrePublicoInput.focus();
                }
            }

            // Validar rol
            if (!rolSelect || !rolSelect.value) {
                errors.push(t('msg-error-role'));
                if (rolSelect) setFieldState(rolSelect, false);
            }

            // Validar biografía
            if (!biografiaTextarea || biografiaTextarea.value.trim().length < 20) {
                errors.push(t('msg-error-bio'));
                if (biografiaTextarea) setFieldState(biografiaTextarea, false);
            }

            if (errors.length > 0) {
                e.preventDefault();
                errors.forEach(err => showNotification(err, 'error'));
                return false;
            }

            // Loading visual
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                const btnText = submitBtn.querySelector('span');
                if (btnText) {
                    btnText.textContent = t('msg-processing');
                }
            }
        });
    }

    /* ==================== AUTOGUARDADO ==================== */
    function saveProgress() {
        const data = {
            nombre_publico: nombrePublicoInput?.value || '',
            rol: rolSelect?.value || '',
            biografia: biografiaTextarea?.value || '',
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

            if (nombrePublicoInput && data.nombre_publico) nombrePublicoInput.value = data.nombre_publico;
            if (rolSelect && data.rol) rolSelect.value = data.rol;
            if (biografiaTextarea && data.biografia) biografiaTextarea.value = data.biografia;
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

// ==================== ANIMACIONES ====================
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
`;
document.head.appendChild(style);