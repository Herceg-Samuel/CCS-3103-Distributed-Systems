import socket

PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

print("Client Observer started... NO multicast access")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"[BROADCAST ONLY]: {data.decode()}")