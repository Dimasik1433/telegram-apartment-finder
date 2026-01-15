from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

BOT_TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ВАШ НОВЫЙ URL (получите актуальный!)
WEB_URL = "https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev"

@dp.message(Command("start"))
async def start_command(message: types.Message):
    # Простая кнопка с URL (не Web App!)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠 Открыть сайт с квартирами",
                    url=WEB_URL  # Обычная ссылка, а не Web App
                )
            ]
        ]
    )
    
    await message.answer(
        "🔍 <b>Поиск новостроек Санкт-Петербурга</b>\n\n"
        "Нажмите кнопку ниже, чтобы открыть сайт с каталогом квартир.\n"
        "Сайт откроется в вашем браузере.",
        parse_mode='HTML',
        reply_markup=keyboard
    )

@dp.message(Command("site"))
async def site_command(message: types.Message):
    await message.answer(
        f"🌐 <b>Сайт с каталогом квартир:</b>\n\n"
        f"{WEB_URL}\n\n"
        f"Скопируйте ссылку и откройте в браузере.",
        parse_mode='HTML'
    )

async def main():
    print("="*50)
    print("🤖 Telegram бот запущен!")
    print(f"🌐 Ваш сайт: {WEB_URL}")
    print("📱 Откройте: @probniy_one_bot")
    print("="*50)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())