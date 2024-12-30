import socket
import threading
import uuid
from datetime import datetime

client_uuids = {}
chat_history = []


def link_handler(link, client):
    global client_uuids, chat_history
    print(f'Server start receiving msg from [{client[0]}:{client[1]}]...')

    client_uuid = str(uuid.uuid4())
    client_uuids[client_uuid] = link

    link.sendall(f'Your UUID is: {client_uuid}'.encode())

    print(f"A client with UUID {client_uuid} has joined the server.")

    while True:
        client_data = link.recv(1024).decode()
        if not client_data:
            continue

        if client_data == "exit":
            print(
                f'Client with UUID {client_uuid} from [{client[0]}:{client[1]}] ended communication.')
            client_uuids.pop(client_uuid, None)
            break

        elif client_data == "list":
            active_clients = ', '.join(client_uuids.keys())
            link.sendall(
                f'Active clients in server: {active_clients}'.encode())

        elif client_data.startswith("forward"):
            try:
                _, target_uuid, message = client_data.split(" ", 2)
                if target_uuid in client_uuids:
                    forward_msg = f"\n{client_uuid}: {message}"
                    client_uuids[target_uuid].sendall(forward_msg.encode())

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    chat_history.append(
                        (client_uuid, target_uuid, message, timestamp))

                    link.sendall(
                        f"Message forwarded to {target_uuid}".encode())
                else:
                    link.sendall(f"Client {target_uuid} not found.".encode())
            except ValueError:
                link.sendall(
                    "Invalid forward command. Use: forward <target_ID> <message>".encode())

        elif client_data.startswith("history"):
            try:
                _, target_uuid = client_data.split(" ", 1)
                relevant_history = [
                    f"\n[{timestamp}] {source}: {msg}"
                    for source, target, msg, timestamp in chat_history
                    if (source == client_uuid and target == target_uuid) or (source == target_uuid and target == client_uuid)
                ]
                if relevant_history:
                    link.sendall("\n".join(relevant_history).encode())
                else:
                    link.sendall("No chat history found.".encode())
            except ValueError:
                link.sendall(
                    "Invalid history command. Use: history <target_ID>".encode())

        else:
            link.sendall(f"Unknown command: {client_data}".encode())

    link.close()


ip_port = ('127.0.0.1', 9999)
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(ip_port)
sk.listen(5)

print('Start socket server, waiting for clients...')

while True:
    try:
        conn, address = sk.accept()
        print(
            f'Create a new thread to receive msg from [{address[0]}:{address[1]}]')
        t = threading.Thread(target=link_handler, args=(conn, address))
        t.start()
    except OSError:
        print("Server socket has been closed.")
        break
