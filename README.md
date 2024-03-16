## Introduction

This project defines a multi-container application using Docker Compose. It sets up the following services:

* **Kafka Clusters (kafka-0, kafka-1)**: This configuration enables distributed messaging capabilities in the application.
* **kafka-ui**: Offer a web-based interface for monitoring your Kafka clusters (requires configuration in ./kafka-ui/config.yml).
* **simple-server**: Built by `node.js express` and used as a a producer to the Kafka clusters.
* **kafka-consumer-worker**: Built by `python asycio` and used as a a consumer to the Kafka clusters.
* **mysql**: Used as the data downstream behind `kafka-consumer-worker`. `init.sql` in the ./dump directory is used to create the required Tables.

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

* Kafka UI: If you configured the ./kafka-ui/config.yml file properly, access the Kafka UI at http://localhost:8080.
* MySQL Database: The MySQL database runs on http://localhost:3306. You can connect to it using your MySQL client UI with the following credentials:
    * Username: `test`
    * Password: `test`
    ```
    mysql -h 127.0.0.1 -u test -p
    # type password: test
    use simple;
    select * from ad_events;
    ```
* Simple Server: This service runs on http://localhost:8888. Its behavior depends on its implementation in the ./simple-server directory.

## Networks
The `docker-compose.yml` defines a network named `app-tier`. All services are connected to this network, enabling them to communicate with each other.
