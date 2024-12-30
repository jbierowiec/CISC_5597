import socket
import threading
import time  # For simulating crashes


class Participant:
    def __init__(self, host, port, account_file, simulate_crash=None):
        """
        Initialize the Participant.
        :param host: Host address
        :param port: Port number
        :param account_file: Path to the account file
        :param simulate_crash: 'before_prepare' or 'after_prepare' to simulate crashes
        """
        self.host = host
        self.port = port
        self.account_file = account_file
        self.temp_balance = None  # Temporary balance for the PREPARE phase
        self.simulate_crash = simulate_crash
        self.crashed = False  # To simulate crash state

    def read_balance(self):
        with open(self.account_file, "r") as f:
            return int(f.read().strip())

    def write_balance(self, balance):
        with open(self.account_file, "w") as f:
            f.write(str(balance))

    def simulate_crash_condition(self, phase):
        """Simulate a crash during a specific phase."""
        if self.simulate_crash == phase:
            print(
                f"Simulating crash during {phase} phase. Participant {self.port} entering crashed state...")
            self.crashed = True
            # Simulates a crash by sleeping indefinitely
            time.sleep(float('inf'))

    def process_message(self, message):
        """
        Process incoming messages.
        :param message: Received message string
        :return: Response string to send back
        """
        if self.crashed:
            print(
                f"Participant {self.port} is in a crashed state. Ignoring message: {message}")
            return None  # Ignore messages when crashed

        try:
            parts = message.split()
            command = parts[0]

            if command == "PREPARE":
                # Simulate crash before responding
                self.simulate_crash_condition('before_prepare')
                print(f"Received PREPARE: {' '.join(parts[1:])}")
                if len(parts) == 5 and parts[1] == "TRANSFER":
                    _, amount, source, destination = parts[1:]
                    amount = int(amount)
                    current_balance = self.read_balance()

                    if self.port == 8002:  # Participant for Account B
                        if source == "B":
                            if current_balance >= amount:
                                self.temp_balance = current_balance - amount
                                print(
                                    f"Prepared YES for Account B with temp balance: {self.temp_balance}")
                                return "YES"
                            else:
                                print("Insufficient funds in Account B.")
                                return "NO"
                        elif destination == "B":
                            self.temp_balance = current_balance + amount
                            print(
                                f"Prepared YES for Account B with temp balance: {self.temp_balance}")
                            return "YES"

                    return "NO"

                else:
                    print(f"Invalid transaction format: {message}")
                    return "NO"

            elif command == "COMMIT":
                print("Processing COMMIT")
                if self.temp_balance is not None:
                    previous_balance = self.read_balance()
                    self.write_balance(self.temp_balance)
                    print(
                        f"Previous Balance = {previous_balance}, Updated Balance = {self.temp_balance}")
                    self.temp_balance = None
                    return "COMMITTED"

            elif command == "ABORT":
                print("Processing ABORT")
                self.temp_balance = None
                return "ABORTED"

            return "UNKNOWN"

        except Exception as e:
            print(f"Error processing message: {e}")
            return "NO"

    def handle_connection(self, conn):
        """
        Handle communication with the coordinator.
        :param conn: Connection object
        """
        try:
            message = conn.recv(1024).decode()
            print(f"Received message: {message}")  # Log received message
            response = self.process_message(message)
            if response:
                # Send response back to the coordinator
                conn.sendall(response.encode())
                print(f"Sent response: {response}")
                if response == "YES" and self.simulate_crash == 'after_prepare':
                    # Simulate crash after sending YES
                    self.simulate_crash_condition('after_prepare')
        except Exception as e:
            print(f"Error handling connection: {e}")

    def start(self):
        """
        Start the participant server to listen for incoming connections.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Participant running on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                print('-' * 20)
                print(f"Connection accepted from {addr}")
                threading.Thread(target=self.handle_connection,
                                 args=(conn,)).start()


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])  # Pass port as an argument
    account_file = sys.argv[2]  # Pass account file as an argument
    simulate_crash = None
    if len(sys.argv) > 3:
        # Pass crash phase as an optional argument
        simulate_crash = sys.argv[3]
    participant = Participant("127.0.0.1", port,
                              account_file, simulate_crash)
    participant.start()
