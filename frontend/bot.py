import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ваш токен бота
TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"

# URL вашего Replit проекта (замените на реальный из Webview)
WEB_APP_URL = "https://organic-space-invention.dmitsmaznov.repl.co"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    welcome_text = f"""
Привет, {user.first_name}! 👋

Я бот для поиска квартир @probniy_one_bot

🏠 **Поиск квартир:**
• Аренда и продажа
• Фильтры по цене и району
• Фото и контакты

Нажмите кнопку ниже, чтобы открыть поиск:
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup={
            "inline_keyboard": [[
                {
                    "text": "🔍 Открыть поиск квартир",
                    "web_app": {"url": WEB_APP_URL}
                }
            ]]
        }
    )
    logger.info(f"Пользователь {user.id} (@{user.username}) запустил бота")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
📱 **@probniy_one_bot - Бот для поиска квартир**

🔧 **Доступные команды:**
/start - Начать работу
/help - Эта справка
/info - Информация о боте

🚀 **Как использовать:**
1. Нажмите кнопку "Открыть поиск квартир"
2. В открывшемся окне задайте параметры
3. Смотрите результаты в реальном времени

📞 **Поддержка:**
По вопросам: @dmitsmaznov
"""
    await update.message.reply_text(help_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /info"""
    info_text = """
🤖 **Информация о боте:**

• Имя: @probniy_one_bot
• ID: 8501696238
• Создатель: @dmitsmaznov
• Версия: 1.0

📍 **Функции:**
- Поиск квартир в Telegram Mini App
- Удобные фильтры
- Быстрый просмотр

🌐 **Ссылка на бота:**
https://t.me/probniy_one_bot
"""
    await update.message.reply_text(info_text)

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка данных из Mini App"""
    data = update.message.web_app_data.data
    logger.info(f"Получены данные из Mini App: {data[:50]}...")
    await update.message.reply_text(
        f"✅ Данные получены!\n\n"
        f"Мы обработали ваш запрос из Mini App.\n"
        f"Результаты поиска показаны в веб-приложении."
    )

def main():
    """Запуск бота"""
    print("=" * 50)
    print("🤖 ЗАПУСК БОТА @probniy_one_bot")
    print("=" * 50)
    print(f"Токен: {TOKEN[:15]}...")
    print(f"URL Mini App: {WEB_APP_URL}")
    print("=" * 50)
    
    try:
        # Создаём приложение
        app = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики команд
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("info", info_command))
        
        print("✅ Обработчики команд добавлены")
        print("⏳ Запускаю polling...")
        print("\n📱 Отправьте /start в Telegram боту @probniy_one_bot")
        print("⏹️  Для остановки: Ctrl+C")
        print("=" * 50)
        
        # Запускаем бота
        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        print("Проверьте токен и интернет соединение")

if __name__ == "__main__":
    main()
