import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"
# Используем порт 8080 вместо 5000
WEB_PAGE_URL = "http://172.31.94.98:8080/apartments.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    text = f"""
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
        InlineKeyboardButton("🔍 Открыть поиск квартир", web_app={"url": WEB_PAGE_URL})
    ]]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Бот @probniy_one_bot*\n\n"
        "🔍 Нажмите кнопку 'Открыть поиск квартир' для просмотра всех доступных вариантов.\n\n"
        "📞 Для связи: @dmitsmaznov",
        parse_mode='Markdown'
    )

def main():
    print("=" * 60)
    print("🤖 БОТ С ВЕБ-ИНТЕРФЕЙСОМ ДЛЯ КВАРТИР")
    print("=" * 60)
    print(f"🌐 Веб-страница: {WEB_PAGE_URL}")
    print("=" * 60)
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    print("✅ Бот запущен!")
    print("📱 Перейдите в Telegram: @probniy_one_bot")
    print("📱 Отправьте: /start")
    print("=" * 60)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
