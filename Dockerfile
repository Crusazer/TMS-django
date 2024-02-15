# Используем базовый образ Python
FROM python:3.10

# Установка переменной окружения для Python (может быть необязательно)
ENV PYTHONUNBUFFERED=1

# Создание и переход в рабочую директорию в контейнере
WORKDIR /TMS-django

# Копирование зависимостей проекта в контейнер
COPY requirements.txt /TMS-django/

# Установка зависимостей проекта
RUN pip install -r requirements.txt

# Копирование остальных файлов проекта в контейнер
COPY . /TMS-django/

# Открываем порт, на котором будет работать Django
EXPOSE 8000

# Запуск команды для запуска Django сервера
# CMD python3 manage.py runserver 0.0.0.0:8000
#ENTRYPOINT ["sleep", "5", "&&", "python3", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

