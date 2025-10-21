// === step_1.js ===
// Manejo de búsqueda de DNI y RUC usando apiperu.dev
// + Corrección de estructura data.data.*
// + Limpieza y desbloqueo de campos dinámicos

document.addEventListener("DOMContentLoaded", function () {
    console.log("🧠 step_1.js cargado correctamente");

    const btnBuscarDNI = document.querySelector('button[data-action="buscar-dni"]');
    const btnBuscarRUC = document.querySelector('button[data-action="buscar-ruc"]');

    // --- CONSULTAR DNI ---
    if (btnBuscarDNI) {
        btnBuscarDNI.addEventListener("click", async function () {
            const dniInput = document.querySelector('input[name="dni"]');
            const nombreInput = document.querySelector('input[name="nombre"]');
            const apellidoInput = document.querySelector('input[name="apellido"]');

            const dni = dniInput.value.trim();
            if (!dni || dni.length !== 8) {
                alert("⚠️ Ingresa un DNI válido de 8 dígitos");
                return;
            }

            try {
                console.log("🔍 Consultando DNI:", dni);
                const response = await fetch(`/users/api/consultar-dni/?dni=${dni}`);
                const data = await response.json();

                console.log("📦 Respuesta del servidor:", data);

                if (data.success && data.data) {
                    // Extraer los datos desde data.data
                    const info = data.data;

                    nombreInput.value = info.nombres || "";
                    apellidoInput.value = `${info.apellido_paterno || ""} ${info.apellido_materno || ""}`.trim();

                    console.log("✅ Datos llenados automáticamente");
                } else {
                    alert("❌ No se encontró información para el DNI ingresado");
                }
            } catch (error) {
                console.error("❌ Error en la consulta DNI:", error);
                alert("Error al consultar el DNI. Intenta nuevamente.");
            }
        });
    }

    // --- CONSULTAR RUC ---
    if (btnBuscarRUC) {
        btnBuscarRUC.addEventListener("click", async function () {
            const rucInput = document.querySelector('input[name="ruc"]');
            const razonSocialInput = document.querySelector('input[name="razon_social"]');
            const ruc = rucInput.value.trim();

            if (!ruc || ruc.length !== 11) {
                alert("⚠️ Ingresa un RUC válido de 11 dígitos");
                return;
            }

            try {
                console.log("🔍 Consultando RUC:", ruc);
                const response = await fetch(`/users/api/consultar-ruc/?ruc=${ruc}`);
                const data = await response.json();

                console.log("📦 Respuesta del servidor:", data);

                if (data.success && data.data) {
                    const info = data.data;
                    razonSocialInput.value = info.razon_social || "";
                    console.log("✅ Razón social completada automáticamente");
                } else {
                    alert("❌ No se encontró información para el RUC ingresado");
                }
            } catch (error) {
                console.error("❌ Error en la consulta RUC:", error);
                alert("Error al consultar el RUC. Intenta nuevamente.");
            }
        });
    }
});
