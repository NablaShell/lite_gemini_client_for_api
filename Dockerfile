FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY backend.py .
COPY static ./static

# Создаем директорию для БД с правильными правами
RUN mkdir -p /data && chmod 777 /data

# Создание непривилегированного пользователя
RUN useradd -m -u 1000 gemini && chown -R gemini:gemini /app /data
USER gemini

EXPOSE 8000
CMD ["python", "backend.py"]
