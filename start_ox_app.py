import subprocess

def start_minikube():
    try:
        subprocess.run("minikube start", shell=True, check=True)
        print("Minikube started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Minikube: {e}")
        return False
    return True

def install_helm_chart(chart_name, chart_directory):
    try:
        subprocess.run(f"helm install {chart_name} {chart_directory}", shell=True, check=True)
        print(f"Helm chart '{chart_name}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Helm chart '{chart_name}': {e}")
        return False
    return True

def main():
    # Start Minikube
    if not start_minikube():
        return

    # Install Helm chart
    chart_name = "ox-app"
    chart_directory = "./ox-app"
    if not install_helm_chart(chart_name, chart_directory):
        return

if __name__ == "__main__":
    main()
