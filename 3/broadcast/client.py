import socket

PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("", PORT))

print("Listening...")

while True:
    data, addr = sock.recvfrom(1024)
    print(addr, data.decode())