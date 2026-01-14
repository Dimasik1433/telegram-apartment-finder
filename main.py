import asyncio
import threading
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import time

# Добавляем backend в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def run_web_server():
    """Запуск веб-сервера на порту 8080"""
    # Меняем директорию на frontend
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    PORT = 8080
    
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # Отключаем логи
    
    server = HTTPServer(('', PORT), Handler)
    print(f"🌐 Веб-сервер запущен: http://localhost:{PORT}")
    server.serve_forever()

async def run_bot():
    """Запуск Telegram бота"""
    try:
        from bot import main as bot_main
        print("🤖 Запускаю бота...")
        await bot_main()
    except Exception as e:
        print(f"❌ Ошибка бота: {e}")

def main():
    print("="*50)
    print("🚀 Запуск приложения")
    print("="*50)
    
    # Запускаем веб-сервер в фоне
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Даем время на запуск веб-сервера
    time.sleep(2)
    
    print("✅ Веб-интерфейс: http://localhost:8080")
    print("✅ Бот: t.me/probniy_one_bot")
    print("\n🛑 Ctrl+C для остановки")
    print("="*50)
    
    # Запускаем бота
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено")

if __name__ == "__main__":
    main()
