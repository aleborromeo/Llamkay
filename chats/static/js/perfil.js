// static/js/perfil.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Perfil.js cargado');
    
    // Inicializar tabs
    initializeTabs();
    
    // Inicializar otros componentes
    initializeProfile();
});

/**
 * Inicializar funcionalidad de tabs
 */
function initializeTabs() {
    console.log('🔄 Inicializando tabs...');
    
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Verificar que existen tabs
    if (tabs.length === 0) {
        console.warn('⚠️ No se encontraron tabs');
        return;
    }
    
    // Agregar event listeners a cada tab
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('onclick');
            if (targetTab) {
                // Extraer el nombre del tab del onclick
                const tabName = targetTab.match(/showTab\('([^']+)'\)/)[1];
                showTab(tabName);
            }
        });
    });
    
    console.log(`✅ ${tabs.length} tabs inicializados`);
}

/**
 * Mostrar tab específico
 * @param {string} tabName - Nombre del tab a mostrar
 */
function showTab(tabName) {
    console.log(`🔍 Mostrando tab: ${tabName}`);
    
    // Ocultar todos los contenidos
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });
    
    // Remover clase active de todos los tabs
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Mostrar el contenido seleccionado
    const targetContent = document.getElementById(tabName);
    if (targetContent) {
        targetContent.classList.add('active');
        
        // Activar el tab correspondiente
        const activeTab = document.querySelector(`[onclick="showTab('${tabName}')"]`);
        if (activeTab) {
            activeTab.classList.add('active');
        }
        
        // Cargar contenido específico del tab si es necesario
        loadTabContent(tabName);
        
        console.log(`✅ Tab ${tabName} activado`);
    } else {
        console.error(`❌ No se encontró contenido para tab: ${tabName}`);
    }
}

/**
 * Cargar contenido específico para cada tab
 * @param {string} tabName - Nombre del tab
 */
function loadTabContent(tabName) {
    switch(tabName) {
        case 'general':
            loadGeneralContent();
            break;
        case 'skills':
            loadSkillsContent();
            break;
        case 'portfolio':
            loadPortfolioContent();
            break;
        case 'history':
            loadHistoryContent();
            break;
        default:
            console.log(`ℹ️ No hay carga específica para tab: ${tabName}`);
    }
}

/**
 * Cargar contenido de la pestaña General
 */
function loadGeneralContent() {
    console.log('📊 Cargando contenido general...');
    
    // Aquí puedes cargar datos dinámicos del usuario
    // Por ejemplo, actualizar estadísticas en tiempo real
    updateUserStats();
    updateRecentActivity();
}

/**
 * Cargar contenido de la pestaña Servicios
 */
function loadSkillsContent() {
    console.log('🛠️ Cargando contenido de servicios...');
    
    // Cargar servicios del usuario desde el backend
    loadUserServices();
}

/**
 * Cargar contenido de la pestaña Portfolio
 */
function loadPortfolioContent() {
    console.log('📸 Cargando contenido del portfolio...');
    
    // Cargar trabajos realizados
    loadUserPortfolio();
}

/**
 * Cargar contenido de la pestaña Historial
 */
function loadHistoryContent() {
    console.log('📋 Cargando historial...');
    
    // Cargar historial de trabajos
    loadWorkHistory();
}

/**
 * Actualizar estadísticas del usuario
 */
function updateUserStats() {
    // Esta función se conectará con el backend para obtener estadísticas reales
    console.log('📈 Actualizando estadísticas...');
    
    // Ejemplo de animación de números
    animateNumbers();
}

/**
 * Animar números en las estadísticas
 */
function animateNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const finalValue = stat.textContent;
        const numericValue = parseInt(finalValue.replace(/[^\d]/g, ''));
        
        if (!isNaN(numericValue)) {
            animateValue(stat, 0, numericValue, 1000, finalValue);
        }
    });
}

/**
 * Animar un valor numérico
 * @param {Element} element - Elemento a animar
 * @param {number} start - Valor inicial
 * @param {number} end - Valor final
 * @param {number} duration - Duración en ms
 * @param {string} originalText - Texto original con formato
 */
function animateValue(element, start, end, duration, originalText) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        
        // Mantener el formato original (ej: "S/ 3,200")
        if (originalText.includes('S/')) {
            element.textContent = `S/ ${current.toLocaleString()}`;
        } else if (originalText.includes('%')) {
            element.textContent = `${current}%`;
        } else {
            element.textContent = current;
        }
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

/**
 * Actualizar actividad reciente
 */
function updateRecentActivity() {
    console.log('⚡ Actualizando actividad reciente...');
    
    // Aquí cargarías la actividad reciente desde el backend
    // Por ahora, solo agregamos un efecto visual
    const activityItems = document.querySelectorAll('#general .info-item');
    activityItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '0.5';
            setTimeout(() => {
                item.style.opacity = '1';
            }, 200);
        }, index * 100);
    });
}

/**
 * Cargar servicios del usuario
 */
