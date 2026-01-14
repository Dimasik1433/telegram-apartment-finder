import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp

# Настройки
BOT_TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"
FEED_URL = "https://raw.githubusercontent.com/dsmaznova-source/my-telegram-app2/refs/heads/main/complexes.json"

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "🏠 Привет! Я бот для отслеживания квартир.\n\n"
        "Команды:\n"
        "/start - это сообщение\n"
        "/apartments - показать квартиры\n"
        "/help - помощь"
    )

@dp.message(Command("apartments"))
async def apartments_command(message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FEED_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data and len(data) > 0:
                        for apartment in data[:3]:  # Первые 3 квартиры
                            text = (
                                f"🏢 {apartment.get('title', 'Без названия')}\n"
                                f"💰 Цена: {apartment.get('price', 'Не указана')}\n"
                                f"📍 {apartment.get('location', 'Не указано')}\n"
                                f"🔗 {apartment.get('url', 'Нет ссылки')}"
                            )
                            await message.answer(text)
                            
                            if apartment.get('image_url'):
                                try:
                                    await message.answer_photo(apartment['image_url'])
                                except:
                                    pass
                    else:
                        await message.answer("😔 Пока нет доступных квартир")
                else:
                    await message.answer("❌ Не удалось загрузить данные")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "🤖 Помощь по боту:\n\n"
        "Я показываю квартиры из фида GitHub.\n"
        "Команды:\n"
        "/start - начать\n"
        "/apartments - показать квартиры\n"
        "/help - это сообщение"
    )

@dp.message()
async def echo_message(message: Message):
    await message.answer("Используйте команды: /start, /apartments, /help")

# Главная функция
async def main():
    logging.info("🤖 Запускаю бота...")
    await dp.start_polling(bot)

# Для запуска отдельно
if __name__ == "__main__":
    asyncio.run(main())
