## Introduction

This project defines a multi-container application using Docker Compose. It sets up the following services:

* **Kafka Clusters (kafka-0, kafka-1)**: This configuration enables distributed messaging capabilities in the application.
* **kafka-ui**: Offer a web-based interface for monitoring your Kafka clusters (requires configuration in ./kafka-ui/config.yml).
* **simple-server**: Built by `node.js-express` and used as a action interface and a producer to the Kafka clusters.
* **airflow**: Built by `python-airflow` and mainly used as a consumer to the Kafka clusters.
  * **airflow-init**: Initialize the db for airflow cluster requirement.
  * **airflow-webserver**: UI for airflow cluser.
  * **airflow-scheduler**: Dispatch tasks to workers.
  * **airflow-worker**: Execute DAG tasks.
* **postgres**: Used as the data downstream behind `airflow`. `init.sql` in the ./dump directory is used to create the required Tables.

## Prerequisites

* Docker: Ensure you have Docker installed and running on your system. You can find installation instructions at https://docs.docker.com/engine/install/.
* Docker Compose: Install Docker Compose following the official guide at https://docs.docker.com/engine/install/.

## Getting Started

1. Clone or Download the Repository: Obtain the project files locally.

2. Build the Images: Run the following command in your terminal under repo folder:

```=Bash
docker-compose build
```
* This will build the needed images.

3. Run the Services: Start all containers defined in the docker-compose.yml file using:

```=Bash
docker-compose up -d
```

* The -d flag detaches the containers from the terminal, allowing them to run in the background.

## Accessing Services (if applicable)

* Kafka UI: Access the Kafka UI at http://localhost:8080.
* pgAdmin: The Postgres database runs on http://localhost:3306. You can connect to it using your pgAdmin client UI on http://localhost:5050
* Simple Server: This service runs on http://localhost:8888. Its behavior depends on its implementation in the ./simple-server directory.

## 

## Networks
The `docker-compose.yml` defines a network named `app-tier`. All services are connected to this network, enabling them to communicate with each other.
