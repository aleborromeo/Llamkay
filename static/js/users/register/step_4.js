// =============================================
// REGISTRO PASO 4 - ANTECEDENTES PENALES (FINAL)
// Version 3.0 - Completamente funcional
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ step_4.js cargado correctamente');
    
    // ==================== ELEMENTOS DEL DOM ====================
    const fileInput = document.getElementById('antecedentes');
    const uploadArea = document.getElementById('uploadArea');
    const fileDisplay = document.getElementById('fileDisplay');
    const form = document.getElementById('registerFourForm');
    const submitBtn = document.getElementById('submitBtn');
    
    // Validar elementos
    if (!fileInput || !uploadArea) {
        console.error('⚠️ No se encontraron elementos de upload');
        return;
    }
    
    // ==================== FUNCIONES HELPER ====================
    
    /**
     * Muestra notificación
     */
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#dc2626' : '#3b82f6'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    /**
     * Formatea tamaño de archivo
     */
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
    
    /**
     * Valida archivo
     */
    function validateFile(file) {
        const maxSize = 5 * 1024 * 1024; // 5MB
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
        
        if (file.size > maxSize) {
            return {
                valid: false,
                error: 'El archivo excede el tamaño máximo de 5MB'
            };
        }
        
        if (!allowedTypes.includes(file.type)) {
            return {
                valid: false,
                error: 'Formato no válido. Solo se aceptan PDF, JPG y PNG'
            };
        }
        
        return { valid: true };
    }
    
    /**
     * Muestra archivo seleccionado
     */
    function displayFile(file) {
        if (!fileDisplay) return;
        
        const fileIcon = file.type === 'application/pdf' ? '📄' : '🖼️';
        
        fileDisplay.innerHTML = `
            <div class="selected-file" style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 1rem;
                background: #f0fdf4;
                border: 2px solid #10b981;
                border-radius: 12px;
                margin-top: 1rem;
                animation: fadeIn 0.3s ease;
            ">
                <div class="file-info-display" style="
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    flex: 1;
                ">
                    <div class="file-icon" style="
                        width: 48px;
                        height: 48px;
                        background: linear-gradient(135deg, #10b981, #059669);
                        border-radius: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-size: 24px;
                        flex-shrink: 0;
                    ">
                        ${fileIcon}
                    </div>
                    <div class="file-details" style="flex: 1; min-width: 0;">
                        <h5 style="
                            color: #065f46;
                            margin: 0 0 0.25rem 0;
                            font-size: 1rem;
                            font-weight: 600;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                        ">${file.name}</h5>
                        <span class="file-size" style="
                            font-size: 0.875rem;
                            color: #059669;
                            font-weight: 500;
                        ">${formatFileSize(file.size)}</span>
                    </div>
                </div>
                <button type="button" onclick="clearFile()" style="
                    background: none;
                    border: none;
                    color: #dc2626;
                    cursor: pointer;
                    font-size: 2rem;
                    padding: 0.5rem;
                    line-height: 1;
                    transition: all 0.2s;
                " onmouseover="this.style.transform='scale(1.2)'; this.style.color='#b91c1c';" 
                   onmouseout="this.style.transform='scale(1)'; this.style.color='#dc2626';">×</button>
            </div>
        `;
    }
    
    /**
     * Limpia archivo seleccionado
     */
    window.clearFile = function() {
        fileInput.value = '';
        if (fileDisplay) {
            fileDisplay.innerHTML = '';
        }
        showNotification('Archivo eliminado', 'info');
    };
    
    /**
     * Resetea área de upload
     */
    function resetUploadArea() {
        if (uploadArea) {
            uploadArea.classList.remove('drag-over');
            uploadArea.style.borderColor = '#d1d5db';
            uploadArea.style.background = '#f8f9fa';
        }
    }
    
    // ==================== EVENTOS DE UPLOAD ====================
    
    // Click para abrir selector
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag over
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('drag-over');
        uploadArea.style.borderColor = '#10b981';
        uploadArea.style.background = '#f0fdf4';
        uploadArea.style.transform = 'scale(1.02)';
    });

    // Drag leave
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        resetUploadArea();
        uploadArea.style.transform = 'scale(1)';
    });

    // Drop
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        resetUploadArea();
        uploadArea.style.transform = 'scale(1)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0]; // Solo el primer archivo
            
            // Validar
            const validation = validateFile(file);
            if (!validation.valid) {
                showNotification(validation.error, 'error');
                return;
            }
            
            // Asignar al input
            const dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
            
            // Mostrar
            displayFile(file);
            showNotification('✅ Archivo cargado correctamente', 'success');
        }
    });

    // Change
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            
            // Validar
            const validation = validateFile(file);
            if (!validation.valid) {
                showNotification(validation.error, 'error');
                this.value = '';
                if (fileDisplay) fileDisplay.innerHTML = '';
                return;
            }
            
            // Mostrar
            displayFile(file);
            showNotification('✅ Archivo seleccionado correctamente', 'success');
        }
    });

    // ==================== VALIDACIÓN DEL FORMULARIO ====================
    
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('📤 Enviando formulario final...');
            
            // Validar que hay archivo
            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                showNotification('⚠️ Por favor sube tu constancia de antecedentes penales', 'error');
                uploadArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
                uploadArea.style.animation = 'shake 0.5s';
                setTimeout(() => {
                    uploadArea.style.animation = '';
                }, 500);
                return false;
            }
            
            // Validar archivo una vez más
            const file = fileInput.files[0];
            const validation = validateFile(file);
            if (!validation.valid) {
                e.preventDefault();
                showNotification(validation.error, 'error');
                return false;
            }
            
            // Mostrar loading en botón
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                submitBtn.innerHTML = `
                    <svg style="animation: spin 1s linear infinite; margin-right: 0.5rem;" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="12" y1="2" x2="12" y2="6"></line>
                        <line x1="12" y1="18" x2="12" y2="22"></line>
                        <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
                        <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
                        <line x1="2" y1="12" x2="6" y2="12"></line>
                        <line x1="18" y1="12" x2="22" y2="12"></line>
                        <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
                        <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
                    </svg>
                    Finalizando registro...
                `;
            }
            
            // Mostrar mensaje de progreso
            showNotification('📤 Enviando tu información...', 'info');
            
            console.log('✅ Formulario válido, procesando registro...');
            
            // Limpiar localStorage de pasos anteriores
            ['registro_step2', 'registro_step3'].forEach(key => {
                localStorage.removeItem(key);
            });
        });
    }

    // ==================== INFORMACIÓN Y AYUDA ====================
    
    // Mostrar mensaje de bienvenida
    setTimeout(() => {
        const hasSeenWelcome = sessionStorage.getItem('step4_welcome');
        if (!hasSeenWelcome) {
            showNotification('📋 Último paso: sube tu certificado de antecedentes penales', 'info');
            sessionStorage.setItem('step4_welcome', 'true');
        }
    }, 500);

    console.log('✅ step_4.js listo - Sistema de registro completo');
});

// ==================== ESTILOS DE ANIMACIÓN ====================

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
    
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
        20%, 40%, 60%, 80% { transform: translateX(10px); }
    }
    
    .file-upload-area {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .file-upload-area:hover {
        transform: scale(1.02);
    }
    
    .btn.loading {
        pointer-events: none;
        opacity: 0.8;
    }
`;

if (!document.getElementById('step4-animations')) {
    style.id = 'step4-animations';
    document.head.appendChild(style);
}