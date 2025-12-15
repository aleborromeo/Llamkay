// =============================================
// REGISTRO PASO 1 - MEJORADO
// i18n + UX + Accesibilidad + Nielsen
// =============================================

document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ step_1.js inicializado");

    /* ==================== TRADUCCIONES ==================== */
    const translations = {
        es: {
            // Sidebar
            'sidebar-title': '¡Únete a nuestra comunidad!',
            'sidebar-description': 'Miles de peruanos ya confían en Llamkay para encontrar trabajo o contratar profesionales.',
            'benefit-1-title': '100% Verificado',
            'benefit-1-desc': 'Todos los usuarios pasan por verificación',
            'benefit-2-title': 'Encuentra cerca',
            'benefit-2-desc': 'Trabajos en tu distrito o comunidad',
            'benefit-3-title': 'Pagos seguros',
            'benefit-3-desc': 'Sistema de protección garantizada',
            'benefit-4-title': 'Chat directo',
            'benefit-4-desc': 'Sin intermediarios, 100% gratis',
            'help-link': '¿Necesitas ayuda?',

            // Main
            'main-title': 'Crear tu cuenta',
            'main-subtitle': 'Completa tu información personal para comenzar',
            'step-1-label': 'Información',
            'step-2-label': 'Ubicación',
            'step-3-label': 'Perfil',
            'step-4-label': 'Verificación',

            // Form
            'legend-identity': 'Datos de Identificación',
            'legend-company': 'Datos de la empresa',
            'legend-contact': 'Datos de contacto',
            'legend-security': 'Seguridad',
            
            'label-dni': 'DNI',
            'label-name': 'Nombres',
            'label-lastname': 'Apellidos',
            'label-birthdate': 'Fecha de nacimiento',
            'label-gender': 'Género',
            'label-ruc': 'RUC',
            'label-business-name': 'Razón social',
            'label-phone': 'Teléfono',
            'label-email': 'Correo electrónico',
            'label-password': 'Contraseña',
            'label-confirm-password': 'Confirmar contraseña',

            'btn-search': 'Buscar',
            'btn-back': 'Atrás',
            'btn-next': 'Siguiente',

            'placeholder-dni': '00000000',
            'placeholder-ruc': '00000000000',
            'placeholder-autocomplete': 'Se completará automáticamente',
            'placeholder-phone': '999 999 999',
            'placeholder-email': 'tu@email.com',
            'placeholder-password': 'Mínimo 8 caracteres',
            'placeholder-repeat-password': 'Repite tu contraseña',

            'help-dni': 'Ingresa tu DNI para autocompletar tus datos',
            'help-ruc': 'Ingresa el RUC de tu empresa',
            'help-age': 'Debes ser mayor de 18 años',

            'option-select-gender': 'Selecciona tu género',
            'option-male': 'Masculino',
            'option-female': 'Femenino',
            'option-other': 'Otro',
            'option-no-say': 'Prefiero no decir',

            'terms-accept': 'Acepto los',
            'terms-link': 'términos y condiciones',
            'terms-and': 'y la',
            'privacy-link': 'política de privacidad',
            'terms-of': 'de Llamkay',

            'footer-have-account': '¿Ya tienes una cuenta?',
            'footer-login': 'Inicia sesión aquí',

            // Notificaciones
            'msg-dni-empty': 'Por favor ingresa tu DNI',
            'msg-dni-length': 'El DNI debe tener 8 dígitos',
            'msg-dni-numbers': 'El DNI solo debe contener números',
            'msg-dni-success': 'Datos encontrados correctamente',
            'msg-ruc-empty': 'Por favor ingresa el RUC',
            'msg-ruc-length': 'El RUC debe tener 11 dígitos',
            'msg-ruc-numbers': 'El RUC solo debe contener números',
            'msg-ruc-success': 'Empresa encontrada correctamente',
            'msg-password-mismatch': 'Las contraseñas no coinciden',
            'msg-terms-required': 'Debes aceptar los términos y condiciones',
            'msg-generic-error': 'Ocurrió un error. Intenta nuevamente',
            'msg-connection-error': 'Error de conexión. Verifica tu internet'
        },
        en: {
            // Sidebar
            'sidebar-title': 'Join our community!',
            'sidebar-description': 'Thousands of Peruvians already trust Llamkay to find work or hire professionals.',
            'benefit-1-title': '100% Verified',
            'benefit-1-desc': 'All users go through verification',
            'benefit-2-title': 'Find nearby',
            'benefit-2-desc': 'Jobs in your district or community',
            'benefit-3-title': 'Secure payments',
            'benefit-3-desc': 'Guaranteed protection system',
            'benefit-4-title': 'Direct chat',
            'benefit-4-desc': 'No intermediaries, 100% free',
            'help-link': 'Need help?',

            // Main
            'main-title': 'Create your account',
            'main-subtitle': 'Complete your personal information to get started',
            'step-1-label': 'Information',
            'step-2-label': 'Location',
            'step-3-label': 'Profile',
            'step-4-label': 'Verification',

            // Form
            'legend-identity': 'Identification Data',
            'legend-company': 'Company Information',
            'legend-contact': 'Contact Information',
            'legend-security': 'Security',
            
            'label-dni': 'ID Number',
            'label-name': 'First Name',
            'label-lastname': 'Last Name',
            'label-birthdate': 'Date of Birth',
            'label-gender': 'Gender',
            'label-ruc': 'Tax ID',
            'label-business-name': 'Business Name',
            'label-phone': 'Phone',
            'label-email': 'Email',
            'label-password': 'Password',
            'label-confirm-password': 'Confirm Password',

            'btn-search': 'Search',
            'btn-back': 'Back',
            'btn-next': 'Next',

            'placeholder-dni': '00000000',
            'placeholder-ruc': '00000000000',
            'placeholder-autocomplete': 'Will be auto-filled',
            'placeholder-phone': '999 999 999',
            'placeholder-email': 'your@email.com',
            'placeholder-password': 'Minimum 8 characters',
            'placeholder-repeat-password': 'Repeat your password',

            'help-dni': 'Enter your ID to auto-fill your data',
            'help-ruc': 'Enter your company Tax ID',
            'help-age': 'You must be over 18 years old',

            'option-select-gender': 'Select your gender',
            'option-male': 'Male',
            'option-female': 'Female',
            'option-other': 'Other',
            'option-no-say': 'Prefer not to say',

            'terms-accept': 'I accept the',
            'terms-link': 'terms and conditions',
            'terms-and': 'and the',
            'privacy-link': 'privacy policy',
            'terms-of': 'of Llamkay',

            'footer-have-account': 'Already have an account?',
            'footer-login': 'Log in here',

            // Notifications
            'msg-dni-empty': 'Please enter your ID',
            'msg-dni-length': 'ID must be 8 digits',
            'msg-dni-numbers': 'ID must contain only numbers',
            'msg-dni-success': 'Data found successfully',
            'msg-ruc-empty': 'Please enter Tax ID',
            'msg-ruc-length': 'Tax ID must be 11 digits',
            'msg-ruc-numbers': 'Tax ID must contain only numbers',
            'msg-ruc-success': 'Company found successfully',
            'msg-password-mismatch': 'Passwords do not match',
            'msg-terms-required': 'You must accept the terms and conditions',
            'msg-generic-error': 'An error occurred. Please try again',
            'msg-connection-error': 'Connection error. Check your internet'
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

        // Actualizar botones
        langButtons.forEach(btn => {
            if (btn.dataset.lang === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Actualizar todos los textos con data-i18n
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

    // Aplicar idioma guardado al cargar
    changeLanguage(currentLang);

    /* ==================== ELEMENTOS ==================== */
    const form = document.getElementById("registerForm");
    const dniInput = document.querySelector('input[name="dni"]');
    const nombreInput = document.querySelector('input[name="nombre"]');
    const apellidoInput = document.querySelector('input[name="apellido"]');
    const rucInput = document.querySelector('input[name="ruc"]');
    const razonSocialInput = document.querySelector('input[name="razon_social"]');
    const btnBuscarDNI = document.querySelector('[data-action="buscar-dni"]');
    const btnBuscarRUC = document.querySelector('[data-action="buscar-ruc"]');
    const passwordToggles = document.querySelectorAll(".password-toggle");

    /* ==================== NOTIFICACIONES ==================== */
    function notify(message, type = "error") {
        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        toast.setAttribute("role", "alert");
        toast.textContent = message;

        Object.assign(toast.style, {
            position: "fixed",
            top: "80px",
            right: "20px",
            background: type === "success" ? "#10b981" : "#dc2626",
            color: "#fff",
            padding: "1rem 1.5rem",
            borderRadius: "12px",
            boxShadow: "0 8px 32px rgba(0,0,0,.2)",
            zIndex: 9999,
            animation: "slideIn 0.3s ease"
        });

        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.animation = "slideOut 0.3s ease";
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    /* ==================== VALIDACIONES ==================== */
    const isNumeric = v => /^\d+$/.test(v);

    function validarDNI(dni) {
        if (!dni) return t("msg-dni-empty");
        if (dni.length !== 8) return t("msg-dni-length");
        if (!isNumeric(dni)) return t("msg-dni-numbers");
        return null;
    }

    function validarRUC(ruc) {
        if (!ruc) return t("msg-ruc-empty");
        if (ruc.length !== 11) return t("msg-ruc-length");
        if (!isNumeric(ruc)) return t("msg-ruc-numbers");
        return null;
    }

    /* ==================== LOADING BOTÓN ==================== */
    function setLoading(btn, state) {
        btn.disabled = state;
        btn.classList.toggle("loading", state);
    }

    /* ==================== BUSCAR DNI ==================== */
    if (btnBuscarDNI && dniInput) {
        btnBuscarDNI.addEventListener("click", async () => {
            const error = validarDNI(dniInput.value.trim());
            if (error) return notify(error);

            setLoading(btnBuscarDNI, true);

            try {
                const res = await fetch(`/users/api/consultar-dni/?dni=${dniInput.value}`);
                const data = await res.json();

                if (data.success) {
                    nombreInput.value = data.data.nombres || "";
                    apellidoInput.value = `${data.data.apellido_paterno || ""} ${data.data.apellido_materno || ""}`.trim();
                    nombreInput.removeAttribute("readonly");
                    apellidoInput.removeAttribute("readonly");
                    notify(t("msg-dni-success"), "success");
                } else {
                    notify(data.error || t("msg-generic-error"));
                }
            } catch {
                notify(t("msg-connection-error"));
            } finally {
                setLoading(btnBuscarDNI, false);
            }
        });
    }

    /* ==================== BUSCAR RUC ==================== */
    if (btnBuscarRUC && rucInput) {
        btnBuscarRUC.addEventListener("click", async () => {
            const error = validarRUC(rucInput.value.trim());
            if (error) return notify(error);

            setLoading(btnBuscarRUC, true);

            try {
                const res = await fetch(`/users/api/consultar-ruc/?ruc=${rucInput.value}`);
                const data = await res.json();

                if (data.success) {
                    razonSocialInput.value = data.data.razon_social || "";
                    razonSocialInput.removeAttribute("readonly");
                    notify(t("msg-ruc-success"), "success");
                } else {
                    notify(data.error || t("msg-generic-error"));
                }
            } catch {
                notify(t("msg-connection-error"));
            } finally {
                setLoading(btnBuscarRUC, false);
            }
        });
    }

    /* ==================== PASSWORD TOGGLE ==================== */
    passwordToggles.forEach(btn => {
        btn.addEventListener("click", () => {
            const input = document.getElementById(btn.dataset.target);
            input.type = input.type === "password" ? "text" : "password";
        });
    });

    /* ==================== SUBMIT ==================== */
    if (form) {
        form.addEventListener("submit", e => {
            const pass1 = document.getElementById("id_password1");
            const pass2 = document.getElementById("id_password2");
            const terms = document.getElementById("acepto_terminos");

            if (pass1 && pass2 && pass1.value !== pass2.value) {
                e.preventDefault();
                return notify(t("msg-password-mismatch"));
            }

            if (terms && !terms.checked) {
                e.preventDefault();
                return notify(t("msg-terms-required"));
            }
        });
    }

    console.log("🎉 step_1.js listo con i18n completo");
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