function loadUserServices() {
    console.log('🔧 Cargando servicios del usuario...');
    
    // Esta función se conectará con el backend
    // Por ahora, agregamos efectos visuales
    const skillTags = document.querySelectorAll('.skill-tag');
    skillTags.forEach((tag, index) => {
        setTimeout(() => {
            tag.style.transform = 'scale(1.05)';
            setTimeout(() => {
                tag.style.transform = 'scale(1)';
            }, 200);
        }, index * 50);
    });
}

/**
 * Cargar portfolio del usuario
 */
function loadUserPortfolio() {
    console.log('🎨 Cargando portfolio...');
    
    // Efectos visuales para portfolio
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    portfolioItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, 100);
        }, index * 150);
    });
}

/**
 * Cargar historial de trabajos
 */
function loadWorkHistory() {
    console.log('📜 Cargando historial de trabajos...');
    
    // Esta función cargará el historial real desde el backend
    // Por ahora, preparamos el contenedor
    const historyContainer = document.getElementById('history');
    if (historyContainer && !historyContainer.innerHTML.trim()) {
        // Si no hay contenido, mostrar mensaje de carga
        historyContainer.innerHTML = `
            <div class="loading-message">
                <div class="spinner"></div>
                <p>Cargando historial de trabajos...</p>
            </div>
        `;
        
        // Simular carga de datos
        setTimeout(() => {
            loadHistoryData();
        }, 1000);
    }
}

/**
 * Cargar datos del historial
 */
function loadHistoryData() {
    const historyContainer = document.getElementById('history');
    historyContainer.innerHTML = historyHTML;
    
    //Animar la aparición del contenido
    const workItems = historyContainer.querySelectorAll('.work-item');
    workItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-20px)';
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, index * 100);
    });
}

/**
 * Inicializar funcionalidades generales del perfil
 */
function initializeProfile() {
    console.log('👤 Inicializando perfil...');
    
    // Agregar event listeners para botones
    initializeButtons();
    
    // Agregar efectos de hover mejorados
    initializeHoverEffects();
    
    // Inicializar tooltips si es necesario
    initializeTooltips();
}

/**
 * Inicializar botones del perfil
 */
function initializeButtons() {
    console.log('🔘 Inicializando botones...');
    
    // Botón de editar perfil
    const editButton = document.querySelector('[onclick="editProfile()"]');
    if (editButton) {
        editButton.addEventListener('click', function(e) {
            e.preventDefault();
            editProfile();
        });
    }
    
    // Botones de acción en cards
    const cardActions = document.querySelectorAll('.card-action');
    cardActions.forEach(action => {
        action.addEventListener('click', function(e) {
            e.preventDefault();
            const cardTitle = this.closest('.card').querySelector('.card-title').textContent;
            console.log(`📝 Editando: ${cardTitle}`);
            // Aquí agregarías la lógica específica para cada tipo de edición
        });
    });
}

/**
 * Función para editar perfil
 */
function editProfile() {
    console.log('✏️ Editando perfil...');
    
    // Aquí implementarías la lógica para editar el perfil
    // Por ejemplo, abrir un modal o redirigir a una página de edición
    alert('Función de edición en desarrollo. Se abrirá un modal de edición.');
    
    // Ejemplo de lo que podrías hacer:
    // openEditModal();
    // o
    // window.location.href = '/usuarios/editar-perfil/';
}

/**
 * Inicializar efectos de hover mejorados
 */
function initializeHoverEffects() {
    console.log('✨ Inicializando efectos de hover...');
    
    // Efectos para cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 12px 40px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 8px 32px rgba(0,0,0,0.1)';
        });
    });
    
    // Efectos para stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(stat => {
        stat.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        stat.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

/**
 * Inicializar tooltips
 */
function initializeTooltips() {
    console.log('💬 Inicializando tooltips...');
    
    // Agregar tooltips a elementos con título
    const elementsWithTitle = document.querySelectorAll('[title]');
    elementsWithTitle.forEach(element => {
        element.addEventListener('mouseenter', function() {
            // Aquí podrías implementar tooltips personalizados
            console.log(`💡 Tooltip: ${this.getAttribute('title')}`);
        });
    });
}

// Funciones globales para mantener compatibilidad
window.showTab = showTab;
window.editProfile = editProfile;

// Agregar estilos CSS adicionales para las animaciones
const additionalStyles = `
    .tab-content {
        transition: opacity 0.3s ease;
    }
    
    .tab-content.active {
        opacity: 1;
    }
    
    .tab-content:not(.active) {
        opacity: 0;
    }
    
    .card {
        transition: all 0.3s ease;
    }
    
    .stat-card {
        transition: all 0.3s ease;
    }
    
    .work-item {
        transition: all 0.3s ease;
    }
    
    .loading-message {
        text-align: center;
        padding: 2rem;
        color: #666;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #07734B;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;

// Inyectar estilos adicionales
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

console.log('🎉 Perfil.js completamente inicializado');