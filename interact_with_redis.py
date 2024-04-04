import subprocess

def get_redis_client_pod_name():
    kubectl_cmd = "kubectl get pods -l app.kubernetes.io/name=ox-app -o jsonpath='{.items[0].metadata.name}'"
    try:
        result = subprocess.run(kubectl_cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.output}")
        return None

def get_redis_server_service_name(component):
    kubectl_cmd = f"kubectl get svc -l app.kubernetes.io/component={component} -o jsonpath=\"{{.items[0].metadata.name}}\""
    try:
        result = subprocess.run(kubectl_cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.output}")
        return None

def exec_command(pod_name, command):
    kubectl_cmd = f"kubectl exec -it {pod_name} -- /bin/sh -c '{command}'"
    try:
        result = subprocess.run(kubectl_cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.output}")

def operation(action, key, value=""):
    if action == "add":
        svc = get_redis_server_service_name("master")
        redis_command = f"set {key} {value}"
    elif action == "get":
        svc = get_redis_server_service_name("replica")
        redis_command = f"get {key}"
    command = f"redis-cli -h {svc}.default.svc.cluster.local -p 6379 -a $REDIS_PASSWORD {redis_command}"
    exec_command(get_redis_client_pod_name(), command)


def main():
    
    operation("add", "OxKey", "OxValue")
    operation("get", "OxKey")


if __name__ == "__main__":
    main()
