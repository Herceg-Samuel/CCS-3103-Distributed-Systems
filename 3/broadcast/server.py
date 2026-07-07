import socket

PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    message = input("Message: ")
    sock.sendto(message.encode(), ("255.255.255.255", PORT))