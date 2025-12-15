// =============================================
// REGISTRO PASO 1 - STEP 1
// i18n + UX + Accesibilidad + Nielsen
// =============================================

document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ step_1.js inicializado");

    /* ==================== I18N ==================== */
    const i18n = document.body.dataset;

    const t = key => i18n[key] || key;

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
            top: "20px",
            right: "20px",
            background: type === "success" ? "#10b981" : "#dc2626",
            color: "#fff",
            padding: "1rem 1.5rem",
            borderRadius: "12px",
            zIndex: 9999
        });

        document.body.appendChild(toast);

        setTimeout(() => toast.remove(), 3000);
    }

    /* ==================== VALIDACIONES ==================== */
    const isNumeric = v => /^\d+$/.test(v);

    function validarDNI(dni) {
        if (!dni) return t("msgDniEmpty");
        if (dni.length !== 8) return t("msgDniLength");
        if (!isNumeric(dni)) return t("msgDniNumbers");
        return null;
    }

    function validarRUC(ruc) {
        if (!ruc) return t("msgRucEmpty");
        if (ruc.length !== 11) return t("msgRucLength");
        if (!isNumeric(ruc)) return t("msgRucNumbers");
        return null;
    }

    /* ==================== LOADING BOTÓN ==================== */
    function setLoading(btn, state) {
        btn.disabled = state;
        btn.classList.toggle("loading", state);
    }

    /* ==================== DNI ==================== */
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
                    apellidoInput.value = `${data.data.apellido_paterno || ""} ${data.data.apellido_materno || ""}`;
                    nombreInput.removeAttribute("readonly");
                    apellidoInput.removeAttribute("readonly");
                    notify(t("msgDniSuccess"), "success");
                } else {
                    notify(data.error || t("msgGenericError"));
                }
            } catch {
                notify(t("msgConnectionError"));
            } finally {
                setLoading(btnBuscarDNI, false);
            }
        });
    }

    /* ==================== RUC ==================== */
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
                    notify(t("msgRucSuccess"), "success");
                } else {
                    notify(data.error || t("msgGenericError"));
                }
            } catch {
                notify(t("msgConnectionError"));
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
                return notify(t("msgPasswordMismatch"));
            }

            if (terms && !terms.checked) {
                e.preventDefault();
                return notify(t("msgTermsRequired"));
            }
        });
    }

    console.log("🎉 step_1.js listo con i18n y UX profesional");
});
