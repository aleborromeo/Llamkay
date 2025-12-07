/**
 * ===================================
 * FUNCIONALIDAD DE VER CHAT (con AJAX)
 * ===================================
 */

let currentChatId = null;
let lastMessageId = null;
let pollingIntervalId = null;
let currentEditingMessageId = null;

/* ================================
 * UTILIDADES
 * ================================ */

function escapeHtml(text) {
    if (text === null || text === undefined) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

/**
 * Construye un elemento DOM <div class="message"> a partir de datos JSON.
 * Se usa tanto para mensajes nuevos (polling) como para los que envía el usuario.
 */
function buildMessageElement(data) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(data.es_mio ? "sent" : "received");
    messageDiv.dataset.mensajeId = data.id_mensaje;

    const contenidoEscapado = escapeHtml(data.contenido || "");
    const textoHtml = data.editado
        ? `<span class="mensaje-editado">${contenidoEscapado} <em>(editado)</em></span>`
        : contenidoEscapado;

    messageDiv.innerHTML = `
        <div class="message-content">
            <p class="message-text"
               data-original-text="${contenidoEscapado}">
                ${textoHtml}
            </p>
            <small>${data.created_at}</small>

            <div class="message-content-footer">
                <div class="translation-controls">
                    <span class="translation-label">Traducir este mensaje:</span>
                    <select class="translation-select">
                        <option value="en">Inglés</option>
                        <option value="es">Español</option>
                        <option value="pt">Portugués</option>
                        <option value="fr">Francés</option>
                    </select>
                    <button type="button" class="translation-btn">Traducir</button>
                </div>

                ${data.es_mio ? `
                    <div class="message-actions">
                        <button class="action-btn edit-btn"
                                data-mensaje-id="${data.id_mensaje}"
                                data-contenido="${contenidoEscapado}"></button>
                        <button class="action-btn delete-btn"
                                data-mensaje-id="${data.id_mensaje}"></button>
                    </div>
                ` : ""}
            </div>
        </div>
    `;

    return messageDiv;
}

/* ================================
 * AUTO-SCROLL
 * ================================ */

function initAutoScroll() {
    const messagesContainer = document.querySelector(".messages");

    if (!messagesContainer) {
        console.error("No se encontró el contenedor de mensajes");
        return;
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    setTimeout(scrollToBottom, 100);

    const observer = new MutationObserver(function (mutations) {
        let shouldScroll = false;
        mutations.forEach(function (mutation) {
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
        subtree: true,
    });

    window.addEventListener("load", function () {
        setTimeout(scrollToBottom, 200);
    });
}

/* ================================
 * MODAL DE EDICIÓN
 * ================================ */

function openEditModal(messageId, currentContent) {
    currentEditingMessageId = messageId;
    const modal = document.getElementById("editModal");
    const textarea = document.getElementById("editTextarea");
    const form = document.getElementById("editForm");

    if (modal && textarea && form) {
        textarea.value = currentContent;
        form.action = `/chats/mensaje/editar/${messageId}/`;
        modal.style.display = "block";
    }
}

function closeEditModal() {
    const modal = document.getElementById("editModal");
    if (modal) {
        modal.style.display = "none";
        currentEditingMessageId = null;
    }
}

function initModalClose() {
    const modal = document.getElementById("editModal");
    const closeBtn = modal ? modal.querySelector(".close") : null;
    const cancelBtn = modal ? modal.querySelector(".cancel-btn") : null;

    if (closeBtn) {
        closeBtn.addEventListener("click", closeEditModal);
    }

    if (cancelBtn) {
        cancelBtn.addEventListener("click", closeEditModal);
    }

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeEditModal();
        }
    });
}

/* ================================
 * ELIMINAR MENSAJE
 * ================================ */

