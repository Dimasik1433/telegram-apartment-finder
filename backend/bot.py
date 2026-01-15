from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

BOT_TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ВАШ ВЕБ-САЙТ (замените на актуальный!)
WEB_URL = "https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev"

@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🏠 Найти квартиру",
                url=WEB_URL  # ЗДЕСЬ ПРАВИЛЬНЫЙ URL!
            )]
        ]
    )
    
    await message.answer(
        "🔍 <b>Поиск новостроек в Санкт-Петербурге</b>\n\n"
        "Нажмите кнопку ниже, чтобы открыть каталог квартир:",
        parse_mode='HTML',
        reply_markup=keyboard
    )

async def main():
    print("🤖 Бот запущен!")
    print(f"🌐 Веб-сайт: {WEB_URL}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())