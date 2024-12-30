# Lab 4 Maintenance - Monitoring a Kafka Cluster

This project implements a Kafka-based messaging system using Python, Docker, and Confluent Kafka. The project contains three major files, `docker-compose.yaml`, `kafka_consumer.py`, and `kafka_producer.py`. The project demonstrates message production and consumption using a Kafka producer and consumer, alongside a Docker Compose setup for Zookeeper, Kafka, and Kpow for monitoring. 

## Features
- **Dockerized Kafka Setup:**
  - Uses Docker Compose to deploy Zookeeper, Kafka, and Kpow.
  - Configures Kafka with external access support for scalability.
- **Message Production:**
  - Python producer script sends messages to a Kafka topic.
- **Message Consumption:**
  - Python consumer script listens to the Kafka topic and processes incoming messages.

## Project Structure

```plaintext
├── docker-compose.yaml
├── kafka_consumer.py
└── kafka_producer.py
```

## Setup Instructions

1. Make sure that `docker-compose.yaml`, `kafka_consumer.py`, and `kafka_producer.py` are all in the same directory.
2. Open separate terminal windows setting up the `docker-compose.yaml` file, and running the `kafka_producer.py` and `kafka_consumer.py` files. 

  ### Kafka Environment Setup
  1. Run the the following command:

     ```bash
     docker-compose up -d
     ```

  2. Verify that all services (Zookeeper, Kafka, Kpow) are running:

     ```bash
     docker-compose ps
     ```

  ### Running the Kafka Producer

  1. Run the producer script:

     ```bash
     python kafka_producer.py
     ```

  2. Observe the producer sending messages to the Kafka topic lab-demo.

  ### Running the Kafka Consumer

  1. Run the consumer script:

     ```bash
     python kafka_consumer.py
     ```

  2. Observe the consumer receiving messages from the Kafka topic lab-demo.


  ### Accessing Kpow Monitoring

  1. Open your browser.
  2. Navigate to the Kpow interface at http://localhost:3000.
  3. Monitor Kafka topics, messages, and other statistics.

## Configuration

- **Kafka Broker Address:**
  - Update the bootstrap_servers value in the producer and consumer scripts to match your Kafka setup.
- **Kafka Topic:**
  - The default topic is lab-demo. Update the topic name in the scripts if needed.
