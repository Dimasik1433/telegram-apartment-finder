from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import aiohttp
import json

bot = Bot(token="8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🌐 Открыть в браузере",
                url="https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev"
            )],
            [
                InlineKeyboardButton(text="🏢 Комплексы", callback_data="complexes"),
                InlineKeyboardButton(text="❓ Помощь", callback_data="help")
            ]
        ]
    )
    
    await message.answer(
        "🏠 <b>Привет! Я бот для поиска новостроек.</b>\n\n"
        "<b>Доступные команды:</b>\n"
        "/start - это сообщение\n"
        "/complexes - список жилых комплексов\n"
        "/web - ссылка на веб-приложение\n"
        "/help - помощь\n\n"
        "<b>Веб-приложение:</b>\n"
        "https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev",
        parse_mode='HTML',
        reply_markup=keyboard
    )

@dp.message(Command("complexes"))
async def complexes(message: types.Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://raw.githubusercontent.com/dsmaznova-source/my-telegram-app2/main/complexes.json') as response:
                data = await response.json()
                
                text = "<b>🏢 Доступные жилые комплексы:</b>\n\n"
                
                if isinstance(data, list):
                    for item in data:
                        text += f"<b>{item.get('title', 'Без названия')}</b>\n"
                        text += f"📍 {item.get('district', 'Не указан')}\n"
                        text += f"📊 {item.get('status', 'Не указан')}\n\n"
                else:
                    text += f"<b>{data.get('title', 'Без названия')}</b>\n"
                    text += f"📍 {data.get('district', 'Не указан')}\n"
                    text += f"📊 {data.get('status', 'Не указан')}\n\n"
                
                text += "\n🌐 <i>Для выбора квартир откройте веб-приложение</i>"
                
                await message.answer(text, parse_mode='HTML')
    except Exception as e:
        await message.answer(f"⚠️ Ошибка загрузки данных: {str(e)}")

@dp.message(Command("web"))
async def web_app(message: types.Message):
    await message.answer(
        "🌐 <b>Веб-приложение новостроек</b>\n\n"
        "Откройте в браузере:\n"
        "<code>https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev</code>\n\n"
        "В веб-приложении вы можете:\n"
        "• Выбрать застройщика\n"
        "• Посмотреть жилые комплексы\n"
        "• Подобрать квартиру\n"
        "• Увидеть расположение на карте",
        parse_mode='HTML'
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "🤖 <b>Помощь по боту</b>\n\n"
        "<b>Команды:</b>\n"
        "/start - начало работы\n"
        "/complexes - список комплексов\n"
        "/web - веб-приложение\n"
        "/help - помощь\n\n"
        "<b>Ссылки:</b>\n"
        "• Веб-приложение: https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev\n"
        "• Фид данных: https://github.com/dsmaznova-source/my-telegram-app2",
        parse_mode='HTML'
    )

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "complexes":
        await complexes(callback.message)
    elif callback.data == "help":
        await help_command(callback.message)
    await callback.answer()

async def main():
    print("🤖 Запускаю Telegram бота...")
    print("📱 Бот: @probniy_one_bot")
    print("🌐 Веб-сайт: https://super-space-waddle-97v9x67jjqx9cpwg6-8080.app.github.dev")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())