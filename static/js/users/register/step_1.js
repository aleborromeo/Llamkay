// === step_1.js ===
// Manejo de búsqueda de DNI y RUC con validaciones mejoradas
// Versión 2.0 - Con manejo de errores robusto

document.addEventListener("DOMContentLoaded", function () {
    console.log("🧠 step_1.js cargado correctamente");

    const btnBuscarDNI = document.querySelector('button[data-action="buscar-dni"]');
    const btnBuscarRUC = document.querySelector('button[data-action="buscar-ruc"]');

    // ==================== HELPER FUNCTIONS ====================
    
    /**
     * Muestra un mensaje de error temporal
     */
    function mostrarError(mensaje) {
        alert(`⚠️ ${mensaje}`);
    }

    /**
     * Muestra un mensaje de éxito temporal
     */
    function mostrarExito(mensaje) {
        console.log(`✅ ${mensaje}`);
    }

    /**
     * Deshabilita un botón durante la consulta
     */
    function deshabilitarBoton(boton, mensaje = "Consultando...") {
        boton.disabled = true;
        boton.textContent = mensaje;
    }

    /**
     * Habilita un botón después de la consulta
     */
    function habilitarBoton(boton, mensaje = "Buscar") {
        boton.disabled = false;
        boton.textContent = mensaje;
    }

    // ==================== CONSULTAR DNI ====================
    
    if (btnBuscarDNI) {
        btnBuscarDNI.addEventListener("click", async function () {
            const dniInput = document.querySelector('input[name="dni"]');
            const nombreInput = document.querySelector('input[name="nombre"]');
            const apellidoInput = document.querySelector('input[name="apellido"]');

            const dni = dniInput.value.trim();

            // Validaciones
            if (!dni) {
                mostrarError("Por favor ingresa un DNI");
                dniInput.focus();
                return;
            }

            if (dni.length !== 8) {
                mostrarError("El DNI debe tener exactamente 8 dígitos");
                dniInput.focus();
                return;
            }

            if (!/^\d+$/.test(dni)) {
                mostrarError("El DNI solo debe contener números");
                dniInput.focus();
                return;
            }

            // Deshabilitar botón durante consulta
            deshabilitarBoton(btnBuscarDNI, "Buscando...");

            try {
                console.log("🔍 Consultando DNI:", dni);
                
                const response = await fetch(`/users/api/consultar-dni/?dni=${dni}`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    }
                });

                const data = await response.json();
                console.log("📦 Respuesta del servidor:", data);

                if (response.ok && data.success && data.data) {
                    // Extraer los datos
                    const info = data.data;

                    // Llenar campos
                    nombreInput.value = info.nombres || "";
                    apellidoInput.value = `${info.apellido_paterno || ""} ${info.apellido_materno || ""}`.trim();

                    // Hacer campos editables
                    nombreInput.removeAttribute('readonly');
                    apellidoInput.removeAttribute('readonly');
                    nombreInput.classList.remove('readonly-field');
                    apellidoInput.classList.remove('readonly-field');

                    mostrarExito("Datos cargados correctamente");
                    
                    // Enfocar siguiente campo
                    document.querySelector('input[name="telefono"]')?.focus();
                    
                } else {
                    const errorMsg = data.error || "No se encontró información para el DNI ingresado";
                    mostrarError(errorMsg);
                    
                    // Permitir edición manual
                    nombreInput.removeAttribute('readonly');
                    apellidoInput.removeAttribute('readonly');
                    nombreInput.classList.remove('readonly-field');
                    apellidoInput.classList.remove('readonly-field');
                    nombreInput.focus();
                }

            } catch (error) {
                console.error("❌ Error en la consulta DNI:", error);
                mostrarError("Error de conexión. Por favor intenta nuevamente.");
                
                // Permitir edición manual en caso de error
                nombreInput.removeAttribute('readonly');
                apellidoInput.removeAttribute('readonly');
                nombreInput.classList.remove('readonly-field');
                apellidoInput.classList.remove('readonly-field');
                
            } finally {
                // Siempre rehabilitar el botón
                habilitarBoton(btnBuscarDNI, "Buscar");
            }
        });
    }

    // ==================== CONSULTAR RUC ====================
    
    if (btnBuscarRUC) {
        btnBuscarRUC.addEventListener("click", async function () {
            const rucInput = document.querySelector('input[name="ruc"]');
            const razonSocialInput = document.querySelector('input[name="razon_social"]');
            const ruc = rucInput.value.trim();

            // Validaciones
            if (!ruc) {
                mostrarError("Por favor ingresa un RUC");
                rucInput.focus();
                return;
            }

            if (ruc.length !== 11) {
                mostrarError("El RUC debe tener exactamente 11 dígitos");
                rucInput.focus();
                return;
            }

            if (!/^\d+$/.test(ruc)) {
                mostrarError("El RUC solo debe contener números");
                rucInput.focus();
                return;
            }

            // Deshabilitar botón durante consulta
            deshabilitarBoton(btnBuscarRUC, "Buscando...");

            try {
                console.log("🔍 Consultando RUC:", ruc);
                
                const response = await fetch(`/users/api/consultar-ruc/?ruc=${ruc}`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    }
                });

                const data = await response.json();
                console.log("📦 Respuesta del servidor:", data);

                if (response.ok && data.success && data.data) {
                    const info = data.data;
                    
                    // Llenar campo
                    razonSocialInput.value = info.razon_social || "";
                    
                    // Hacer campo editable
                    razonSocialInput.removeAttribute('readonly');
                    razonSocialInput.classList.remove('readonly-field');
                    
                    mostrarExito("Razón social cargada correctamente");
                    
                    // Enfocar siguiente campo
                    document.querySelector('input[name="telefono"]')?.focus();
                    
                } else {
                    const errorMsg = data.error || "No se encontró información para el RUC ingresado";
                    mostrarError(errorMsg);
                    
                    // Permitir edición manual
                    razonSocialInput.removeAttribute('readonly');
                    razonSocialInput.classList.remove('readonly-field');
                    razonSocialInput.focus();
                }

            } catch (error) {
                console.error("❌ Error en la consulta RUC:", error);
                mostrarError("Error de conexión. Por favor intenta nuevamente.");
                
                // Permitir edición manual en caso de error
                razonSocialInput.removeAttribute('readonly');
                razonSocialInput.classList.remove('readonly-field');
                
            } finally {
                // Siempre rehabilitar el botón
                habilitarBoton(btnBuscarRUC, "Buscar");
            }
        });
    }

    // ==================== VALIDACIÓN DE FORMULARIO ====================
    
    const form = document.getElementById('registerForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const nombreInput = document.querySelector('input[name="nombre"]');
            const apellidoInput = document.querySelector('input[name="apellido"]');
            const razonSocialInput = document.querySelector('input[name="razon_social"]');
            
            // Validar que los campos readonly estén llenos
            if (nombreInput && !nombreInput.value.trim()) {
                e.preventDefault();
                mostrarError("Por favor busca el DNI primero");
                return false;
            }
            
            if (apellidoInput && !apellidoInput.value.trim()) {
                e.preventDefault();
                mostrarError("Por favor busca el DNI primero");
                return false;
            }
            
            if (razonSocialInput && !razonSocialInput.value.trim()) {
                e.preventDefault();
                mostrarError("Por favor busca el RUC primero");
                return false;
            }
        });
    }
});