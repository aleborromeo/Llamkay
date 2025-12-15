// =============================================
// REGISTRO PASO 2 - UBICACIÓN MEJORADO
// i18n + UX + Accesibilidad + Cascada
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ step_2.js iniciado');

    /* ==================== TRADUCCIONES ==================== */
    const translations = {
        es: {
            // Sidebar
            'sidebar-title': '¿Por qué necesitamos tu ubicación?',
            'sidebar-description': 'Tu ubicación nos ayuda a conectarte con oportunidades cerca de ti.',
            'benefit-1-title': 'Trabajos cercanos',
            'benefit-1-desc': 'Encuentra oportunidades en tu zona',
            'benefit-2-title': 'Trabaja desde casa',
            'benefit-2-desc': 'Reduce tiempos de traslado',
            'benefit-3-title': 'Respuesta rápida',
            'benefit-3-desc': 'Conecta con usuarios locales',
            'benefit-4-title': 'Privacidad garantizada',
            'benefit-4-desc': 'Tu dirección exacta está protegida',
            'help-link': '¿Necesitas ayuda?',

            // Main
            'main-title': 'Tu ubicación',
            'main-subtitle': 'Indícanos dónde te encuentras',
            'step-1-label': 'Información',
            'step-2-label': 'Ubicación',
            'step-3-label': 'Perfil',
            'step-4-label': 'Verificación',

            // Form
            'legend-address': 'Dirección',
            'legend-location': 'Ubicación geográfica',
            
            'label-address': 'Dirección completa',
            'label-department': 'Departamento',
            'label-province': 'Provincia',
            'label-district': 'Distrito',

            'placeholder-address': 'Ej: Av. Larco 123, Dpto. 501',
            
            'help-address': 'Tu dirección exacta está protegida y no se muestra públicamente.',

            'option-select-department': 'Selecciona tu departamento',
            'option-select-province-first': 'Primero selecciona un departamento',
            'option-select-district-first': 'Primero selecciona una provincia',

            'btn-back': 'Anterior',
            'btn-next': 'Siguiente',

            'footer-have-account': '¿Ya tienes una cuenta?',
            'footer-login': 'Inicia sesión aquí',

            // Mensajes
            'msg-loading': 'Cargando...',
            'msg-processing': 'Procesando...',
            'msg-error-address': 'Por favor ingresa tu dirección',
            'msg-error-department': 'Por favor selecciona un departamento',
            'msg-error-province': 'Por favor selecciona una provincia',
            'msg-error-district': 'Por favor selecciona un distrito',
            'msg-error-load-provinces': 'Error al cargar provincias',
            'msg-error-load-districts': 'Error al cargar distritos',
            'msg-no-provinces': 'No hay provincias disponibles',
            'msg-no-districts': 'No hay distritos disponibles'
        },
        en: {
            // Sidebar
            'sidebar-title': 'Why do we need your location?',
            'sidebar-description': 'Your location helps us connect you with opportunities near you.',
            'benefit-1-title': 'Nearby jobs',
            'benefit-1-desc': 'Find opportunities in your area',
            'benefit-2-title': 'Work from home',
            'benefit-2-desc': 'Reduce travel time',
            'benefit-3-title': 'Fast response',
            'benefit-3-desc': 'Connect with local users',
            'benefit-4-title': 'Privacy guaranteed',
            'benefit-4-desc': 'Your exact address is protected',
            'help-link': 'Need help?',

            // Main
            'main-title': 'Your location',
            'main-subtitle': 'Tell us where you are',
            'step-1-label': 'Information',
            'step-2-label': 'Location',
            'step-3-label': 'Profile',
            'step-4-label': 'Verification',

            // Form
            'legend-address': 'Address',
            'legend-location': 'Geographic Location',
            
            'label-address': 'Full Address',
            'label-department': 'Department',
            'label-province': 'Province',
            'label-district': 'District',

            'placeholder-address': 'E.g.: Av. Larco 123, Apt. 501',
            
            'help-address': 'Your exact address is protected and not shown publicly.',

            'option-select-department': 'Select your department',
            'option-select-province-first': 'First select a department',
            'option-select-district-first': 'First select a province',

            'btn-back': 'Previous',
            'btn-next': 'Next',

            'footer-have-account': 'Already have an account?',
            'footer-login': 'Log in here',

            // Messages
            'msg-loading': 'Loading...',
            'msg-processing': 'Processing...',
            'msg-error-address': 'Please enter your address',
            'msg-error-department': 'Please select a department',
            'msg-error-province': 'Please select a province',
            'msg-error-district': 'Please select a district',
            'msg-error-load-provinces': 'Error loading provinces',
            'msg-error-load-districts': 'Error loading districts',
            'msg-no-provinces': 'No provinces available',
            'msg-no-districts': 'No districts available'
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

        // Actualizar options del select (solo los de placeholder)
        updateSelectPlaceholders();
    }

    function updateSelectPlaceholders() {
        const departamentoSelect = document.getElementById('id_departamento');
        const provinciaSelect = document.getElementById('id_provincia');
        const distritoSelect = document.getElementById('id_distrito');

        if (departamentoSelect.value === '') {
            departamentoSelect.querySelector('option[value=""]').textContent = t('option-select-department');
        }
        if (provinciaSelect.disabled) {
            provinciaSelect.querySelector('option[value=""]').textContent = t('option-select-province-first');
        }
        if (distritoSelect.disabled) {
            distritoSelect.querySelector('option[value=""]').textContent = t('option-select-district-first');
        }
    }

    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            changeLanguage(btn.dataset.lang);
        });
    });

    // Aplicar idioma guardado
    changeLanguage(currentLang);

    /* ==================== ELEMENTOS ==================== */
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

    /* ==================== NOTIFICACIONES ==================== */
    function showNotification(message, type = 'info') {
        const div = document.createElement('div');
        div.className = `notification ${type}`;
        div.setAttribute('role', 'alert');
        div.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: ${type === 'error' ? '#dc2626' : '#10b981'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,.2);
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        div.textContent = message;
        document.body.appendChild(div);
        
        setTimeout(() => {
            div.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => div.remove(), 300);
        }, 3000);
    }

    /* ==================== HELPERS ==================== */
    function resetSelect(select, text, disabled = true) {
        select.innerHTML = `<option value="">${text}</option>`;
        select.disabled = disabled;
    }

    function setLoading(select) {
        resetSelect(select, t('msg-loading'), true);
    }

    function populateSelect(select, items, idKey, labelKey) {
        const placeholder = select.id === 'id_provincia' 
            ? t('option-select-province-first') 
            : t('option-select-district-first');
        
        resetSelect(select, placeholder, false);
        
        items.forEach(item => {
            const opt = document.createElement('option');
            opt.value = item[idKey];
            opt.textContent = item[labelKey];
            select.appendChild(opt);
        });
        select.disabled = false;
    }

    /* ==================== DEPARTAMENTO → PROVINCIA ==================== */
    departamentoSelect.addEventListener('change', async function () {
        resetSelect(provinciaSelect, t('msg-loading'));
        resetSelect(distritoSelect, t('option-select-district-first'));

        if (!this.value) {
            resetSelect(provinciaSelect, t('option-select-province-first'), true);
            return;
        }

        setLoading(provinciaSelect);

        try {
            const res = await fetch(`${urlProvincias}?id_departamento=${this.value}`);
            const data = await res.json();

            if (Array.isArray(data) && data.length) {
                populateSelect(provinciaSelect, data, 'id_provincia', 'nombre');
            } else {
                resetSelect(provinciaSelect, t('msg-no-provinces'), true);
                showNotification(t('msg-no-provinces'), 'error');
            }
        } catch {
            showNotification(t('msg-error-load-provinces'), 'error');
            resetSelect(provinciaSelect, t('msg-error-load-provinces'), true);
        }
    });

    /* ==================== PROVINCIA → DISTRITO ==================== */
    provinciaSelect.addEventListener('change', async function () {
        resetSelect(distritoSelect, t('msg-loading'));

        if (!this.value) {
            resetSelect(distritoSelect, t('option-select-district-first'), true);
            return;
        }

        setLoading(distritoSelect);

        try {
            const res = await fetch(`${urlDistritos}?id_provincia=${this.value}`);
            const data = await res.json();

            if (Array.isArray(data) && data.length) {
                populateSelect(distritoSelect, data, 'id_distrito', 'nombre');
            } else {
                resetSelect(distritoSelect, t('msg-no-districts'), true);
                showNotification(t('msg-no-districts'), 'error');
            }
        } catch {
            showNotification(t('msg-error-load-districts'), 'error');
            resetSelect(distritoSelect, t('msg-error-load-districts'), true);
        }
    });

    /* ==================== VALIDACIÓN ==================== */
    form.addEventListener('submit', function (e) {
        const errors = [];

        if (!direccionInput.value.trim()) errors.push(t('msg-error-address'));
        if (!departamentoSelect.value) errors.push(t('msg-error-department'));
        if (!provinciaSelect.value) errors.push(t('msg-error-province'));
        if (!distritoSelect.value) errors.push(t('msg-error-district'));

        if (errors.length) {
            e.preventDefault();
            errors.forEach(msg => showNotification(msg, 'error'));
            return;
        }

        const btn = form.querySelector('button[type="submit"]');
        if (btn) {
            btn.disabled = true;
            const btnText = btn.querySelector('span');
            if (btnText) {
                btnText.textContent = t('msg-processing');
            }
        }
    });

    console.log('✅ step_2.js listo con i18n y cascada');
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