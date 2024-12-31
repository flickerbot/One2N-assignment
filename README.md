# One2N-assignment


# RabbitMQ Deployment with Custom Scaler
 Requirement -- Dynamically scaling consumer pods based on RabbitMQ queue depth and packaging everything using helm 

## Components

1. **Producer**: This component generates messages and sends them to the RabbitMQ queue.
2. **Consumer**: This component consumes messages from the RabbitMQ queue. The number of consumer pods is scaled dynamically based on the queue depth.
3. **RabbitMQ**: RabbitMQ is deployed using the official `rabbitmq:3-management` Docker image. It serves as the message broker between the producer and consumer.
4. **Custom Scaler**: A Python script (running in a custom scaler pod) monitors the RabbitMQ queue depth using the RabbitMQ HTTP API. Based on the queue depth, the custom scaler increases or decreases the number of consumer pods. If the queue depth exceeds a defined threshold, the scaler will scale up the consumer pods. If the queue depth is low, the scaler will scale down the consumer pods.

## How the Application Works

1. **Producer and Consumer Docker Images**:
   - The **Producer** Docker image is responsible for generating messages and pushing them to the RabbitMQ queue.
   - The **Consumer** Docker image consumes these messages from the RabbitMQ queue.
   - Both the producer and consumer containers expect the following environment variables for RabbitMQ connection:
     - `RABBITMQ_USER`
     - `RABBITMQ_PASSWORD`
   
2. **RabbitMQ Deployment**:
   - RabbitMQ is deployed using the official `rabbitmq:3-management` Docker image.
   - The environment variables `RABBITMQ_USER` and `RABBITMQ_PASSWORD` are passed securely using **Kubernetes Secrets** to avoid hardcoding sensitive information.

3. **Custom Scaler**:
   - The **Custom Scaler** logic is implemented using a Python script that leverages the RabbitMQ HTTP API to fetch the queue depth.
     To make the process automated rather than running the script manuually I have created a docker image that is running the scaling logic in the customscaler pod. 
     I HAVE UPLOADED THE CODE FOR THIS IN CODE DIRECTORY 

    -- Basic working of the custom scaler --  
   - If the queue depth exceeds the upper threshold, the custom scaler increases the number of consumer pods.
   - If the queue depth is below the lower threshold, the custom scaler decreases the number of consumer pods.
   - Values for upper and lower threshold are defined in helm values.yaml so you can change the values as per need 
   

## Setup and Deployment

### Prerequisites

1. **Kubernetes Cluster**:
   - This application assumes that a **Kubernetes cluster** is already set up locally ( I have used Minikube).
   
2. **Helm**:
   - Make sure **Helm** is installed to manage Kubernetes applications.

### Installing the Helm Chart

To install this application on your Kubernetes cluster, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/flickerbot/One2N-assignment
   cd rabbitmq-deployment-one2nfinal
  
2. **Install the Helm Chart**: 
   helm install rabbitmq-one2n ./rabbitmq-deployment-one2nfinal-0.1.0.tgz

3. **Verify the Installation**
   kubectl get all

4. **Access RabbitMQ Management UI**:
   kubectl port-forward svc/rabbitmq-service 15672:15672

Open http://localhost:15672 in your browser and log in using the default credentials:
Username: admin                                       # you can change these credentials by changing the values in values.yaml file 
Password: admin123                                    













