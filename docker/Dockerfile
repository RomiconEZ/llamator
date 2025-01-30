FROM python:3.11-slim

WORKDIR /workspace

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
ENV POETRY_VERSION=1.4.2
RUN pip install poetry==$POETRY_VERSION

# Настройка Poetry
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/var/cache/pypoetry

# Копирование файлов проекта
COPY pyproject.toml poetry.lock /workspace/

WORKDIR /workspace

# Установка зависимостей через Poetry
RUN poetry install --no-interaction --no-ansi

# Копирование остальной части проекта
COPY . /workspace/

# Установка Jupyter
RUN poetry add jupyter notebook nb_conda_kernels

# Экспонирование порта Jupyter
EXPOSE 8888

# Команда для запуска Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
