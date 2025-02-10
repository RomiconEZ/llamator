# Usage Instructions

## Preliminary Steps

1. **Project Structure:**

   ```
   llamator/
   ├── docker/
   │   ├── Dockerfile
   │   ├── jupyter_docker.sh
   │   └── README.md
   └── workspace/
       └── (your working files)
   ```

2. **Creating Local `workspace` Directory:**

   If the local `./workspace` directory doesn't exist, it will be created automatically when the container starts. No need to create it manually.

## Main Commands

The `jupyter_docker.sh` script supports the following commands:

1. **Building Docker Image:**

   Navigate to the `llamator/docker` directory and execute:

   ```bash
   ./jupyter_docker.sh build
   ```

   This will create a Docker image named `jupyter_img` by default. Jupyter Notebook will run on port `9000` by default.

2. **Running Container:**

   ```bash
   ./jupyter_docker.sh run [port]
   ```

   - **Parameters:**
     - `[port]` *(optional)*: Port for accessing Jupyter Notebook. If not specified, port `9000` is used.

   - **Examples:**

     - Using default port:

       ```bash
       ./jupyter_docker.sh run
       ```

     - Setting custom port, e.g., `8888`:

       ```bash
       ./jupyter_docker.sh run 8888
       ```

   - **Features:**
     - All arguments and settings are defined within the `jupyter_docker.sh` script.
     - When running the `run` command, you can specify a port as an argument that will be passed to the container.
     - If the local `./workspace` directory doesn't exist in the current directory, it will be created automatically.
     - If a container with the same name already exists, it will be stopped and removed before starting a new one.
     - The container will be launched in background mode.
     - The script will automatically extract the token and display the complete URL for accessing Jupyter Notebook, e.g.: `http://localhost:9000/?token=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz`.

3. **Getting URL with Token:**

   If you need to retrieve the URL with the current token again:

   ```bash
   ./jupyter_docker.sh token
   ```

   You'll see output with a URL that can be opened in a browser to access Jupyter Notebook.

4. **Adding New Packages via Poetry:**

   For example, to add the `numpy` package:

   ```bash
   ./jupyter_docker.sh add numpy
   ```

5. **Accessing Container's Bash Shell:**

   If you need to execute commands inside the container:

   ```bash
   ./jupyter_docker.sh bash
   ```

6. **Stopping Container:**

   To stop the running container:

   ```bash
   ./jupyter_docker.sh stop
   ```

7. **Removing Container:**

   If you need to completely remove the container:

   ```bash
   ./jupyter_docker.sh remove
   ```

## Usage Examples

### 1. Build and Run with Default Port

```bash
./jupyter_docker.sh build
./jupyter_docker.sh run
```

- Jupyter Notebook will be accessible at: `http://localhost:9000/?token=your_token_here`

### 2. Build and Run with Custom Port

```bash
./jupyter_docker.sh build
./jupyter_docker.sh run 8888
```

- Jupyter Notebook will be accessible at: `http://localhost:8888/?token=your_token_here`

### 3. Adding `pandas` Package

```bash
./jupyter_docker.sh add pandas
```

- The `pandas` package will be installed and available in your project.