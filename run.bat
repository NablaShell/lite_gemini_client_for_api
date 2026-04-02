@echo off
echo 🚀 Запуск Gemini 2.5 Flash клиента

if not exist .env (
    echo ❌ Файл .env не найден!
    echo 📝 Создай .env файл с содержимым: GEMINI_API_KEY=твой_ключ
    exit /b 1
)

echo 📦 Сборка образа...
docker compose build

echo 🚀 Запуск контейнера...
docker compose up -d

echo ✅ Клиент запущен!
echo 🌐 Открой в браузере: http://localhost:8000
echo 📋 Логи: docker compose logs -f
