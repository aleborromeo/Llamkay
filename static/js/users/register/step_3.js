// =============================================
// REGISTRO PASO 3 - PERFIL PROFESIONAL
// Version 3.0 - Completamente funcional
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ step_3.js cargado correctamente');
    
    // ==================== ELEMENTOS DEL DOM ====================
    const estudiosSelect = document.getElementById('id_estudios');
    const carreraField = document.getElementById('field-carrera');
    const carreraInput = document.getElementById('id_carrera');
    const certificacionesInput = document.getElementById('id_certificaciones');
    const uploadArea = document.getElementById('uploadArea');
    const fileList = document.getElementById('fileList');
    const form = document.querySelector('.register-form');

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
                error: `${file.name} excede el tamaño máximo de 5MB`
            };
        }
        
        if (!allowedTypes.includes(file.type)) {
            return {
                valid: false,
                error: `${file.name} no es un formato válido (solo PDF, JPG, PNG)`
            };
        }
        
        return { valid: true };
    }

    /**
     * Muestra archivos seleccionados
     */
    function displayFiles(files) {
        if (!fileList) return;
        
        fileList.innerHTML = '';
        
        Array.from(files).forEach((file, index) => {
            const fileDiv = document.createElement('div');
            fileDiv.className = 'selected-file';
            fileDiv.style.cssText = `
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 1rem;
                background: #f8f9fa;
                border-radius: 12px;
                margin-top: 0.75rem;
                animation: fadeIn 0.3s ease;
            `;
            
            fileDiv.innerHTML = `
                <div class="file-info-display" style="display: flex; align-items: center; gap: 0.75rem; flex: 1;">
                    <div class="file-icon" style="
                        width: 40px;
                        height: 40px;
                        background: linear-gradient(135deg, #07734B, #15AC75);
                        border-radius: 8px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-size: 20px;
                        flex-shrink: 0;
                    ">
                        ${file.type === 'application/pdf' ? '📄' : '🖼️'}
                    </div>
                    <div class="file-details" style="flex: 1; min-width: 0;">
                        <h5 style="
                            color: #1a1a1a;
                            margin: 0 0 0.25rem 0;
                            font-size: 0.95rem;
                            font-weight: 600;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                        ">${file.name}</h5>
                        <span class="file-size" style="
                            font-size: 0.85rem;
                            color: #666;
                        ">${formatFileSize(file.size)}</span>
                    </div>
                </div>
                <button type="button" class="remove-file" data-index="${index}" style="
                    background: none;
                    border: none;
                    color: #dc2626;
                    font-size: 1.5rem;
                    cursor: pointer;
                    padding: 0.5rem;
                    transition: all 0.2s;
                ">×</button>
            `;
            
            fileList.appendChild(fileDiv);
        });
        
        // Agregar event listeners a botones de eliminar
        document.querySelectorAll('.remove-file').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                removeFile(index);
            });
        });
    }

    /**
     * Elimina un archivo de la lista
     */
    function removeFile(index) {
        if (!certificacionesInput || !certificacionesInput.files) return;
        
        const dt = new DataTransfer();
        const files = Array.from(certificacionesInput.files);
        
        files.forEach((file, i) => {
            if (i !== index) {
                dt.items.add(file);
            }
        });
        
        certificacionesInput.files = dt.files;
        displayFiles(certificacionesInput.files);
        
        if (certificacionesInput.files.length === 0) {
            showNotification('Archivo eliminado', 'info');
        }
    }

    // ==================== TOGGLE CAMPO CARRERA ====================
    
    if (estudiosSelect && carreraField && carreraInput) {
        function toggleCarrera() {
            const nivel = estudiosSelect.value;
            
            if (nivel === 'universitario' || nivel === 'posgrado') {
                carreraField.style.display = 'block';
                carreraInput.required = true;
            } else {
                carreraField.style.display = 'none';
                carreraInput.required = false;
                carreraInput.value = '';
            }
        }
        
        estudiosSelect.addEventListener('change', toggleCarrera);
        
        // Ejecutar al cargar para estado inicial
        toggleCarrera();
    }

    // ==================== FILE UPLOAD CON DRAG & DROP ====================
    
    if (uploadArea && certificacionesInput && fileList) {
        
        // Click para abrir selector
        uploadArea.addEventListener('click', () => {
            certificacionesInput.click();
        });

        // Drag over
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadArea.classList.add('drag-over');
            uploadArea.style.borderColor = '#07734B';
            uploadArea.style.background = '#e8f5f0';
        });

        // Drag leave
        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadArea.classList.remove('drag-over');
            uploadArea.style.borderColor = '#d1d5db';
            uploadArea.style.background = '#f8f9fa';
        });

        // Drop
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadArea.classList.remove('drag-over');
            uploadArea.style.borderColor = '#d1d5db';
            uploadArea.style.background = '#f8f9fa';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                // Validar archivos
                const validFiles = [];
                let hasErrors = false;
                
                Array.from(files).forEach(file => {
                    const validation = validateFile(file);
                    if (validation.valid) {
                        validFiles.push(file);
                    } else {
                        showNotification(validation.error, 'error');
                        hasErrors = true;
                    }
                });
                
                if (validFiles.length > 0) {
                    const dt = new DataTransfer();
                    validFiles.forEach(file => dt.items.add(file));
                    certificacionesInput.files = dt.files;
                    displayFiles(certificacionesInput.files);
                    
                    if (!hasErrors) {
                        showNotification(`${validFiles.length} archivo(s) agregado(s)`, 'success');
                    }
                }
            }
        });

        // Change
        certificacionesInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                // Validar archivos
                const validFiles = [];
                let hasErrors = false;
                
                Array.from(this.files).forEach(file => {
                    const validation = validateFile(file);
                    if (validation.valid) {
                        validFiles.push(file);
                    } else {
                        showNotification(validation.error, 'error');
                        hasErrors = true;
                    }
                });
                
                if (validFiles.length > 0) {
                    const dt = new DataTransfer();
                    validFiles.forEach(file => dt.items.add(file));
                    this.files = dt.files;
                    displayFiles(this.files);
                    
                    if (!hasErrors) {
                        showNotification(`${validFiles.length} archivo(s) seleccionado(s)`, 'success');
                    }
                } else {
                    this.value = '';
                }
            }
        });
    }

    // ==================== VALIDACIÓN DEL FORMULARIO ====================
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const errors = [];
            
            // Validar habilidades
            const habilidadesInput = document.getElementById('id_habilidades');
            if (habilidadesInput && !habilidadesInput.value.trim()) {
                errors.push('Por favor describe tus habilidades');
            }
            
            // Validar disponibilidad
            const disponibilidadSelect = document.getElementById('id_disponibilidad');
            if (disponibilidadSelect && !disponibilidadSelect.value) {
                errors.push('Por favor selecciona tu disponibilidad');
            }
            
            // Validar estudios
            if (estudiosSelect && !estudiosSelect.value) {
                errors.push('Por favor selecciona tu nivel de estudios');
            }
            
            // Validar carrera si es necesario
            if (carreraInput && carreraInput.required && !carreraInput.value.trim()) {
                errors.push('Por favor ingresa tu carrera universitaria');
            }
            
            if (errors.length > 0) {
                e.preventDefault();
                errors.forEach(error => showNotification(error, 'error'));
                
                // Enfocar primer campo con error
                if (habilidadesInput && !habilidadesInput.value.trim()) {
                    habilidadesInput.focus();
                }
                
                return false;
            }
            
            // Mostrar loading
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
            }
            
            console.log('✅ Formulario step 3 válido, enviando...');
        });
    }

    // ==================== AUTO-GUARDAR PROGRESO ====================
    
    function saveProgress() {
        const progress = {
            habilidades: document.getElementById('id_habilidades')?.value || '',
            experiencia: document.getElementById('id_experiencia')?.value || '',
            disponibilidad: document.getElementById('id_disponibilidad')?.value || '',
            tarifa: document.getElementById('id_tarifa')?.value || '',
            estudios: estudiosSelect?.value || '',
            carrera: carreraInput?.value || ''
        };
        localStorage.setItem('registro_step3', JSON.stringify(progress));
    }
    
    function loadProgress() {
        try {
            const saved = localStorage.getItem('registro_step3');
            if (saved) {
                const progress = JSON.parse(saved);
                
                if (progress.habilidades) {
                    const habilidadesInput = document.getElementById('id_habilidades');
                    if (habilidadesInput) habilidadesInput.value = progress.habilidades;
                }
                
                if (progress.experiencia) {
                    const experienciaSelect = document.getElementById('id_experiencia');
                    if (experienciaSelect) experienciaSelect.value = progress.experiencia;
                }
                
                if (progress.disponibilidad) {
                    const disponibilidadSelect = document.getElementById('id_disponibilidad');
                    if (disponibilidadSelect) disponibilidadSelect.value = progress.disponibilidad;
                }
                
                if (progress.tarifa) {
                    const tarifaInput = document.getElementById('id_tarifa');
                    if (tarifaInput) tarifaInput.value = progress.tarifa;
                }
                
                if (progress.estudios && estudiosSelect) {
                    estudiosSelect.value = progress.estudios;
                    // Trigger change para mostrar campo carrera si aplica
                    estudiosSelect.dispatchEvent(new Event('change'));
                    
                    if (progress.carrera && carreraInput) {
                        carreraInput.value = progress.carrera;
                    }
                }
            }
        } catch (e) {
            console.error('Error al cargar progreso:', e);
        }
    }
    
    // Cargar progreso
    loadProgress();
    
    // Guardar en cada cambio
    const fieldsToWatch = [
        'id_habilidades',
        'id_experiencia',
        'id_disponibilidad',
        'id_tarifa',
        'id_estudios',
        'id_carrera'
    ];
    
    fieldsToWatch.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', saveProgress);
            field.addEventListener('change', saveProgress);
        }
    });

    console.log('✅ step_3.js listo');
});

// Agregar estilos de animación
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
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .remove-file:hover {
        transform: scale(1.2);
        color: #b91c1c !important;
    }
`;
if (!document.getElementById('step3-animations')) {
    style.id = 'step3-animations';
    document.head.appendChild(style);
}