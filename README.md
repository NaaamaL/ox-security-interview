# Interacting with Redis in Minikube

This project provides scripts to interact with a Redis server deployed in Minikube using Helm. The project includes the following components:

- `interact_with_redis.py`: Python script to add and read keys to Redis.
- `start_ox_app.py`: Python script to start Minikube and deploy the `ox-app` Helm chart.
- `ox-app/`: Helm chart directory containing the deployment configuration for a Redis server and Redis client.

## Getting Started

### Prerequisites
- Minikube
- Helm

### Installation

1. Clone this repository:

    ```
    git clone https://github.com/yourusername/yourrepository.git
    ```

2. Change into the project directory:

    ```
    cd yourrepository
    ```

3. Start Minikube and deploy the `ox-app` Helm chart by running:

    ```
    python start_ox_app.py
    ```

    This script will start Minikube and deploy the Helm chart. Wait for the application to be fully deployed before proceeding.

4. Once the application is deployed, interact with Redis by running:

    ```
    python interact_with_redis.py
    ```

    This script allows you to add and read keys to Redis.

## Usage

- **`interact_with_redis.py`**: This script allows you to interact with the deployed Redis server. You can add and read keys to Redis by running this script.

- **`start_ox_app.py`**: This script starts Minikube and deploys the `ox-app` Helm chart. It sets up the environment for interacting with Redis.

## Note

- Ensure that Minikube and Helm are properly installed and configured before running the scripts.
- Wait for the application to be fully deployed after running `start_ox_app.py` before executing `interact_with_redis.py`.
