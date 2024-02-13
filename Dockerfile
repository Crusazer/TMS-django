# Используем базовый образ Python
FROM python:3.10

# Установка переменной окружения для Python (может быть необязательно)
ENV PYTHONUNBUFFERED=1

# Создание и переход в рабочую директорию в контейнере
WORKDIR /tms_project

# Копирование зависимостей проекта в контейнер
COPY requirements.txt /tms_project/

# Установка зависимостей проекта
RUN pip install -r requirements.txt

# Копирование остальных файлов проекта в контейнер
COPY . /tms_project/

# Открываем порт, на котором будет работать Django
EXPOSE 8000

# Запуск команды для запуска Django сервера
# CMD python3 manage.py runserver 0.0.0.0:8000
#CMD sleep 20 && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
