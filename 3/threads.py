import socket
import threading

def handle_client(client_socket, addr):
    # Display active thread information
    current_thread = threading.current_thread()
    print(f"[Thread ID: {current_thread.ident}] handling client {addr}")
    print(f"Active Thread Count (Before Processing): {threading.active_count()}")

    request = client_socket.recv(1024)
    print(f"Received from {addr}: {request.decode()}")
    client_socket.send(b'Hello from server')
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)

print("Server is up and monitoring threads...")
while True:
    client_sock, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_sock, addr))
    client_thread.start()