function deleteMessage(messageId) {
    if (!confirm("¿Estás seguro de que quieres eliminar este mensaje?")) {
        return;
    }

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch(`/chats/mensaje/eliminar/${messageId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const msgEl = document.querySelector(
                    `.message[data-mensaje-id="${messageId}"]`
                );
                if (msgEl) {
                    msgEl.remove();
                }
            } else {
                alert(data.error || "Error al eliminar el mensaje");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Error al eliminar el mensaje");
        });
}

/* ================================
 * TEXTAREA AUTOSIZE
 * ================================ */

function initTextareaResize() {
    const textarea = document.querySelector(".message-form textarea");
    const form = document.querySelector(".message-form");

    if (!textarea || !form) return;

    function autoResize() {
        textarea.style.height = "auto";
        const newHeight = Math.min(Math.max(textarea.scrollHeight, 20), 100);
        textarea.style.height = newHeight + "px";
    }

    textarea.addEventListener("input", autoResize);

    textarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            form.dispatchEvent(
                new Event("submit", { cancelable: true, bubbles: true })
            );
        }
    });

    autoResize();
}

/* ================================
 * ENVÍO DE MENSAJE (AJAX)
 * ================================ */

function initFormSubmit() {
    const form = document.querySelector(".message-form");
    const textarea = document.querySelector(".message-form textarea");
    const messagesContainer = document.querySelector(".messages");

    if (!form || !textarea || !messagesContainer) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const content = textarea.value.trim();
        if (!content) {
            alert("Por favor escribe un mensaje");
            return false;
        }

        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrfToken,
            },
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    console.error("Error al enviar mensaje:", data);
                    alert("No se pudo enviar el mensaje.");
                    return;
                }

                // Crear el nodo del nuevo mensaje (enviado por el usuario actual)
                const messageDiv = buildMessageElement(data);
                messagesContainer.appendChild(messageDiv);

                // actualizar último id conocido
                lastMessageId = data.id_mensaje;

                // Reiniciar textarea
                textarea.value = "";
                textarea.style.height = "auto";

                // Scroll al final
                messagesContainer.scrollTop = messagesContainer.scrollHeight;

                // Enganchar eventos en el nuevo mensaje
                attachActionButtons(messageDiv);
                attachTranslationControls(messageDiv);
            })
            .catch((error) => {
                console.error("Error al enviar mensaje:", error);
                alert("Ocurrió un error al enviar el mensaje");
            });
    });
}

/* ================================
 * EDICIÓN DE MENSAJE (AJAX)
 * ================================ */

function initEditFormAjax() {
    const editForm = document.getElementById("editForm");
    const editTextarea = document.getElementById("editTextarea");

    if (!editForm || !editTextarea) return;

    editForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const content = editTextarea.value.trim();
        if (!content) {
            alert("El mensaje no puede estar vacío");
            return;
        }

        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        const formData = new FormData(editForm);

        fetch(editForm.action, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrfToken,
            },
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    console.error("Error al editar mensaje:", data);
                    alert("No se pudo editar el mensaje.");
                    return;
                }

                const msgEl = document.querySelector(
                    `.message[data-mensaje-id="${data.id_mensaje}"]`
                );
                if (msgEl) {
                    const p = msgEl.querySelector(".message-text");
                    if (p) {
                        const contenidoEscapado = escapeHtml(data.contenido || "");
                        if (data.editado) {
                            p.innerHTML = `<span class="mensaje-editado">${contenidoEscapado} <em>(editado)</em></span>`;
                        } else {
                            p.textContent = data.contenido;
                        }
                        // actualizar data-original-text para traducciones
                        p.dataset.originalText = contenidoEscapado;
                    }

                    // Actualizar atributo data-contenido del botón editar
                    const editBtn = msgEl.querySelector(".edit-btn");
                    if (editBtn) {
                        editBtn.dataset.contenido = data.contenido;
                    }

                    // resetear estado de traducción (si lo había)
                    delete msgEl.dataset.originalHtml;
                    msgEl.dataset.isTranslated = "false";
                }

                closeEditModal();
            })
            .catch((error) => {
                console.error("Error al editar mensaje:", error);
                alert("Ocurrió un error al editar el mensaje");
            });
    });
}

/* ================================
 * BOTONES EDITAR / ELIMINAR
 * ================================ */

function attachActionButtons(root) {
    const editButtons = root.querySelectorAll(".edit-btn");
    const deleteButtons = root.querySelectorAll(".delete-btn");

    editButtons.forEach((btn) => {
        btn.addEventListener("click", function () {
            const messageId = this.dataset.mensajeId;
            const contenido = this.dataset.contenido;
            openEditModal(messageId, contenido);
        });
    });

    deleteButtons.forEach((btn) => {
        btn.addEventListener("click", function () {
            const messageId = this.dataset.mensajeId;
            deleteMessage(messageId);
        });
    });
}

function initActionButtons() {
    attachActionButtons(document);
}

/* ================================
 * TRADUCCIÓN DE MENSAJES
 * ================================ */

function translateMessage(messageElem, targetLang) {
    const messageId = messageElem.dataset.mensajeId;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    if (!messageId) return;

    const url = `/chats/mensaje/traducir/${messageId}/`;

    const formData = new URLSearchParams();
    formData.append("target_lang", targetLang || "en");

    const textElem = messageElem.querySelector(".message-text");
    const controls = messageElem.querySelector(".translation-controls");
    const label = controls ? controls.querySelector(".translation-label") : null;
    const button = controls ? controls.querySelector(".translation-btn") : null;

    if (button) {
        button.disabled = true;
        button.textContent = "Traduciendo...";
    }

    fetch(url, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                console.error("Error al traducir:", data);
                alert(data.error || "No se pudo traducir el mensaje.");
                return;
            }

            if (!textElem) return;

            // Guardamos el HTML original solo una vez
            if (!messageElem.dataset.originalHtml) {
                messageElem.dataset.originalHtml = textElem.innerHTML;
            }

            const translated = escapeHtml(data.texto_traducido || "");
            const wasEdited = !!messageElem.querySelector(".mensaje-editado");

            if (wasEdited) {
                textElem.innerHTML = `<span class="mensaje-editado">${translated} <em>(editado)</em></span>`;
            } else {
                textElem.textContent = data.texto_traducido;
            }

            messageElem.dataset.isTranslated = "true";

            if (label && button) {
                label.textContent = "Regresar al lenguaje original:";
                const idiomaOrigen = (data.idioma_origen || "es").toUpperCase();
                button.textContent = `Ver en ${idiomaOrigen}`;
                button.classList.add("is-restore");
            }
        })
        .catch((error) => {
            console.error("Error al traducir mensaje:", error);
            alert("Ocurrió un error al traducir el mensaje.");
        })
        .finally(() => {
            if (button) {
                button.disabled = false;
                if (!button.classList.contains("is-restore")) {
                    button.textContent = "Traducir";
                }
            }
        });
}

function restoreOriginalMessage(messageElem) {
    const textElem = messageElem.querySelector(".message-text");
    const controls = messageElem.querySelector(".translation-controls");
    const label = controls ? controls.querySelector(".translation-label") : null;
    const button = controls ? controls.querySelector(".translation-btn") : null;

    const originalHtml = messageElem.dataset.originalHtml;

    if (!originalHtml || !textElem) return;

    textElem.innerHTML = originalHtml;
    messageElem.dataset.isTranslated = "false";

    if (label && button) {
        label.textContent = "Traducir este mensaje:";
        button.textContent = "Traducir";
        button.classList.remove("is-restore");
    }
}

function attachTranslationControls(root) {
    const containers = root.querySelectorAll(".translation-controls");

    containers.forEach((container) => {
        const select = container.querySelector(".translation-select");
        const button = container.querySelector(".translation-btn");
        const messageElem = container.closest(".message");

        if (!select || !button || !messageElem) return;

        button.addEventListener("click", function () {
            const isTranslated = messageElem.dataset.isTranslated === "true";

            if (isTranslated) {
                restoreOriginalMessage(messageElem);
            } else {
                const targetLang = select.value || "en";
                translateMessage(messageElem, targetLang);
            }
        });
    });
}

/* ================================
 * POLLING DE MENSAJES NUEVOS
 * ================================ */

function initLastMessageId() {
    const lastMsgEl = document.querySelector(".messages .message:last-of-type");
    if (lastMsgEl) {
        lastMessageId = lastMsgEl.dataset.mensajeId;
    } else {
        lastMessageId = null;
    }
}

function fetchNewMessages() {
    if (!currentChatId) return;

    const messagesContainer = document.querySelector(".messages");
    if (!messagesContainer) return;

    let url = `/chats/chat/${currentChatId}/mensajes-nuevos/`;
    if (lastMessageId) {
        url += `?after_id=${lastMessageId}`;
    }

    fetch(url, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                console.error("Error al obtener mensajes nuevos:", data);
                return;
            }

            if (!Array.isArray(data.mensajes) || data.mensajes.length === 0) {
                return;
            }

            data.mensajes.forEach((msg) => {
                const msgEl = buildMessageElement(msg);
                messagesContainer.appendChild(msgEl);
                lastMessageId = msg.id_mensaje;

                attachActionButtons(msgEl);
                attachTranslationControls(msgEl);
            });

            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch((error) => {
            console.error("Error en polling de mensajes:", error);
        });
}

function startPollingNewMessages() {
    if (!currentChatId) return;
    initLastMessageId();
    pollingIntervalId = setInterval(fetchNewMessages, 3000); // cada 3s
}

/* ================================
 * INICIALIZACIÓN
 * ================================ */

document.addEventListener("DOMContentLoaded", function () {
    console.log("Inicializando ver-chat.js");

    const chatWindow = document.querySelector(".chat-window");

    if (chatWindow) {
        currentChatId = chatWindow.dataset.chatId || null;

        initAutoScroll();
        initTextareaResize();
        initFormSubmit();
        initModalClose();
        initActionButtons();
        initEditFormAjax();
        attachTranslationControls(document);
        startPollingNewMessages();

        console.log("ver-chat.js inicializado correctamente");
    }
});
