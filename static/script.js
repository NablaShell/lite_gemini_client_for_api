const API_URL = 'http://127.0.0.1:8000/api';

class GeminiClient {
    constructor() {
        this.messageContainer = document.getElementById('messages');
        this.userInput = document.getElementById('userInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.statusSpan = document.querySelector('#status span:last-child');
        
        this.init();
    }
    
    async init() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        await this.checkHealth();
    }
    
    async checkHealth() {
        try {
            const response = await fetch(`${API_URL}/health`);
            if (response.ok) {
                this.updateStatus('✅ API готов', '#4ade80');
            } else {
                this.updateStatus('❌ API недоступен', '#ef4444');
            }
        } catch (error) {
            this.updateStatus('❌ Нет подключения к бэкенду', '#ef4444');
            console.error('Health check failed:', error);
        }
    }
    
    updateStatus(text, color) {
        this.statusSpan.textContent = text;
        const dot = document.querySelector('.status-dot');
        if (dot) dot.style.background = color;
    }
    
    addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        if (type === 'bot') {
            messageDiv.innerHTML = this.formatMarkdown(text);
        } else {
            messageDiv.textContent = text;
        }
        
        this.messageContainer.appendChild(messageDiv);
        this.scrollToBottom();
        return messageDiv;
    }
    
    formatMarkdown(text) {
        // Простое форматирование
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>')
            .replace(/\n/g, '<br>');
    }
    
    addLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot';
        loadingDiv.innerHTML = '<div class="loading"></div> Думаю...';
        loadingDiv.id = 'loading-message';
        this.messageContainer.appendChild(loadingDiv);
        this.scrollToBottom();
        return loadingDiv;
    }
    
    removeLoadingMessage() {
        const loadingMsg = document.getElementById('loading-message');
        if (loadingMsg) loadingMsg.remove();
    }
    
    scrollToBottom() {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
    
    async sendMessage() {
        const text = this.userInput.value.trim();
        if (!text) return;
        
        // Добавляем сообщение пользователя
        this.addMessage(text, 'user');
        this.userInput.value = '';
        this.sendBtn.disabled = true;
        
        // Показываем индикатор загрузки
        this.addLoadingMessage();
        
        try {
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            this.removeLoadingMessage();
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.error) {
                this.addMessage(`❌ Ошибка: ${data.error}`, 'error');
            } else {
                this.addMessage(data.response, 'bot');
            }
            
        } catch (error) {
            this.removeLoadingMessage();
            this.addMessage(`❌ Ошибка подключения: ${error.message}`, 'error');
            console.error('Send error:', error);
        } finally {
            this.sendBtn.disabled = false;
            this.userInput.focus();
        }
    }
}

// Запуск приложения
document.addEventListener('DOMContentLoaded', () => {
    new GeminiClient();
});
