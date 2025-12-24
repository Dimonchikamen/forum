# Dockerfile
FROM python:3.12-slim

# Установка зависимостей системы (если нужны, например, для Pillow)
RUN apt-get update && apt-get install -y \
    gcc \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . .

# Открываем порт (по умолчанию 8000 для Django)
EXPOSE 8000

# Запуск сервера (в продакшене лучше использовать Gunicorn + Nginx)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]