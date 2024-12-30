import socket
import json
import time


def submit_value(node_ip, node_port, value):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((node_ip, node_port))

    request = json.dumps({"type": "submit_value", "value": value})
    client_socket.sendall(request.encode())

    response = client_socket.recv(1024).decode()
    client_socket.close()
    return json.loads(response)


def proposer_b():
    # Slightly shorter delay to simulate Value_B winning scenarios
    response = submit_value("127.0.0.1", 5002, "Value_B")
    print("Proposer B Response:", response)


if __name__ == "__main__":
    proposer_b()
