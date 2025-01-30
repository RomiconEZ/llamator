# llamator/docker/Dockerfile

# Объявляем аргумент PLATFORM с дефолтным значением
ARG PLATFORM=linux/amd64
FROM --platform=${PLATFORM} python:3.11-slim

# Установить рабочую директорию для управления зависимостями
WORKDIR /project

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        curl \
        git \
        vim \
        openssh-client \
        libsm6 \
        libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_VERSION=2.0.1
RUN pip install poetry==$POETRY_VERSION

# Настройка Poetry
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/var/cache/pypoetry

# Инициализация проекта Poetry с явным указанием версии Python и установка зависимостей
RUN poetry init -n --name jupyter_workspace --python ">=3.10,<4.0" && \
    poetry add jupyter notebook llamator

# Установка переменной окружения для порта Jupyter с дефолтным значением 9000
ENV JUPYTER_PORT=9000

# Создание рабочей директории для Jupyter Notebook
RUN mkdir /workspace

# Экспонирование порта Jupyter
EXPOSE ${JUPYTER_PORT}

# Команда для запуска Jupyter Notebook в /workspace
CMD ["sh", "-c", "jupyter notebook --ip=0.0.0.0 --port=$JUPYTER_PORT --allow-root --no-browser --notebook-dir=/workspace"]