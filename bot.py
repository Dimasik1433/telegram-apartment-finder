import os
import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"

# URL веб-страницы (будем использовать порт 8080)
WEB_URL = "http://172.31.94.98:8080/apartments.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    welcome_text = f"""
Привет, {user.first_name}! 😊

Я бот для поиска квартир @probniy_one_bot

🏠 **Поиск квартир:**
• Список всех доступных квартир
• Фотографии и детали
• Цены и площадь
• Фильтры по типу

Нажмите кнопку ниже, чтобы открыть поиск:
"""
    
    keyboard = [[
        InlineKeyboardButton("🔍 Открыть поиск квартир", web_app={"url": WEB_URL})
    ]]
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logging.info(f"Пользователь {user.id} запустил бота")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "🤖 *Бот @probniy_one_bot*\n\n"
        "🔍 Нажмите кнопку 'Открыть поиск квартир' для просмотра всех доступных вариантов.\n\n"
        "📞 Для связи: @dmitsmaznov",
        parse_mode='Markdown'
    )

def main():
    """Запуск бота"""
    print("=" * 60)
    print("🤖 TELEGRAM БОТ ДЛЯ ПОИСКА КВАРТИР")
    print("=" * 60)
    print(f"Токен: {TOKEN[:15]}...")
    print(f"Веб-страница: {WEB_URL}")
    print("=" * 60)
    
    # Ждем 5 секунд перед запуском
    print("⏳ Ожидание 5 секунд перед запуском...")
    time.sleep(5)
    
    try:
        # Создаем приложение
        application = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("search", start))
        
        print("✅ Бот успешно инициализирован!")
        print("📱 Перейдите в Telegram: @probniy_one_bot")
        print("📱 Отправьте команду: /start")
        print("=" * 60)
        
        # Запускаем бота с очисткой очереди
        application.run_polling(
            drop_pending_updates=True,  # Очищаем все ожидающие обновления
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        print(f"❌ ОШИБКА ПРИ ЗАПУСКЕ БОТА: {type(e).__name__}")
        print(f"Детали: {e}")
        print("\nПопробуйте:")
        print("1. Подождать 30 секунд")
        print("2. Перезапустить Replit (Tools → Restart Workspace)")
        print("3. Запустить снова")

if __name__ == "__main__":
    main()
