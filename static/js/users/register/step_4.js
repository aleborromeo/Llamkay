// =============================================
// REGISTRO PASO 4 - VERIFICACIÓN MEJORADO
// i18n + UX/UI + Nielsen + Accesibilidad
// =============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ step_4.js cargado');

    /* ==================== TRADUCCIONES ==================== */
    const translations = {
        es: {
            // Sidebar
            'sidebar-title': 'Completa tu perfil profesional',
            'sidebar-description': 'Esta información ayuda a que te encuentren más rápido y con mejores oportunidades.',
            'benefit-1-title': 'Más visibilidad',
            'benefit-1-desc': 'Tu perfil aparece mejor posicionado',
            'benefit-2-title': 'Mayor confianza',
            'benefit-2-desc': 'Los empleadores prefieren perfiles completos',
            'benefit-3-title': 'Mejores coincidencias',
            'benefit-3-desc': 'Te mostramos trabajos acordes a ti',

            // Main
            'main-title': 'Completa tu perfil profesional',
            'main-subtitle': 'Esta información ayuda a que te encuentren más rápido y con mejores oportunidades.',
            'step-1-label': 'Información',
            'step-2-label': 'Ubicación',
            'step-3-label': 'Perfil',
            'step-4-label': 'Verificación',

            // Form
            'legend-professional': 'Perfil profesional',
            'legend-about': 'Sobre ti',
            'legend-availability': 'Disponibilidad',

            'label-title': 'Título profesional',
            'label-experience': 'Años de experiencia',
            'label-description': 'Descripción profesional',
            'label-schedule': 'Disponibilidad horaria',
            'label-modality': 'Modalidad de trabajo',

            'placeholder-title': 'Ej: Electricista, Diseñador gráfico, Albañil',
            'placeholder-description': 'Describe tu experiencia, habilidades y el tipo de trabajos que realizas.',

            'help-title': 'Este título será lo primero que vean quienes te busquen.',
            'help-description': 'Una buena descripción aumenta la confianza y las oportunidades.',

            'option-select': 'Selecciona una opción',
            'option-years-0-1': 'Menos de 1 año',
            'option-years-1-3': '1 a 3 años',
            'option-years-3-5': '3 a 5 años',
            'option-years-5+': 'Más de 5 años',

            'option-fulltime': 'Tiempo completo',
            'option-parttime': 'Medio tiempo',
            'option-weekends': 'Fines de semana',
            'option-flexible': 'Flexible',

            'option-onsite': 'Presencial',
            'option-remote': 'Remoto',
            'option-hybrid': 'Mixto',

            'tip-title': 'Consejo',
            'tip-description': 'Un perfil completo y claro aumenta tus oportunidades de ser contactado.',

            'btn-back': 'Anterior',
            'btn-finish': 'Finalizar',

            'footer-have-account': '¿Ya tienes una cuenta?',
            'footer-login': 'Inicia sesión aquí',

            // Validaciones
            'msg-error-title': 'El título debe tener al menos 3 caracteres',
            'msg-error-experience': 'Por favor selecciona tus años de experiencia',
            'msg-error-description': 'La descripción debe tener al menos 20 caracteres',
            'msg-processing': 'Procesando...',
            'msg-completing': 'Completando registro...'
        },
        en: {
            // Sidebar
            'sidebar-title': 'Complete your professional profile',
            'sidebar-description': 'This information helps you get found faster and with better opportunities.',
            'benefit-1-title': 'More visibility',
            'benefit-1-desc': 'Your profile appears better positioned',
            'benefit-2-title': 'Greater trust',
            'benefit-2-desc': 'Employers prefer complete profiles',
            'benefit-3-title': 'Better matches',
            'benefit-3-desc': 'We show you jobs that suit you',

            // Main
            'main-title': 'Complete your professional profile',
            'main-subtitle': 'This information helps you get found faster and with better opportunities.',
            'step-1-label': 'Information',
            'step-2-label': 'Location',
            'step-3-label': 'Profile',
            'step-4-label': 'Verification',

            // Form
            'legend-professional': 'Professional Profile',
            'legend-about': 'About You',
            'legend-availability': 'Availability',

            'label-title': 'Professional Title',
            'label-experience': 'Years of Experience',
            'label-description': 'Professional Description',
            'label-schedule': 'Time Availability',
            'label-modality': 'Work Modality',

            'placeholder-title': 'E.g.: Electrician, Graphic Designer, Mason',
            'placeholder-description': 'Describe your experience, skills and the type of work you do.',

            'help-title': 'This title will be the first thing people see when they search for you.',
            'help-description': 'A good description increases trust and opportunities.',

            'option-select': 'Select an option',
            'option-years-0-1': 'Less than 1 year',
            'option-years-1-3': '1 to 3 years',
            'option-years-3-5': '3 to 5 years',
            'option-years-5+': 'More than 5 years',

            'option-fulltime': 'Full time',
            'option-parttime': 'Part time',
            'option-weekends': 'Weekends',
            'option-flexible': 'Flexible',

            'option-onsite': 'On-site',
            'option-remote': 'Remote',
            'option-hybrid': 'Hybrid',

            'tip-title': 'Tip',
            'tip-description': 'A complete and clear profile increases your chances of being contacted.',

            'btn-back': 'Previous',
            'btn-finish': 'Finish',

            'footer-have-account': 'Already have an account?',
            'footer-login': 'Log in here',

            // Validations
            'msg-error-title': 'Title must be at least 3 characters',
            'msg-error-experience': 'Please select your years of experience',
            'msg-error-description': 'Description must be at least 20 characters',
            'msg-processing': 'Processing...',
            'msg-completing': 'Completing registration...'
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

    /* ==================== ELEMENTOS ==================== */
    const form = document.getElementById('profile-form');
    const tituloInput = document.getElementById('id_titulo');
    const descripcionInput = document.getElementById('id_descripcion');
    const experienciaSelect = document.getElementById('id_experiencia');
    const disponibilidadSelect = document.getElementById('id_disponibilidad');
    const modalidadSelect = document.getElementById('id_modalidad');
    const submitBtn = form?.querySelector('button[type="submit"]');

    if (!form) return;

    /* ==================== NOTIFICACIONES ==================== */
    function showNotification(message, type = 'error') {
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
            box-shadow: 0 8px 32px rgba(0,0,0,.2);
            z-index: 9999;
            animation: slideIn .3s ease;
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

    /* ==================== VALIDACIONES EN VIVO ==================== */
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

    /* ==================== SUBMIT FORM ==================== */
    form.addEventListener('submit', (e) => {
        let hasErrors = false;

        // Validar título
        if (!tituloInput || tituloInput.value.trim().length < 3) {
            showInlineError(tituloInput, t('msg-error-title'));
            setFieldState(tituloInput, false);
            hasErrors = true;
            if (tituloInput) tituloInput.focus();
        }

        // Validar descripción
        if (!descripcionInput || descripcionInput.value.trim().length < 20) {
            showInlineError(descripcionInput, t('msg-error-description'));
            setFieldState(descripcionInput, false);
            hasErrors = true;
            if (!hasErrors && descripcionInput) descripcionInput.focus();
        }

        // Validar experiencia
        if (!experienciaSelect || !experienciaSelect.value) {
            showInlineError(experienciaSelect, t('msg-error-experience'));
            setFieldState(experienciaSelect, false);
            hasErrors = true;
        }

        if (hasErrors) {
            e.preventDefault();
            return false;
        }

        // Estado de carga
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
            const btnText = submitBtn.querySelector('span');
            if (btnText) {
                btnText.textContent = t('msg-completing');
            }
        }
    });

    /* ==================== ACCESIBILIDAD TECLADO ==================== */
    const allSelects = [experienciaSelect, disponibilidadSelect, modalidadSelect];
    allSelects.forEach(select => {
        if (!select) return;
        select.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                select.click();
            }
        });
    });

    console.log('🎯 step_4.js inicializado correctamente');
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