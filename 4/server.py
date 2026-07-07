import socket
import time

BROADCAST_IP = '255.255.255.255'
PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Server started (broadcast mode)")

while True:
    msg = input("Server message: ")
    message = f"[SERVER BROADCAST]: {msg}"
    sock.sendto(message.encode(), (BROADCAST_IP, PORT))