// Función para mostrar banner de notificación
function showBanner(type, title, message) {
    // Remover banner existente si existe
    const existingBanner = document.querySelector('.notification-banner');
    if (existingBanner) {
        existingBanner.remove();
    }

    // Crear nuevo banner
    const banner = document.createElement('div');
    banner.className = `notification-banner ${type}`;
    
    // Definir iconos según el tipo
    const icons = {
        error: '❌',
        success: '✅',
        warning: '⚠️'
    };

    banner.innerHTML = `
        <span class="banner-icon">${icons[type] || '📢'}</span>
        <div class="banner-content">
            <div class="banner-title">${title}</div>
            <div class="banner-message">${message}</div>
        </div>
        <button class="close-btn" onclick="hideBanner()">&times;</button>
    `;

    document.body.appendChild(banner);

    // Mostrar banner con animación
    setTimeout(() => {
        banner.classList.add('show');
    }, 100);

    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        hideBanner();
    }, 5000);
}

// Función para ocultar banner
function hideBanner() {
    const banner = document.querySelector('.notification-banner');
    if (banner) {
        banner.classList.remove('show');
        setTimeout(() => {
            banner.remove();
        }, 300);
    }
}

// Event listener principal para el campo de certificaciones
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]'); // Campo de certificaciones
    
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            
            if (file) {
                // Agregar clase visual cuando se selecciona un archivo
                this.classList.add('file-selected');
                
                // Validar tamaño del archivo (5MB = 5 * 1024 * 1024 bytes)
                const maxSize = 5 * 1024 * 1024;
                if (file.size > maxSize) {
                    showBanner('error', 'Archivo demasiado grande', 
                             'El archivo excede el tamaño máximo permitido de 5MB.');
                    this.value = '';
                    this.classList.remove('file-selected');
                    return;
                }
                
                // Validar tipo de archivo
                const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
                if (!allowedTypes.includes(file.type)) {
                    showBanner('error', 'Tipo de archivo no válido', 
                             'Solo se aceptan archivos PDF, JPG, JPEG y PNG.');
                    this.value = '';
                    this.classList.remove('file-selected');
                    return;
                }

                // Si todo está bien, mostrar mensaje de éxito
                showBanner('success', 'Certificación cargada', 
                         `${file.name} se ha seleccionado correctamente.`);
                
            } else {
                this.classList.remove('file-selected');
            }
        });
    }
});