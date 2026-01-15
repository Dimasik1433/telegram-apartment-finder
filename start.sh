#!/bin/bash
echo "Останавливаем всё..."
pkill -f python 2>/dev/null

echo "Запускаем веб-сервер..."
cd frontend
python -m http.server 8080 &
sleep 2

echo "Запускаем бота..."
cd ../backend
python bot.py