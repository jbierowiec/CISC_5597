# CISC 5597 Distributed Systems Labs

This repository contains all four labs that I and [Rahul Kumar](https://github.com/kumarrah2002) have worked on in relation to Distributed Systems.

## Labs 
- Lab 1
  - This lab focused on networking and creating a system in which multiple clients can communicate with each other via a server. 
- Lab 2
  - This lab focused on developing a basic paxos algorithm and simulating consensus and consistency. Different scenarios were created to validate that the algorithm works properly. Two clients were created, client A and client B, and the task of the server was to determine which client would win the majority of the votes. 
- Lab 3
  - This lab focused on developing and simulating 2PC (Two Phase Commit Protocol). Different scenarios were created to validate that the algorithm works properly in the use case of transferring $100 from one account to another as well as adding a bonus to the same two different accounts. These transactions were made via participants communicating with coordinators. The lab also includes a scenario where the transaction between the accounts sent by the partipants, fail before and after responding to the coordinator. 
- Lab 4
  - This lab focused on implementing and playing around with a real-world distributed system. There were a few options to choose from, and out of the options available, monitoring a Kafka cluster was the choice made. This lab demonstrates message production and consumption via Kafka producers and consumers. A docker compose setup was also included in order to monitor Zookeeper, Kafka and Kpow. 

## Project Structure

```plaintext
├── Lab_1
├── Lab_2
├── Lab_3
└── Lab_4
```
