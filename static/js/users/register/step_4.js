// ===== REGISTRO PASO 4 - Antecedentes Penales =====

document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 Registro Step 4 - Antecedentes Penales iniciado');
    
    const fileInput = document.getElementById('antecedentes');
    const fileUploadDisplay = document.getElementById('fileUploadDisplay');
    const selectedFilesContainer = document.getElementById('selectedFiles');
    
    if (!fileInput || !fileUploadDisplay) {
        console.warn('⚠️ No se encontraron elementos de upload');
        return;
    }
    
    // Manejar selección de archivo
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        if (!file) {
            resetFileDisplay();
            return;
        }
        
        // Validar tamaño (5MB)
        const maxSize = 5 * 1024 * 1024;
        if (file.size > maxSize) {
            showNotification('El archivo excede el tamaño máximo de 5MB', 'error');
            this.value = '';
            resetFileDisplay();
            return;
        }
        
        // Validar tipo
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
        if (!allowedTypes.includes(file.type)) {
            showNotification('Solo se aceptan archivos PDF, JPG, JPEG y PNG', 'error');
            this.value = '';
            resetFileDisplay();
            return;
        }
        
        // Mostrar archivo seleccionado
        displaySelectedFile(file);
        showNotification('Archivo cargado correctamente', 'success');
    });
    
    // Drag and drop
    fileUploadDisplay.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.classList.add('drag-over');
    });
    
    fileUploadDisplay.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.classList.remove('drag-over');
    });
    
    fileUploadDisplay.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });
    
    /**
     * Mostrar archivo seleccionado
     */
    function displaySelectedFile(file) {
        fileUploadDisplay.classList.add('has-files');
        
        const fileName = file.name;
        const fileSize = formatFileSize(file.size);
        
        if (selectedFilesContainer) {
            selectedFilesContainer.innerHTML = `
                <div class="upload-file-item">
                    <span class="upload-file-name">${fileName}</span>
                    <span class="upload-file-size">${fileSize}</span>
                </div>
            `;
        }
        
        // Crear lista dentro del display si no existe el container
        if (!selectedFilesContainer) {
            let uploadList = fileUploadDisplay.querySelector('.upload-files-list');
            if (!uploadList) {
                uploadList = document.createElement('div');
                uploadList.className = 'upload-files-list';
                fileUploadDisplay.appendChild(uploadList);
            }
            
            uploadList.innerHTML = `
                <div class="upload-file-item">
                    <span class="upload-file-name">${fileName}</span>
                    <span class="upload-file-size">${fileSize}</span>
                </div>
            `;
        }
    }
    
    /**
     * Resetear display de archivos
     */
    function resetFileDisplay() {
        fileUploadDisplay.classList.remove('has-files');
        if (selectedFilesContainer) {
            selectedFilesContainer.innerHTML = '';
        }
        const uploadList = fileUploadDisplay.querySelector('.upload-files-list');
        if (uploadList) {
            uploadList.remove();
        }
    }
    
    /**
     * Formatear tamaño de archivo
     */
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
    
    // Validación del formulario
    const form = document.getElementById('registerFourForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                showNotification('Por favor sube tu constancia de antecedentes penales', 'error');
                fileInput.focus();
                return false;
            }
        });
    }
    
    console.log('✅ Registro Step 4 listo');
});