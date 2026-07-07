import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
client_socket.send(b'Hello server')
response = client_socket.recv(1024)
print(f"Received from server: {response.decode()}")
client_socket.close()