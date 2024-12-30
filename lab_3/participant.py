import socket
import threading


class Participant:
    def __init__(self, host, port, account_file):
        self.host = host
        self.port = port
        self.account_file = account_file
        self.temp_balance = None  # Temporary balance for the PREPARE phase

    def read_balance(self):
        with open(self.account_file, "r") as f:
            balance = int(f.read().strip())
            # Debug: Print balance
            return balance

    def write_balance(self, balance):
        with open(self.account_file, "w") as f:
            f.write(str(balance))

    def process_message(self, message):
        try:
            parts = message.split()
            command = parts[0]

            if command == "PREPARE":
                print(f"Received PREPARE: {' '.join(parts[1:])}")
                if len(parts) == 5 and parts[1] == "TRANSFER":
                    # Parse TRANSFER: PREPARE TRANSFER <amount> <source> <destination>
                    _, amount, source, destination = parts[1:]
                    amount = int(amount)
                    current_balance = self.read_balance()

                    if self.port == 8001:  # Participant for Account A
                        if source == "A":
                            if current_balance >= amount:
                                self.temp_balance = current_balance - amount
                                return "YES"
                            else:
                                print("Insufficient funds in Account A.")
                                return "NO"
                        elif destination == "A":
                            self.temp_balance = current_balance + amount
                            return "YES"

                    elif self.port == 8002:  # Participant for Account B
                        if source == "B":
                            if current_balance >= amount:
                                self.temp_balance = current_balance - amount
                                return "YES"
                            else:
                                print("Insufficient funds in Account B.")
                                return "NO"
                        elif destination == "B":
                            self.temp_balance = current_balance + amount
                            return "YES"

                    return "NO"

                if len(parts) == 3 and parts[1] == "BONUS":
                    # Parse BONUS: PREPARE BONUS <percent>
                    _, percent = parts[1:]
                    percent = int(percent)

                    if self.port == 8001:  # Participant for Account A
                        # Calculate bonus from A's balance
                        current_balance = self.read_balance()
                        bonus_amount = (current_balance * percent) // 100
                        # Add bonus to A's temporary balance
                        self.temp_balance = current_balance + bonus_amount
                        print(
                            f"BONUS Operation: Adding {bonus_amount} to A, New Balance = {self.temp_balance}")
                        return "YES"

                    elif self.port == 8002:  # Participant for Account B
                        # Bonus amount calculated by Participant A, add the same amount to B
                        current_balance = self.read_balance()
                        # Bonus applied proportionally
                        bonus_amount = (current_balance * percent) // 100
                        self.temp_balance = current_balance + bonus_amount
                        print(
                            f"BONUS Operation: Adding {bonus_amount} to B, New Balance = {self.temp_balance}")
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
        message = conn.recv(1024).decode()
        print(f"Received message: {message}")  # Log received message
        response = self.process_message(message)
        if response:
            conn.sendall(response.encode())

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Participant running on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                # Log new connections
                print('-'*20)
                print(f"Connection accepted from {addr}")
                threading.Thread(target=self.handle_connection,
                                 args=(conn,)).start()


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])  # Pass port as an argument
    account_file = sys.argv[2]  # Pass account file as an argument
    participant = Participant("127.0.0.1", port, account_file)
    participant.start()
