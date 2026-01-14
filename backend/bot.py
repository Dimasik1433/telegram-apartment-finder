import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from database import Database
from parser import FidParser

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Конфигурация
BOT_TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"
WEB_APP_URL = "https://ВАШ_НИК.github.io/ВАШ_РЕПОЗИТОРИЙ/frontend/"
FID_URL = "https://ваш-сайт.ru/fid.xml"  # URL вашего фида

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database()
parser = FidParser(FID_URL)

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text="🔍 Поиск квартир",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ],
            [
                types.KeyboardButton(text="🔄 Обновить базу"),
                types.KeyboardButton(text="ℹ️ Помощь")
            ]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🏠 *Бот поиска квартир от Группы Аквилон*\n\n"
        "Я показываю актуальные варианты из наших проектов.\n"
        "Нажмите кнопку ниже, чтобы начать поиск!",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Обновление базы данных
@dp.message(lambda message: message.text == "🔄 Обновить базу")
async def update_database(message: types.Message):
    await message.answer("🔄 Обновляю базу квартир...")
    
    apartments = parser.parse_feed()
    db.save_apartments(apartments)
    
    await message.answer(f"✅ Обновлено {len(apartments)} квартир")

# API endpoint для Mini App
@dp.message(Command("api"))
async def api_search(message: types.Message):
    """API для поиска квартир (используется Mini App)"""
    try:
        # Получаем параметры из запроса
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        filters = {}
        
        # Парсим параметры типа: /api price:5000000 rooms:1,2 district:Центр
        for arg in args:
            if ':' in arg:
                key, value = arg.split(':', 1)
                filters[key] = value
        
        # Поиск в БД
        apartments = db.search_apartments(filters)
        
        # Отправляем результат (в реальности тут будет JSON API)
        if apartments:
            response = f"Найдено {len(apartments)} квартир:\n\n"
            for apt in apartments[:3]:  # Показываем первые 3
                response += f"• {apt['rooms']}-к, {apt['area']}м², {apt['price']:,.0f} руб.\n"
                response += f"  {apt['district']}\n\n"
            
            if len(apartments) > 3:
                response += f"... и ещё {len(apartments)-3} вариантов"
        else:
            response = "По вашему запросу ничего не найдено"
        
        await message.answer(response)
        
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

# Запуск парсера по расписанию
async def scheduled_parser():
    """Запускает парсинг каждые 4 часа"""
    while True:
        try:
            apartments = parser.parse_feed()
            db.save_apartments(apartments)
            logging.info(f"Спаршено {len(apartments)} квартир")
        except Exception as e:
            logging.error(f"Ошибка парсинга: {e}")
        
        await asyncio.sleep(4 * 3600)  # 4 часа

# Главная функция
async def main():
    # Запускаем фоновую задачу парсинга
    asyncio.create_task(scheduled_parser())
    
    # Запускаем бота
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
