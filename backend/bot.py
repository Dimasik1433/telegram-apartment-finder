from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

# ВАШИ ДАННЫЕ
BOT_TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"
WEB_APP_URL = "https://dimasik1433.github.io/telegram-apartment-finder/"

# Создаем бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    # Кнопка для открытия Mini App
    button = types.KeyboardButton(
        text="🔍 Найти квартиру",
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    
    await message.answer(
        "🏠 *Привет! Я тестовый бот для поиска квартир.*\n\n"
        "Нажмите кнопку ниже, чтобы открыть каталог:\n\n"
        "Бот: @probniy_one_bot\n"
        "GitHub: Dimasik1433/telegram-apartment-finder",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Главная функция
async def main():
    print("=" * 60)
    print("🤖 TELEGRAM BOT LAUNCHED")
    print("=" * 60)
    print(f"Bot: @probniy_one_bot")
    print(f"Web App: {WEB_APP_URL}")
    print("=" * 60)
    print("📱 Open Telegram -> @probniy_one_bot -> /start")
    print("=" * 60)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
