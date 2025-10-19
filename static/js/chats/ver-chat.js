/**
 * ===================================
 * FUNCIONALIDAD DE VER CHAT
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
 * Eliminar mensaje
 */
function deleteMessage(messageId) {
    if (confirm('¿Estás seguro de que quieres eliminar este mensaje?')) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(`/chats/mensaje/eliminar/${messageId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Error al eliminar el mensaje');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al eliminar el mensaje');
        });
    }
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
            form.submit();
        }
    });
    
    autoResize();
}

/**
 * Manejar envío de formulario
 */
function initFormSubmit() {
    const form = document.querySelector('.message-form');
    const textarea = document.querySelector('.message-form textarea');
    
    if (!form || !textarea) return;
    
    form.addEventListener('submit', function(e) {
        const content = textarea.value.trim();
        
        if (!content) {
            e.preventDefault();
            alert('Por favor escribe un mensaje');
            return false;
        }
        
        const messagesContainer = document.querySelector('.messages');
        if (messagesContainer) {
            textarea.value = '';
            textarea.style.height = 'auto';
            
            setTimeout(function() {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }, 50);
        }
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
 * Inicializar event listeners para botones de acción
 */
function initActionButtons() {
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const messageId = this.dataset.mensajeId;
            const contenido = this.dataset.contenido;
            openEditModal(messageId, contenido);
        });
    });
    
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const messageId = this.dataset.mensajeId;
            deleteMessage(messageId);
        });
    });
}

/**
 * Inicializar todo cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Inicializando ver-chat.js');
    
    // Verificar que estamos en la página correcta
    if (document.querySelector('.chat-window')) {
        initAutoScroll();
        initTextareaResize();
        initFormSubmit();
        initModalClose();
        initActionButtons();
        
        console.log('✅ Ver-chat.js inicializado correctamente');
    }
});