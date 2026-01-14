// Инициализация Telegram Web App
document.addEventListener('DOMContentLoaded', function() {
    console.log("Telegram Mini App загружен");
    
    if (window.Telegram && Telegram.WebApp) {
        const tg = Telegram.WebApp;
        
        // Настройки Telegram
        tg.expand(); // На весь экран
        tg.ready(); // Готово к показу
        
        console.log("Пользователь Telegram:", tg.initDataUnsafe.user);
    } else {
        console.log("Запущено в браузере (не в Telegram)");
    }
    
    console.log("Бот: @probniy_one_bot");
    console.log("GitHub: Dimasik1433/telegram-apartment-finder");
});
