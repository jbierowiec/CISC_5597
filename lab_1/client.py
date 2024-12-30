import socket
import threading


def receive_messages(sock):
    while True:
        try:
            server_reply = sock.recv(1024).decode()
            if server_reply:
                print(f"\n{server_reply}\n")
            else:
                break
        except ConnectionResetError:
            print("Server connection lost.")
            break


ip_port = ('127.0.0.1', 9999)
# ip_port = ('34.42.153.159', 80)
s = socket.socket()
s.connect(ip_port)

# Receive UUID from the server
uuid = s.recv(1024).decode()
print(f"Received UUID from server: {uuid}")

# Start a thread to listen for incoming messages
receiver_thread = threading.Thread(target=receive_messages, args=(s,))
receiver_thread.daemon = True
receiver_thread.start()

while True:
    inp = input(
        'Type a command (list, forward ID string, history ID, exit): ').strip()
    if not inp:
        continue
    s.sendall(inp.encode())

    if inp == "exit":
        print(f'Goodbye {uuid}')
        break

s.close()
receiver_thread.join()
