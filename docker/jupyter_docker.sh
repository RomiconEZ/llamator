#!/usr/bin/env bash

# llamator/docker/jupyter_docker.sh

set -e

# ===== Настраиваемые Параметры =====
IMAGE_NAME="jupyter_img"                 # Имя Docker-образа
CONTAINER_NAME="jupyter_cont"            # Имя Docker-контейнера
DEFAULT_JUPYTER_PORT=9000                # Значение порта по умолчанию
PROJECT_DIR="/project"                   # Рабочая директория внутри контейнера
MAX_RETRIES=30                           # Максимальное количество попыток получения токена
SLEEP_INTERVAL=2                         # Интервал ожидания между попытками (секунды)
PLATFORM="linux/amd64"                   # Платформа Docker

# Определение платформы, если необходимо (опционально)
if [[ $(uname -m) == "arm64" ]]; then
    PLATFORM="linux/arm64/v8"
fi

# Получение порта из аргументов или использование значения по умолчанию
if [ "$1" == "run" ] && [ -n "$2" ]; then
    JUPYTER_PORT="$2"
    shift 2
else
    JUPYTER_PORT="$DEFAULT_JUPYTER_PORT"
fi

# Определение текущего рабочего каталога
CURRENT_DIR=$(pwd)
WORKSPACE_DIR="$CURRENT_DIR/workspace"

case $1 in
    build)
        echo "Сборка Docker-образа '$IMAGE_NAME' для платформы $PLATFORM с портом $JUPYTER_PORT..."
        docker build . -t "$IMAGE_NAME" --build-arg PLATFORM=$PLATFORM --build-arg JUPYTER_PORT=$JUPYTER_PORT
        echo "Образ '$IMAGE_NAME' успешно создан."
        ;;

    run)
        # Проверка и создание локальной директории
        if [ ! -d "$WORKSPACE_DIR" ]; then
            echo "Директория '$WORKSPACE_DIR' не существует. Создание..."
            mkdir -p "$WORKSPACE_DIR"
            echo "Директория '$WORKSPACE_DIR' создана."
        else
            echo "Директория '$WORKSPACE_DIR' уже существует."
        fi

        # Проверка существующего контейнера
        if [ "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
            if [ "$(docker ps -q -f name=^${CONTAINER_NAME}$)" ]; then
                echo "Контейнер '$CONTAINER_NAME' уже запущен."
            else
                echo "Запуск существующего контейнера '$CONTAINER_NAME' с портом $JUPYTER_PORT..."
                docker start "$CONTAINER_NAME"
                echo "Контейнер '$CONTAINER_NAME' запущен."
            fi
        else
            echo "Создание и запуск нового контейнера '$CONTAINER_NAME' с портом $JUPYTER_PORT..."
            docker run \
                --platform $PLATFORM \
                -v "$WORKSPACE_DIR":/workspace \
                -d \
                -p "$JUPYTER_PORT:$JUPYTER_PORT" \
                --name "$CONTAINER_NAME" \
                "$IMAGE_NAME"
            echo "Контейнер '$CONTAINER_NAME' успешно запущен."
        fi

        # Ожидание запуска Jupyter и получение токена
        echo "Ожидание запуска Jupyter Notebook..."
        RETRIES=0
        while true; do
            if [ $RETRIES -ge $MAX_RETRIES ]; then
                echo "Не удалось получить токен Jupyter Notebook после $(($MAX_RETRIES * $SLEEP_INTERVAL)) секунд."
                exit 1
            fi

            TOKEN_OUTPUT=$(docker exec "$CONTAINER_NAME" jupyter notebook list 2>/dev/null)
            if [[ $TOKEN_OUTPUT == *"token="* ]]; then
                TOKEN=$(echo "$TOKEN_OUTPUT" | grep -o 'token=[a-zA-Z0-9]*' | cut -d'=' -f2)
                break
            fi

            sleep $SLEEP_INTERVAL
            RETRIES=$((RETRIES + 1))
        done

        URL="http://localhost:$JUPYTER_PORT/?token=$TOKEN"
        echo "Jupyter Notebook доступен по адресу:"
        echo "$URL"
        ;;

    add)
        if [ -z "$2" ]; then
            echo "Пожалуйста, укажите название пакета: ./jupyter_docker.sh add package_name"
            exit 1
        fi
        echo "Добавление пакета '$2' с помощью Poetry..."
        # Выполняем команду в директории /project контейнера
        docker exec -w "$PROJECT_DIR" "$CONTAINER_NAME" poetry add "$2"
        echo "Пакет '$2' успешно добавлен."
        ;;

    token)
        TOKEN_OUTPUT=$(docker exec "$CONTAINER_NAME" jupyter notebook list 2>/dev/null)
        if [[ $TOKEN_OUTPUT == *"token="* ]]; then
            TOKEN=$(echo "$TOKEN_OUTPUT" | grep -o 'token=[a-zA-Z0-9]*' | cut -d'=' -f2)
            URL="http://localhost:$JUPYTER_PORT/?token=$TOKEN"
            echo "Jupyter Notebook доступен по адресу:"
            echo "$URL"
        else
            echo "Не удалось получить токен. Убедитесь, что контейнер запущен и Jupyter Notebook работает."
            exit 1
        fi
        ;;

    bash)
        echo "Запуск оболочки Bash внутри контейнера '$CONTAINER_NAME'..."
        docker exec -it "$CONTAINER_NAME" /bin/bash
        ;;

    stop)
        echo "Остановка контейнера '$CONTAINER_NAME'..."
        docker stop "$CONTAINER_NAME"
        echo "Контейнер '$CONTAINER_NAME' остановлен."
        ;;

    remove)
        echo "Удаление контейнера '$CONTAINER_NAME'..."
        docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
        echo "Контейнер '$CONTAINER_NAME' удалён."
        ;;

    *)
        echo "Неизвестная команда."
        echo "Использование: ./jupyter_docker.sh {build|run [port]|add|token|bash|stop|remove}"
        exit 1
        ;;
esac