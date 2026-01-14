// config.js - Конфигурация приложения
const CONFIG = {
    // API endpoints
    API_BASE_URL: 'https://ваш-домен.ru/api',
    
    // Настройки приложения
    APP_NAME: 'Группа Аквилон',
    APP_VERSION: '1.0.0',
    
    // Настройки поиска
    DEFAULT_LIMIT: 50,
    DEFAULT_SORT: 'price_asc',
    
    // Кэширование
    CACHE_DURATION: 300000, // 5 минут в миллисекундах
    
    // Цвета темы
    THEME_COLORS: {
        primary: '#2c3e50',
        secondary: '#3498db',
        accent: '#e74c3c'
    }
};

// Экспорт для использования в других файлах
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
