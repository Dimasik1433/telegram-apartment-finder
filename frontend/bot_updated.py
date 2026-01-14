import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"

# URL вашей веб-страницы с квартирами
# Если веб-сервер запущен на localhost:5000
WEB_PAGE_URL = "http://172.31.94.98:5000/apartments.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    welcome_text = f"""
Привет, {user.first_name}! 😊

Я бот для поиска квартир @probniy_one_bot

🏠 **Поиск квартир:**
• Аренда и продажа
• Фильтры по цене и району
• Фото и контакты

Нажмите кнопку ниже, чтобы открыть поиск:
"""
    
    keyboard = [[
        InlineKeyboardButton(
            "🔍 Открыть поиск квартир", 
            web_app={"url": WEB_PAGE_URL}
        )
    ]]
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Бот для поиска квартир*\n\n"
        "🔍 *Как использовать:*\n"
        "1. Нажмите кнопку 'Открыть поиск квартир'\n"
        "2. В открывшемся окне просмотрите список квартир\n"
        "3. Используйте фильтры для поиска по типу\n"
        "4. Нажмите 'Подробнее' для деталей\n\n"
        "📱 *Для связи:* @probniy_one_bot",
        parse_mode='Markdown'
    )

def main():
    print("=" * 60)
    print("🤖 БОТ ДЛЯ ПОИСКА КВАРТИР С ВЕБ-ИНТЕРФЕЙСОМ")
    print("=" * 60)
    print(f"🌐 Веб-страница: {WEB_PAGE_URL}")
    print("=" * 60)
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    print("✅ Бот запущен!")
    print("📱 Отправьте /start в Telegram @probniy_one_bot")
    print("=" * 60)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
