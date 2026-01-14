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
        def do_GET(self):
            # Маршрутизация для SPA (Single Page Application)
            if self.path.startswith('/api/'):
                # API запросы обрабатываем отдельно
                self.handle_api()
            else:
                # Для всех остальных запросов отдаем index.html
                if self.path == '/' or '.' not in self.path.split('/')[-1]:
                    self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        
        def handle_api(self):
            """Обработка API запросов"""
            if self.path == '/api/developers':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # Загружаем данные из фида
                import json
                import requests
                try:
                    response = requests.get('https://raw.githubusercontent.com/dsmaznova-source/my-telegram-app2/main/complexes.json', timeout=5)
                    data = response.json()
                    
                    # Формируем список застройщиков
                    developers = []
                    if isinstance(data, list):
                        for item in data:
                            developer_name = item.get('developer', 'Аквилон')  # По умолчанию Аквилон
                            if developer_name not in [d['name'] for d in developers]:
                                developers.append({
                                    'name': developer_name,
                                    'logo': item.get('logo', ''),
                                    'complexes_count': sum(1 for i in data if i.get('developer', 'Аквилон') == developer_name)
                                })
                    else:
                        developers = [{
                            'name': data.get('developer', 'Аквилон'),
                            'logo': data.get('logo', ''),
                            'complexes_count': 1
                        }]
                    
                    self.wfile.write(json.dumps(developers).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
            
            elif self.path == '/api/complexes':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                import json
                import requests
                try:
                    response = requests.get('https://raw.githubusercontent.com/dsmaznova-source/my-telegram-app2/main/complexes.json', timeout=5)
                    data = response.json()
                    
                    # Преобразуем в список комплексов
                    complexes = []
                    if isinstance(data, list):
                        complexes = data
                    else:
                        complexes = [data]
                    
                    self.wfile.write(json.dumps(complexes).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        def log_message(self, format, *args):
            pass  # Отключаем логи

    server = HTTPServer(('', PORT), Handler)
    print(f"🌐 Веб-сервер запущен: http://localhost:{PORT}")
    print(f"📡 API доступно по: http://localhost:{PORT}/api/")
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
    print("🚀 Запуск приложения: Веб-интерфейс + Telegram бот")
    print("="*50)
    
    # Запускаем веб-сервер в фоне
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    time.sleep(2)
    
    print("✅ Веб-интерфейс: http://localhost:8080")
    print("✅ API данные: http://localhost:8080/api/developers")
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