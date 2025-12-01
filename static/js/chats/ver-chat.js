/**
 * ===================================
 * FUNCIONALIDAD DE VER CHAT (con AJAX)
 * ===================================
 */

let currentEditingMessageId = null;

/**
 * Auto-scroll al final de los mensajes
 */
function initAutoScroll() {
    const messagesContainer = document.querySelector('.messages');
    
    if (!messagesContainer) {
        console.error('No se encontró el contenedor de mensajes');
        return;
    }
    
    function scrollToBottom() {
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }
    
    setTimeout(scrollToBottom, 100);
    
    const observer = new MutationObserver(function(mutations) {
        let shouldScroll = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                shouldScroll = true;
            }
        });
        if (shouldScroll) {
            setTimeout(scrollToBottom, 50);
        }
    });
    
    observer.observe(messagesContainer, { 
        childList: true, 
        subtree: true
    });
    
    window.addEventListener('load', function() {
        setTimeout(scrollToBottom, 200);
    });
}

/**
 * Abrir modal de edición
 */
function openEditModal(messageId, currentContent) {
    currentEditingMessageId = messageId;
    const modal = document.getElementById('editModal');
    const textarea = document.getElementById('editTextarea');
    const form = document.getElementById('editForm');
    
    if (modal && textarea && form) {
        textarea.value = currentContent;
        form.action = `/chats/mensaje/editar/${messageId}/`;
        modal.style.display = 'block';
    }
}

/**
 * Cerrar modal de edición
 */
function closeEditModal() {
    const modal = document.getElementById('editModal');
    if (modal) {
        modal.style.display = 'none';
        currentEditingMessageId = null;
    }
}

/**
 * Eliminar mensaje (AJAX)
 */
function deleteMessage(messageId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este mensaje?')) {
        return;
    }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/chats/mensaje/eliminar/${messageId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const msgEl = document.querySelector(`.message[data-mensaje-id="${messageId}"]`);
            if (msgEl) {
                msgEl.remove();
            }
        } else {
            alert(data.error || 'Error al eliminar el mensaje');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al eliminar el mensaje');
    });
}

/**
 * Auto-resize del textarea
 */
function initTextareaResize() {
    const textarea = document.querySelector('.message-form textarea');
    const form = document.querySelector('.message-form');
    
    if (!textarea || !form) return;
    
    function autoResize() {
        textarea.style.height = 'auto';
        const newHeight = Math.min(Math.max(textarea.scrollHeight, 20), 100);
        textarea.style.height = newHeight + 'px';
    }
    
    textarea.addEventListener('input', autoResize);
    
    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        }
    });
    
    autoResize();
}

/**
 * Envío de formulario de mensaje (AJAX)
 */
function initFormSubmit() {
    const form = document.querySelector('.message-form');
    const textarea = document.querySelector('.message-form textarea');
    const messagesContainer = document.querySelector('.messages');

    if (!form || !textarea || !messagesContainer) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const content = textarea.value.trim();
        if (!content) {
            alert('Por favor escribe un mensaje');
            return false;
        }

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Error al enviar mensaje:', data);
                alert('No se pudo enviar el mensaje.');
                return;
            }

            // Crear el nodo del nuevo mensaje (enviado por el usuario actual)
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', 'sent');
            messageDiv.dataset.mensajeId = data.id_mensaje;

            let innerHtml = `
                <div class="message-content">
                    <p>${data.editado 
                        ? `<span class="mensaje-editado">${data.contenido} <em>(editado)</em></span>` 
                        : data.contenido
                    }</p>
                    <small>${data.created_at}</small>
                    <div class="message-actions">
                        <button class="action-btn edit-btn" data-mensaje-id="${data.id_mensaje}" data-contenido="${data.contenido.replace(/"/g, '&quot;')}"></button>
                        <button class="action-btn delete-btn" data-mensaje-id="${data.id_mensaje}"></button>
                    </div>
                </div>
            `;
            messageDiv.innerHTML = innerHtml;

            messagesContainer.appendChild(messageDiv);

            // Reiniciar textarea
            textarea.value = '';
            textarea.style.height = 'auto';

            // Scroll al final
            messagesContainer.scrollTop = messagesContainer.scrollHeight;

            // Volver a enganchar eventos de acciones en los nuevos botones
            attachActionButtons(messageDiv);
        })
        .catch(error => {
            console.error('Error al enviar mensaje:', error);
            alert('Ocurrió un error al enviar el mensaje');
        });
    });
}

/**
 * Envío del formulario de edición (AJAX)
 */
function initEditFormAjax() {
    const editForm = document.getElementById('editForm');
    const editTextarea = document.getElementById('editTextarea');

    if (!editForm || !editTextarea) return;

    editForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const content = editTextarea.value.trim();
        if (!content) {
            alert('El mensaje no puede estar vacío');
            return;
        }

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData(editForm);

        fetch(editForm.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Error al editar mensaje:', data);
                alert('No se pudo editar el mensaje.');
                return;
            }

            const msgEl = document.querySelector(`.message[data-mensaje-id="${data.id_mensaje}"]`);
            if (msgEl) {
                const p = msgEl.querySelector('.message-content p');
                if (p) {
                    if (data.editado) {
                        p.innerHTML = `<span class="mensaje-editado">${data.contenido} <em>(editado)</em></span>`;
                    } else {
                        p.textContent = data.contenido;
                    }
                }
                // Actualizar atributo data-contenido del botón editar
                const editBtn = msgEl.querySelector('.edit-btn');
                if (editBtn) {
                    editBtn.dataset.contenido = data.contenido;
                }
            }

            closeEditModal();
        })
        .catch(error => {
            console.error('Error al editar mensaje:', error);
            alert('Ocurrió un error al editar el mensaje');
        });
    });
}

/**
 * Cerrar modal al hacer clic fuera
 */
function initModalClose() {
    const modal = document.getElementById('editModal');
    const closeBtn = modal ? modal.querySelector('.close') : null;
    const cancelBtn = modal ? modal.querySelector('.cancel-btn') : null;
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeEditModal);
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', closeEditModal);
    }
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeEditModal();
        }
    });
}

/**
 * Enganchar eventos de acción (editar / eliminar) a un contenedor
 */
function attachActionButtons(root) {
    const editButtons = root.querySelectorAll('.edit-btn');
    const deleteButtons = root.querySelectorAll('.delete-btn');

    editButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const messageId = this.dataset.mensajeId;
            const contenido = this.dataset.contenido;
            openEditModal(messageId, contenido);
        });
    });

    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const messageId = this.dataset.mensajeId;
            deleteMessage(messageId);
        });
    });
}

/**
 * Inicializar event listeners para botones de acción existentes
 */
function initActionButtons() {
    attachActionButtons(document); // aplica a todo el documento inicial
}

/**
 * Inicializar todo cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando ver-chat.js');
    
    // Verificar que estamos en la página de chat
    if (document.querySelector('.chat-window')) {
        initAutoScroll();
        initTextareaResize();
        initFormSubmit();
        initModalClose();
        initActionButtons();
        initEditFormAjax();
        
        console.log('ver-chat.js inicializado correctamente');
    }
});
