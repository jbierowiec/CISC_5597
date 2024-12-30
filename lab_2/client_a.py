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


def proposer_a():
    time.sleep(1.5)  # Moderate delay
    response = submit_value("127.0.0.1", 5001, "Value_A")
    print("Proposer A Response:", response)


if __name__ == "__main__":
    proposer_a()
