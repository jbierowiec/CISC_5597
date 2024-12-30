# Lab 2 Consensus and Consistency - Basic Paxos Algorithm 

This project implements a basic paxos algorithm in relation to consensus and consistency. This project contains three major files, `client_a.py`, `client_b.py`, and `server.py` in which different scenarios in reaching a majority consensus is reached. Each scenario demonstrates different consensus outcomes, with `Value_A` or `Value_B` being written to `CISC5597.txt` reaching consensus under specific conditions.

## Features
- **Distributed Consensus:**
  - Implements the Paxos algorithm for achieving consensus in distributed systems.
  - Supports multiple proposal rounds and resolves conflicts.
- **Logging:**
  - Logs all significant events, including proposals, acceptances, and consensus.
  - Tracks the rejection and acceptance of proposals by nodes.
- **Scalable Design:**
  - Includes a server script and multiple client scripts for simulating distributed nodes.

## Project Structure

```plaintext
├── CISC5597.txt
├── client_a.py
├── client_b.py
├── paxos.log
├── run_clients.sh
└── server.py
```

## Setup Instructions

1. Make sure that `client_a.py`, `client_b.py`, and `server.py` are all in the same directory.
  
2. Open separate terminal windows for each server and client as instructed in each of the scenarios below.

  ### Scenario 1: Single Proposer (Client A Only)

  In this scenario, only `client_a.py` runs, proposing `Value_A`. Since it’s the only proposer, `Value_A` should reach consensus without competition.

  1. Start the `Server Nodes` in separate terminals:

     ```bash
     # Terminal 1
     python server.py 0  # Node 0 on port 5001

     # Terminal 2
     python server.py 1  # Node 1 on port 5002

     # Terminal 3
     python server.py 2  # Node 2 on port 5003
     ```

  2. Run `Client A` in a new terminal:

     ```bash
     # Terminal 4
     python client_a.py
     ```

  ### Scenario 2: Two Proposers (Client A Wins Over Client B)

  In this scenario, both `client_a.py` and `client_b.py` propose values, but `Value_A` wins due to `client_a.py` being run first, with a slight delay before running `client_b.py`.

  1. Start the `Server Nodes` in separate terminals:

     ```bash
     # Terminal 1
     python server.py 0  # Node 0 on port 5001

     # Terminal 2
     python server.py 1  # Node 1 on port 5002

     # Terminal 3
     python server.py 2  # Node 2 on port 5003
     ```

  2. Run `Client A` and `Client B` in two new terminals:

     ```bash
     # Terminal 4
     python client_a.py  # Start immediately

     # Terminal 5 
     sleep 1 && python client_b.py  # Start after a short delay
     ```

  ### Scenario 3: Two Proposers (Client B Wins Over Client A)

  In this scenario, `client_b.py` is run first, proposing `Value_B`, followed by `client_a.py` after a delay. `Value_B` should reach consensus as it’s proposed first.

  1. Start the `Server Nodes` in separate terminals:

     ```bash
     # Terminal 1
     python server.py 0  # Node 0 on port 5001

     # Terminal 2
     python server.py 1  # Node 1 on port 5002

     # Terminal 3
     python server.py 2  # Node 2 on port 5003
     ```

  2. Run `Client B` in a new terminal:

     ```bash
     # Terminal 4
     python client_b.py  # Start immediately

     # Terminal 5
     sleep 1 && python client_a.py  # Start after a short delay
     ```
