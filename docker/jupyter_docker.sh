#!/bin/bash
set -e

# ===== Настраиваемые Параметры =====
IMAGE_NAME="jupyter_img"                 # Имя Docker-образа
CONTAINER_NAME="jupyter_cont"            # Имя Docker-контейнера
DEFAULT_JUPYTER_PORT=9001                # Значение порта по умолчанию
PROJECT_DIR="/project"                   # Рабочая директория внутри контейнера
MAX_RETRIES=30                           # Максимальное количество попыток получения токена
SLEEP_INTERVAL=2                         # Интервал ожидания между попытками (секунды)
PLATFORM_DEFAULT="linux/amd64"           # Платформа Docker по умолчанию

# Определение платформы, если необходимо (опционально)
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" || "$ARCH" == "aarch64" ]]; then
    PLATFORM="linux/arm64/v8"
else
    PLATFORM="$PLATFORM_DEFAULT"
fi

# Функция для отображения помощи
function show_help {
    echo "Использование: ./jupyter_docker.sh {build|run [порт]|add package_name|token|bash|stop|remove}"
    exit 1
}

# Проверка наличия команды
if [ -z "$1" ]; then
    show_help
fi

# Определение текущего каталога, чтобы workspace монтировался относительно него
CURRENT_DIR=$(pwd)
WORKSPACE_DIR="$CURRENT_DIR/workspace"

# Функция для проверки и создания рабочей директории
function ensure_workspace {
    if [ ! -d "$WORKSPACE_DIR" ]; then
        echo "Директория '$WORKSPACE_DIR' не существует. Создание..."
        mkdir -p "$WORKSPACE_DIR"
        echo "Директория '$WORKSPACE_DIR' создана."
    else
        echo "Директория '$WORKSPACE_DIR' уже существует."
    fi
}

# Функция для остановки и удаления контейнера, если он существует
function remove_existing_container {
    if [ "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
        echo "Контейнер '$CONTAINER_NAME' существует."
        if [ "$(docker ps -q -f name=^${CONTAINER_NAME}$)" ]; then
            echo "Остановка работающего контейнера '$CONTAINER_NAME'..."
            docker stop "$CONTAINER_NAME"
            echo "Контейнер '$CONTAINER_NAME' остановлен."
        fi
        echo "Удаление контейнера '$CONTAINER_NAME'..."
        docker rm "$CONTAINER_NAME"
        echo "Контейнер '$CONTAINER_NAME' удалён."
    fi
}

case $1 in
    build)
        echo "Сборка Docker-образа '$IMAGE_NAME' для платформы $PLATFORM..."
        docker build . -t "$IMAGE_NAME" --build-arg PLATFORM="$PLATFORM"
        echo "Образ '$IMAGE_NAME' успешно создан."
        ;;

    run)
        # Определение порта
        if [ -n "$2" ]; then
            JUPYTER_PORT="$2"
        else
            JUPYTER_PORT="$DEFAULT_JUPYTER_PORT"
        fi

        echo "Используемый порт Jupyter Notebook: $JUPYTER_PORT"

        # Проверка и создание локальной директории workspace
        ensure_workspace

        # Остановка и удаление существующего контейнера, если он существует
        remove_existing_container

        echo "Создание и запуск нового контейнера '$CONTAINER_NAME' на порту $JUPYTER_PORT..."
        docker run \
            --platform "$PLATFORM" \
            -v "$WORKSPACE_DIR":/workspace \
            -d \
            -p "$JUPYTER_PORT:$JUPYTER_PORT" \
            -e JUPYTER_PORT="$JUPYTER_PORT" \
            --name "$CONTAINER_NAME" \
            "$IMAGE_NAME"
        echo "Контейнер '$CONTAINER_NAME' успешно запущен."

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
        show_help
        ;;
esac