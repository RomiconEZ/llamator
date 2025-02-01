# llamator/docker/Dockerfile

# Declare PLATFORM argument with default value
ARG PLATFORM=linux/amd64
FROM --platform=${PLATFORM} python:3.11-slim

# Set working directory for dependency management
WORKDIR /project

# Install system dependencies
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

# Install Poetry
ENV POETRY_VERSION=2.0.1
RUN pip install poetry==$POETRY_VERSION

# Configure Poetry
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/var/cache/pypoetry

# Initialize Poetry project with explicit Python version and install dependencies
RUN poetry init -n --name jupyter_workspace --python ">=3.10,<4.0" && \
    poetry add jupyter notebook llamator

# Set environment variable for Jupyter port with default value 9000
ENV JUPYTER_PORT=9000

# Create working directory for Jupyter Notebook
RUN mkdir /workspace

# Expose Jupyter port
EXPOSE ${JUPYTER_PORT}

# Command to run Jupyter Notebook in /workspace
CMD ["sh", "-c", "jupyter notebook --ip=0.0.0.0 --port=$JUPYTER_PORT --allow-root --no-browser --notebook-dir=/workspace"]