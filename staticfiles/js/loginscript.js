// Soft Minimalism Login Form JavaScript
class SoftMinimalismLoginForm {
    constructor() {
        this.form = document.getElementById('loginForm');
        this.emailInput = document.getElementById('email');
        this.passwordInput = document.getElementById('password');
        this.passwordToggle = document.getElementById('passwordToggle');

        this.init();
    }

    init() {
        this.setupPasswordToggle();
        this.setupGentleEffects();
        
        // Adiciona placeholders para as animações dos labels
        this.emailInput.setAttribute('placeholder', ' ');
        this.passwordInput.setAttribute('placeholder', ' ');
    }

    setupPasswordToggle() {
        if (!this.passwordToggle) return;
        
        this.passwordToggle.addEventListener('click', () => {
            const type = this.passwordInput.type === 'password' ? 'text' : 'password';
            this.passwordInput.type = type;
            this.passwordToggle.classList.toggle('toggle-active', type === 'text');
        });
    }

    setupGentleEffects() {
        // Efeitos visuais nos inputs
        [this.emailInput, this.passwordInput].forEach(input => {
            input.addEventListener('focus', (e) => {
                const container = e.target.closest('.field-container');
                if (container) {
                    container.style.transition = 'all 0.3s ease';
                    container.style.transform = 'translateY(-1px)';
                }
            });

            input.addEventListener('blur', (e) => {
                const container = e.target.closest('.field-container');
                if (container) {
                    container.style.transform = 'translateY(0)';
                }
            });
        });

        // Efeito de clique no botão
        const button = document.querySelector('.comfort-button');
        if (button) {
            button.addEventListener('mousedown', () => {
                button.style.transform = 'scale(0.98)';
            });
            button.addEventListener('mouseup', () => {
                button.style.transform = 'scale(1)';
            });
            button.addEventListener('mouseleave', () => {
                button.style.transform = 'scale(1)';
            });
        }
    }
}

// Inicializa quando o DOM carregar
document.addEventListener('DOMContentLoaded', () => {
    new SoftMinimalismLoginForm();
});