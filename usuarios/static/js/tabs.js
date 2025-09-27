// static/js/tabs.js - Versión corregida y unificada
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Sistema de tabs iniciado');
    
    // Inicializar tabs
    initializeTabs();
});

/**
 * Inicializar sistema de tabs
 */
function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    if (tabs.length === 0 || tabContents.length === 0) {
        console.warn('⚠️ No se encontraron tabs o contenido de tabs');
        return;
    }
    
    console.log(`✅ Encontrados ${tabs.length} tabs y ${tabContents.length} contenidos`);
    
    // Agregar event listeners a cada tab
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const targetTab = this.getAttribute('data-tab');
            
            if (targetTab) {
                showTab(targetTab);
            } else {
                console.error('❌ Tab sin atributo data-tab:', this);
            }
        });
    });
    
    // Activar el primer tab por defecto si ninguno está activo
    const activeTab = document.querySelector('.tab.active');
    if (!activeTab && tabs.length > 0) {
        const firstTab = tabs[0];
        const firstTabTarget = firstTab.getAttribute('data-tab');
        if (firstTabTarget) {
            showTab(firstTabTarget);
        }
    }
}

/**
 * Mostrar tab específico
 * @param {string} tabName - Nombre del tab a mostrar
 */
function showTab(tabName) {
    console.log(`🔍 Cambiando a tab: ${tabName}`);
    
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Remover clase active de todos los tabs
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Ocultar todos los contenidos
    tabContents.forEach(content => {
        content.classList.remove('active');
        content.style.display = 'none'; // Asegurar que esté oculto
    });
    
    // Activar el tab correspondiente
    const activeTab = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeTab) {
        activeTab.classList.add('active');
        console.log(`✅ Tab activado: ${tabName}`);
    } else {
        console.error(`❌ No se encontró tab con data-tab="${tabName}"`);
    }
    
    // Mostrar el contenido seleccionado
    const targetContent = document.getElementById(tabName);
    if (targetContent) {
        targetContent.classList.add('active');
        targetContent.style.display = 'block'; // Asegurar que esté visible
        
        // Cargar contenido específico del tab si es necesario
        loadTabContent(tabName);
        
        console.log(`✅ Contenido mostrado: ${tabName}`);
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
        case 'experience':
            loadExperienceContent();
            break;
        case 'certifications':
            loadCertificationsContent();
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
    animateNumbers();
}

/**
 * Cargar contenido de la pestaña Servicios
 */
function loadSkillsContent() {
    console.log('🛠️ Cargando contenido de servicios...');
    
    const skillsContainer = document.getElementById('skills');
    if (skillsContainer) {
        // Animar la aparición del contenido
        const skillItems = skillsContainer.querySelectorAll('p');
        skillItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-20px)';
            setTimeout(() => {
                item.style.transition = 'all 0.3s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, index * 100);
        });
    }
}

/**
 * Cargar contenido de la pestaña Portfolio
 */
function loadPortfolioContent() {
    console.log('📸 Cargando contenido del portfolio...');
    
    const portfolioContainer = document.getElementById('portfolio');
    if (portfolioContainer) {
        // Animar elementos del portfolio
        const portfolioItems = portfolioContainer.querySelectorAll('li, img');
        portfolioItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            setTimeout(() => {
                item.style.transition = 'all 0.4s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 150);
        });
    }
}

/**
 * Cargar contenido de la pestaña Experiencia
 */
function loadExperienceContent() {
    console.log('💼 Cargando contenido de experiencia...');
    
    const experienceContainer = document.getElementById('experience');
    if (experienceContainer) {
        console.log('✅ Contenido de experiencia cargado');
    }
}

/**
 * Cargar contenido de la pestaña Certificaciones
 */
function loadCertificationsContent() {
    console.log('🎓 Cargando certificaciones...');
    
    const certContainer = document.getElementById('certifications');
    if (certContainer) {
        const certItems = certContainer.querySelectorAll('p, a');
        certItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'scale(0.9)';
            setTimeout(() => {
                item.style.transition = 'all 0.3s ease';
                item.style.opacity = '1';
                item.style.transform = 'scale(1)';
            }, index * 100);
        });
    }
}

/**
 * Cargar contenido de la pestaña Historial
 */
function loadHistoryContent() {
    console.log('📋 Cargando historial...');
    
    const historyContainer = document.getElementById('history');
    if (historyContainer) {
        const historyItems = historyContainer.querySelectorAll('p');
        historyItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-15px)';
            setTimeout(() => {
                item.style.transition = 'all 0.3s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, index * 80);
        });
    }
}

/**
 * Animar números en las estadísticas
 */
function animateNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const finalValue = stat.textContent;
        const numericValue = parseInt(finalValue.replace(/[^\d]/g, ''));
        
        if (!isNaN(numericValue) && numericValue > 0) {
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
        
        // Mantener el formato original
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

// Hacer funciones disponibles globalmente para compatibilidad
window.showTab = showTab;

// Agregar estilos CSS para mejorar las transiciones
const tabStyles = `
    .tab-content {
        display: none;
        opacity: 0;
        transition: opacity 0.3s ease, transform 0.3s ease;
        transform: translateY(10px);
    }
    
    .tab-content.active {
        display: block;
        opacity: 1;
        transform: translateY(0);
    }
    
    .tab {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .tab:hover {
        background-color: rgba(7, 115, 75, 0.1);
        transform: translateY(-2px);
    }
    
    .tab.active {
        background-color: #07734B;
        color: white;
        box-shadow: 0 4px 12px rgba(7, 115, 75, 0.3);
    }
    
    /* Animaciones para elementos internos */
    #skills p, #portfolio li, #certifications p, #history p {
        transition: all 0.3s ease;
    }
    
    /* Loading state para tabs */
    .tab-loading {
        position: relative;
        pointer-events: none;
    }
    
    .tab-loading::after {
        content: '';
        position: absolute;
        top: 50%;
        right: 10px;
        width: 12px;
        height: 12px;
        border: 2px solid transparent;
        border-top: 2px solid currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        transform: translateY(-50%);
    }
    
    @keyframes spin {
        0% { transform: translateY(-50%) rotate(0deg); }
        100% { transform: translateY(-50%) rotate(360deg); }
    }
`;

// Inyectar estilos
const styleSheet = document.createElement('style');
styleSheet.textContent = tabStyles;
document.head.appendChild(styleSheet);

console.log('🎉 Sistema de tabs completamente inicializado');

document.addEventListener('DOMContentLoaded', function() {
    // Si ya hay un tab activo en el HTML, asegúrate de que se vea
    const activeTab = document.querySelector('.tab.active');
    if (activeTab) {
        const tabName = activeTab.getAttribute('data-tab');
        if (tabName) {
            showTab(tabName); // fuerza la activación visual
        }
    }
});
