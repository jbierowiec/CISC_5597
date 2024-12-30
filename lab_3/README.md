# Lab 3 Two Phase Commit Protocol 

This project simulates a distributed **Two-Phase Commit (2PC)** protocol with three nodes based on a coordinator (`coordinator.py`) file and two participant (`participant_crash.py` & `participant.py`) files managing accounts. The protocol ensures atomicity and consistency for distributed transactions.

## Features 

- **Coordinator:**
  - Manages the Two-Phase Commit process.
  - Coordinates between participants to ensure transaction consistency.
- **Participants:**
  - Respond to the coordinator during the PREPARE and COMMIT phases.
  - Maintain a local balance file representing their state.
- **Crash Simulation:**
  - Simulates crashes during different phases (e.g., before or after the PREPARE phase) to test system robustness.

## Project Structure

```plaintext
├── account_a.txt
├── account_b.txt
├── coordinator.py
├── participant_crash.py
└── participant.py
```

## Setup Instructions

1. Make sure that `coordinator.py`, `participant_crash.py`, and `participant.py` are all in the same directory.
  
2. Open separate terminal windows for each participant and coordinator as instructed in each of the scenarios below.

  ### Scenario 1: No Failures (Participant 1 transfers $100 from Account A to Account B to Participant 2)

  In this scenario, two `participant.py` files are ran in different ports and referring to different accounts.

  1. Make sure that `account_a.txt` starts with $200, and `account_b.txt` starts with $300.

  2. Start the `particpants` in separate terminals:

     ```bash
     # Terminal 1
     python participant.py 8001 account_a.txt

     # Terminal 2
     python participant.py 8002 account_b.txt
     ```

  3. Each `participant` listens for connections and processes incoming transactions.

  4. Execute a transaction with the `coordinator` in separate terminals:

     Transfer `100` from Account A to Account B:
     ```bash
     # Terminal 3
     python coordinator.py "TRANSFER 100 A B"
     ```
     Add a bonus of `20%` to Account A and Account B:
     ```bash
     # Terminal 4
     python coordinator.py "BONUS 20"
     ```

   5. The `coordinator` sends PREPARE messages to both `participants`, collects their votes, and sends a COMMIT if all `participants` vote YES, or ABORT if any `participant` votes NO.

  ### Scenario 2: No Failures (Participant 1 transfers $100 from Account A to Account B to Participant 2)

  In this scenario, two `participant.py` files are ran in different ports and referring to different accounts.

  1. Make sure that `account_a.txt` starts with $90, and `account_b.txt` starts with $50.

  2. Start the `particpants` in separate terminals:

     ```bash
     # Terminal 1
     python participant.py 8001 account_a.txt

     # Terminal 2
     python participant.py 8002 account_b.txt
     ```

  3. Each `participant` listens for connections and processes incoming transactions.

  4. Execute a transaction with the `coordinator` in separate terminals:

     Transfer `100` from Account A to Account B:
     ```bash
     # Terminal 3
     python coordinator.py "TRANSFER 100 A B"
     ```
     Add a bonus of `20%` to Account A and Account B:
     ```bash
     # Terminal 4
     python coordinator.py "BONUS 20"
     ```

   5. The `coordinator` sends PREPARE messages to both `participants`, collects their votes, and sends a COMMIT if all `participants` vote YES, or ABORT if any `participant` votes NO.

  ### Scenario 3: Failures (Node 2 crashes before & after responding to the coordinator)

  #### Case 1: Node 2 crashes BEFORE responding to the coordinator

  Now, run the following code for the `participant` instead of the original `participant` code, in order to simulate the node crashing `BEFORE` sending a response for the PREPARE stage:

  1. Make sure that `account_a.txt` starts with $200, and `account_b.txt` starts with $300.

  2. Start the `particpant` in separate terminals:

     ```bash
     # Terminal 1
     python participant_crash.py 8002 account_b.txt before_prepare
     ```

  3. Execute a transaction with the `coordinator` in separate terminals:

     Transfer `100` from Account A to Account B:
     ```bash
     # Terminal 2
     python coordinator.py "TRANSFER 100 A B"
     ```
     Add a bonus of `20%` to Account A and Account B:
     ```bash
     # Terminal 3
     python coordinator.py "BONUS 20"
     ```

  #### Case 2: Node 2 crashes AFTER responding to the coordinator

  Now, run the following code for the `participant` instead of the original `participant` code, in order to simulate the node crashing `AFTER` sending a response for the COMMIT stage:

  1. Make sure that `account_a.txt` starts with $200, and `account_b.txt` starts with $300.

  2. Start the `particpant` in separate terminals:

     ```bash
     # Terminal 1
     python participant_crash.py 8002 account_b.txt after_prepare
     ```

  3. Execute a transaction with the `coordinator` in separate terminals:

     Transfer `100` from Account A to Account B:
     ```bash
     # Terminal 2
     python coordinator.py "TRANSFER 100 A B"
     ```
     Add a bonus of `20%` to Account A and Account B:
     ```bash
     # Terminal 3
     python coordinator.py "BONUS 20"
     ```
