function toggleCarrera() {
            const estudiosSelect = document.getElementById("id_estudios");
            const carreraField = document.getElementById("field-carrera");
            if (estudiosSelect.value === "universitario") {
                carreraField.style.display = "block";
            } else {
                carreraField.style.display = "none";
            }
        }

        document.addEventListener("DOMContentLoaded", function () {
            const estudios = document.getElementById("id_estudios");
            if (estudios) {
                estudios.addEventListener("change", toggleCarrera);
                toggleCarrera();  // Llamar al cargar por si hay valor precargado
            }
        });