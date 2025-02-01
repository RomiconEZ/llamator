#!/bin/bash
set -e

# ===== Configurable Parameters =====
IMAGE_NAME="jupyter_img"                 # Docker image name
CONTAINER_NAME="jupyter_cont"            # Docker container name
DEFAULT_JUPYTER_PORT=9001                # Default port value
PROJECT_DIR="/project"                   # Working directory inside container
MAX_RETRIES=30                           # Maximum number of token retrieval attempts
SLEEP_INTERVAL=2                         # Wait interval between attempts (seconds)
PLATFORM_DEFAULT="linux/amd64"           # Default Docker platform

# Platform determination if needed (optional)
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" || "$ARCH" == "aarch64" ]]; then
    PLATFORM="linux/arm64/v8"
else
    PLATFORM="$PLATFORM_DEFAULT"
fi

# Help display function
function show_help {
    echo "Usage: ./jupyter_docker.sh {build|run [port]|add package_name|token|bash|stop|remove}"
    exit 1
}

# Command presence check
if [ -z "$1" ]; then
    show_help
fi

# Determine current directory for workspace mounting relative to it
CURRENT_DIR=$(pwd)
WORKSPACE_DIR="$CURRENT_DIR/workspace"

# Function to check and create working directory
function ensure_workspace {
    if [ ! -d "$WORKSPACE_DIR" ]; then
        echo "Directory '$WORKSPACE_DIR' doesn't exist. Creating..."
        mkdir -p "$WORKSPACE_DIR"
        echo "Directory '$WORKSPACE_DIR' created."
    else
        echo "Directory '$WORKSPACE_DIR' already exists."
    fi
}

# Function to stop and remove container if it exists
function remove_existing_container {
    if [ "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
        echo "Container '$CONTAINER_NAME' exists."
        if [ "$(docker ps -q -f name=^${CONTAINER_NAME}$)" ]; then
            echo "Stopping running container '$CONTAINER_NAME'..."
            docker stop "$CONTAINER_NAME"
            echo "Container '$CONTAINER_NAME' stopped."
        fi
        echo "Removing container '$CONTAINER_NAME'..."
        docker rm "$CONTAINER_NAME"
        echo "Container '$CONTAINER_NAME' removed."
    fi
}

case $1 in
    build)
        echo "Building Docker image '$IMAGE_NAME' for platform $PLATFORM..."
        docker build . -t "$IMAGE_NAME" --build-arg PLATFORM="$PLATFORM"
        echo "Image '$IMAGE_NAME' successfully created."
        ;;

    run)
        # Port determination
        if [ -n "$2" ]; then
            JUPYTER_PORT="$2"
        else
            JUPYTER_PORT="$DEFAULT_JUPYTER_PORT"
        fi

        echo "Using Jupyter Notebook port: $JUPYTER_PORT"

        # Check and create local workspace directory
        ensure_workspace

        # Stop and remove existing container if it exists
        remove_existing_container

        echo "Creating and starting new container '$CONTAINER_NAME' on port $JUPYTER_PORT..."
        docker run \
            --platform "$PLATFORM" \
            -v "$WORKSPACE_DIR":/workspace \
            -d \
            -p "$JUPYTER_PORT:$JUPYTER_PORT" \
            -e JUPYTER_PORT="$JUPYTER_PORT" \
            --name "$CONTAINER_NAME" \
            "$IMAGE_NAME"
        echo "Container '$CONTAINER_NAME' successfully started."

        # Wait for Jupyter to start and get token
        echo "Waiting for Jupyter Notebook to start..."
        RETRIES=0
        while true; do
            if [ $RETRIES -ge $MAX_RETRIES ]; then
                echo "Failed to get Jupyter Notebook token after $(($MAX_RETRIES * $SLEEP_INTERVAL)) seconds."
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
        echo "Jupyter Notebook is accessible at:"
        echo "$URL"
        ;;

    add)
        if [ -z "$2" ]; then
            echo "Please specify package name: ./jupyter_docker.sh add package_name"
            exit 1
        fi
        echo "Adding package '$2' using Poetry..."
        docker exec -w "$PROJECT_DIR" "$CONTAINER_NAME" poetry add "$2"
        echo "Package '$2' successfully added."
        ;;

    token)
        TOKEN_OUTPUT=$(docker exec "$CONTAINER_NAME" jupyter notebook list 2>/dev/null)
        if [[ $TOKEN_OUTPUT == *"token="* ]]; then
            TOKEN=$(echo "$TOKEN_OUTPUT" | grep -o 'token=[a-zA-Z0-9]*' | cut -d'=' -f2)
            URL="http://localhost:$JUPYTER_PORT/?token=$TOKEN"
            echo "Jupyter Notebook is accessible at:"
            echo "$URL"
        else
            echo "Failed to get token. Make sure the container is running and Jupyter Notebook is working."
            exit 1
        fi
        ;;

    bash)
        echo "Starting Bash shell inside container '$CONTAINER_NAME'..."
        docker exec -it "$CONTAINER_NAME" /bin/bash
        ;;

    stop)
        echo "Stopping container '$CONTAINER_NAME'..."
        docker stop "$CONTAINER_NAME"
        echo "Container '$CONTAINER_NAME' stopped."
        ;;

    remove)
        echo "Removing container '$CONTAINER_NAME'..."
        docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
        echo "Container '$CONTAINER_NAME' removed."
        ;;

    *)
        echo "Unknown command."
        show_help
        ;;
esac