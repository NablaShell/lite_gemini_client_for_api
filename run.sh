#!/bin/bash

# run.sh - для Linux/Mac
# run.bat - для Windows

echo "🚀 Запуск Gemini 2.5 Flash клиента"

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Создай .env файл с содержимым: GEMINI_API_KEY=твой_ключ"
    exit 1
fi

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "📥 Установи Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Сборка и запуск
echo "📦 Сборка образа..."
docker compose build

echo "🚀 Запуск контейнера..."
docker compose up -d

echo "✅ Клиент запущен!"
echo "🌐 Открой в браузере: http://localhost:8000"
echo "📋 Логи: docker compose logs -f"
