import os
import time
import requests
from kubernetes import client, config
from kubernetes.client import AppsV1Api

# Load Kubernetes config (use kubeconfig or in-cluster config)
config.load_incluster_config()  # If running inside Kubernetes, else use load_kube_config()
#config.load_kube_config()  # Loads the kubeconfig file from ~/.kube/config



# Kubernetes API clients
v1_apps = AppsV1Api()
v1_core = client.CoreV1Api()

# Fetch RabbitMQ credentials from environment variables (set by Kubernetes secrets)
#RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

# RabbitMQ API URL to fetch queue depth
#RABBITMQ_URL = f"http://localhost:15672/api/queues/%2F/my-queue"         # for testing the code withoot pod and running it manually 
RABBITMQ_URL = f"http://{RABBITMQ_HOST}:15672/api/queues/%2F/my-queue"
# Consumer Deployment details
NAMESPACE = "default"
DEPLOYMENT_NAME = "mq-consumer"


def get_rabbitmq_queue_depth():
    """Fetch the queue depth from RabbitMQ via HTTP API."""
    try:
        response = requests.get(RABBITMQ_URL, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
        response.raise_for_status()
        queue_info = response.json()
        return queue_info.get('messages', 0)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching queue depth: {e}")
        return 0

def scale_consumer_deployment(replica_count):
    """Scale the consumer deployment based on queue depth."""
    try:
        deployment = v1_apps.read_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE)
        deployment.spec.replicas = replica_count
        v1_apps.patch_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE, deployment)
        print(f"Scaled {DEPLOYMENT_NAME} to {replica_count} replicas.")
    except client.exceptions.ApiException as e:
        print(f"Error scaling deployment: {e}")

def run_controller():
    """Main loop that checks RabbitMQ queue depth and scales the consumer accordingly."""
    while True:
        queue_depth = get_rabbitmq_queue_depth()
        print(f"Queue depth: {queue_depth} messages")
        
        if queue_depth > QUEUE_THRESHOLD_UPPER:
            print("Queue depth is high, scaling up...")
            scale_consumer_deployment(SCALE_UP_REPLICAS)
        elif queue_depth <= QUEUE_THRESHOLD_LOWER:
            print("Queue depth is low, scaling down...")
            scale_consumer_deployment(SCALE_DOWN_REPLICAS)
        else:
            print("Queue depth is within normal range, no scaling needed.")
        
        time.sleep(30)  # Check every 30 seconds

if __name__ == '__main__':
    run_controller()
