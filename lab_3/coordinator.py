import socket
import sys

class Coordinator:
    def __init__(self, host, port, participants):
        self.host = host
        self.port = port
        self.participants = participants

    def send_message(self, host, port, message):
        try:
            print(f"Sending message to {host}:{port} - {message}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(message.encode())
                response = s.recv(1024).decode()
                print(f"Received response from {host}:{port} - {response}")
                return response
        except Exception as e:
            print(f"Error communicating with {host}:{port}: {e}")
            return "NO"

    def handle_transaction(self, transaction):
        print(f"Handling transaction: {transaction}")

        # Prepare Phase
        print("Sending prepare to participants...")
        votes = []
        for host, port in self.participants:
            vote = self.send_message(host, port, f"PREPARE {transaction}")
            votes.append(vote)

        # Commit or Abort Phase
        if all(vote == "YES" for vote in votes):
            print("All participants voted YES. Sending COMMIT.")
            for host, port in self.participants:
                self.send_message(host, port, "COMMIT")
        else:
            print("One or more participants voted NO. Sending ABORT.")
            for host, port in self.participants:
                self.send_message(host, port, "ABORT")

    def start(self, transaction):
        self.handle_transaction(transaction)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python coordinator.py '<transaction>'")
        print("Example: python coordinator.py 'TRANSFER 100 A B'")
        print("         python coordinator.py 'BONUS 20'")
        sys.exit(1)

    transaction = sys.argv[1]  # Transaction passed as command-line argument
    participants = [("127.0.0.1", 8001), ("127.0.0.1", 8002)]
    coordinator = Coordinator("localhost", 8000, participants)
    coordinator.start(transaction)
