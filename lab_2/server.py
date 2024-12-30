import multiprocessing
import socket
import json
import time
import random
from threading import Thread, Lock
import logging
import signal
import sys

# Node configuration
NODE_IPS = ["127.0.0.1", "127.0.0.1", "127.0.0.1"]
NODE_PORTS = [5001, 5002, 5003]
FILE_NAME = "CISC5597.txt"

# Logging setup
logging.basicConfig(level=logging.INFO, filename='paxos.log', filemode='a')


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.proposal_number = 0
        self.promised_proposal = -1
        self.accepted_value = None
        self.accepted_proposal = -1
        self.file_lock = Lock()
        self.majority = len(NODE_PORTS) // 2 + 1  # Majority threshold

        # Initialize shared file
        self.initialize_file()

    def initialize_file(self):
        with self.file_lock:
            with open(FILE_NAME, 'w') as f:
                f.write("")

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((NODE_IPS[self.node_id], NODE_PORTS[self.node_id]))
        server_socket.listen(5)
        print(
            f"Node {self.node_id} listening on port {NODE_PORTS[self.node_id]}")

        while True:
            client_socket, _ = server_socket.accept()
            Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode()
        request = json.loads(data)
        response = {}

        if request['type'] == "submit_value":
            response = self.prepare_phase(request['value'])
        elif request['type'] == "prepare":
            response = self.on_prepare(request['proposal_number'])
        elif request['type'] == "accept":
            response = self.on_accept(
                request['proposal_number'], request['value'])
        elif request['type'] == "broadcast":
            self.write_to_file(request['value'])
            logging.info(
                f"Node {self.node_id}: Broadcast value '{request['value']}' written to file.")
            response = {"status": "broadcast_received"}

        client_socket.sendall(json.dumps(response).encode())
        client_socket.close()

    def prepare_phase(self, value):
        self.proposal_number += 1
        promises = []
        highest_accepted_proposal = -1
        highest_accepted_value = None

        time.sleep(random.uniform(0.1, 1.0))  # Simulate network delay

        for ip, port in zip(NODE_IPS, NODE_PORTS):
            if (ip, port) != (NODE_IPS[self.node_id], NODE_PORTS[self.node_id]):
                response = self.send_message(ip, port, {
                    "type": "prepare",
                    "proposal_number": self.proposal_number
                })
                if response and response['status'] == "promise":
                    promises.append(True)
                    if response['acceptedProposal'] > highest_accepted_proposal:
                        highest_accepted_proposal = response['acceptedProposal']
                        highest_accepted_value = response['acceptedValue']
                else:
                    promises.append(False)

        # Adopt the highest accepted value if a valid promise is received
        if highest_accepted_value is not None:
            value = highest_accepted_value

        # Proceed to the accept phase only if the majority promised
        if promises.count(True) >= self.majority:
            return self.accept_phase(value)
        else:
            logging.info(f"Node {self.node_id}: Prepare phase failed.")
            return {"status": "failure", "message": "Majority not reached in prepare phase"}

    def accept_phase(self, value):
        accepts = []

        for ip, port in zip(NODE_IPS, NODE_PORTS):
            response = self.send_message(ip, port, {
                "type": "accept",
                "proposal_number": self.proposal_number,
                "value": value
            })
            if response and response['status'] == "accept":
                accepts.append(True)
            else:
                accepts.append(False)

        if accepts.count(True) >= self.majority:
            self.write_to_file(value)
            logging.info(
                f"Node {self.node_id}: Consensus reached for value '{value}'. Broadcasting value to all nodes."
            )
            self.broadcast_consensus(value)  # Broadcast the agreed value
            return {"status": "success", "message": "Consensus reached"}
        else:
            logging.info(f"Node {self.node_id}: Accept phase failed.")
            return {"status": "failure", "message": "Majority not reached in accept phase"}

    def on_prepare(self, proposal_number):
        if proposal_number > self.promised_proposal:
            self.promised_proposal = proposal_number
            return {
                "status": "promise",
                "acceptedProposal": self.accepted_proposal,
                "acceptedValue": self.accepted_value
            }
        # Reject only if the proposal number is less than the promised proposal
        return {"status": "reject"}

    def on_accept(self, proposal_number, value):
        if proposal_number >= self.promised_proposal:
            self.promised_proposal = proposal_number
            self.accepted_proposal = proposal_number
            self.accepted_value = value
            logging.info(
                f"Node {self.node_id}: Accepted proposal {proposal_number} with value '{value}'.")
            return {"status": "accept"}
        logging.info(
            f"Node {self.node_id}: Rejected proposal {proposal_number}.")
        return {"status": "reject"}

    def write_to_file(self, value):
        with self.file_lock:
            with open(FILE_NAME, 'w') as f:
                f.write(value)
            logging.info(
                f"Node {self.node_id}: Written value '{value}' to file.")

    def send_message(self, ip, port, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))
                sock.sendall(json.dumps(message).encode())
                response = json.loads(sock.recv(1024).decode())
                return response
        except Exception as e:
            logging.error(f"Node {self.node_id}: Error sending message: {e}")
            return None

    def broadcast_consensus(self, value):
        for ip, port in zip(NODE_IPS, NODE_PORTS):
            if (ip, port) != (NODE_IPS[self.node_id], NODE_PORTS[self.node_id]):
                self.send_message(
                    ip, port, {"type": "broadcast", "value": value})


def run_node(node_id):
    node = Node(node_id)

    def handle_exit_signal(signum, frame):
        logging.info(f"Node {node_id}: Received exit signal. Shutting down.")
        sys.exit(0)

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, handle_exit_signal)
    signal.signal(signal.SIGTERM, handle_exit_signal)

    try:
        node.start_server()
    except KeyboardInterrupt:
        logging.info(f"Node {node_id}: Interrupted by user. Shutting down.")
        sys.exit(0)


if __name__ == "__main__":
    processes = []
    for node_id in range(len(NODE_PORTS)):
        process = multiprocessing.Process(target=run_node, args=(node_id,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
