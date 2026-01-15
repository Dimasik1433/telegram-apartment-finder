from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Токен вашего бота
BOT_TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    # Создаем простую клавиатуру с одной кнопкой
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🏠 Подробнее о новостройках",
                url="https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev"
            )]
        ]
    )
    
    await message.answer(
        "🏠 <b>Привет! Я бот по новостройкам Санкт-Петербурга.</b>\n\n"
        "Здесь вы можете посмотреть:\n"
        "• Жилые комплексы от застройщиков\n"
        "• Выбрать квартиру\n"
        "• Узнать расположение на карте\n\n"
        "Нажмите кнопку ниже, чтобы открыть подробную информацию:",
        parse_mode='HTML',
        reply_markup=keyboard
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "🤖 <b>Помощь</b>\n\n"
        "Просто нажмите кнопку «Подробнее» в команде /start\n"
        "Или откройте сайт напрямую:\n"
        "https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev",
        parse_mode='HTML'
    )

@dp.message()
async def echo_message(message: types.Message):
    # На любое сообщение отвечаем про кнопку
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🏠 Открыть подробности",
                url="https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev"
            )]
        ]
    )
    
    await message.answer(
        "Нажмите кнопку ниже, чтобы открыть сайт с новостройками:",
        reply_markup=keyboard
    )

async def main():
    print("🤖 Бот запущен!")
    print("📱 Откройте Telegram: @probniy_one_bot")
    print("🌐 Сайт: https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())