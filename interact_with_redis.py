import subprocess

def get_redis_client_pod_name() -> str:
    """
    Returns the name of the redis client pod.

    Returns:
        The name of the redis client pod.
    """
    kubectl_cmd = "kubectl get pods -l app.kubernetes.io/name=ox-app -o jsonpath='{.items[0].metadata.name}'"
    try:
        result = subprocess.run(kubectl_cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.output}")
        return None

def get_redis_server_service_name(component: str) -> str:
    """
    Returns the name of the redis server service.

    The service is identified using the component label.

    Args:
        component (str): The component label of the redis server service.

    Returns:
        The name of the redis server service.
    """
    kubectl_cmd = (
        f"kubectl get svc -l app.kubernetes.io/component={component} "
        "-o jsonpath='{.items[0].metadata.name}'"
    )
    try:
        result = subprocess.run(
            kubectl_cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.output}")
        return None


def exec_command(pod_name: str, command: str):
    """
    Execute a command in a k8s pod.

    The function will execute the command specified in `command` in the pod
    specified by `pod_name`. The stdout of the command will be printed to the
    console.

    Args:
        pod_name (str): The name of the pod in which to execute the command.
        command (str): The command to execute.
    """
    kubectl_cmd = f"kubectl exec -it {pod_name} -- /bin/sh -c '{command}'"
    try:
        result = subprocess.run(
            kubectl_cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.output}")

def operation(action: str, key: str, value: str = "") -> None:
    """
    Perform a redis operation.

    The function will execute the appropriate redis operation on the server
    specified by the `action` parameter. The key and value parameters are used
    as arguments to the operation.

    Args:
        action (str): The name of the redis operation to perform. Valid values
            are "add" or "get".
        key (str): The key to use as an argument to the operation.
        value (str): The value to use as an argument to the operation.
            Defaults to "".
    """
    if action == "add":
        svc = get_redis_server_service_name("master")
        redis_command = f"set {key} {value}"
    elif action == "get":
        svc = get_redis_server_service_name("replica")
        redis_command = f"get {key}"
    else:
        raise ValueError(f"Invalid action: {action}")
    command = (
        f"redis-cli -h {svc}.default.svc.cluster.local -p 6379 -a $REDIS_PASSWORD "
        f"{redis_command}"
    )
    exec_command(get_redis_client_pod_name(), command)

def main():
    
    operation("add", "OxKey", "OxValue")
    operation("get", "OxKey")

if __name__ == "__main__":
    main()
