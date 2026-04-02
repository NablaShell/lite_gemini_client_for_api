FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY backend.py .
COPY static ./static

# Создание непривилегированного пользователя
RUN useradd -m -u 1000 gemini && chown -R gemini:gemini /app
USER gemini

# Запуск
EXPOSE 8000
CMD ["python", "backend.py"]
