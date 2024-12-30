# Lab 1 Networking - Multiple Users Chatting

This project implements a basic client-server communication system using Python's `socket` library. The server assigns a unique UUID to each connected client and allows them to exchange messages. This project contains two files, `client.py` and `server.py` to ensure client-server communication. 

## Features

- **Server:**
  - Assigns a unique UUID to each client upon connection.
  - Handles multiple client connections using threading.
  - Displays messages from connected clients in the terminal.
  - Accepts commands such as `list`, `forward ID string`, `history ID`, and `exit`:
    - `list`: The server sends back all the active client IDs.
    - `forward ID string`: The server should be able to understand that this client wants to send
the msg(string) to the other client with the ID that listed the command. The server should be able to forward the message to the target in the following format: source ID: message_content
    - `history ID`: The server should send back the chatting history between the requested client and the client with the ID listed in the command.
    - `exit`: The server should send back a message "Goodbye" and close the connection.
- **Client:**
  - Connects to the server and receives a unique UUID.
  - Allows the user to send and receive messages.
  - Exits gracefully when the user types exit.

## Project Structure

```plaintext
├── client.py
└── server.py
```

## Setup Instructions 

1. Make sure that you are in the `Lab_1` directory.

2. To run the server, follow these steps:

  - Open a terminal

  - Run the server script
    ```bash
    python server.py
    ```

3. To run the client, follow these steps:

  - Open another terminal

  - Run the server script
    ```bash
    python client.py
    ```
