# bot.py - Telegram бот для поиска квартир
import os
from telegram import Update, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Получаем токен из переменных окружения или указываем прямо здесь
BOT_TOKEN = 8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w  # Замените на ваш токен!
WEB_APP_URL = "https://github.com/Dimasik1433/telegram-apartment-finder.git"  # Ваш URL

# Команда /start
async def start(update: Update, context: CallbackContext):
    # Кнопка для открытия Mini App
    keyboard = [[
        {
            "text": "🏠 Открыть поиск квартир",
            "web_app": {"url": WEB_APP_URL}
        }
    ]]
    
    await update.message.reply_text(
        "Привет! Я бот для поиска квартир.\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение:",
        reply_markup={
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
    )

# Основная функция
def main():
    # Создаем приложение
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    
    # Запускаем бота
    print("🤖 Бот запускается...")
    print(f"🌐 Mini App URL: {WEB_APP_URL}")
    app.run_polling()

if __name__ == "__main__":
    main()
