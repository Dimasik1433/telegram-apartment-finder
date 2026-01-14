import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
import aiohttp
import json

# Настройки
BOT_TOKEN = "8501696238:AAFgt9SjdWYNssUhA1VkX2vFMPZ_3Y45l7w"
FEED_URL = "https://raw.githubusercontent.com/dsmaznova-source/my-telegram-app2/refs/heads/main/complexes.json"
WEB_APP_URL = "https://super-space-waddle-97v9x67jjqx9cpwg6.github.dev"  # URL веб-приложения

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_command(message: Message):
    # Создаем кнопку для открытия веб-приложения
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🏠 Открыть веб-приложение",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )],
            [
                InlineKeyboardButton(text="📋 Комплексы", callback_data="complexes"),
                InlineKeyboardButton(text="❓ Помощь", callback_data="help")
            ]
        ]
    )
    
    await message.answer(
        "🏠 <b>Привет! Я бот для поиска новостроек.</b>\n\n"
        "Я могу показать:\n"
        "• Жилые комплексы от застройщиков\n"
        "• Доступные квартиры\n"
        "• Расположение на карте\n\n"
        "Нажмите кнопку ниже, чтобы открыть полный веб-интерфейс:",
        parse_mode='HTML',
        reply_markup=keyboard
    )

@dp.message(Command("complexes"))
async def complexes_command(message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FEED_URL) as response:
                if response.status == 200:
                    text = await response.text()
                    
                    try:
                        data = json.loads(text)
                        complexes = data if isinstance(data, list) else [data]
                        
                        if complexes:
                            # Отправляем первые 2 комплекса с кнопками
                            for complex_data in complexes[:2]:
                                text_message = (
                                    f"🏢 <b>{complex_data.get('title', 'Без названия')}</b>\n"
                                    f"📍 Район: {complex_data.get('district', 'Не указан')}\n"
                                    f"📊 Статус: {complex_data.get('status', 'Не указан')}\n\n"
                                    f"<i>Откройте веб-приложение для выбора квартир</i>"
                                )
                                
                                keyboard = InlineKeyboardMarkup(
                                    inline_keyboard=[[
                                        InlineKeyboardButton(
                                            text="📱 Открыть в веб-приложении",
                                            web_app=WebAppInfo(url=f"{WEB_APP_URL}#complex={complex_data.get('title', '')}")
                                        )
                                    ]]
                                )
                                
                                await message.answer(text_message, parse_mode='HTML', reply_markup=keyboard)
                                
                                # Если есть картинка
                                if complex_data.get('image'):
                                    try:
                                        await message.answer_photo(complex_data['image'])
                                    except:
                                        pass
                        else:
                            await message.answer("😔 Пока нет данных о комплексах")
                            
                    except json.JSONDecodeError:
                        await message.answer("❌ Ошибка в формате данных")
                        
                else:
                    await message.answer(f"❌ Ошибка загрузки: HTTP {response.status}")
                    
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")

@dp.message(Command("web"))
async def web_app_command(message: Message):
    """Команда для открытия веб-приложения"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🚀 Открыть веб-приложение",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]]
    )
    
    await message.answer(
        "🌐 <b>Веб-приложение новостроек</b>\n\n"
        "В веб-приложении вы можете:\n"
        "• Выбрать застройщика\n"
        "• Посмотреть жилые комплексы\n"
        "• Подобрать квартиру\n"
        "• Увидеть расположение на карте\n\n"
        "Нажмите кнопку ниже, чтобы открыть:",
        parse_mode='HTML',
        reply_markup=keyboard
    )

@dp.message(Command("help"))
async def help_command(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Веб-приложение", web_app=WebAppInfo(url=WEB_APP_URL))],
            [InlineKeyboardButton(text="📱 Комплексы", callback_data="complexes")],
            [InlineKeyboardButton(text="📍 Карта", callback_data="map")]
        ]
    )
    
    await message.answer(
        "🤖 <b>Помощь по боту</b>\n\n"
        "<b>Команды:</b>\n"
        "/start - начать работу\n"
        "/web - открыть веб-приложение\n"
        "/complexes - список комплексов\n"
        "/help - эта справка\n\n"
        "<b>Веб-приложение:</b>\n"
        "• Выбор застройщиков\n"
        "• Подбор квартир\n"
        "• Яндекс.Карты\n\n"
        "<b>Ссылки:</b>\n"
        f"Веб-приложение: {WEB_APP_URL}\n"
        "Фид данных: https://github.com/dsmaznova-source/my-telegram-app2",
        parse_mode='HTML',
        reply_markup=keyboard
    )

# Обработка callback-запросов
@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "complexes":
        await complexes_command(callback.message)
    elif callback.data == "help":
        await help_command(callback.message)
    elif callback.data == "map":
        await callback.message.answer(
            "🗺️ <b>Карта новостроек</b>\n\n"
            "Откройте веб-приложение для просмотра интерактивной карты с расположением жилых комплексов.",
            parse_mode='HTML'
        )
    
    await callback.answer()

@dp.message()
async def echo_message(message: Message):
    await message.answer(
        "Используйте команды:\n"
        "/start - начало работы\n"
        "/web - веб-приложение\n"
        "/complexes - список комплексов\n"
        "/help - помощь\n\n"
        "Или откройте веб-приложение через меню."
    )

# Главная функция
async def main():
    logging.info("🤖 Запускаю бота с веб-интерфейсом...")
    logging.info(f"🌐 Веб-приложение: {WEB_APP_URL}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())