# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir poetry==1.8.0

# Копируем оставшиеся файлы проекта
COPY . /app/

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Запускаем приложение
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]