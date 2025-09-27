// ----- SISTEMA DE AJUSTES DEL CHAT ESTILO MESSENGER -----

class ChatSettings {
    constructor() {
        this.settings = {
            background: 'gradient-1',
            font: 'roboto',
            fontSize: 16
        };
        
        this.loadSettings();
        this.initializeSettings();
    }

    // Cargar configuraciones guardadas
    loadSettings() {
        const saved = localStorage.getItem('chatSettings');
        if (saved) {
            this.settings = { ...this.settings, ...JSON.parse(saved) };
        }
    }

    // Guardar configuraciones
    saveSettings() {
        localStorage.setItem('chatSettings', JSON.stringify(this.settings));
    }

    // Inicializar el sistema de ajustes
    initializeSettings() {
        this.applySettings();
        this.setupEventListeners();
    }

    // Aplicar ajustes al chat
    applySettings() {
        const body = document.body;
        
        // Aplicar fondo
        body.className = body.className.replace(/bg-gradient-\d+/g, '');
        body.classList.add(`bg-${this.settings.background}`);
        
        // Aplicar fuente
        body.className = body.className.replace(/font-\w+/g, '');
        body.classList.add(`font-${this.settings.font}`);
        
        // Aplicar tamaño de fuente
        const messages = document.querySelector('.messages');
        if (messages) {
            messages.style.fontSize = `${this.settings.fontSize}px`;
        }
        
        // Actualizar UI de ajustes
        this.updateSettingsUI();
    }

    // Configurar event listeners
    setupEventListeners() {
        // Botón de ajustes
        const settingsBtn = document.querySelector('.chat-settings-btn');
        if (settingsBtn) {
            settingsBtn.addEventListener('click', () => this.toggleSettings());
        }

        // Cerrar ajustes
        const closeBtn = document.querySelector('.close-settings');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeSettings());
        }

        // Overlay
        const overlay = document.querySelector('.settings-overlay');
        if (overlay) {
            overlay.addEventListener('click', () => this.closeSettings());
        }

        // Selectores de color
        document.querySelectorAll('.color-option').forEach(option => {
            option.addEventListener('click', (e) => {
                const gradient = e.target.dataset.gradient;
                this.changeBackground(gradient);
            });
        });

        // Selectores de fuente
        document.querySelectorAll('.font-option').forEach(option => {
            option.addEventListener('click', (e) => {
                const font = e.target.dataset.font;
                this.changeFont(font);
            });
        });

        // Botones de tamaño
        document.querySelector('.size-increase')?.addEventListener('click', () => {
            this.changeFontSize(this.settings.fontSize + 2);
        });

        document.querySelector('.size-decrease')?.addEventListener('click', () => {
            this.changeFontSize(this.settings.fontSize - 2);
        });

        // Botón reset
        document.querySelector('.reset-btn')?.addEventListener('click', () => {
            this.resetSettings();
        });
    }

    // Abrir/cerrar panel de ajustes
    toggleSettings() {
        const panel = document.querySelector('.settings-panel');
        const overlay = document.querySelector('.settings-overlay');
        
        panel.classList.toggle('open');
        overlay.classList.toggle('active');
    }

    closeSettings() {
        const panel = document.querySelector('.settings-panel');
        const overlay = document.querySelector('.settings-overlay');
        
        panel.classList.remove('open');
        overlay.classList.remove('active');
    }

    // Cambiar fondo
    changeBackground(gradient) {
        this.settings.background = gradient;
        this.saveSettings();
        this.applySettings();
    }

    // Cambiar fuente
    changeFont(font) {
        this.settings.font = font;
        this.saveSettings();
        this.applySettings();
    }

    // Cambiar tamaño de fuente
    changeFontSize(size) {
        if (size >= 12 && size <= 24) {
            this.settings.fontSize = size;
            this.saveSettings();
            this.applySettings();
        }
    }

    // Resetear ajustes
    resetSettings() {
        this.settings = {
            background: 'gradient-1',
            font: 'roboto',
            fontSize: 16
        };
        this.saveSettings();
        this.applySettings();
    }

    // Actualizar UI de ajustes
    updateSettingsUI() {
        // Actualizar colores activos
        document.querySelectorAll('.color-option').forEach(option => {
            option.classList.remove('active');
            if (option.dataset.gradient === this.settings.background) {
                option.classList.add('active');
            }
        });

        // Actualizar fuentes activas
        document.querySelectorAll('.font-option').forEach(option => {
            option.classList.remove('active');
            if (option.dataset.font === this.settings.font) {
                option.classList.add('active');
            }
        });

        // Actualizar display de tamaño
        const sizeDisplay = document.querySelector('.size-display');
        if (sizeDisplay) {
            sizeDisplay.textContent = `${this.settings.fontSize}px`;
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    new ChatSettings();
});

// Clases CSS para fondos dinámicos
const backgroundClasses = {
    'gradient-1': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'gradient-2': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'gradient-3': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'gradient-4': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'gradient-5': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'gradient-6': 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    'gradient-7': 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
    'gradient-8': 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
};

// Aplicar fondos dinámicamente
function applyDynamicBackground(gradientKey) {
    const gradient = backgroundClasses[gradientKey];
    if (gradient) {
        document.body.style.background = gradient;
    }
}
