// Preview de la foto seleccionada
        document.getElementById('foto').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.querySelector('.profile-photo').src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });